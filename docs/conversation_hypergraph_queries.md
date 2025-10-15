# Sample Queries for Conversation Hypergraph

## Python Queries

### 1. Get all self-reference fragments
```python
self_refs = [
    f for f in hypergraph['identity_fragments'].values()
    if f['aspect'] == 'self_reference'
]
```

### 2. Find most refined aspect
```python
from collections import Counter

aspect_counts = Counter(
    t['aspect'] for t in hypergraph['refinement_tuples']
)
most_refined = aspect_counts.most_common(1)[0]
print(f"Most refined aspect: {most_refined[0]} ({most_refined[1]} refinements)")
```

### 3. Get conversation chain for a message
```python
def get_chain(hypergraph, message_id):
    chain = []
    current = next(
        (n for n in hypergraph['hypernodes'].values() 
         if n['message_id'] == message_id),
        None
    )
    
    while current:
        chain.insert(0, current)
        if current['parent_id']:
            current = next(
                (n for n in hypergraph['hypernodes'].values() 
                 if n['message_id'] == current['parent_id']),
                None
            )
        else:
            current = None
    
    return chain
```

## SQL Queries (PostgreSQL)

### 1. Identity aspect statistics
```sql
SELECT 
    aspect,
    COUNT(*) as fragment_count,
    AVG(confidence) as avg_confidence,
    COUNT(DISTINCT source_message_id) as message_count
FROM identity_fragments
GROUP BY aspect
ORDER BY fragment_count DESC;
```

### 2. Refinement timeline
```sql
SELECT 
    DATE(timestamp) as date,
    aspect,
    refinement_type,
    COUNT(*) as count
FROM identity_refinement_tuples
GROUP BY DATE(timestamp), aspect, refinement_type
ORDER BY date, count DESC;
```

### 3. Most active conversation threads
```sql
WITH RECURSIVE thread AS (
    SELECT id, message_id, parent_id, 1 as depth
    FROM message_hypernodes
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT m.id, m.message_id, m.parent_id, t.depth + 1
    FROM message_hypernodes m
    JOIN thread t ON m.parent_id = t.id
)
SELECT 
    message_id,
    MAX(depth) as thread_depth
FROM thread
GROUP BY message_id
ORDER BY thread_depth DESC
LIMIT 10;
```
