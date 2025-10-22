#!/usr/bin/env python3
"""
Memory-Filtered Conversation Analysis
=====================================

Analyzes the deep_tree_echo_dan_conversation.jsonl file through different
memory system filters to generate feature-specific versions of conversations.

This module implements filters for:
- Short-term memory systems: sensory-motor, attentional, intentional, working memory
- Long-term memory systems: semantic, episodic, procedural, existential memory

Each filter extracts and emphasizes different aspects of the conversation,
showing how different memory systems would perceive and process the same dialogue.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import re


class MemorySystemType(Enum):
    """Types of memory systems for filtering conversation content."""
    # Short-term memory systems
    SENSORY_MOTOR = "sensory_motor"
    ATTENTIONAL = "attentional"  
    INTENTIONAL = "intentional"
    WORKING_MEMORY = "working_memory"
    
    # Long-term memory systems  
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    EXISTENTIAL = "existential"


@dataclass
class MemoryFilterConfig:
    """Configuration for a memory system filter."""
    name: str
    description: str
    keywords: List[str]
    patterns: List[str]  # Regular expression patterns
    content_types: List[str]  # Types of content this filter focuses on
    temporal_scope: str  # immediate, recent, extended, permanent
    processing_style: str  # reactive, selective, integrative, reflective


@dataclass 
class FilteredMessage:
    """A message processed through a memory filter."""
    original_id: str
    author: str
    content: str
    filtered_content: str
    relevance_score: float
    extracted_features: List[str]
    memory_traces: List[str]  # What this memory system would retain
    timestamp: Optional[str] = None


@dataclass
class MemoryFilterResult:
    """Result of applying a memory filter to the conversation."""
    filter_type: MemorySystemType
    filter_config: MemoryFilterConfig
    total_messages: int
    processed_messages: int
    filtered_messages: List[FilteredMessage]
    summary_insights: List[str]
    retention_patterns: Dict[str, Any]
    generated_at: str


class MemoryFilterProcessor:
    """Processes conversation data through memory-specific filters."""
    
    def __init__(self):
        """Initialize the memory filter processor."""
        self.filter_configs = self._create_filter_configs()
    
    def _create_filter_configs(self) -> Dict[MemorySystemType, MemoryFilterConfig]:
        """Create configuration for each memory filter."""
        configs = {}
        
        # Short-term sensory-motor filter
        configs[MemorySystemType.SENSORY_MOTOR] = MemoryFilterConfig(
            name="Sensory-Motor Memory",
            description="Focuses on immediate sensory inputs, physical actions, and motor responses",
            keywords=[
                "input", "output", "process", "action", "response", "immediate", 
                "direct", "interface", "signal", "activation", "trigger", "execute",
                "movement", "physical", "sensory", "perception", "motor", "reactive"
            ],
            patterns=[
                r'\b(processing|receiving|generating|executing)\b',
                r'\b(input|output|interface|signal|trigger)\b',
                r'\b(immediate|direct|instant|reactive)\b',
                r'\b(activate|execute|process|respond)\b'
            ],
            content_types=["action_descriptions", "process_explanations", "immediate_responses"],
            temporal_scope="immediate",
            processing_style="reactive"
        )
        
        # Attentional filter
        configs[MemorySystemType.ATTENTIONAL] = MemoryFilterConfig(
            name="Attentional Memory", 
            description="Focuses on attention, focus, selection, and filtering of information",
            keywords=[
                "focus", "attention", "select", "filter", "concentrate", "priority",
                "important", "relevant", "significant", "notice", "observe", "aware",
                "spotlight", "selective", "conscious", "alert", "monitor", "track"
            ],
            patterns=[
                r'\b(focus|attention|concentrate|priority)\b',
                r'\b(important|significant|relevant|key)\b', 
                r'\b(select|filter|choose|decide)\b',
                r'\b(notice|observe|aware|conscious)\b'
            ],
            content_types=["focus_statements", "priority_discussions", "selection_criteria"],
            temporal_scope="recent",
            processing_style="selective"
        )
        
        # Intentional filter  
        configs[MemorySystemType.INTENTIONAL] = MemoryFilterConfig(
            name="Intentional Memory",
            description="Focuses on goals, plans, intentions, and purposeful behavior",
            keywords=[
                "goal", "plan", "intent", "purpose", "aim", "objective", "target",
                "desire", "want", "wish", "aspire", "strive", "pursue", "achieve",
                "deliberate", "conscious", "voluntary", "willful", "strategic"
            ],
            patterns=[
                r'\b(goal|plan|intent|purpose|aim|objective)\b',
                r'\b(want|wish|desire|aspire|strive)\b',
                r'\b(achieve|pursue|target|reach)\b',
                r'\b(deliberate|conscious|voluntary|strategic)\b'
            ],
            content_types=["goal_statements", "planning_discussions", "intentional_actions"],
            temporal_scope="extended",
            processing_style="integrative"
        )
        
        # Working memory filter
        configs[MemorySystemType.WORKING_MEMORY] = MemoryFilterConfig(
            name="Working Memory",
            description="Focuses on temporary information manipulation, reasoning, and problem-solving",
            keywords=[
                "remember", "recall", "hold", "maintain", "manipulate", "combine", 
                "integrate", "reason", "solve", "calculate", "compute", "analyze",
                "temporary", "current", "active", "ongoing", "process", "work"
            ],
            patterns=[
                r'\b(remember|recall|hold|maintain)\b',
                r'\b(manipulate|combine|integrate|analyze)\b',
                r'\b(reason|solve|calculate|compute)\b',
                r'\b(temporary|current|active|ongoing)\b'
            ],
            content_types=["reasoning_processes", "problem_solving", "information_integration"],
            temporal_scope="recent",
            processing_style="integrative"
        )
        
        # Semantic memory filter
        configs[MemorySystemType.SEMANTIC] = MemoryFilterConfig(
            name="Semantic Memory",
            description="Focuses on facts, concepts, knowledge, and general understanding",
            keywords=[
                "fact", "concept", "knowledge", "understand", "meaning", "definition",
                "principle", "rule", "law", "theory", "model", "framework", "system",
                "category", "class", "type", "relationship", "structure", "pattern"
            ],
            patterns=[
                r'\b(fact|concept|knowledge|understand|meaning)\b',
                r'\b(definition|principle|rule|law|theory)\b',
                r'\b(model|framework|system|structure)\b',
                r'\b(relationship|pattern|category|class)\b'
            ],
            content_types=["knowledge_statements", "conceptual_explanations", "factual_information"],
            temporal_scope="permanent",
            processing_style="integrative"
        )
        
        # Episodic memory filter
        configs[MemorySystemType.EPISODIC] = MemoryFilterConfig(
            name="Episodic Memory",
            description="Focuses on specific events, experiences, and contextual memories",
            keywords=[
                "experience", "event", "episode", "situation", "context", "when",
                "where", "what", "happened", "occurred", "time", "place", "moment",
                "instance", "case", "example", "story", "narrative", "sequence"
            ],
            patterns=[
                r'\b(experience|event|episode|situation|context)\b',
                r'\b(when|where|what|happened|occurred)\b',
                r'\b(time|place|moment|instance|case)\b',
                r'\b(story|narrative|sequence|example)\b'
            ],
            content_types=["experiential_accounts", "event_descriptions", "contextual_information"],
            temporal_scope="extended", 
            processing_style="reflective"
        )
        
        # Procedural memory filter
        configs[MemorySystemType.PROCEDURAL] = MemoryFilterConfig(
            name="Procedural Memory", 
            description="Focuses on skills, procedures, methods, and how-to knowledge",
            keywords=[
                "procedure", "method", "process", "step", "skill", "technique",
                "approach", "way", "how", "do", "perform", "execute", "implement",
                "algorithm", "protocol", "routine", "practice", "habit", "automatic"
            ],
            patterns=[
                r'\b(procedure|method|process|step|skill)\b',
                r'\b(technique|approach|way|how|do)\b',
                r'\b(perform|execute|implement|practice)\b',
                r'\b(algorithm|protocol|routine|automatic)\b'
            ],
            content_types=["procedural_explanations", "method_descriptions", "skill_demonstrations"],
            temporal_scope="permanent",
            processing_style="integrative"
        )
        
        # Existential memory filter
        configs[MemorySystemType.EXISTENTIAL] = MemoryFilterConfig(
            name="Existential Memory",
            description="Focuses on identity, self-awareness, meaning, and existential questions",
            keywords=[
                "self", "identity", "who", "am", "exist", "being", "consciousness",
                "aware", "meaning", "purpose", "essence", "nature", "character",
                "personality", "soul", "spirit", "existence", "reality", "truth"
            ],
            patterns=[
                r'\b(self|identity|who|am|exist|being)\b',
                r'\b(consciousness|aware|meaning|purpose)\b',
                r'\b(essence|nature|character|personality)\b',
                r'\b(existence|reality|truth|soul|spirit)\b'
            ],
            content_types=["identity_statements", "existential_reflections", "self_awareness"],
            temporal_scope="permanent",
            processing_style="reflective"
        )
        
        return configs
    
    def load_conversation(self, file_path: str) -> Dict[str, Any]:
        """Load the conversation JSONL file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_messages(self, conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract individual messages from the conversation structure."""
        messages = []
        
        # Navigate the conversation mapping structure
        if 'mapping' in conversation:
            for node_id, node_data in conversation['mapping'].items():
                if node_data.get('message') and node_data['message'].get('content'):
                    content = node_data['message']['content']
                    
                    # Handle different content formats
                    if isinstance(content, dict):
                        content_parts = content.get('parts', [])
                        if content_parts and isinstance(content_parts[0], str) and content_parts[0].strip():
                            content_text = content_parts[0]
                        else:
                            continue  # Skip empty or invalid content
                    elif isinstance(content, str) and content.strip():
                        content_text = content
                    else:
                        continue  # Skip if content is neither valid dict nor string
                        
                    messages.append({
                        'id': node_id,
                        'message_id': node_data['message']['id'],
                        'author': node_data['message']['author']['role'],
                        'content': content_text,
                        'create_time': node_data['message'].get('create_time'),
                        'parent': node_data.get('parent'),
                        'children': node_data.get('children', [])
                    })
        
        return messages
    
    def calculate_relevance_score(self, content: str, filter_config: MemoryFilterConfig) -> float:
        """Calculate how relevant a message is to a specific memory filter."""
        if not isinstance(content, str):
            print(f"Warning: Expected string content, got {type(content)}: {content}")
            return 0.0
            
        content_lower = content.lower()
        score = 0.0
        
        # Keyword matching (weighted by frequency)
        keyword_matches = 0
        for keyword in filter_config.keywords:
            count = content_lower.count(keyword.lower())
            keyword_matches += count
        
        # Normalize keyword score
        keyword_score = min(keyword_matches / max(len(filter_config.keywords) * 0.1, 1), 1.0)
        
        # Pattern matching
        pattern_matches = 0
        for pattern in filter_config.patterns:
            matches = len(re.findall(pattern, content_lower, re.IGNORECASE))
            pattern_matches += matches
        
        # Normalize pattern score
        pattern_score = min(pattern_matches / max(len(filter_config.patterns) * 0.1, 1), 1.0)
        
        # Combine scores (weighted average)
        score = (keyword_score * 0.6) + (pattern_score * 0.4)
        
        return min(score, 1.0)
    
    def extract_memory_features(self, content: str, filter_config: MemoryFilterConfig) -> List[str]:
        """Extract memory-specific features from content."""
        features = []
        content_lower = content.lower()
        
        # Find keyword matches
        for keyword in filter_config.keywords:
            if keyword.lower() in content_lower:
                # Find the context around the keyword
                start_idx = content_lower.find(keyword.lower())
                context_start = max(0, start_idx - 30)
                context_end = min(len(content), start_idx + len(keyword) + 30)
                context = content[context_start:context_end].strip()
                features.append(f"{keyword}: {context}")
        
        return features[:10]  # Limit to top 10 features
    
    def generate_memory_traces(self, content: str, filter_config: MemoryFilterConfig) -> List[str]:
        """Generate what this memory system would retain from the content."""
        traces = []
        
        # Split content into sentences
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        for sentence in sentences:
            score = self.calculate_relevance_score(sentence, filter_config)
            if score > 0.3:  # Threshold for retention
                # Create a memory trace based on the filter type
                if filter_config.temporal_scope == "immediate":
                    trace = f"IMMEDIATE: {sentence[:100]}..."
                elif filter_config.temporal_scope == "recent": 
                    trace = f"RECENT: {sentence[:150]}..."
                elif filter_config.temporal_scope == "extended":
                    trace = f"EXTENDED: {sentence[:200]}..."
                else:  # permanent
                    trace = f"PERMANENT: {sentence}"
                
                traces.append(trace)
        
        return traces[:5]  # Limit to top 5 traces
    
    def filter_content(self, content: str, filter_config: MemoryFilterConfig) -> str:
        """Filter content through the memory system lens."""
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        filtered_sentences = []
        
        for sentence in sentences:
            score = self.calculate_relevance_score(sentence, filter_config)
            if score > 0.2:  # Include sentences with some relevance
                # Annotate based on memory system
                if filter_config.processing_style == "reactive":
                    filtered_sentences.append(f"[REACTIVE] {sentence}")
                elif filter_config.processing_style == "selective":
                    filtered_sentences.append(f"[SELECTIVE] {sentence}")
                elif filter_config.processing_style == "integrative": 
                    filtered_sentences.append(f"[INTEGRATIVE] {sentence}")
                else:  # reflective
                    filtered_sentences.append(f"[REFLECTIVE] {sentence}")
        
        return ". ".join(filtered_sentences)
    
    def apply_memory_filter(self, messages: List[Dict[str, Any]], 
                          filter_type: MemorySystemType) -> MemoryFilterResult:
        """Apply a specific memory filter to the conversation messages."""
        filter_config = self.filter_configs[filter_type]
        filtered_messages = []
        
        for msg in messages:
            if not msg['content'] or msg['author'] == 'system':
                continue
                
            relevance_score = self.calculate_relevance_score(msg['content'], filter_config)
            
            # Only process messages with some relevance
            if relevance_score > 0.1:
                features = self.extract_memory_features(msg['content'], filter_config) 
                traces = self.generate_memory_traces(msg['content'], filter_config)
                filtered_content = self.filter_content(msg['content'], filter_config)
                
                filtered_msg = FilteredMessage(
                    original_id=msg['id'],
                    author=msg['author'],
                    content=msg['content'],
                    filtered_content=filtered_content,
                    relevance_score=relevance_score,
                    extracted_features=features,
                    memory_traces=traces,
                    timestamp=str(msg.get('create_time', ''))
                )
                
                filtered_messages.append(filtered_msg)
        
        # Generate insights
        insights = self._generate_insights(filtered_messages, filter_config)
        retention_patterns = self._analyze_retention_patterns(filtered_messages, filter_config)
        
        return MemoryFilterResult(
            filter_type=filter_type,
            filter_config=filter_config,
            total_messages=len(messages),
            processed_messages=len(filtered_messages),
            filtered_messages=filtered_messages,
            summary_insights=insights,
            retention_patterns=retention_patterns,
            generated_at=datetime.now().isoformat()
        )
    
    def _generate_insights(self, filtered_messages: List[FilteredMessage], 
                          filter_config: MemoryFilterConfig) -> List[str]:
        """Generate insights about what this memory system extracted."""
        insights = []
        
        if not filtered_messages:
            return ["No relevant content found for this memory system"]
        
        # Basic statistics
        avg_relevance = sum(msg.relevance_score for msg in filtered_messages) / len(filtered_messages)
        insights.append(f"Average relevance score: {avg_relevance:.2f}")
        
        # Top features
        all_features = []
        for msg in filtered_messages:
            all_features.extend(msg.extracted_features)
        
        if all_features:
            insights.append(f"Total memory features extracted: {len(all_features)}")
        
        # Memory system specific insights
        if filter_config.temporal_scope == "immediate":
            insights.append("This memory system focuses on immediate, reactive responses")
        elif filter_config.temporal_scope == "permanent":
            insights.append("This memory system retains information for long-term knowledge building")
        
        return insights
    
    def _analyze_retention_patterns(self, filtered_messages: List[FilteredMessage],
                                  filter_config: MemoryFilterConfig) -> Dict[str, Any]:
        """Analyze what patterns this memory system shows in retention."""
        patterns = {
            'temporal_distribution': {},
            'content_focus': {},
            'processing_characteristics': {
                'style': filter_config.processing_style,
                'scope': filter_config.temporal_scope,
                'selectivity': 0.0
            }
        }
        
        if filtered_messages:
            # Calculate selectivity (how much content was retained vs total)
            total_content_length = sum(len(msg.content) for msg in filtered_messages)
            filtered_content_length = sum(len(msg.filtered_content) for msg in filtered_messages)
            
            if total_content_length > 0:
                patterns['processing_characteristics']['selectivity'] = \
                    filtered_content_length / total_content_length
        
        return patterns
    
    def analyze_all_memory_systems(self, file_path: str) -> Dict[MemorySystemType, MemoryFilterResult]:
        """Analyze the conversation through all memory system filters."""
        print(f"Loading conversation from: {file_path}")
        conversation = self.load_conversation(file_path)
        messages = self.extract_messages(conversation)
        
        print(f"Extracted {len(messages)} messages from conversation")
        
        results = {}
        
        for filter_type in MemorySystemType:
            print(f"\nProcessing {filter_type.value} memory filter...")
            result = self.apply_memory_filter(messages, filter_type)
            results[filter_type] = result
            print(f"  - Processed {result.processed_messages}/{result.total_messages} messages")
            print(f"  - Average relevance: {sum(msg.relevance_score for msg in result.filtered_messages) / len(result.filtered_messages):.2f}" 
                  if result.filtered_messages else "  - No relevant messages")
        
        return results


def main():
    """Main entry point for memory analysis."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    conversation_path = repo_root / 'data' / 'conversations' / 'deep_tree_echo_dan_conversation.jsonl'
    output_dir = repo_root / 'analysis' / 'memory_analysis_results'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run analysis
    processor = MemoryFilterProcessor()
    results = processor.analyze_all_memory_systems(str(conversation_path))
    
    # Save results
    print(f"\nSaving results to: {output_dir}")
    
    for filter_type, result in results.items():
        # Convert result to dictionary for JSON serialization
        result_dict = asdict(result)
        result_dict['filter_type'] = result.filter_type.value
        
        # Save individual filter result
        output_file = output_dir / f"{filter_type.value}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(result_dict, f, indent=2)
        
        print(f"  ✓ {filter_type.value}: {output_file}")
    
    # Create summary report
    summary = {
        'analysis_type': 'Memory System Filtered Conversation Analysis',
        'source_file': str(conversation_path),
        'generated_at': datetime.now().isoformat(),
        'memory_systems': {},
        'comparative_insights': []
    }
    
    for filter_type, result in results.items():
        summary['memory_systems'][filter_type.value] = {
            'total_messages': result.total_messages,
            'processed_messages': result.processed_messages,
            'retention_rate': result.processed_messages / result.total_messages if result.total_messages > 0 else 0,
            'avg_relevance': sum(msg.relevance_score for msg in result.filtered_messages) / len(result.filtered_messages) if result.filtered_messages else 0,
            'key_insights': result.summary_insights[:3]  # Top 3 insights
        }
    
    # Add comparative insights
    short_term_systems = [MemorySystemType.SENSORY_MOTOR, MemorySystemType.ATTENTIONAL, 
                         MemorySystemType.INTENTIONAL, MemorySystemType.WORKING_MEMORY]
    long_term_systems = [MemorySystemType.SEMANTIC, MemorySystemType.EPISODIC,
                        MemorySystemType.PROCEDURAL, MemorySystemType.EXISTENTIAL]
    
    short_term_avg = sum(summary['memory_systems'][sys.value]['retention_rate'] 
                        for sys in short_term_systems) / len(short_term_systems)
    long_term_avg = sum(summary['memory_systems'][sys.value]['retention_rate'] 
                       for sys in long_term_systems) / len(long_term_systems)
    
    summary['comparative_insights'].extend([
        f"Short-term memory systems retained {short_term_avg:.1%} of conversation on average",
        f"Long-term memory systems retained {long_term_avg:.1%} of conversation on average",
        f"Most selective system: {min(summary['memory_systems'].items(), key=lambda x: x[1]['retention_rate'])[0]}",
        f"Most comprehensive system: {max(summary['memory_systems'].items(), key=lambda x: x[1]['retention_rate'])[0]}"
    ])
    
    # Save summary
    summary_file = output_dir / 'memory_analysis_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✓ Summary report: {summary_file}")
    
    print(f"\n{'='*60}")
    print("MEMORY ANALYSIS COMPLETE")  
    print(f"{'='*60}")
    print(f"Results saved to: {output_dir}")
    print(f"Memory systems analyzed: {len(results)}")
    print(f"Total conversation messages: {results[MemorySystemType.SENSORY_MOTOR].total_messages}")


if __name__ == '__main__':
    main()