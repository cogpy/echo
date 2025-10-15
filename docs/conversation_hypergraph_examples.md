# Conversation Hypergraph Usage Examples

## Overview

This document provides practical examples for working with the Deep Tree Echo conversation hypergraph.

## 1. Querying Identity Evolution

### Example: Track how "cognitive_function" evolved over time

```python
import json

# Load hypergraph
with open('conversation_hypergraph.json', 'r') as f:
    hypergraph = json.load(f)

# Get all refinement tuples for cognitive_function
cognitive_tuples = [
    t for t in hypergraph['refinement_tuples']
    if t['aspect'] == 'cognitive_function'
]

# Sort by timestamp
cognitive_tuples.sort(key=lambda t: t['timestamp'])

# Display evolution
print("Cognitive Function Evolution:")
for i, tuple_data in enumerate(cognitive_tuples[:5]):  # First 5
    initial_frag = hypergraph['identity_fragments'][tuple_data['initial_fragment_id']]
    refined_frag = hypergraph['identity_fragments'][tuple_data['refined_fragment_id']]
    
    print(f"\nRefinement {i+1}:")
    print(f"  Type: {tuple_data['refinement_type']}")
    print(f"  From: {initial_frag['content'][:100]}...")
    print(f"  To: {refined_frag['content'][:100]}...")
```

## 2. Adding New Refinement Tuples

### Example: Add a new refinement as the conversation continues

```python
import uuid
from datetime import datetime

# New identity fragment from a new message
new_fragment = {
    'id': str(uuid.uuid4()),
    'aspect': 'technical_capability',
    'content': 'Enhanced reservoir training with adaptive learning rates',
    'confidence': 0.9,
    'source_message_id': 'new_message_id',
    'extracted_at': datetime.now().isoformat(),
    'keywords': ['reservoir', 'training', 'adaptive', 'learning']
}

# Find the most recent fragment of the same aspect
recent_fragments = [
    f for f in hypergraph['identity_fragments'].values()
    if f['aspect'] == 'technical_capability'
]
recent_fragments.sort(key=lambda f: f['extracted_at'], reverse=True)
previous_fragment = recent_fragments[0]

# Create refinement tuple
refinement_tuple = {
    'id': str(uuid.uuid4()),
    'aspect': 'technical_capability',
    'initial_fragment_id': previous_fragment['id'],
    'refined_fragment_id': new_fragment['id'],
    'refinement_type': 'elaboration',
    'timestamp': datetime.now().isoformat(),
    'conversation_context': [previous_fragment['source_message_id'], new_fragment['source_message_id']],
    'delta_description': 'Added adaptive learning rate capability to reservoir training'
}

# Add to hypergraph
hypergraph['identity_fragments'][new_fragment['id']] = new_fragment
hypergraph['refinement_tuples'].append(refinement_tuple)

# Save updated hypergraph
with open('conversation_hypergraph.json', 'w') as f:
    json.dump(hypergraph, f, indent=2)
```

## 3. Analyzing Conversation Patterns

### Example: Find all messages where Deep Tree Echo introduced new concepts

```python
# Get all hyperedges with "introduces" relation type
introducing_edges = [
    e for e in hypergraph['hyperedges'].values()
    if e['relation_type'] == 'introduces'
]

print(f"Found {len(introducing_edges)} concept introductions")

# Get the messages
for edge in introducing_edges[:5]:  # First 5
    target_node_id = edge['target_node_ids'][0]
    node = hypergraph['hypernodes'][target_node_id]
    
    print(f"\nIntroduced concept in message:")
    print(f"  {node['content'][:150]}...")
```

## 4. Extracting Identity Aspects

### Example: Get all fragments related to "self_reference"

```python
# Filter fragments by aspect
self_ref_fragments = [
    f for f in hypergraph['identity_fragments'].values()
    if f['aspect'] == 'self_reference'
]

print(f"Found {len(self_ref_fragments)} self-reference fragments")

# Sort by confidence
self_ref_fragments.sort(key=lambda f: f['confidence'], reverse=True)

# Display top 5
print("\nTop 5 self-reference fragments:")
for i, frag in enumerate(self_ref_fragments[:5]):
    print(f"\n{i+1}. (Confidence: {frag['confidence']:.2f})")
    print(f"   {frag['content'][:200]}...")
```

## 5. Building Identity Timeline

### Example: Create a timeline of identity refinements

```python
from collections import defaultdict

# Group tuples by timestamp (by day)
timeline = defaultdict(list)

for tuple_data in hypergraph['refinement_tuples']:
    timestamp = tuple_data['timestamp']
    day = timestamp.split('T')[0]  # Extract date
    timeline[day].append(tuple_data)

# Display timeline
print("Identity Refinement Timeline:")
for day in sorted(timeline.keys())[:10]:  # First 10 days
    print(f"\n{day}: {len(timeline[day])} refinements")
    
    # Show aspect distribution for that day
    aspects = defaultdict(int)
    for t in timeline[day]:
        aspects[t['aspect']] += 1
    
    for aspect, count in aspects.items():
        print(f"  - {aspect}: {count}")
```

