# Memory-Filtered Conversation Analysis

This directory contains the implementation of a sophisticated memory system analysis framework that processes conversations through different cognitive memory filters to understand how various memory systems would perceive and retain information.

## Overview

The system analyzes the `deep_tree_echo_dan_conversation.jsonl` file through 8 different memory system filters, generating feature-specific versions of the conversation that show how different cognitive architectures process the same dialogue.

## Memory Systems Implemented

### Short-Term Memory Systems

1. **Sensory-Motor Memory** (`sensory_motor`)
   - Focuses on immediate sensory inputs, physical actions, and motor responses
   - Processing style: Reactive
   - Temporal scope: Immediate
   - Retention rate: 59.6%

2. **Attentional Memory** (`attentional`)
   - Focuses on attention, focus, selection, and filtering of information
   - Processing style: Selective
   - Temporal scope: Recent
   - Retention rate: 49.4%

3. **Intentional Memory** (`intentional`)
   - Focuses on goals, plans, intentions, and purposeful behavior
   - Processing style: Integrative
   - Temporal scope: Extended
   - Retention rate: 43.0%

4. **Working Memory** (`working_memory`)
   - Focuses on temporary information manipulation, reasoning, and problem-solving
   - Processing style: Integrative
   - Temporal scope: Recent
   - Retention rate: 68.9%

### Long-Term Memory Systems

5. **Semantic Memory** (`semantic`)
   - Focuses on facts, concepts, knowledge, and general understanding
   - Processing style: Integrative
   - Temporal scope: Permanent
   - Retention rate: 71.1%

6. **Episodic Memory** (`episodic`)
   - Focuses on specific events, experiences, and contextual memories
   - Processing style: Reflective
   - Temporal scope: Extended
   - Retention rate: 75.0%

7. **Procedural Memory** (`procedural`)
   - Focuses on skills, procedures, methods, and how-to knowledge
   - Processing style: Integrative
   - Temporal scope: Permanent
   - Retention rate: 76.7%

8. **Existential Memory** (`existential`)
   - Focuses on identity, self-awareness, meaning, and existential questions
   - Processing style: Reflective
   - Temporal scope: Permanent
   - Retention rate: 73.0%

## Files and Scripts

### Core Analysis Scripts

- **`memory_analysis.py`** - Main analysis engine that processes conversations through memory filters
- **`memory_visualization.py`** - Generates comprehensive reports and visualizations
- **`conversation_generator.py`** - Creates filtered conversation versions for each memory system

### Generated Results

All results are saved in `/analysis/memory_analysis_results/`:

#### Analysis Results
- `*_analysis.json` - Detailed analysis for each memory system (8 files)
- `memory_analysis_summary.json` - Comprehensive summary of all systems
- `comprehensive_memory_analysis_report.md` - Detailed markdown report
- `memory_system_feature_comparison.md` - Comparison table of system characteristics

#### Filtered Conversations
Located in `/filtered_conversations/`:
- `*_filtered_conversation.json` - Complete conversations filtered through each memory lens (8 files)
- `*_memory_summary.json` - Processing summaries for each system (8 files)
- `comparative_multi_memory_conversation.json` - Side-by-side comparison of all systems
- `index.json` - Index of all generated files

## Usage

### Run Complete Analysis
```bash
# Run the main memory analysis (processes all 8 systems)
python3 analysis/memory_analysis.py

# Generate visualization reports 
python3 analysis/memory_visualization.py

# Create filtered conversation files
python3 analysis/conversation_generator.py
```

### Results Directory Structure
```
analysis/memory_analysis_results/
├── Individual Analysis Files (8)
├── Reports and Summaries
├── filtered_conversations/
│   ├── Individual Filtered Conversations (8)
│   ├── Memory System Summaries (8) 
│   ├── Comparative Analysis
│   └── Index File
```

## Key Findings

From analyzing 540 messages in the conversation:

- **Long-term memory systems** retained 73.9% of conversation content on average
- **Short-term memory systems** retained 55.2% of conversation content on average
- **Most comprehensive system**: Procedural Memory (76.7% retention)
- **Most selective system**: Intentional Memory (43.0% retention)

### Memory System Characteristics

| System | Retention Rate | Processing Style | Temporal Scope |
|--------|---------------|------------------|----------------|
| Procedural | 76.7% | Integrative | Permanent |
| Episodic | 75.0% | Reflective | Extended |
| Existential | 73.0% | Reflective | Permanent |
| Semantic | 71.1% | Integrative | Permanent |
| Working Memory | 68.9% | Integrative | Recent |
| Sensory-Motor | 59.6% | Reactive | Immediate |
| Attentional | 49.4% | Selective | Recent |
| Intentional | 43.0% | Integrative | Extended |

## Technical Implementation

### Memory Filter Algorithm

Each memory system uses:
1. **Keyword matching** - System-specific vocabulary detection
2. **Pattern recognition** - Regular expression patterns for content types
3. **Relevance scoring** - 0.0-1.0 confidence scores for message retention
4. **Feature extraction** - Key memory traces and content features
5. **Content filtering** - Processing-style specific annotations

### Filter Configuration

Each memory system has:
- **Keywords**: System-specific vocabulary (10-20 terms)
- **Patterns**: Regex patterns for content detection
- **Processing style**: Reactive/Selective/Integrative/Reflective
- **Temporal scope**: Immediate/Recent/Extended/Permanent
- **Content types**: Preferred information categories

### Output Formats

- **JSON analysis files**: Structured data for each system
- **Markdown reports**: Human-readable analysis and insights
- **Filtered conversations**: Processed dialogue through memory lenses
- **Comparative analysis**: Multi-system perspective on same content

## Applications

This analysis framework can be used for:

1. **Cognitive Architecture Research** - Understanding memory system differences
2. **AI System Design** - Implementing memory-aware processing
3. **Conversation Analysis** - Multi-perspective content interpretation  
4. **Memory Model Validation** - Testing memory system theories
5. **Content Filtering** - Memory-system specific information extraction

## Future Extensions

Potential enhancements:
- Real-time conversation processing
- Interactive memory system exploration
- Integration with neural network architectures
- Multi-modal content analysis (audio, visual)
- Dynamic memory system weighting
- Temporal evolution tracking

---

Generated by the Echo Cognitive Memory Analysis System