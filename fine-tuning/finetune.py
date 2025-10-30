#!/usr/bin/env python3
"""
Deep Tree Echo Fine-Tuning Script
==================================

This script implements a fine-tuning mechanism for creating an LLM with Echo identity
that responds with Echo persona even without a system prompt.

Supports multiple fine-tuning approaches:
1. OpenAI Fine-tuning API
2. Hugging Face Transformers (local fine-tuning)
3. Dataset preparation for other platforms

Usage:
    python finetune.py --provider openai --config config.json
    python finetune.py --provider huggingface --model gpt2 --epochs 3
    python finetune.py --prepare-only --output prepared_dataset.jsonl
"""

import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatasetValidator:
    """Validates and preprocesses the training dataset."""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.examples = []
        self.stats = {}
    
    def load_and_validate(self) -> List[Dict[str, str]]:
        """Load and validate the training dataset."""
        logger.info(f"Loading dataset from {self.dataset_path}")
        
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    example = json.loads(line.strip())
                    
                    # Validate required fields
                    if 'prompt' not in example or 'completion' not in example:
                        logger.warning(f"Line {line_num}: Missing required fields")
                        continue
                    
                    # Validate non-empty
                    if not example['prompt'].strip() or not example['completion'].strip():
                        logger.warning(f"Line {line_num}: Empty prompt or completion")
                        continue
                    
                    self.examples.append(example)
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Line {line_num}: Invalid JSON - {e}")
                    continue
        
        logger.info(f"Loaded {len(self.examples)} valid examples")
        self._compute_stats()
        return self.examples
    
    def _compute_stats(self):
        """Compute dataset statistics."""
        if not self.examples:
            return
        
        prompt_lengths = [len(ex['prompt']) for ex in self.examples]
        completion_lengths = [len(ex['completion']) for ex in self.examples]
        
        self.stats = {
            'total_examples': len(self.examples),
            'avg_prompt_length': sum(prompt_lengths) / len(prompt_lengths),
            'avg_completion_length': sum(completion_lengths) / len(completion_lengths),
            'max_prompt_length': max(prompt_lengths),
            'max_completion_length': max(completion_lengths),
            'min_prompt_length': min(prompt_lengths),
            'min_completion_length': min(completion_lengths)
        }
    
    def print_stats(self):
        """Print dataset statistics."""
        logger.info("Dataset Statistics:")
        for key, value in self.stats.items():
            logger.info(f"  {key}: {value if isinstance(value, int) else f'{value:.2f}'}")


