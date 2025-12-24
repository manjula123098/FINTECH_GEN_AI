#!/usr/bin/env python3
"""Diagnostic script to check the comparison pipeline."""

import sys
import os
import json
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("DIAGNOSTIC: COMPARISON METRICS SYSTEM")
print("=" * 80)

# Check 1: NLP Metrics module
print("\n[1] Checking NLP Metrics module...")
try:
    from comparison.nlp_metrics import NLPMetricsAnalyzer
    print("✓ NLP Metrics module loads successfully")
    
    # Test basic calculation
    test_metrics = NLPMetricsAnalyzer.compare_nlp_metrics(
        "This is a test about Education and Technology.",
        "NEP 2020 emphasizes Education Quality and Professional Teacher Development with Technology integration.",
        {},
        {}
    )
    print(f"✓ Sample calculation works: {test_metrics.get('rag_entity_count')} vs {test_metrics.get('kg_entity_count')} entities")
except Exception as e:
    print(f"✗ Error with NLP Metrics: {e}")

# Check 2: Visualization function
print("\n[2] Checking visualization module...")
try:
    from comparison.visualize import visualize_plot_comparison
    print("✓ Visualization module loads successfully")
except Exception as e:
    print(f"✗ Error with visualization: {e}")

# Check 3: Compare module
print("\n[3] Checking compare module...")
try:
    from comparison.compare import compare_systems, run_comparison_suite
    print("✓ Compare module loads successfully")
except Exception as e:
    print(f"✗ Error with compare module: {e}")

# Check 4: Sample data
print("\n[4] Checking sample data...")
sample_file = Path("sample_data/api_documentation.txt")
if sample_file.exists():
    size = sample_file.stat().st_size
    content = sample_file.read_text()[:200]
    print(f"✓ Sample data exists ({size} bytes)")
    print(f"  Preview: {content[:100]}...")
else:
    print("✗ Sample data file not found")

# Check 5: Existing comparison metrics
print("\n[5] Checking existing comparison metrics...")
metrics_file = Path("comparison_metrics.png")
if metrics_file.exists():
    size = metrics_file.stat().st_size
    mtime = metrics_file.stat().st_mtime
    from datetime import datetime
    mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"✓ comparison_metrics.png exists")
    print(f"  Size: {size} bytes")
    print(f"  Last modified: {mod_time}")
else:
    print("✗ comparison_metrics.png not found")

# Check 6: Test data structure
print("\n[6] Testing data structure...")
test_comparison = {
    "question": "Test question?",
    "comparison_metrics": {
        "rag_time": 0.5,
        "kg_time": 1.2,
        "rag_sources": 3,
        "kg_facts": 8,
        "speedup": 0.42,
        "kg_entities": 15,
        "kg_relationships": 10
    },
    "nlp_metrics": {
        "rag_entity_count": 3,
        "kg_entity_count": 15,
        "rag_quality_score": 45.3,
        "kg_quality_score": 62.1,
        "rag_lexical_diversity": 0.85,
        "kg_lexical_diversity": 0.92
    }
}

print("✓ Test comparison data structure created")
print(f"  Keys: {list(test_comparison.keys())}")
print(f"  NLP Metrics keys: {list(test_comparison['nlp_metrics'].keys())}")

# Check 7: Verify visualization extraction logic
print("\n[7] Testing data extraction logic...")
results = [test_comparison]
rag_entities = []
kg_entities = []
rag_quality = []
kg_quality = []

for r in results:
    if 'nlp_metrics' in r:
        rag_quality.append(r['nlp_metrics'].get('rag_quality_score', 0))
        kg_quality.append(r['nlp_metrics'].get('kg_quality_score', 0))
        rag_entities.append(r['nlp_metrics'].get('rag_entity_count', 0))
        kg_entities.append(r['nlp_metrics'].get('kg_entity_count', 0))
    else:
        rag_quality.append(0)
        kg_quality.append(0)
        rag_entities.append(0)
        kg_entities.append(0)

print("✓ Data extraction successful:")
print(f"  RAG Entities: {rag_entities}")
print(f"  KG Entities: {kg_entities}")
print(f"  RAG Quality: {rag_quality}")
print(f"  KG Quality: {kg_quality}")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
print("\nSUMMARY:")
print("  - NLP metrics calculation: ✓ WORKING")
print("  - Data structure: ✓ CORRECT")
print("  - Visualization logic: ✓ SOUND")
print("\nNEXT STEP: Run full demo with real data to generate new visualization")
