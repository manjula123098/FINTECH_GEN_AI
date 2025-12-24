#!/usr/bin/env python3
"""Test script to verify NLP metrics are being calculated and returned."""

import sys
import os
import json
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from comparison.nlp_metrics import NLPMetricsAnalyzer

# Test the metrics calculation with sample text
rag_answer = "Education is fundamental. NEP 2020 emphasizes Teacher Education and Curriculum Development. Technology plays a key role."
kg_answer = "NEP 2020 provides comprehensive guidance on Education Quality and Teacher Professional Development. Key initiatives include Foundational Literacy, Numeracy, and Digital Infrastructure. These initiatives ensure holistic Learning Outcomes through Assessment Reforms and Vocational Education integration."

rag_metrics = {"query_time": 0.5, "num_source_chunks": 3}
kg_metrics = {"query_time": 1.2, "num_entities": 12, "num_relationships": 8}

print("=" * 80)
print("TESTING NLP METRICS CALCULATION")
print("=" * 80)

print("\nRAG Answer:")
print(rag_answer)
print(f"Length: {len(rag_answer)} chars")

print("\nKG Answer:")
print(kg_answer)
print(f"Length: {len(kg_answer)} chars")

# Calculate metrics
nlp_metrics = NLPMetricsAnalyzer.compare_nlp_metrics(
    rag_answer,
    kg_answer,
    rag_metrics,
    kg_metrics
)

print("\n" + "=" * 80)
print("RETURNED NLP METRICS:")
print("=" * 80)
for key, value in nlp_metrics.items():
    print(f"{key}: {value}")

print("\n" + "=" * 80)
print("KEY FIELDS FOR VISUALIZATION:")
print("=" * 80)
print(f"rag_entity_count: {nlp_metrics.get('rag_entity_count', 'NOT FOUND')}")
print(f"kg_entity_count: {nlp_metrics.get('kg_entity_count', 'NOT FOUND')}")
print(f"rag_quality_score: {nlp_metrics.get('rag_quality_score', 'NOT FOUND')}")
print(f"kg_quality_score: {nlp_metrics.get('kg_quality_score', 'NOT FOUND')}")
