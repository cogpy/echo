# Garden of Memory - Framework Membranes

This directory contains membrane wrappers for each integrated framework.

## Available Membranes

- **openhands_membrane.py**: Code generation & execution (OpenHands)
- **ii_agent_membrane.py**: General-purpose agent orchestration
- **ii_verl_membrane.py**: Reinforcement learning & policy optimization
- **ii_researcher_membrane.py**: Research workflows & literature analysis
- **ii_thought_membrane.py**: Chain-of-thought reasoning
- **openmanus_membrane.py**: Creative task execution
- **commonground_membrane.py**: Multi-agent coordination
- **lemonai_membrane.py**: Full-stack agentic workflows

## Usage

```python
from hypergraph import HypergraphMemory
from memory_sync import MemorySyncProtocol, FrameworkMemoryInterface
from membranes import OpenHandsMembrane

# Initialize
memory = HypergraphMemory()
sync = MemorySyncProtocol(memory)
interface = FrameworkMemoryInterface("OpenHands", sync)

# Create membrane
membrane = OpenHandsMembrane(interface)

# Use membrane
result = membrane.execute_task(task)
```
