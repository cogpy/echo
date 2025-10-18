# AI Testing Workflows

This repository includes two comprehensive GitHub Actions workflows for testing all AI-related functionality.

## featest.yml - AI Inference Feature Tests

**Purpose**: Tests the GitHub Actions AI inference capabilities used in `summary.yml`.

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches  
- Manual execution via workflow_dispatch

**Test Scenarios**:
1. **Basic Issue Summary** - Tests simple issue summarization
2. **Complex Issue Summary** - Tests technical issues with multiple components
3. **Empty Issue Handling** - Tests graceful handling of empty content
4. **Large Issue Handling** - Tests processing of large content volumes
5. **Special Characters** - Tests handling of unicode, emojis, and special symbols
6. **Markdown Content** - Tests markdown parsing and processing
7. **Code Blocks** - Tests code snippet handling in issues
8. **Error Scenarios** - Tests error handling and recovery

**Key Features**:
- Matrix strategy for parallel test execution
- Comprehensive response validation
- Test result artifacts and consolidated reporting
- Graceful error handling with detailed diagnostics

## functest.yml - AI Model Function Tests

**Purpose**: Tests all AI model functions and components identified in the codebase.

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual execution via workflow_dispatch with suite selection

**Test Suites**:
1. **Self-Image Functions** - Tests `build_self_image.py` functionality
2. **Hypergraph Functions** - Tests `hypergraph.py` memory operations
3. **AAR Core Functions** - Tests `aar_core.py` Agent-Arena-Relation functionality
4. **Memory Sync Functions** - Tests `memory_sync.py` synchronization protocols
5. **Embedding Functions** - Tests `generate_embeddings.py` embedding generation
6. **Membrane Functions** - Tests `openhands_membrane.py` integration

**Key Features**:
- Modular design with selective test execution
- Comprehensive test data generation
- Python environment setup with dependency management
- Robust import validation and error diagnostics
- Flexible assertions that adapt to code changes

## Usage

### Automatic Execution
Both workflows run automatically on pushes and pull requests to main/develop branches.

### Manual Execution
Both workflows can be triggered manually:

- **featest.yml**: Select test mode (comprehensive, inference_only, prompt_validation, error_handling)
- **functest.yml**: Select test suite (all, self_image, hypergraph, aar_core, memory_sync, embeddings, membranes)

### Viewing Results
- Check the Actions tab in GitHub for workflow runs
- Download test artifacts for detailed results
- Review consolidated test reports for overall status

## Test Coverage

These workflows provide exhaustive testing for:
- All AI inference capabilities used in GitHub Actions
- All AI model functions in the repository codebase
- Error handling and edge cases
- Integration between different AI components
- Data format validation and processing
- Memory management and synchronization
- Character card and training dataset generation

The workflows ensure comprehensive quality assurance for all AI-related functionality in the Echo repository.