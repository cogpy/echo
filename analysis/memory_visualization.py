#!/usr/bin/env python3
"""
Memory Analysis Visualization and Reporting
===========================================

Creates visualizations and detailed reports from the memory-filtered 
conversation analysis results.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import textwrap


class MemoryAnalysisReporter:
    """Generates reports and visualizations from memory analysis results."""
    
    def __init__(self, results_dir: str):
        """Initialize with path to analysis results."""
        self.results_dir = Path(results_dir)
        self.results = {}
        self.summary = {}
        self._load_results()
    
    def _load_results(self):
        """Load all analysis results."""
        # Load summary
        summary_file = self.results_dir / 'memory_analysis_summary.json'
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                self.summary = json.load(f)
        
        # Load individual results
        memory_systems = [
            'sensory_motor', 'attentional', 'intentional', 'working_memory',
            'semantic', 'episodic', 'procedural', 'existential'
        ]
        
        for system in memory_systems:
            result_file = self.results_dir / f'{system}_analysis.json'
            if result_file.exists():
                with open(result_file, 'r') as f:
                    self.results[system] = json.load(f)
    
    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive markdown report."""
        report = []
        
        # Header
        report.append("# Memory-Filtered Conversation Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        # Overview
        if self.summary:
            report.append("## Executive Summary")
            report.append("")
            report.append(f"**Analysis Date:** {self.summary.get('generated_at', 'Unknown')}")
            report.append(f"**Source:** {Path(self.summary.get('source_file', '')).name}")
            report.append(f"**Memory Systems Analyzed:** {len(self.results)}")
            report.append("")
            
            # Key findings
            report.append("### Key Findings")
            report.append("")
            for insight in self.summary.get('comparative_insights', []):
                report.append(f"- {insight}")
            report.append("")
        
        # Memory System Analysis
        report.append("## Memory System Analysis")
        report.append("")
        
        # Short-term vs Long-term comparison
        short_term = ['sensory_motor', 'attentional', 'intentional', 'working_memory']
        long_term = ['semantic', 'episodic', 'procedural', 'existential']
        
        report.append("### Short-Term Memory Systems")
        report.append("")
        for system in short_term:
            if system in self.results:
                report.extend(self._generate_system_section(system, self.results[system]))
        
        report.append("### Long-Term Memory Systems")
        report.append("")
        for system in long_term:
            if system in self.results:
                report.extend(self._generate_system_section(system, self.results[system]))
        
        # Comparative Analysis
        report.append("## Comparative Analysis")
        report.append("")
        report.extend(self._generate_comparative_section())
        
        # Sample Filtered Content
        report.append("## Sample Filtered Content")
        report.append("")
        report.extend(self._generate_sample_content())
        
        return "\n".join(report)
    
    def _generate_system_section(self, system_name: str, result_data: Dict) -> List[str]:
        """Generate a section for a specific memory system."""
        section = []
        
        config = result_data.get('filter_config', {})
        
        section.append(f"#### {config.get('name', system_name.replace('_', ' ').title())}")
        section.append("")
        section.append(f"**Description:** {config.get('description', 'No description available')}")
        section.append("")
        
        # Statistics
        section.append("**Processing Statistics:**")
        section.append(f"- Messages processed: {result_data.get('processed_messages', 0)}/{result_data.get('total_messages', 0)}")
        
        retention_rate = 0
        if result_data.get('total_messages', 0) > 0:
            retention_rate = result_data.get('processed_messages', 0) / result_data.get('total_messages', 0)
        section.append(f"- Retention rate: {retention_rate:.1%}")
        
        # Average relevance
        filtered_msgs = result_data.get('filtered_messages', [])
        if filtered_msgs:
            avg_relevance = sum(msg.get('relevance_score', 0) for msg in filtered_msgs) / len(filtered_msgs)
            section.append(f"- Average relevance: {avg_relevance:.2f}")
        
        section.append("")
        
        # Key insights
        insights = result_data.get('summary_insights', [])
        if insights:
            section.append("**Key Insights:**")
            for insight in insights:
                section.append(f"- {insight}")
            section.append("")
        
        # Processing characteristics
        processing = result_data.get('retention_patterns', {}).get('processing_characteristics', {})
        if processing:
            section.append("**Processing Characteristics:**")
            section.append(f"- Style: {processing.get('style', 'Unknown')}")
            section.append(f"- Temporal scope: {processing.get('scope', 'Unknown')}")
            section.append(f"- Selectivity: {processing.get('selectivity', 0):.1%}")
            section.append("")
        
        return section
    
    def _generate_comparative_section(self) -> List[str]:
        """Generate comparative analysis between memory systems."""
        section = []
        
        if not self.results:
            return ["No results available for comparison."]
        
        # Calculate retention rates
        retention_rates = {}
        for system, data in self.results.items():
            total = data.get('total_messages', 0)
            processed = data.get('processed_messages', 0)
            retention_rates[system] = processed / total if total > 0 else 0
        
        # Sort by retention rate
        sorted_systems = sorted(retention_rates.items(), key=lambda x: x[1], reverse=True)
        
        section.append("### Retention Rate Ranking")
        section.append("")
        section.append("| Rank | Memory System | Retention Rate | Processing Style |")
        section.append("|------|---------------|----------------|------------------|")
        
        for i, (system, rate) in enumerate(sorted_systems, 1):
            config = self.results[system].get('filter_config', {})
            name = config.get('name', system.replace('_', ' ').title())
            style = config.get('processing_style', 'Unknown')
            section.append(f"| {i} | {name} | {rate:.1%} | {style.title()} |")
        
        section.append("")
        
        # Short-term vs Long-term analysis
        short_term = ['sensory_motor', 'attentional', 'intentional', 'working_memory']
        long_term = ['semantic', 'episodic', 'procedural', 'existential']
        
        st_rates = [retention_rates.get(s, 0) for s in short_term if s in retention_rates]
        lt_rates = [retention_rates.get(s, 0) for s in long_term if s in retention_rates]
        
        if st_rates and lt_rates:
            st_avg = sum(st_rates) / len(st_rates)
            lt_avg = sum(lt_rates) / len(lt_rates)
            
            section.append("### Short-Term vs Long-Term Memory Systems")
            section.append("")
            section.append(f"- **Short-term average retention:** {st_avg:.1%}")
            section.append(f"- **Long-term average retention:** {lt_avg:.1%}")
            section.append("")
            
            if lt_avg > st_avg:
                section.append("Long-term memory systems show higher retention rates, suggesting the conversation contains more content relevant to knowledge, experience, and identity than immediate sensory-motor responses.")
            else:
                section.append("Short-term memory systems show higher retention rates, suggesting the conversation is more focused on immediate processing and reactive responses.")
        
        return section
    
    def _generate_sample_content(self) -> List[str]:
        """Generate sample filtered content from each memory system."""
        section = []
        
        for system_name, result_data in self.results.items():
            filtered_msgs = result_data.get('filtered_messages', [])
            if not filtered_msgs:
                continue
            
            # Get highest relevance message
            top_msg = max(filtered_msgs, key=lambda x: x.get('relevance_score', 0))
            
            config = result_data.get('filter_config', {})
            system_title = config.get('name', system_name.replace('_', ' ').title())
            
            section.append(f"### {system_title}")
            section.append("")
            
            section.append(f"**Relevance Score:** {top_msg.get('relevance_score', 0):.2f}")
            section.append("")
            
            # Original content (truncated)
            original = top_msg.get('content', '')
            if len(original) > 300:
                original = original[:300] + "..."
            section.append("**Original Content:**")
            section.append("```")
            section.append(original)
            section.append("```")
            section.append("")
            
            # Filtered content
            filtered = top_msg.get('filtered_content', '')
            if len(filtered) > 400:
                filtered = filtered[:400] + "..."
            section.append("**Filtered Content:**")
            section.append("```")
            section.append(filtered)
            section.append("```")
            section.append("")
            
            # Memory traces
            traces = top_msg.get('memory_traces', [])
            if traces:
                section.append("**Memory Traces:**")
                for trace in traces[:3]:  # Show top 3
                    section.append(f"- {trace}")
                section.append("")
            
            section.append("---")
            section.append("")
        
        return section
    
    def generate_feature_comparison_table(self) -> str:
        """Generate a comparison table of extracted features."""
        if not self.results:
            return "No results available for feature comparison."
        
        table = []
        table.append("# Memory System Feature Comparison")
        table.append("")
        table.append("| Memory System | Top Keywords | Processing Style | Temporal Scope |")
        table.append("|---------------|--------------|------------------|----------------|")
        
        for system_name, result_data in self.results.items():
            config = result_data.get('filter_config', {})
            name = config.get('name', system_name.replace('_', ' ').title())
            
            # Get top keywords (first 3)
            keywords = config.get('keywords', [])[:3]
            keyword_str = ", ".join(keywords) if keywords else "None"
            
            style = config.get('processing_style', 'Unknown')
            scope = config.get('temporal_scope', 'Unknown')
            
            table.append(f"| {name} | {keyword_str} | {style.title()} | {scope.title()} |")
        
        return "\n".join(table)
    
    def save_reports(self, output_dir: Optional[Path] = None):
        """Save all reports to files."""
        if output_dir is None:
            output_dir = self.results_dir
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Comprehensive report
        comprehensive_report = self.generate_comprehensive_report()
        report_file = output_dir / 'comprehensive_memory_analysis_report.md'
        with open(report_file, 'w') as f:
            f.write(comprehensive_report)
        
        print(f"✓ Comprehensive report: {report_file}")
        
        # Feature comparison
        feature_comparison = self.generate_feature_comparison_table()
        feature_file = output_dir / 'memory_system_feature_comparison.md'
        with open(feature_file, 'w') as f:
            f.write(feature_comparison)
        
        print(f"✓ Feature comparison: {feature_file}")
        
        return {
            'comprehensive_report': report_file,
            'feature_comparison': feature_file
        }


def main():
    """Main entry point for memory visualization."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    results_dir = repo_root / 'analysis' / 'memory_analysis_results'
    
    if not results_dir.exists():
        print(f"Error: Results directory not found: {results_dir}")
        print("Please run memory_analysis.py first to generate results.")
        return
    
    # Generate reports
    reporter = MemoryAnalysisReporter(str(results_dir))
    report_files = reporter.save_reports()
    
    print(f"\n{'='*60}")
    print("MEMORY ANALYSIS REPORTS GENERATED")  
    print(f"{'='*60}")
    
    for report_type, file_path in report_files.items():
        print(f"{report_type.replace('_', ' ').title()}: {file_path}")


if __name__ == '__main__':
    main()