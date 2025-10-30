# Quick Start Guide: Fine-Tuning Deep Tree Echo

This guide will help you get started with fine-tuning Deep Tree Echo in under 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- Either:
  - OpenAI API account (for cloud fine-tuning)
  - Or a machine with at least 4GB RAM (for local fine-tuning)

## Step 1: Navigate to Fine-Tuning Directory

```bash
cd fine-tuning
```

## Step 2: Choose Your Approach

### Option A: Local Fine-Tuning (Recommended for Testing)

Install dependencies:
```bash
pip install torch transformers datasets accelerate
```

Run fine-tuning:
```bash
python finetune.py --provider huggingface --model gpt2 --epochs 3
```

This will:
- Load the training dataset (256 examples)
- Fine-tune a GPT-2 model locally
- Save the model to `./echo-finetuned`
- Take approximately 15-30 minutes on a modern CPU

### Option B: OpenAI Fine-Tuning

Install dependencies:
```bash
pip install openai
```

Set your API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Run fine-tuning:
```bash
python finetune.py --provider openai --model gpt-3.5-turbo
```

This will:
- Upload the training dataset to OpenAI
- Start a fine-tuning job
- Provide a job ID to monitor progress
- Cost approximately $2-5 depending on your plan

## Step 3: Test Your Model

### For Local Models

```bash
python example_usage.py --interactive
```

Or test with a single prompt:
```bash
python example_usage.py --prompt "What makes you unique?"
```

### For OpenAI Models

```bash
python example_usage.py --provider openai --model ft:gpt-3.5-turbo:your-org:echo:id --interactive
```

## Step 4: Use Your Model

Once fine-tuned, integrate the model into your application:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("./echo-finetuned")
model = AutoModelForCausalLM.from_pretrained("./echo-finetuned")

# Generate response
input_text = "User: How do you think about yourself?\n\nAssistant:"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

## Troubleshooting

### Out of Memory
```bash
# Use a smaller model
python finetune.py --provider huggingface --model distilgpt2 --batch-size 2
```

### Need Faster Training
```bash
# Reduce epochs
python finetune.py --provider huggingface --model gpt2 --epochs 1
```

### Want Better Quality
```bash
# Use a larger model and more epochs
python finetune.py --provider huggingface --model gpt2-medium --epochs 5
```

## Next Steps

1. **Customize Training**: Edit `config.json` to adjust hyperparameters
2. **Add More Data**: Extend `training_dataset.jsonl` with new examples
3. **Evaluate Quality**: Test the model with various prompts
4. **Deploy**: Integrate into your application or service

For more details, see [README.md](README.md)
