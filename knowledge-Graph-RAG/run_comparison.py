#!/usr/bin/env python
"""Quick script to run full comparison and generate updated visualization."""

import asyncio
import os
from demo import initialize_systems, run_comparison_suite
from rich.console import Console

# Set environment to skip interactive prompts
os.environ['CI'] = '1'

console = Console()

async def run_full_comparison():
    """Run full comparison suite to generate updated graph."""
    console.print("[yellow]Initializing systems...[/yellow]")
    
    # Manually initialize without prompts
    from traditional_rag import TraditionalRAG
    from knowledge_graph import KnowledgeGraphRAG
    from pathlib import Path
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Initialize Traditional RAG
    rag_system = TraditionalRAG()
    doc_path = Path(__file__).parent / "sample_data" / "api_documentation.txt"
    documents = rag_system.load_documents(str(doc_path))
    rag_system.build_index(documents)
    console.print("[green][OK] Traditional RAG initialized[/green]")
    
    # Initialize Knowledge Graph RAG
    kg_system = KnowledgeGraphRAG()
    doc_texts = [doc.page_content for doc in documents]
    await kg_system.add_documents_to_graph(doc_texts, source="api_documentation")
    console.print("[green][OK] Knowledge Graph RAG initialized[/green]")
    
    console.print("[yellow]Running full comparison suite...[/yellow]")
    comparisons = await run_comparison_suite(rag_system, kg_system, verbose=False)
    
    console.print(f"\n[green]✓ Generated {len(comparisons)} comparisons with NLP metrics[/green]")
    
    # Show NLP metrics sample
    if comparisons and 'nlp_metrics' in comparisons[0]:
        metrics = comparisons[0]['nlp_metrics']
        console.print(f"\n[cyan]Sample NLP Metrics from Q1:[/cyan]")
        console.print(f"  RAG Entities: {metrics.get('rag_entity_count', 0)}")
        console.print(f"  KG Entities: {metrics.get('kg_entity_count', 0)}")
        console.print(f"  RAG Quality: {metrics.get('rag_quality_score', 0):.1f}/100")
        console.print(f"  KG Quality: {metrics.get('kg_quality_score', 0):.1f}/100")
    
    console.print("[green]\n✓ Graph visualization saved to: comparison_metrics.png[/green]")

if __name__ == "__main__":
    asyncio.run(run_full_comparison())
