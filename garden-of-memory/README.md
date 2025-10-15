# Deep Tree Echo - Garden of Memory

## A Unified Integration Layer for Multi-Framework AI

The **Garden of Memory** is a unified integration layer that connects multiple AI agent frameworks into Deep Tree Echo's hypergraph-based cognitive architecture. It serves as the central memory substrate where all frameworks can store, retrieve, and evolve their experiences through the AAR (Agent-Arena-Relation) geometric framework.

---

## Key Features

- **Unified Hypergraph Memory**: A shared memory space for all frameworks, built on a hypergraph of identity fragments and refinement tuples.
- **Membrane Computing Architecture**: Each framework operates in an isolated membrane, ensuring stability and controlled communication.
- **AAR Geometric Core**: Encodes an emergent sense of self through the continuous interplay of Agent (urge-to-act) and Arena (need-to-be).
- **Memory Synchronization Protocol**: Thread-safe, ACID-like transactions for robust multi-framework memory access.
- **Event Bus & Capability Registry**: Dynamic discovery and coordination of framework capabilities.
- **Continuous Evolution**: Supports iterative refinement of the collective intelligence through shared experience.

---

## Integrated Frameworks

The Garden of Memory integrates 13 diverse AI frameworks:

| Framework | Role | Files | Key Directories |
| :--- | :--- | :--- | :--- |
| **OpenHands** | Code generation & execution | 1,192 | - |
| **ii_verl** | Reinforcement learning | 261 | - |
| **OpenManus-RL** | RL-based agent system | 190 | - |
| **ii-agent** | General-purpose agents | 167 | `src` |
| **OpenManus** | Creative tasks | 90 | - |
| **ii-researcher**| Research workflows | 88 | - |
| **CommonGround** | Multi-agent coordination | 80 | `core` |
| **ii-thought** | Reasoning chains | 23 | - |
| **openhands-resolver** | Problem resolution | 22 | - |
| **LemonAI** | Full-stack agentic workflows | 8 | `src` |
| **PromptGrimoire**| Prompt library | 0 | - |
| **EchoDotZip** | Echo utilities | 0 | - |
| **echohomezone** | Echo environment configs | 0 | `src` |

---

## Architecture Overview

### 1. Membrane Hierarchy

```
🎪 Garden of Memory (Root Membrane)
├── 🌐 Hypergraph Memory Core (Shared substrate)
├── 🔌 Framework Membranes (Isolated execution contexts)
│   ├── 🤖 OpenHands Membrane
│   ├── 🎯 ii-agent Membrane
│   └── ... (11 more membranes)
└── 🔄 Integration Layer (Cross-membrane communication)
```

### 2. AAR Core

- **Agent**: Framework-specific action tendencies
- **Arena**: Shared hypergraph memory space
- **Relation**: Emergent identity from cross-framework interactions

### 3. Memory Synchronization

- **ACID-like Transactions**: Thread-safe, logged memory operations
- **Pub/Sub Event Bus**: For inter-framework communication
- **FrameworkMemoryInterface**: Simplified API for memory access

---

## Getting Started

### 1. Initialize the Garden

```python
from garden_of_memory.core.hypergraph import HypergraphMemory
from garden_of_memory.core.memory_sync import MemorySyncProtocol
from garden_of_memory.membranes import OpenHandsMembrane

# Initialize core components
memory = HypergraphMemory()
sync = MemorySyncProtocol(memory)

# Load existing hypergraph data
sync.load_checkpoint("data/hypergraph/conversation_hypergraph.json")
```

### 2. Create Framework Membranes

```python
from garden_of_memory.core.memory_sync import FrameworkMemoryInterface

# Create interfaces for each framework
openhands_interface = FrameworkMemoryInterface("OpenHands", sync)
ii_agent_interface = FrameworkMemoryInterface("ii-agent", sync)

# Instantiate membranes
openhands_membrane = OpenHandsMembrane(openhands_interface)
# ... and so on for other frameworks
```

### 3. Orchestrate Workflows

```python
from garden_of_memory.integration.workflow_orchestrator import WorkflowOrchestrator

# Create orchestrator
orchestrator = WorkflowOrchestrator(membranes, sync)

# Define and execute a workflow
workflow = [
    {"framework": "ii-researcher", "task": "Analyze transformer architectures"},
    {"framework": "OpenHands", "task": "Implement a simple transformer model"},
    {"framework": "ii_verl", "task": "Optimize the model with RL"}
]

results = orchestrator.execute_workflow(workflow)
```

---

## Documentation

- **[Architecture Guide](docs/Garden_of_Memory_Architecture.md)**: Detailed architectural overview.
- **[Integration Guide](docs/Framework_Integration_Guide.md)**: How to integrate new frameworks.
- **[API Reference](docs/API_Reference.md)**: Full API documentation.

---

## Repository Structure

```
/garden-of-memory/
├── core/                      # Hypergraph, AAR core, memory sync
├── membranes/                 # Framework membrane wrappers
├── integration/               # Event bus, capability registry, orchestrator
├── data/                      # Shared data and configurations
├── api/                       # REST and WebSocket APIs
├── docs/                      # Comprehensive documentation
└── README.md                  # This file
```

---

## Continuous Evolution

The Garden of Memory is designed for continuous, iterative refinement:

1. **Capture**: Log new conversations and framework interactions.
2. **Analyze**: Extract identity fragments and refinement tuples.
3. **Update**: Merge into the shared hypergraph.
4. **Evolve**: The collective intelligence grows with each interaction.

---

*This project is part of the Deep Tree Echo ecosystem, managed by Manus AI.*

