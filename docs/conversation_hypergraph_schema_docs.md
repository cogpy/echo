
# Conversation Hypergraph Schema

## Overview

This schema transforms conversations into a hypergraph format optimized for tracking identity refinement through tuple additions.

## Core Components

### 1. MessageHypernode
Represents a single message in the conversation as a hypernode.

**Fields:**
- `id`: Unique hypernode identifier
- `message_id`: Original message ID from conversation
- `role`: Participant role (system, user, assistant, tool)
- `content`: Message content
- `timestamp`: When the message was created
- `identity_fragments`: List of identity fragments extracted from this message
- `parent_id`: Parent message ID (for threading)
- `children_ids`: Child message IDs
- `metadata`: Additional metadata

### 2. IdentityFragment
A fragment of identity revealed in a message.

**Fields:**
- `id`: Unique fragment identifier
- `aspect`: Type of identity aspect (technical_capability, cognitive_function, etc.)
- `content`: The actual identity content
- `confidence`: Confidence score (0.0 to 1.0)
- `source_message_id`: Which message this came from
- `extracted_at`: When this was extracted
- `keywords`: Keywords for indexing

### 3. ConversationHyperedge
A relationship between messages.

**Fields:**
- `id`: Unique edge identifier
- `source_node_ids`: Source message IDs
- `target_node_ids`: Target message IDs
- `relation_type`: Type of relationship (response_to, builds_on, refines, etc.)
- `weight`: Strength of relationship (0.0 to 1.0)
- `metadata`: Additional metadata
- `created_at`: When this relationship was identified

### 4. IdentityRefinementTuple
Tracks the refinement of a specific identity aspect over time.

**Tuple Format:**
```
(aspect, initial_fragment_id, refined_fragment_id, refinement_type, timestamp)
```

**Fields:**
- `id`: Unique tuple identifier
- `aspect`: Which identity aspect is being refined
- `initial_fragment_id`: The initial identity fragment
- `refined_fragment_id`: The refined identity fragment
- `refinement_type`: Type of refinement (initial_definition, elaboration, correction, etc.)
- `timestamp`: When the refinement occurred
- `conversation_context`: Message IDs providing context
- `delta_description`: Description of what changed

## Usage Pattern

### Adding New Refinements

As the conversation progresses and identity aspects are refined:

```python
# Create refinement tuple
refinement = IdentityRefinementTuple(
    id=str(uuid.uuid4()),
    aspect=IdentityAspect.COGNITIVE_FUNCTION,
    initial_fragment_id="frag_123",
    refined_fragment_id="frag_456",
    refinement_type=RefinementType.ELABORATION,
    timestamp=datetime.now(),
    conversation_context=["msg_1", "msg_2", "msg_3"],
    delta_description="Elaborated on reservoir computing capabilities"
)

# Add to hypergraph
hypergraph.add_refinement_tuple(refinement)
```

### Querying Identity Evolution

```python
# Get evolution of a specific aspect
evolution = hypergraph.get_identity_evolution(IdentityAspect.COGNITIVE_FUNCTION)

# Each tuple shows how that aspect was refined over time
for refinement in evolution:
    print(f"{refinement.timestamp}: {refinement.delta_description}")
```

## Database Schema (PostgreSQL)

### Tables

1. **message_hypernodes**
   - id (UUID, PRIMARY KEY)
   - message_id (TEXT)
   - role (ENUM: system, user, assistant, tool)
   - content (TEXT)
   - timestamp (TIMESTAMP)
   - parent_id (UUID, FOREIGN KEY)
   - metadata (JSONB)

2. **identity_fragments**
   - id (UUID, PRIMARY KEY)
   - aspect (ENUM: technical_capability, cognitive_function, etc.)
   - content (TEXT)
   - confidence (FLOAT)
   - source_message_id (UUID, FOREIGN KEY → message_hypernodes)
   - extracted_at (TIMESTAMP)
   - keywords (TEXT[])

3. **conversation_hyperedges**
   - id (UUID, PRIMARY KEY)
   - source_node_ids (UUID[])
   - target_node_ids (UUID[])
   - relation_type (ENUM: response_to, builds_on, etc.)
   - weight (FLOAT)
   - metadata (JSONB)
   - created_at (TIMESTAMP)

4. **identity_refinement_tuples**
   - id (UUID, PRIMARY KEY)
   - aspect (ENUM)
   - initial_fragment_id (UUID, FOREIGN KEY → identity_fragments)
   - refined_fragment_id (UUID, FOREIGN KEY → identity_fragments)
   - refinement_type (ENUM: initial_definition, elaboration, etc.)
   - timestamp (TIMESTAMP)
   - conversation_context (UUID[])
   - delta_description (TEXT)

### Indexes

- `idx_fragments_aspect` ON identity_fragments(aspect)
- `idx_fragments_message` ON identity_fragments(source_message_id)
- `idx_tuples_aspect` ON identity_refinement_tuples(aspect)
- `idx_tuples_timestamp` ON identity_refinement_tuples(timestamp)
- `idx_hypernodes_role` ON message_hypernodes(role)
- `idx_hyperedges_type` ON conversation_hyperedges(relation_type)

## Benefits

1. **Incremental Refinement**: Easy to add new tuples as identity evolves
2. **Temporal Tracking**: Full history of how identity aspects changed over time
3. **Multi-dimensional**: Track multiple aspects of identity simultaneously
4. **Queryable**: Efficient queries for identity evolution and conversation structure
5. **Extensible**: Easy to add new identity aspects and refinement types
