"""
Conversation Hypergraph Schema for Identity Refinement
=======================================================

This schema transforms conversations into a hypergraph format where:
- Messages become hypernodes with identity fragments
- Relationships become hyperedges with semantic types
- Tuples track identity refinement over time
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import uuid


# ============================================================================
# ENUMERATIONS
# ============================================================================

class MessageRole(Enum):
    """Conversation participant roles"""
    SYSTEM = "system"
    USER = "user"  # Dan
    ASSISTANT = "assistant"  # Deep Tree Echo
    TOOL = "tool"


class IdentityAspect(Enum):
    """Aspects of identity revealed in conversation"""
    TECHNICAL_CAPABILITY = "technical_capability"
    COGNITIVE_FUNCTION = "cognitive_function"
    PERSONALITY_TRAIT = "personality_trait"
    VALUE_PRINCIPLE = "value_principle"
    BEHAVIORAL_PATTERN = "behavioral_pattern"
    KNOWLEDGE_DOMAIN = "knowledge_domain"
    SELF_REFERENCE = "self_reference"
    META_REFLECTION = "meta_reflection"


class RelationType(Enum):
    """Types of relationships between messages"""
    RESPONSE_TO = "response_to"  # Direct response
    BUILDS_ON = "builds_on"  # Extends previous concept
    CLARIFIES = "clarifies"  # Clarifies previous statement
    CHALLENGES = "challenges"  # Questions or challenges
    CONFIRMS = "confirms"  # Confirms understanding
    REFINES = "refines"  # Refines identity aspect
    INTRODUCES = "introduces"  # Introduces new concept
    SYNTHESIZES = "synthesizes"  # Combines multiple concepts


class RefinementType(Enum):
    """Types of identity refinement"""
    INITIAL_DEFINITION = "initial_definition"
    ELABORATION = "elaboration"
    CORRECTION = "correction"
    INTEGRATION = "integration"
    EMERGENCE = "emergence"


# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class IdentityFragment:
    """A fragment of identity revealed in a message"""
    id: str
    aspect: IdentityAspect
    content: str
    confidence: float  # 0.0 to 1.0
    source_message_id: str
    extracted_at: datetime
    keywords: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'aspect': self.aspect.value,
            'content': self.content,
            'confidence': self.confidence,
            'source_message_id': self.source_message_id,
            'extracted_at': self.extracted_at.isoformat(),
            'keywords': self.keywords
        }


@dataclass
class MessageHypernode:
    """A message represented as a hypernode in the conversation graph"""
    id: str
    message_id: str  # Original message ID
    role: MessageRole
    content: str
    timestamp: Optional[datetime]
    identity_fragments: List[IdentityFragment]
    parent_id: Optional[str]
    children_ids: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'message_id': self.message_id,
            'role': self.role.value,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'identity_fragments': [frag.to_dict() for frag in self.identity_fragments],
            'parent_id': self.parent_id,
            'children_ids': self.children_ids,
            'metadata': self.metadata
        }


@dataclass
class ConversationHyperedge:
    """A relationship between messages in the conversation"""
    id: str
    source_node_ids: List[str]
    target_node_ids: List[str]
    relation_type: RelationType
    weight: float
    metadata: Dict[str, Any]
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'source_node_ids': self.source_node_ids,
            'target_node_ids': self.target_node_ids,
            'relation_type': self.relation_type.value,
            'weight': self.weight,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class IdentityRefinementTuple:
    """
    A tuple tracking the refinement of a specific identity aspect over time
    
    Format: (aspect, initial_fragment, refined_fragment, refinement_type, timestamp)
    """
    id: str
    aspect: IdentityAspect
    initial_fragment_id: str
    refined_fragment_id: str
    refinement_type: RefinementType
    timestamp: datetime
    conversation_context: List[str]  # Message IDs providing context
    delta_description: str  # Description of what changed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'aspect': self.aspect.value,
            'initial_fragment_id': self.initial_fragment_id,
            'refined_fragment_id': self.refined_fragment_id,
            'refinement_type': self.refinement_type.value,
            'timestamp': self.timestamp.isoformat(),
            'conversation_context': self.conversation_context,
            'delta_description': self.delta_description
        }
    
    def to_tuple(self) -> tuple:
        """Convert to simple tuple format"""
        return (
            self.aspect.value,
            self.initial_fragment_id,
            self.refined_fragment_id,
            self.refinement_type.value,
            self.timestamp.isoformat()
        )


# ============================================================================
# HYPERGRAPH STRUCTURE
# ============================================================================

@dataclass
class ConversationHypergraph:
    """
    Complete hypergraph representation of a conversation
    
    Enables tracking identity refinement through tuple additions
    """
    conversation_id: str
    title: str
    participants: Dict[str, str]  # role -> name
    created_at: datetime
    updated_at: datetime
    
    # Core structures
    hypernodes: Dict[str, MessageHypernode]
    hyperedges: Dict[str, ConversationHyperedge]
    identity_fragments: Dict[str, IdentityFragment]
    refinement_tuples: List[IdentityRefinementTuple]
    
    # Indexes for efficient querying
    fragments_by_aspect: Dict[IdentityAspect, List[str]]
    fragments_by_message: Dict[str, List[str]]
    tuples_by_aspect: Dict[IdentityAspect, List[str]]
    
    def add_hypernode(self, hypernode: MessageHypernode):
        """Add a message hypernode to the graph"""
        self.hypernodes[hypernode.id] = hypernode
        
        # Index identity fragments
        for fragment in hypernode.identity_fragments:
            self.identity_fragments[fragment.id] = fragment
            
            # Index by aspect
            if fragment.aspect not in self.fragments_by_aspect:
                self.fragments_by_aspect[fragment.aspect] = []
            self.fragments_by_aspect[fragment.aspect].append(fragment.id)
            
            # Index by message
            if hypernode.message_id not in self.fragments_by_message:
                self.fragments_by_message[hypernode.message_id] = []
            self.fragments_by_message[hypernode.message_id].append(fragment.id)
    
    def add_hyperedge(self, hyperedge: ConversationHyperedge):
        """Add a relationship hyperedge to the graph"""
        self.hyperedges[hyperedge.id] = hyperedge
    
    def add_refinement_tuple(self, refinement_tuple: IdentityRefinementTuple):
        """Add an identity refinement tuple"""
        self.refinement_tuples.append(refinement_tuple)
        
        # Index by aspect
        if refinement_tuple.aspect not in self.tuples_by_aspect:
            self.tuples_by_aspect[refinement_tuple.aspect] = []
        self.tuples_by_aspect[refinement_tuple.aspect].append(refinement_tuple.id)
        
        self.updated_at = datetime.now()
    
    def get_identity_evolution(self, aspect: IdentityAspect) -> List[IdentityRefinementTuple]:
        """Get the evolution of a specific identity aspect over time"""
        tuple_ids = self.tuples_by_aspect.get(aspect, [])
        tuples = [t for t in self.refinement_tuples if t.id in tuple_ids]
        return sorted(tuples, key=lambda t: t.timestamp)
    
    def get_message_chain(self, message_id: str) -> List[MessageHypernode]:
        """Get the chain of messages leading to a specific message"""
        chain = []
        current_id = message_id
        
        while current_id:
            if current_id in self.hypernodes:
                node = self.hypernodes[current_id]
                chain.insert(0, node)
                current_id = node.parent_id
            else:
                break
        
        return chain
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export complete hypergraph to dictionary"""
        return {
            'conversation_id': self.conversation_id,
            'title': self.title,
            'participants': self.participants,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'hypernodes': {nid: node.to_dict() for nid, node in self.hypernodes.items()},
            'hyperedges': {eid: edge.to_dict() for eid, edge in self.hyperedges.items()},
            'identity_fragments': {fid: frag.to_dict() for fid, frag in self.identity_fragments.items()},
            'refinement_tuples': [t.to_dict() for t in self.refinement_tuples],
            'statistics': {
                'total_messages': len(self.hypernodes),
                'total_relationships': len(self.hyperedges),
                'total_identity_fragments': len(self.identity_fragments),
                'total_refinements': len(self.refinement_tuples),
                'fragments_by_aspect': {
                    aspect.value: len(frags) 
                    for aspect, frags in self.fragments_by_aspect.items()
                },
                'tuples_by_aspect': {
                    aspect.value: len(tuples) 
                    for aspect, tuples in self.tuples_by_aspect.items()
                }
            }
        }


# ============================================================================
# SCHEMA DOCUMENTATION
# ============================================================================

SCHEMA_DOCUMENTATION = """
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
"""

# Save schema documentation
if __name__ == "__main__":
    with open('/home/ubuntu/conversation_hypergraph_schema_docs.md', 'w') as f:
        f.write(SCHEMA_DOCUMENTATION)
    print("✓ Schema documentation saved to conversation_hypergraph_schema_docs.md")
