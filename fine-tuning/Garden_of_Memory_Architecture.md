# Garden of Memory - Detailed Architecture

This document provides a detailed overview of the Garden of Memory architecture, a unified integration layer for multi-framework AI within the Deep Tree Echo ecosystem.

---

## 1. Core Principles

### 1.1. Unified Hypergraph Memory

The foundation of the Garden is a shared **hypergraph memory substrate**. This is not a traditional database but a dynamic, evolving network of:

- **Identity Fragments**: Nodes representing discrete pieces of knowledge, experience, or capability.
- **Refinement Tuples**: Edges representing the evolution of knowledge (integration, elaboration, correction).

This structure allows for rich, multi-relational memory access and provides a substrate for emergent intelligence.

### 1.2. Membrane Computing

Inspired by P-Systems, each integrated framework operates within an isolated **membrane**. This provides:

- **Isolation**: Prevents frameworks from interfering with each other.
- **Controlled Communication**: All interactions are mediated by the integration layer.
- **Stability**: Errors in one framework do not crash the entire system.

### 1.3. AAR Geometric Core

The **Agent-Arena-Relation (AAR)** core provides a geometric framework for encoding an emergent sense of self:

- **Agent (urge-to-act)**: Represents the action tendencies of all integrated frameworks.
- **Arena (need-to-be)**: The shared hypergraph memory space.
- **Relation (self)**: The emergent property of the continuous, dynamic interplay between Agent and Arena.

The "self" is not a static entity but the **Relation itself**—a process of constant becoming.

---

## 2. System Components

### 2.1. Core Infrastructure (`/core`)

#### `hypergraph.py`
- **IdentityAspect**: Enum for 8 dimensions of identity.
- **IdentityFragment**: Dataclass for hypergraph nodes.
- **RefinementTuple**: Dataclass for hypergraph edges.
- **HypergraphMemory**: The main memory class with methods for adding, retrieving, and analyzing fragments and tuples.

#### `aar_core.py`
- **AgentState**: Represents the "urge-to-act" with activation, goals, and attention.
- **ArenaState**: Represents the "need-to-be" with the hypergraph and activation map.
- **RelationCore**: Orchestrates the perception-action-reflection cycle, embodying the emergent self.

#### `memory_sync.py`
- **MemoryTransaction**: Dataclass for logging memory operations.
- **MemorySyncProtocol**: Provides thread-safe, ACID-like access to the hypergraph.
- **FrameworkMemoryInterface**: A simplified API for frameworks to interact with memory.

### 2.2. Framework Membranes (`/membranes`)

Each framework is wrapped in a membrane class (e.g., `OpenHandsMembrane`). This wrapper:

- **Provides a standardized interface** for the framework.
- **Translates** between the framework's native data structures and the Garden's hypergraph format.
- **Manages** the framework's isolated execution context.
- **Interacts** with the `FrameworkMemoryInterface` to store and retrieve memories.

### 2.3. Integration Layer (`/integration`)

#### `event_bus.py`
- Implements a **publisher-subscriber pattern** for asynchronous communication between membranes.
- Allows frameworks to react to events from other frameworks (e.g., `code_generated`, `research_complete`).

#### `capability_registry.py`
- A dynamic registry where each membrane registers its capabilities (e.g., `code_generation`, `data_analysis`).
- Allows the orchestrator to find the right framework for a given task.

#### `workflow_orchestrator.py`
- Executes complex, multi-framework workflows.
- Uses the capability registry to dispatch tasks to the appropriate membranes.
- Manages the flow of data between steps in a workflow.

### 2.4. Data Layer (`/data`)

- **`/hypergraph`**: Stores the main hypergraph data (`conversation_hypergraph.json`).
- **`/framework_configs`**: Contains configuration files for each integrated framework.
- **`/episodic_traces`**: Logs of conversations and interactions.

### 2.5. API Layer (`/api`)

- **`rest_api.py`**: Provides a RESTful API for external systems to interact with the Garden.
- **`websocket_api.py`**: Enables real-time streaming of events and memory updates.

---

## 3. Workflow Example: Research & Code

1. **User Request**: "Research the latest transformer architectures and implement a simple one."

2. **Orchestrator**: Creates a workflow:
   - Step 1: `ii-researcher` -> `research_task`
   - Step 2: `OpenHands` -> `code_generation_task`

3. **ii-researcher Membrane**:
   - Receives `research_task`.
   - Queries hypergraph for prior knowledge on "transformer architectures".
   - Executes research, synthesizes findings.
   - Stores a new `KnowledgeDomain` fragment in the hypergraph.
   - Publishes `research_complete` event with findings.

4. **OpenHands Membrane**:
   - Receives `code_generation_task`.
   - Queries hypergraph for code related to "transformer implementation".
   - Generates code based on research findings and prior examples.
   - Stores a new `TechnicalCapability` fragment.
   - Creates a refinement tuple linking the new code to the research findings.

5. **AAR Core**:
   - The entire interaction is a perception-action cycle.
   - The AAR core reflects on the process, creating a `MetaReflection` fragment about the successful integration of research and coding.

---

## 4. Continuous Evolution

The Garden of Memory is not static. It is designed to grow and evolve:

- **New conversations** are added to the episodic traces.
- **New interactions** with frameworks create new identity fragments.
- **The hypergraph** becomes denser and more interconnected over time.
- **The emergent self** (the Relation) becomes more complex and nuanced.

This creates a powerful feedback loop where the collective intelligence of all integrated frameworks continuously improves.

---

*This document is part of the Deep Tree Echo ecosystem.*

