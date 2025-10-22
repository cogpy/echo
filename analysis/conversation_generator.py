#!/usr/bin/env python3
"""
Memory-Filtered Conversation Generator
=====================================

Generates feature-specific versions of the conversation through each
memory system filter, creating distinct conversation files that show
how different memory systems would perceive and retain the dialogue.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import asdict


class FilteredConversationGenerator:
    """Generates conversation files filtered through memory system lenses."""
    
    def __init__(self, results_dir: str):
        """Initialize with path to memory analysis results."""
        self.results_dir = Path(results_dir)
        self.results = {}
        self._load_results()
    
    def _load_results(self):
        """Load memory analysis results."""
        memory_systems = [
            'sensory_motor', 'attentional', 'intentional', 'working_memory',
            'semantic', 'episodic', 'procedural', 'existential'
        ]
        
        for system in memory_systems:
            result_file = self.results_dir / f'{system}_analysis.json'
            if result_file.exists():
                with open(result_file, 'r') as f:
                    self.results[system] = json.load(f)
    
    def generate_filtered_conversation(self, memory_system: str) -> Dict[str, Any]:
        """Generate a filtered conversation for a specific memory system."""
        if memory_system not in self.results:
            raise ValueError(f"No results found for memory system: {memory_system}")
        
        result_data = self.results[memory_system]
        config = result_data['filter_config']
        filtered_messages = result_data['filtered_messages']
        
        # Sort messages by timestamp if available
        sorted_messages = sorted(
            filtered_messages, 
            key=lambda x: float(x.get('timestamp', 0)) if x.get('timestamp') else 0
        )
        
        # Create conversation structure
        conversation = {
            'title': f"Deep Tree Echo Conversation - {config['name']} Filter",
            'description': config['description'],
            'filter_type': memory_system,
            'filter_config': config,
            'processing_stats': {
                'total_original_messages': result_data['total_messages'],
                'filtered_messages_count': len(filtered_messages),
                'retention_rate': len(filtered_messages) / result_data['total_messages'] if result_data['total_messages'] > 0 else 0,
                'average_relevance': sum(msg['relevance_score'] for msg in filtered_messages) / len(filtered_messages) if filtered_messages else 0
            },
            'generated_at': datetime.now().isoformat(),
            'messages': [],
            'memory_insights': result_data.get('summary_insights', []),
            'retention_patterns': result_data.get('retention_patterns', {})
        }
        
        # Process messages
        for i, msg in enumerate(sorted_messages):
            message_entry = {
                'id': f"filtered_{i+1:03d}",
                'original_id': msg['original_id'],
                'sequence': i + 1,
                'author': msg['author'],
                'content': {
                    'original': msg['content'],
                    'filtered': msg['filtered_content'],
                    'relevance_score': msg['relevance_score']
                },
                'memory_processing': {
                    'extracted_features': msg['extracted_features'],
                    'memory_traces': msg['memory_traces'],
                    'retention_reason': self._get_retention_reason(msg, config)
                },
                'timestamp': msg.get('timestamp')
            }
            
            conversation['messages'].append(message_entry)
        
        return conversation
    
    def _get_retention_reason(self, message: Dict, config: Dict) -> str:
        """Determine why this message was retained by the memory system."""
        reasons = []
        
        # Check for high relevance
        relevance = message.get('relevance_score', 0)
        if relevance > 0.8:
            reasons.append("high relevance")
        elif relevance > 0.5:
            reasons.append("moderate relevance")
        
        # Check for memory features
        features = message.get('extracted_features', [])
        if len(features) > 3:
            reasons.append("multiple memory features")
        
        # Check memory traces
        traces = message.get('memory_traces', [])
        if len(traces) > 2:
            reasons.append("strong memory traces")
        
        # Processing style specific reasons
        style = config.get('processing_style', '')
        if style == 'reactive':
            reasons.append("immediate processing response")
        elif style == 'selective':
            reasons.append("selective attention focus")  
        elif style == 'integrative':
            reasons.append("information integration")
        elif style == 'reflective':
            reasons.append("reflective processing")
        
        return "; ".join(reasons) if reasons else "general memory system alignment"
    
    def generate_memory_system_summary(self, memory_system: str) -> Dict[str, Any]:
        """Generate a summary of how a memory system processed the conversation."""
        if memory_system not in self.results:
            return {}
        
        result_data = self.results[memory_system]
        config = result_data['filter_config']
        filtered_messages = result_data['filtered_messages']
        
        # Analyze patterns
        author_distribution = {}
        relevance_levels = {'high': 0, 'medium': 0, 'low': 0}
        feature_frequency = {}
        
        for msg in filtered_messages:
            # Author distribution
            author = msg.get('author', 'unknown')
            author_distribution[author] = author_distribution.get(author, 0) + 1
            
            # Relevance levels
            relevance = msg.get('relevance_score', 0)
            if relevance > 0.7:
                relevance_levels['high'] += 1
            elif relevance > 0.4:
                relevance_levels['medium'] += 1
            else:
                relevance_levels['low'] += 1
            
            # Feature frequency
            for feature in msg.get('extracted_features', []):
                # Extract the keyword from feature string
                if ':' in feature:
                    keyword = feature.split(':')[0].strip()
                    feature_frequency[keyword] = feature_frequency.get(keyword, 0) + 1
        
        # Top features
        top_features = sorted(feature_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        summary = {
            'memory_system': memory_system,
            'system_name': config['name'],
            'description': config['description'],
            'processing_characteristics': {
                'style': config['processing_style'],
                'temporal_scope': config['temporal_scope'],
                'keywords': config['keywords'][:10]  # Top 10 keywords
            },
            'conversation_analysis': {
                'total_messages_processed': len(filtered_messages),
                'author_distribution': author_distribution,
                'relevance_distribution': relevance_levels,
                'top_features': dict(top_features),
                'retention_rate': len(filtered_messages) / result_data['total_messages'] if result_data['total_messages'] > 0 else 0
            },
            'key_insights': result_data.get('summary_insights', []),
            'generated_at': datetime.now().isoformat()
        }
        
        return summary
    
    def generate_comparative_conversation(self) -> Dict[str, Any]:
        """Generate a conversation showing all memory system perspectives side by side."""
        if not self.results:
            return {}
        
        # Get all unique original message IDs that were processed by any system
        all_message_ids = set()
        for system_data in self.results.values():
            for msg in system_data.get('filtered_messages', []):
                all_message_ids.add(msg['original_id'])
        
        # Build comparative structure
        comparative = {
            'title': 'Deep Tree Echo Conversation - Multi-Memory System Perspective',
            'description': 'The same conversation as perceived through different memory system filters',
            'memory_systems': list(self.results.keys()),
            'generated_at': datetime.now().isoformat(),
            'messages': []
        }
        
        # For each message ID, show how each memory system processed it
        for msg_id in sorted(all_message_ids):
            message_perspectives = {
                'original_id': msg_id,
                'perspectives': {}
            }
            
            # Original content (get from any system that has this message)
            original_content = None
            original_author = None
            timestamp = None
            
            # Collect perspectives from each memory system
            for system_name, system_data in self.results.items():
                filtered_messages = system_data.get('filtered_messages', [])
                
                # Find this message in this system's results
                system_msg = next((msg for msg in filtered_messages if msg['original_id'] == msg_id), None)
                
                if system_msg:
                    if not original_content:
                        original_content = system_msg['content']
                        original_author = system_msg['author']
                        timestamp = system_msg.get('timestamp')
                    
                    message_perspectives['perspectives'][system_name] = {
                        'retained': True,
                        'relevance_score': system_msg['relevance_score'],
                        'filtered_content': system_msg['filtered_content'],
                        'memory_traces': system_msg['memory_traces'][:3],  # Top 3
                        'key_features': system_msg['extracted_features'][:3]  # Top 3
                    }
                else:
                    message_perspectives['perspectives'][system_name] = {
                        'retained': False,
                        'reason': 'Below relevance threshold for this memory system'
                    }
            
            message_perspectives.update({
                'original_content': original_content,
                'author': original_author,
                'timestamp': timestamp
            })
            
            comparative['messages'].append(message_perspectives)
        
        return comparative
    
    def save_all_filtered_conversations(self, output_dir: Optional[Path] = None):
        """Save filtered conversations for all memory systems."""
        if output_dir is None:
            output_dir = self.results_dir / 'filtered_conversations'
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = {}
        
        # Generate individual memory system conversations
        for memory_system in self.results.keys():
            print(f"Generating filtered conversation for {memory_system}...")
            
            # Full filtered conversation
            conversation = self.generate_filtered_conversation(memory_system)
            conv_file = output_dir / f'{memory_system}_filtered_conversation.json'
            
            with open(conv_file, 'w') as f:
                json.dump(conversation, f, indent=2)
            
            saved_files[f'{memory_system}_conversation'] = conv_file
            
            # Memory system summary
            summary = self.generate_memory_system_summary(memory_system)
            summary_file = output_dir / f'{memory_system}_memory_summary.json'
            
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            saved_files[f'{memory_system}_summary'] = summary_file
            
            print(f"  ✓ Conversation: {conv_file}")
            print(f"  ✓ Summary: {summary_file}")
        
        # Generate comparative conversation
        print("Generating comparative multi-perspective conversation...")
        comparative = self.generate_comparative_conversation()
        comp_file = output_dir / 'comparative_multi_memory_conversation.json'
        
        with open(comp_file, 'w') as f:
            json.dump(comparative, f, indent=2)
        
        saved_files['comparative'] = comp_file
        print(f"  ✓ Comparative: {comp_file}")
        
        # Generate index file
        index = {
            'title': 'Memory-Filtered Conversation Analysis - Generated Files',
            'description': 'Index of all generated conversation files and summaries',
            'generated_at': datetime.now().isoformat(),
            'memory_systems': list(self.results.keys()),
            'files': {
                'individual_conversations': [
                    f'{system}_filtered_conversation.json' 
                    for system in self.results.keys()
                ],
                'memory_summaries': [
                    f'{system}_memory_summary.json' 
                    for system in self.results.keys()
                ],
                'comparative_analysis': 'comparative_multi_memory_conversation.json'
            },
            'statistics': {
                'total_memory_systems': len(self.results),
                'total_files_generated': len(saved_files)
            }
        }
        
        index_file = output_dir / 'index.json'
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        saved_files['index'] = index_file
        print(f"  ✓ Index: {index_file}")
        
        return saved_files


def main():
    """Main entry point for conversation generation."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    results_dir = repo_root / 'analysis' / 'memory_analysis_results'
    
    if not results_dir.exists():
        print(f"Error: Results directory not found: {results_dir}")
        print("Please run memory_analysis.py first to generate results.")
        return
    
    # Generate filtered conversations
    generator = FilteredConversationGenerator(str(results_dir))
    saved_files = generator.save_all_filtered_conversations()
    
    print(f"\n{'='*60}")
    print("FILTERED CONVERSATIONS GENERATED")
    print(f"{'='*60}")
    print(f"Output directory: {results_dir / 'filtered_conversations'}")
    print(f"Total files generated: {len(saved_files)}")
    print(f"Memory systems processed: {len(generator.results)}")


if __name__ == '__main__':
    main()