class OpenAIFineTuner:
    """Fine-tune using OpenAI's fine-tuning API."""
    
    def __init__(self, api_key: Optional[str] = None):
        try:
            import openai
            self.openai = openai
            if api_key:
                self.openai.api_key = api_key
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            raise
    
    def prepare_dataset(self, examples: List[Dict[str, str]], output_path: str):
        """Prepare dataset in OpenAI format."""
        logger.info(f"Preparing OpenAI format dataset: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                # OpenAI fine-tuning format
                formatted = {
                    "messages": [
                        {"role": "user", "content": example['prompt']},
                        {"role": "assistant", "content": example['completion']}
                    ]
                }
                f.write(json.dumps(formatted) + '\n')
        
        logger.info(f"Prepared {len(examples)} examples for OpenAI fine-tuning")
        return output_path
    
    def upload_and_finetune(self, dataset_path: str, model: str = "gpt-3.5-turbo",
                           suffix: str = "echo", **kwargs):
        """Upload dataset and start fine-tuning job."""
        logger.info(f"Uploading dataset: {dataset_path}")
        
        try:
            # Upload training file
            with open(dataset_path, 'rb') as f:
                response = self.openai.File.create(
                    file=f,
                    purpose='fine-tune'
                )
            file_id = response.id
            logger.info(f"File uploaded: {file_id}")
            
            # Create fine-tuning job
            logger.info(f"Creating fine-tuning job for model: {model}")
            job = self.openai.FineTuningJob.create(
                training_file=file_id,
                model=model,
                suffix=suffix,
                **kwargs
            )
            
            logger.info(f"Fine-tuning job created: {job.id}")
            logger.info(f"Status: {job.status}")
            logger.info(f"Monitor at: https://platform.openai.com/finetune/{job.id}")
            
            return job
            
        except Exception as e:
            logger.error(f"Error during fine-tuning: {e}")
            raise


class HuggingFaceFineTuner:
    """Fine-tune using Hugging Face Transformers."""
    
    def __init__(self):
        try:
            import torch
            from transformers import (
                AutoTokenizer, 
                AutoModelForCausalLM,
                TrainingArguments,
                Trainer,
                DataCollatorForLanguageModeling
            )
            from datasets import Dataset
            
            self.torch = torch
            self.AutoTokenizer = AutoTokenizer
            self.AutoModelForCausalLM = AutoModelForCausalLM
            self.TrainingArguments = TrainingArguments
            self.Trainer = Trainer
            self.DataCollatorForLanguageModeling = DataCollatorForLanguageModeling
            self.Dataset = Dataset
            
        except ImportError as e:
            logger.error(f"Required packages not installed: {e}")
            logger.error("Install with: pip install torch transformers datasets")
            raise
    
    def prepare_dataset(self, examples: List[Dict[str, str]], tokenizer):
        """Prepare dataset for Hugging Face training."""
        logger.info("Preparing Hugging Face dataset")
        
        # Format examples as conversational text
        formatted_texts = []
        for ex in examples:
            text = f"User: {ex['prompt']}\n\nAssistant: {ex['completion']}"
            formatted_texts.append({"text": text})
        
        # Create dataset
        dataset = self.Dataset.from_list(formatted_texts)
        
        # Tokenize
        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                padding="max_length",
                truncation=True,
                max_length=512
            )
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        return tokenized_dataset
    
    def finetune(self, examples: List[Dict[str, str]], 
                 model_name: str = "gpt2",
                 output_dir: str = "./echo-finetuned",
                 epochs: int = 3,
                 batch_size: int = 4,
                 learning_rate: float = 5e-5,
                 **kwargs):
        """Fine-tune a Hugging Face model."""
        logger.info(f"Loading model: {model_name}")
        
        # Load tokenizer and model
        tokenizer = self.AutoTokenizer.from_pretrained(model_name)
        model = self.AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add pad token if needed
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Prepare dataset
        dataset = self.prepare_dataset(examples, tokenizer)
        
        # Training arguments
        training_args = self.TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
            logging_dir=f"{output_dir}/logs",
            logging_steps=10,
            save_steps=100,
            save_total_limit=2,
            **kwargs
        )
        
        # Data collator
        data_collator = self.DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = self.Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator
        )
        
        # Train
        logger.info("Starting fine-tuning...")
        trainer.train()
        
        # Save
        logger.info(f"Saving model to {output_dir}")
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        logger.info("Fine-tuning complete!")
        return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune an LLM with Deep Tree Echo identity"
    )
    
    parser.add_argument(
        '--dataset',
        type=str,
        default='training_dataset.jsonl',
        help='Path to training dataset (default: training_dataset.jsonl)'
    )
    
    parser.add_argument(
        '--provider',
        type=str,
        choices=['openai', 'huggingface'],
        help='Fine-tuning provider'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Base model to fine-tune (e.g., gpt-3.5-turbo, gpt2, llama2)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./echo-finetuned',
        help='Output directory for fine-tuned model'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=3,
        help='Number of training epochs (for HuggingFace)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=4,
        help='Training batch size (for HuggingFace)'
    )
    
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=5e-5,
        help='Learning rate (for HuggingFace)'
    )
    
    parser.add_argument(
        '--prepare-only',
        action='store_true',
        help='Only prepare the dataset without training'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key for OpenAI'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration JSON file'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    if args.config and Path(args.config).exists():
        with open(args.config, 'r') as f:
            config = json.load(f)
            # Update args with config values
            for key, value in config.items():
                if not getattr(args, key, None):
                    setattr(args, key, value)
    
    # Validate and load dataset
    validator = DatasetValidator(args.dataset)
    examples = validator.load_and_validate()
    validator.print_stats()
    
    if not examples:
        logger.error("No valid examples found in dataset")
        return 1
    
    # Prepare-only mode
    if args.prepare_only:
        output_path = args.output_dir if args.output_dir else 'prepared_dataset.jsonl'
        logger.info(f"Preparing dataset only, saving to: {output_path}")
        
        if args.provider == 'openai':
            tuner = OpenAIFineTuner()
            tuner.prepare_dataset(examples, output_path)
        else:
            # Generic JSONL format
            with open(output_path, 'w', encoding='utf-8') as f:
                for ex in examples:
                    f.write(json.dumps(ex) + '\n')
        
        logger.info(f"Dataset prepared: {output_path}")
        return 0
    
    # Fine-tuning
    if not args.provider:
        logger.error("Please specify --provider (openai or huggingface)")
        return 1
    
    if args.provider == 'openai':
        if not args.model:
            args.model = 'gpt-3.5-turbo'
        
        tuner = OpenAIFineTuner(api_key=args.api_key)
        
        # Prepare dataset
        prepared_path = f"{args.output_dir}/openai_format.jsonl"
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
        tuner.prepare_dataset(examples, prepared_path)
        
        # Start fine-tuning
        job = tuner.upload_and_finetune(
            prepared_path,
            model=args.model,
            suffix="echo"
        )
        
        logger.info(f"Fine-tuning job started: {job.id}")
        
    elif args.provider == 'huggingface':
        if not args.model:
            args.model = 'gpt2'
        
        tuner = HuggingFaceFineTuner()
        output_dir = tuner.finetune(
            examples,
            model_name=args.model,
            output_dir=args.output_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate
        )
        
        logger.info(f"Model saved to: {output_dir}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
