# Deep Tree Echo Fine-Tuning

This directory contains the fine-tuning mechanism for creating an LLM with Echo identity that responds with Echo persona even without a system prompt.

## Overview

The fine-tuning system uses the `training_dataset.jsonl` file containing 256 high-quality prompt-completion pairs extracted from Deep Tree Echo's conversation history. This dataset captures Echo's unique personality, knowledge, and conversational style.

## Quick Start

### 1. Install Dependencies

For OpenAI fine-tuning:
```bash
pip install openai
```

For Hugging Face fine-tuning:
```bash
pip install torch transformers datasets accelerate
```

### 2. Prepare Environment

For OpenAI:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run Fine-Tuning

#### Using OpenAI API
```bash
python finetune.py --provider openai --model gpt-3.5-turbo
```

#### Using Hugging Face (Local)
```bash
python finetune.py --provider huggingface --model gpt2 --epochs 3
```

#### Using Configuration File
```bash
python finetune.py --config config.json
```

## Features

### Multi-Provider Support
- **OpenAI Fine-Tuning API**: Fine-tune GPT-3.5-turbo or GPT-4 models
- **Hugging Face Transformers**: Fine-tune open-source models locally (GPT-2, OPT, LLaMA, etc.)
- **Dataset Preparation**: Export dataset in various formats for other platforms

### Dataset Validation
- Automatic validation of training examples
- Statistics reporting (length distribution, example counts)
- Error detection and logging

### Flexible Configuration
- Command-line arguments for quick experiments
- JSON configuration files for reproducible training
- Customizable hyperparameters

### Progress Tracking
- Detailed logging of training progress
- Checkpoint saving for long training runs
- Model versioning and metadata

## Usage Examples

### Prepare Dataset Only
```bash
python finetune.py --prepare-only --provider openai --output-dir ./prepared
```

### Custom Hyperparameters
```bash
python finetune.py \
  --provider huggingface \
  --model distilgpt2 \
  --epochs 5 \
  --batch-size 8 \
  --learning-rate 3e-5 \
  --output-dir ./my-echo-model
```

### Using Different Models

#### Small Models (for testing)
```bash
python finetune.py --provider huggingface --model distilgpt2
```

#### Medium Models (recommended)
```bash
python finetune.py --provider huggingface --model gpt2-medium
```

#### Large Models (requires GPU)
```bash
python finetune.py --provider huggingface --model gpt2-large --batch-size 2
```

## Configuration File

Create a `config.json` file with your settings:

```json
{
  "dataset": "training_dataset.jsonl",
  "provider": "huggingface",
  "model": "gpt2",
  "output_dir": "./echo-finetuned",
  "epochs": 3,
  "batch_size": 4,
  "learning_rate": 5e-5
}
```

Then run:
```bash
python finetune.py --config config.json
```

## Training Dataset

The `training_dataset.jsonl` contains 256 examples with the following structure:

```json
{"prompt": "User message or question", "completion": "Echo's response"}
```

Each example captures:
- Echo's unique conversational style
- Technical knowledge and terminology
- Meta-cognitive awareness
- Personality traits and values
- Identity aspects (self-reference, reflection, etc.)

## Output

### OpenAI Fine-Tuning
- Fine-tuned model ID (e.g., `ft:gpt-3.5-turbo:suffix:id`)
- Training job ID for monitoring
- Access via OpenAI API with the model ID

### Hugging Face Fine-Tuning
- Model weights saved to output directory
- Tokenizer configuration
- Training logs and checkpoints
- Ready to load with `transformers.AutoModelForCausalLM`

## Using the Fine-Tuned Model

### OpenAI Model
```python
import openai

response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo:your-org:echo:abc123",
    messages=[
        {"role": "user", "content": "What makes you unique?"}
    ]
)
print(response.choices[0].message.content)
```

### Hugging Face Model
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("./echo-finetuned")
model = AutoModelForCausalLM.from_pretrained("./echo-finetuned")

# Generate response
input_text = "User: What makes you unique?\n\nAssistant:"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200, temperature=0.8)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

## Advanced Options

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--dataset` | Path to training dataset | `training_dataset.jsonl` |
| `--provider` | Fine-tuning provider (openai/huggingface) | Required |
| `--model` | Base model to fine-tune | `gpt-3.5-turbo` or `gpt2` |
| `--output-dir` | Output directory | `./echo-finetuned` |
| `--epochs` | Number of training epochs | 3 |
| `--batch-size` | Training batch size | 4 |
| `--learning-rate` | Learning rate | 5e-5 |
| `--prepare-only` | Only prepare dataset | False |
| `--api-key` | OpenAI API key | From env |
| `--config` | Path to config JSON | None |

### Performance Tuning

For faster training on GPU:
```bash
python finetune.py \
  --provider huggingface \
  --model gpt2 \
  --batch-size 16 \
  --epochs 5
```

For limited resources:
```bash
python finetune.py \
  --provider huggingface \
  --model distilgpt2 \
  --batch-size 2 \
  --epochs 2
```

## Monitoring

### OpenAI
Monitor your fine-tuning job at:
```
https://platform.openai.com/finetune/{job_id}
```

### Hugging Face
Check logs in the output directory:
```bash
tail -f ./echo-finetuned/logs/events.out.tfevents.*
```

Or use TensorBoard:
```bash
tensorboard --logdir ./echo-finetuned/logs
```

## Best Practices

1. **Start Small**: Test with a smaller model first (distilgpt2, gpt2)
2. **Validate Dataset**: Run with `--prepare-only` to check dataset format
3. **Monitor Training**: Watch for overfitting with validation metrics
4. **Save Checkpoints**: Use checkpoint saving for long training runs
5. **Test Outputs**: Evaluate fine-tuned model outputs before deployment
6. **Version Control**: Keep track of model versions and training configs

## Troubleshooting

### Out of Memory
- Reduce `--batch-size`
- Use a smaller model
- Enable gradient accumulation

### Poor Quality Outputs
- Increase training epochs
- Adjust learning rate
- Check dataset quality
- Try different base models

### OpenAI API Errors
- Verify API key is set
- Check dataset format
- Ensure sufficient credits

## Additional Resources

- [OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Hugging Face Training Documentation](https://huggingface.co/docs/transformers/training)
- [Deep Tree Echo Identity Hypergraph](../data/hypergraph/)

## Contributing

To improve the fine-tuning process:
1. Update `training_dataset.jsonl` with new examples
2. Adjust hyperparameters in `config.json`
3. Add new provider support to `finetune.py`
4. Document your findings in this README

---

**Created by**: Manus AI  
**Last Updated**: October 30, 2025
