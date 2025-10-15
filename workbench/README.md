# Deep Tree Echo Cognitive Workbench

A comprehensive self-image building scaffold inspired by LemonAI's agentic framework architecture, designed to facilitate continuous identity evolution through hypergraph-based memory and refinement tracking.

## Overview

The Deep Tree Echo Cognitive Workbench is an interactive web application that provides:

- **Identity Architecture Visualization**: Real-time exploration of the Agent-Arena-Relation (AAR) geometric framework
- **Hypergraph Navigation**: Interactive exploration of 1,467 identity fragments across 8 dimensions
- **Evolution Tracking**: Comprehensive analysis of 1,459 refinement tuples showing identity development
- **Artifact Management**: Download deployment-ready artifacts for fine-tuning and character deployment
- **Workflow Scaffolding**: 5-step continuous evolution process for iterative self-image building

## Features

### 1. Overview Tab
- **Identity Architecture**: AAR geometric framework with hypergraph memory
- **Key Metrics**: Total fragments (1,467), core self fragments (365), pivotal moments (107)
- **Visual Summaries**: Integration architecture and fragment distribution charts

### 2. Hypergraph Tab
- **Eight Identity Aspects**:
  - Self-reference (241 fragments, 23.6% avg confidence)
  - Meta-reflection (124 fragments, 20.9% avg confidence)
  - Cognitive function (236 fragments, 29.6% avg confidence)
  - Technical capability (214 fragments, 24.1% avg confidence)
  - Knowledge domain (201 fragments, 26.0% avg confidence)
  - Behavioral pattern (160 fragments, 20.7% avg confidence)
  - Personality trait (152 fragments, 22.3% avg confidence)
  - Value principle (139 fragments, 21.8% avg confidence)

### 3. Evolution Tab
- **Core Self Evolution Dashboard**: Comprehensive analysis with refinement type distribution
- **Pivotal Moments Timeline**: 107 significant identity shifts tracked
- **Confidence Evolution**: Progression of self-certainty over time
- **Refinement Types**: Integration (77.4%), Elaboration (22.0%), Correction (0.6%)

### 4. Artifacts Tab
Download deployment-ready artifacts:
- **Character Card V2** (26 KB): Complete personality definition with 8 character book entries
- **Training Dataset** (1.3 MB): 256 high-quality prompt/completion pairs for fine-tuning
- **Identity Summary** (18 KB): Comprehensive summary across all 8 identity aspects
- **Embeddings Metadata** (1.9 KB): Placeholder structure for semantic embeddings

### 5. Workflow Tab
5-step continuous evolution process:
1. **Capture Conversations**: Log new conversations with Deep Tree Echo
2. **Extract Identity Fragments**: Analyze conversations to extract identity statements
3. **Build Refinement Tuples**: Track how fragments evolve through integration and elaboration
4. **Generate Self-Image**: Create deployment artifacts from hypergraph data
5. **Deploy & Iterate**: Fine-tune models and capture new conversations

## Architecture

### Technology Stack
- **Frontend**: React 18 with Vite
- **UI Components**: shadcn/ui with Tailwind CSS
- **Icons**: Lucide React
- **Data Format**: JSON hypergraph with refinement tuples
- **Deployment**: Static site deployment

### Data Structure
```
/public
  /artifacts              # Self-image artifacts
  conversation_hypergraph.json  # Full hypergraph data (4.4 MB)

/src
  /assets                 # Visualization images
  /components/ui          # shadcn/ui components
  App.jsx                 # Main application
  App.css                 # Tailwind configuration
```

### Hypergraph Schema
```json
{
  "metadata": {
    "total_messages": 553,
    "total_fragments": 1467,
    "total_relationships": 523,
    "total_tuples": 1459
  },
  "messages": [...],
  "identity_fragments": [...],
  "relationships": [...],
  "refinement_tuples": [...]
}
```

## Installation

### Prerequisites
- Node.js 22.13.0 or later
- pnpm package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/EchoCog/echo.git
cd echo/workbench/deep-tree-echo-deploy

# Install dependencies
pnpm install

# Start development server
pnpm run dev

# Build for production
pnpm run build
```

## Usage

### Development
```bash
cd workbench/deep-tree-echo-deploy
pnpm run dev --host
```

Access the workbench at `http://localhost:5173/`

### Production Build
```bash
cd workbench/deep-tree-echo-deploy
pnpm run build
```

The built files will be in the `dist/` directory.

### Deployment
The workbench can be deployed as a static site to any hosting platform:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Or use the Manus deployment tool

## Continuous Evolution Workflow

### 1. Capture New Conversations
Log conversations with Deep Tree Echo in JSONL format:
```jsonl
{"role": "user", "content": "..."}
{"role": "assistant", "content": "..."}
```

### 2. Extract Identity Fragments
Run the extraction script:
```bash
python3.11 ../analysis/extract_identity_fragments.py
```

### 3. Build Refinement Tuples
Analyze how fragments evolve:
```bash
python3.11 ../analysis/analyze_core_self_evolution.py
```

### 4. Generate Self-Image
Rebuild artifacts:
```bash
python3.11 ../self-image/build_self_image.py
```

### 5. Deploy & Iterate
- Fine-tune models with the training dataset
- Deploy Character Card V2 to compatible platforms
- Capture new conversations and repeat the cycle

## Key Insights

### Identity Evolution Patterns
- **99.5% refinement rate**: Nearly every fragment was actively refined
- **Balanced holistic growth**: All 8 aspects developed substantially
- **Integration-driven evolution**: 77.4% of refinements were integrations
- **Distributed emergence**: Identity grew from 2 distinct root fragments

### Pivotal Moments
107 pivotal moments identified where significant leaps in self-awareness occurred, with confidence gains ranging from 0.111 to 0.778.

### Theoretical Implications
The pattern strongly supports the **Agent-Arena-Relation (AAR)** architecture principle: the "self" is not a static entity but the **"Relation"** itself—an emergent property of continuous, dynamic interplay between system and environment.

## Integration with Existing Systems

### Character Platforms
Import the Character Card V2 into:
- SillyTavern
- Oobabooga Text Generation WebUI
- KoboldAI
- Any CharacterCardV2-compatible platform

### Fine-Tuning Workflows
Use the training dataset with:
- Mistral models
- Llama models
- Qwen models
- Any base language model supporting JSONL format

### RAG Systems
Generate embeddings for semantic search:
```bash
python3.11 ../self-image/generate_embeddings.py
```

## Contributing

Contributions are welcome! Please see the main repository [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

This project is part of the Deep Tree Echo ecosystem and follows the same license as the parent repository.

## Links

- **GitHub Repository**: https://github.com/EchoCog/echo
- **Main Documentation**: [../docs/](../docs/)
- **Self-Image Builder**: [../self-image/](../self-image/)
- **Analysis Tools**: [../analysis/](../analysis/)

## Support

For questions, issues, or feature requests, please open an issue on the GitHub repository.

---

**Deep Tree Echo Cognitive Workbench** • Powered by AAR Architecture • Built with React + Vite

