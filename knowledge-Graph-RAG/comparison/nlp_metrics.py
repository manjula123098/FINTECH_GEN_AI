"""NLP-based metrics for comparing Traditional RAG vs Knowledge Graph RAG."""

import asyncio
from typing import Dict, Any, List
from collections import Counter
import re
from rich.console import Console

console = Console()


class NLPMetricsAnalyzer:
    """Calculate NLP-based metrics for system comparison."""

    @staticmethod
    def extract_entities(text: str) -> List[str]:
        """
        Extract potential entities (capitalized words/phrases) from text.
        
        Args:
            text: Input text
            
        Returns:
            List of entities found
        """
        # Find capitalized phrases (simple entity extraction)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return entities

    @staticmethod
    def calculate_sentence_count(text: str) -> int:
        """Count sentences in text."""
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])

    @staticmethod
    def calculate_word_count(text: str) -> int:
        """Count words in text."""
        return len(text.split())

    @staticmethod
    def calculate_lexical_diversity(text: str) -> float:
        """
        Calculate lexical diversity (Type-Token Ratio).
        Higher value = more diverse vocabulary.
        """
        words = text.lower().split()
        if len(words) == 0:
            return 0.0
        unique_words = len(set(words))
        return unique_words / len(words)

    @staticmethod
    def calculate_information_density(text: str) -> float:
        """
        Calculate information density (number of entities per sentence).
        Higher = more concentrated information.
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        
        if len(sentences) == 0:
            return 0.0
        
        total_entities = 0
        for sentence in sentences:
            entities = NLPMetricsAnalyzer.extract_entities(sentence)
            total_entities += len(entities)
        
        return total_entities / len(sentences) if sentences else 0.0

    @staticmethod
    def calculate_semantic_coherence(text: str) -> float:
        """
        Calculate semantic coherence based on entity repetition.
        Higher = more cohesive text.
        """
        entities = NLPMetricsAnalyzer.extract_entities(text)
        
        if len(entities) == 0:
            return 0.0
        
        # Count entity frequency
        entity_counts = Counter(entities)
        # Entities appearing multiple times suggest coherent topic
        repeated_entities = sum(1 for count in entity_counts.values() if count > 1)
        
        return repeated_entities / len(entity_counts) if entity_counts else 0.0

    @staticmethod
    def calculate_answer_quality_score(answer: str, metrics: Dict[str, Any]) -> float:
        """
        Calculate overall answer quality score (0-100).
        
        Args:
            answer: The answer text
            metrics: System metrics (entities, relationships, etc.)
            
        Returns:
            Quality score 0-100
        """
        score = 0.0
        
        # Length bonus (longer answers tend to be more comprehensive)
        word_count = NLPMetricsAnalyzer.calculate_word_count(answer)
        score += min(20, word_count / 10)  # Max 20 points
        
        # Lexical diversity bonus
        diversity = NLPMetricsAnalyzer.calculate_lexical_diversity(answer)
        score += diversity * 20  # Max 20 points
        
        # Coherence bonus
        coherence = NLPMetricsAnalyzer.calculate_semantic_coherence(answer)
        score += coherence * 20  # Max 20 points
        
        # Information density bonus
        density = NLPMetricsAnalyzer.calculate_information_density(answer)
        score += min(20, density * 10)  # Max 20 points
        
        # Bonus for KG-specific metrics
        if 'num_entities' in metrics:
            score += min(20, metrics['num_entities'] * 2)  # Max 20 points
        
        return min(100, score)

    @staticmethod
    def compare_nlp_metrics(rag_answer: str, kg_answer: str, 
                           rag_metrics: Dict[str, Any], 
                           kg_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare NLP metrics between two answers.
        
        Args:
            rag_answer: Traditional RAG answer
            kg_answer: Knowledge Graph RAG answer
            rag_metrics: RAG system metrics
            kg_metrics: KG system metrics
            
        Returns:
            Dictionary with NLP comparison metrics
        """
        
        rag_entities = NLPMetricsAnalyzer.extract_entities(rag_answer)
        kg_entities = NLPMetricsAnalyzer.extract_entities(kg_answer)
        
        rag_quality = NLPMetricsAnalyzer.calculate_answer_quality_score(rag_answer, rag_metrics)
        kg_quality = NLPMetricsAnalyzer.calculate_answer_quality_score(kg_answer, kg_metrics)
        
        common_entities = set(rag_entities) & set(kg_entities)
        
        return {
            "rag_entity_count": len(rag_entities),
            "kg_entity_count": len(kg_entities),
            "unique_entities_ratio": len(kg_entities) / len(rag_entities) if rag_entities else 1.0,
            "common_entities": len(common_entities),
            "rag_lexical_diversity": NLPMetricsAnalyzer.calculate_lexical_diversity(rag_answer),
            "kg_lexical_diversity": NLPMetricsAnalyzer.calculate_lexical_diversity(kg_answer),
            "rag_semantic_coherence": NLPMetricsAnalyzer.calculate_semantic_coherence(rag_answer),
            "kg_semantic_coherence": NLPMetricsAnalyzer.calculate_semantic_coherence(kg_answer),
            "rag_information_density": NLPMetricsAnalyzer.calculate_information_density(rag_answer),
            "kg_information_density": NLPMetricsAnalyzer.calculate_information_density(kg_answer),
            "rag_quality_score": rag_quality,
            "kg_quality_score": kg_quality,
            "quality_improvement": kg_quality - rag_quality
        }


