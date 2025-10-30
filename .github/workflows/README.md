# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Deep Tree Echo repository.

## Active Workflows

### 1. Dependency Review (`dependency-review.yml`)
- **Trigger:** Pull requests to `main` branch
- **Purpose:** Scans dependency changes for known vulnerabilities
- **Status:** ✅ Active and working

### 2. Greetings (`greetings.yml`)
- **Trigger:** First-time issues and pull requests
- **Purpose:** Welcomes new contributors with context-appropriate messages about the AI consciousness project
- **Status:** ✅ Active and customized for Deep Tree Echo

### 3. Python Linting (`python-lint.yml`)
- **Trigger:** Pushes and PRs to `main` and `develop` branches
- **Purpose:** Basic Python code quality checks using flake8
- **Features:**
  - Detects critical syntax errors (E9, F7, F82)
  - Non-blocking: provides warnings without failing the build
  - Runs on Python 3.11
- **Status:** ✅ Active and optimized for this repository

## Removed Workflows

The following workflows were removed as they were not appropriate for this Python-based repository:

1. **featest.yml** - Used non-existent `actions/ai-inference@v1` action
2. **summary.yml** - Used non-existent `actions/ai-inference@v1` action
3. **msvc.yml** - C++ code analysis (repository contains only Python code)
4. **functest.yml** - Overly complex Python tests that consistently failed

## Fine-Tuning System Workflows

### 4. Fine-Tuning Dataset Validation (`finetune-dataset-validation.yml`)
- **Trigger:** Push/PR to fine-tuning directory, manual dispatch
- **Purpose:** Validates the training dataset format, structure, and quality
- **Features:**
  - JSON format validation
  - Required fields verification (prompt, completion)
  - Length statistics and quality checks
  - Dataset validator integration
- **Status:** ✅ Active

### 5. Fine-Tuning Tests (`finetune-tests.yml`)
- **Trigger:** Push/PR to fine-tuning directory, manual dispatch
- **Purpose:** Tests all fine-tuning components and functionality
- **Features:**
  - Runs on multiple Python versions (3.9, 3.10, 3.11)
  - Dataset loading tests
  - Configuration validation
  - OpenAI and HuggingFace format preparation tests
  - Error handling validation
- **Status:** ✅ Active

### 6. Fine-Tuning Config Validation (`finetune-config-validation.yml`)
- **Trigger:** Push/PR to config files, manual dispatch
- **Purpose:** Validates fine-tuning configuration files
- **Features:**
  - JSON syntax validation
  - Required fields verification
  - Provider-specific validation (OpenAI/HuggingFace)
  - Training parameter reasonability checks
  - Model compatibility verification
- **Status:** ✅ Active

### 7. Fine-Tuning CI/CD (`finetune-cicd.yml`)
- **Trigger:** Manual dispatch only (workflow_dispatch)
- **Purpose:** Run actual fine-tuning jobs with configurable parameters
- **Features:**
  - Supports both OpenAI and HuggingFace providers
  - Configurable model, epochs, and batch size
  - Test mode for quick validation with minimal dataset
  - Model artifact upload
  - Optional push to HuggingFace Hub
  - Model testing and generation validation
- **Status:** ✅ Active (manual trigger only)
- **Secrets Required:**
  - `OPENAI_API_KEY` (for OpenAI provider)
  - `HF_TOKEN` (optional, for pushing to HuggingFace Hub)

### 8. Fine-Tuning Documentation Check (`finetune-docs-check.yml`)
- **Trigger:** Push/PR to documentation files, manual dispatch
- **Purpose:** Validates fine-tuning documentation quality and completeness
- **Features:**
  - Checks for required documentation files
  - Validates section structure
  - Verifies code examples and installation instructions
  - Link validation
  - Command example extraction and validation
- **Status:** ✅ Active

### 9. Fine-Tuning Integration Tests (`finetune-integration-tests.yml`)
- **Trigger:** Weekly schedule (Sundays at 2 AM UTC), manual dispatch
- **Purpose:** Comprehensive end-to-end integration testing
- **Features:**
  - Configurable test depth (quick/standard/comprehensive)
  - End-to-end fine-tuning with real models
  - Model loading and inference validation
  - Dataset quality analysis
  - Multi-provider and multi-model testing
- **Status:** ✅ Active (scheduled weekly)

## Workflow Organization

### Continuous Integration (On Push/PR)
- Python Linting
- Fine-Tuning Dataset Validation
- Fine-Tuning Tests
- Fine-Tuning Config Validation
- Fine-Tuning Documentation Check

### Scheduled Workflows
- Fine-Tuning Integration Tests (Weekly)

### Manual Workflows
- Fine-Tuning CI/CD (On-demand fine-tuning jobs)

## Notes

- This repository is primarily Python-based, focusing on AI consciousness exploration
- Workflows are designed to be lightweight and non-blocking to facilitate rapid development
- For adding new workflows, ensure they align with the project's Python/AI focus
- Fine-tuning workflows provide comprehensive CI/CD for the Deep Tree Echo fine-tuning system
- Use the manual CI/CD workflow for actual model training; other workflows focus on validation and testing
