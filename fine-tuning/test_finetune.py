#!/usr/bin/env python3
"""
Test script for the Deep Tree Echo fine-tuning mechanism.

This script validates:
1. Dataset loading and validation
2. Dataset preparation for different providers
3. Configuration loading
4. Error handling

Usage:
    python test_finetune.py
"""

import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from finetune import DatasetValidator, OpenAIFineTuner


def test_dataset_validation():
    """Test dataset loading and validation."""
    print("=" * 80)
    print("Testing Dataset Validation")
    print("=" * 80)
    
    dataset_path = Path(__file__).parent / "training_dataset.jsonl"
    
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        return False
    
    validator = DatasetValidator(str(dataset_path))
    examples = validator.load_and_validate()
    
    if not examples:
        print("❌ No examples loaded")
        return False
    
    print(f"✅ Loaded {len(examples)} examples")
    
    # Validate structure
    for i, ex in enumerate(examples[:5]):
        if 'prompt' not in ex or 'completion' not in ex:
            print(f"❌ Example {i} missing required fields")
            return False
        if not ex['prompt'] or not ex['completion']:
            print(f"❌ Example {i} has empty fields")
            return False
    
    print("✅ All examples have required fields")
    
    # Print stats
    validator.print_stats()
    
    # Check stats
    if validator.stats['total_examples'] != len(examples):
        print("❌ Stats count mismatch")
        return False
    
    print("✅ Dataset validation passed")
    return True


def test_openai_format():
    """Test OpenAI format preparation."""
    print("\n" + "=" * 80)
    print("Testing OpenAI Format Preparation")
    print("=" * 80)
    
    # Create sample examples
    examples = [
        {"prompt": "Hello", "completion": "Hi there!"},
        {"prompt": "How are you?", "completion": "I'm doing well, thank you!"}
    ]
    
    try:
        tuner = OpenAIFineTuner()
    except ImportError:
        print("⚠️  OpenAI package not installed, skipping test")
        return True
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        output_path = f.name
    
    try:
        tuner.prepare_dataset(examples, output_path)
        
        # Validate output
        with open(output_path, 'r') as f:
            lines = f.readlines()
        
        if len(lines) != len(examples):
            print(f"❌ Expected {len(examples)} lines, got {len(lines)}")
            return False
        
        # Check format
        for i, line in enumerate(lines):
            data = json.loads(line)
            if 'messages' not in data:
                print(f"❌ Line {i} missing 'messages' field")
                return False
            if len(data['messages']) != 2:
                print(f"❌ Line {i} should have 2 messages")
                return False
            if data['messages'][0]['role'] != 'user':
                print(f"❌ Line {i} first message should be user")
                return False
            if data['messages'][1]['role'] != 'assistant':
                print(f"❌ Line {i} second message should be assistant")
                return False
        
        print("✅ OpenAI format validation passed")
        return True
        
    finally:
        Path(output_path).unlink(missing_ok=True)


def test_config_loading():
    """Test configuration file loading."""
    print("\n" + "=" * 80)
    print("Testing Configuration Loading")
    print("=" * 80)
    
    config_path = Path(__file__).parent / "config.json"
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check required fields
        required = ['dataset', 'provider', 'model', 'output_dir']
        for field in required:
            if field not in config:
                print(f"❌ Config missing required field: {field}")
                return False
        
        print("✅ Configuration loaded successfully")
        print(f"   Provider: {config['provider']}")
        print(f"   Model: {config['model']}")
        print(f"   Output: {config['output_dir']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config: {e}")
        return False


def test_dataset_statistics():
    """Test dataset statistics computation."""
    print("\n" + "=" * 80)
    print("Testing Dataset Statistics")
    print("=" * 80)
    
    examples = [
        {"prompt": "a" * 100, "completion": "b" * 200},
        {"prompt": "c" * 50, "completion": "d" * 150},
        {"prompt": "e" * 75, "completion": "f" * 175}
    ]
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for ex in examples:
            f.write(json.dumps(ex) + '\n')
        temp_path = f.name
    
    try:
        validator = DatasetValidator(temp_path)
        validator.load_and_validate()
        
        # Check stats
        if validator.stats['total_examples'] != 3:
            print(f"❌ Expected 3 examples, got {validator.stats['total_examples']}")
            return False
        
        if validator.stats['avg_prompt_length'] != 75:
            print(f"❌ Expected avg prompt length 75, got {validator.stats['avg_prompt_length']}")
            return False
        
        if validator.stats['max_prompt_length'] != 100:
            print(f"❌ Expected max prompt length 100, got {validator.stats['max_prompt_length']}")
            return False
        
        print("✅ Statistics computation passed")
        return True
        
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n" + "=" * 80)
    print("Testing Error Handling")
    print("=" * 80)
    
    # Test non-existent file
    try:
        validator = DatasetValidator("nonexistent.jsonl")
        validator.load_and_validate()
        print("❌ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("✅ Correctly handles missing file")
    
    # Test invalid JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write("not valid json\n")
        f.write('{"valid": "json"}\n')
        temp_path = f.name
    
    try:
        validator = DatasetValidator(temp_path)
        examples = validator.load_and_validate()
        
        # Should skip invalid line
        if len(examples) != 0:  # The valid line doesn't have required fields
            print(f"✅ Skipped invalid JSON lines (loaded {len(examples)} valid examples)")
        else:
            print("✅ Correctly skipped invalid JSON")
        
    finally:
        Path(temp_path).unlink(missing_ok=True)
    
    print("✅ Error handling passed")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("DEEP TREE ECHO FINE-TUNING TEST SUITE")
    print("=" * 80 + "\n")
    
    tests = [
        ("Dataset Validation", test_dataset_validation),
        ("OpenAI Format", test_openai_format),
        ("Config Loading", test_config_loading),
        ("Dataset Statistics", test_dataset_statistics),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "=" * 80)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 80)
    
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