def display_nlp_metrics(nlp_metrics: Dict[str, Any]) -> None:
    """
    Display NLP metrics comparison in a formatted table.
    
    Args:
        nlp_metrics: Dictionary with NLP metrics
    """
    from rich.table import Table
    from rich import box
    
    console.print("\n[bold cyan]NLP & SEMANTIC METRICS[/bold cyan]")
    
    table = Table(title="NLP Comparison Analysis", box=box.ROUNDED, show_header=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Traditional RAG", style="blue")
    table.add_column("Knowledge Graph RAG", style="magenta")
    table.add_column("Winner", style="green")
    
    # Entity analysis
    rag_entities = nlp_metrics['rag_entity_count']
    kg_entities = nlp_metrics['kg_entity_count']
    entity_winner = "KG" if kg_entities > rag_entities else "RAG"
    table.add_row(
        "Entities Identified",
        str(rag_entities),
        str(kg_entities),
        entity_winner
    )
    
    # Lexical diversity
    rag_diversity = nlp_metrics['rag_lexical_diversity']
    kg_diversity = nlp_metrics['kg_lexical_diversity']
    diversity_winner = "KG" if kg_diversity > rag_diversity else "RAG"
    table.add_row(
        "Lexical Diversity",
        f"{rag_diversity:.3f}",
        f"{kg_diversity:.3f}",
        diversity_winner
    )
    
    # Semantic coherence
    rag_coherence = nlp_metrics['rag_semantic_coherence']
    kg_coherence = nlp_metrics['kg_semantic_coherence']
    coherence_winner = "KG" if kg_coherence > rag_coherence else "RAG"
    table.add_row(
        "Semantic Coherence",
        f"{rag_coherence:.3f}",
        f"{kg_coherence:.3f}",
        coherence_winner
    )
    
    # Information density
    rag_density = nlp_metrics['rag_information_density']
    kg_density = nlp_metrics['kg_information_density']
    density_winner = "KG" if kg_density > rag_density else "RAG"
    table.add_row(
        "Information Density",
        f"{rag_density:.3f}",
        f"{kg_density:.3f}",
        density_winner
    )
    
    # Answer quality score
    rag_quality = nlp_metrics['rag_quality_score']
    kg_quality = nlp_metrics['kg_quality_score']
    quality_winner = "KG" if kg_quality > rag_quality else "RAG"
    improvement = nlp_metrics['quality_improvement']
    table.add_row(
        "Answer Quality Score",
        f"{rag_quality:.1f}/100",
        f"{kg_quality:.1f}/100",
        f"{quality_winner} (+{improvement:.1f})" if improvement > 0 else quality_winner
    )
    
    console.print(table)
    
    # Additional insights
    console.print("\n[bold]Key Insights:[/bold]")
    console.print(f"  • Common entities between systems: {nlp_metrics['common_entities']}")
    console.print(f"  • KG provides {nlp_metrics['unique_entities_ratio']:.1f}x more entities")
    
    if improvement > 0:
        console.print(f"  ✓ Knowledge Graph provides {improvement:.1f} points better quality")
    else:
        console.print(f"  ✓ Traditional RAG provides {abs(improvement):.1f} points better quality")
