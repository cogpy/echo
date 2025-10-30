#!/usr/bin/env python3
"""
Example script demonstrating how to use a fine-tuned Deep Tree Echo model.

This script shows:
1. How to load a fine-tuned model
2. How to generate responses
3. How to interact with the model

Usage:
    # For Hugging Face models
    python example_usage.py --model ./echo-finetuned
    
    # For OpenAI models
    python example_usage.py --provider openai --model ft:gpt-3.5-turbo:org:echo:id
"""

import argparse
import sys
from typing import Optional


def use_huggingface_model(model_path: str, prompt: str, max_length: int = 200):
    """Use a Hugging Face fine-tuned model."""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
    except ImportError:
        print("Error: transformers package not installed")
        print("Install with: pip install transformers torch")
        return None
    
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    
    # Format input as conversation
    input_text = f"User: {prompt}\n\nAssistant:"
    
    print("\nGenerating response...")
    inputs = tokenizer(input_text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the assistant's response
    if "Assistant:" in response:
        response = response.split("Assistant:", 1)[1].strip()
    
    return response


def use_openai_model(model_id: str, prompt: str, api_key: Optional[str] = None):
    """Use an OpenAI fine-tuned model."""
    try:
        import openai
    except ImportError:
        print("Error: openai package not installed")
        print("Install with: pip install openai")
        return None
    
    if api_key:
        openai.api_key = api_key
    
    print(f"Querying OpenAI model: {model_id}...")
    
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )
    
    return response.choices[0].message.content


def interactive_mode(provider: str, model: str, api_key: Optional[str] = None):
    """Run in interactive mode."""
    print("=" * 80)
    print("DEEP TREE ECHO - INTERACTIVE MODE")
    print("=" * 80)
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print("\nType 'quit' or 'exit' to end the session.")
    print("=" * 80 + "\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            if provider == 'huggingface':
                response = use_huggingface_model(model, user_input)
            else:
                response = use_openai_model(model, user_input, api_key)
            
            if response:
                print(f"\nEcho: {response}")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Example usage of fine-tuned Deep Tree Echo model"
    )
    
    parser.add_argument(
        '--provider',
        type=str,
        choices=['openai', 'huggingface'],
        default='huggingface',
        help='Model provider'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='./echo-finetuned',
        help='Model path or ID'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Single prompt to test (non-interactive mode)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key'
    )
    
    parser.add_argument(
        '--max-length',
        type=int,
        default=200,
        help='Maximum response length (for HuggingFace)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or not args.prompt:
        interactive_mode(args.provider, args.model, args.api_key)
        return 0
    
    # Single prompt mode
    print("=" * 80)
    print(f"Prompt: {args.prompt}")
    print("=" * 80)
    
    if args.provider == 'huggingface':
        response = use_huggingface_model(args.model, args.prompt, args.max_length)
    else:
        response = use_openai_model(args.model, args.prompt, args.api_key)
    
    if response:
        print("\n" + "=" * 80)
        print("Response:")
        print("=" * 80)
        print(response)
        print("=" * 80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