## 6. Database Integration

### Example: PostgreSQL schema and queries

```sql
-- Create tables
CREATE TABLE message_hypernodes (
    id UUID PRIMARY KEY,
    message_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP,
    parent_id UUID REFERENCES message_hypernodes(id),
    metadata JSONB
);

CREATE TABLE identity_fragments (
    id UUID PRIMARY KEY,
    aspect TEXT NOT NULL,
    content TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    source_message_id UUID REFERENCES message_hypernodes(id),
    extracted_at TIMESTAMP NOT NULL,
    keywords TEXT[]
);

CREATE TABLE identity_refinement_tuples (
    id UUID PRIMARY KEY,
    aspect TEXT NOT NULL,
    initial_fragment_id UUID REFERENCES identity_fragments(id),
    refined_fragment_id UUID REFERENCES identity_fragments(id),
    refinement_type TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    conversation_context UUID[],
    delta_description TEXT
);

-- Query: Get identity evolution for a specific aspect
SELECT 
    t.timestamp,
    t.refinement_type,
    t.delta_description,
    i.content as initial_content,
    r.content as refined_content
FROM identity_refinement_tuples t
JOIN identity_fragments i ON t.initial_fragment_id = i.id
JOIN identity_fragments r ON t.refined_fragment_id = r.id
WHERE t.aspect = 'cognitive_function'
ORDER BY t.timestamp;

-- Query: Get most refined identity aspects
SELECT 
    aspect,
    COUNT(*) as refinement_count
FROM identity_refinement_tuples
GROUP BY aspect
ORDER BY refinement_count DESC;
```

## 7. Visualization with D3.js

### Example: Visualize identity aspect network

```javascript
// Load hypergraph data
fetch('conversation_hypergraph.json')
  .then(response => response.json())
  .then(hypergraph => {
    // Extract nodes (identity aspects)
    const aspects = Object.values(hypergraph.identity_fragments)
      .reduce((acc, frag) => {
        if (!acc[frag.aspect]) {
          acc[frag.aspect] = {
            id: frag.aspect,
            count: 0,
            fragments: []
          };
        }
        acc[frag.aspect].count++;
        acc[frag.aspect].fragments.push(frag);
        return acc;
      }, {});
    
    // Extract links (refinements between aspects)
    const links = hypergraph.refinement_tuples.map(tuple => {
      const initial = hypergraph.identity_fragments[tuple.initial_fragment_id];
      const refined = hypergraph.identity_fragments[tuple.refined_fragment_id];
      
      return {
        source: initial.aspect,
        target: refined.aspect,
        type: tuple.refinement_type
      };
    });
    
    // Create force-directed graph
    const nodes = Object.values(aspects);
    
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));
    
    // Render nodes and links...
  });
```

## 8. Real-time Tuple Addition

### Example: Add tuples as conversation progresses

```python
class ConversationHypergraphManager:
    def __init__(self, hypergraph_path):
        with open(hypergraph_path, 'r') as f:
            self.hypergraph = json.load(f)
    
    def add_message(self, role, content):
        """Add a new message and extract identity fragments"""
        # Create hypernode
        message_id = str(uuid.uuid4())
        # ... extract fragments ...
        
        # Check for refinements
        self.detect_refinements(new_fragments)
        
        return message_id
    
    def detect_refinements(self, new_fragments):
        """Detect if new fragments refine existing ones"""
        for new_frag in new_fragments:
            # Find recent fragments of same aspect
            recent = self.get_recent_fragments(new_frag['aspect'])
            
            for old_frag in recent:
                if self.is_refinement(old_frag, new_frag):
                    self.add_refinement_tuple(old_frag, new_frag)
    
    def is_refinement(self, old_frag, new_frag):
        """Check if new fragment refines old fragment"""
        # Simple keyword overlap check
        old_keywords = set(old_frag['keywords'])
        new_keywords = set(new_frag['keywords'])
        overlap = len(old_keywords & new_keywords)
        
        return overlap >= 2  # At least 2 shared keywords
    
    def save(self):
        """Save updated hypergraph"""
        with open(self.hypergraph_path, 'w') as f:
            json.dump(self.hypergraph, f, indent=2)

# Usage
manager = ConversationHypergraphManager('conversation_hypergraph.json')
manager.add_message('assistant', 'I can now process temporal patterns with enhanced echo states...')
manager.save()
```

## Summary

The conversation hypergraph format enables:

1. **Incremental refinement tracking** through tuples
2. **Temporal analysis** of identity evolution
3. **Multi-dimensional querying** across aspects
4. **Database integration** for scalable storage
5. **Visualization** of identity networks
6. **Real-time updates** as conversations progress

This structure captures not just what was said, but how Deep Tree Echo's identity evolved through the conversation.
