#!/usr/bin/env python3
"""
Helper script to add inline citations to manuscript chapters.
This script identifies potential citation locations and suggests citations to add.
"""

import re
from pathlib import Path

# Citation mapping for common references
CITATION_MAP = {
    # Core papers
    "Transformer": "(Vaswani et al., 2017)",
    "Attention is All You Need": "(Vaswani et al., 2017)",
    "GPT-1": "(Radford et al., 2018)",
    "GPT-2": "(Radford et al., 2019)",
    "GPT-3": "(Brown et al., 2020)",
    "GPT-4": "(OpenAI, 2023)",
    "BERT": "(Devlin et al., 2018)",
    "T5": "(Raffel et al., 2020)",
    "LSTM": "(Hochreiter & Schmidhuber, 1997)",
    "Bahdanau": "(Bahdanau et al., 2014)",
    "InstructGPT": "(Ouyang et al., 2022)",
    "RLHF": "(Ouyang et al., 2022)",
    "Scaling Laws": "(Kaplan et al., 2020)",
    "Chain-of-Thought": "(Wei et al., 2022)",
}

# Model specifications that need citations
SPEC_PATTERNS = {
    r"175[0B]?亿参数": "(Brown et al., 2020)",
    r"1750亿参数": "(Brown et al., 2020)",
    r"28\.4 BLEU": "(Vaswani et al., 2017)",
    r"41\.8 BLEU": "(Vaswani et al., 2017)",
}

def find_citation_opportunities(file_path):
    """Find locations in file that might need citations."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    opportunities = []

    # Check for model names without citations
    for term, citation in CITATION_MAP.items():
        # Pattern to find term not already followed by a citation
        pattern = rf"{re.escape(term)}(?!\s*\([^)]+,\s*\d{{4}}\))"
        matches = re.finditer(pattern, content)
        for match in matches:
            context_start = max(0, match.start() - 50)
            context_end = min(len(content), match.end() + 50)
            context = content[context_start:context_end]
            opportunities.append({
                'position': match.start(),
                'term': term,
                'suggested_citation': citation,
                'context': context
            })

    # Check for specifications
    for pattern, citation in SPEC_PATTERNS.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            # Check if already has a citation nearby
            nearby_text = content[match.start():min(len(content), match.end() + 30)]
            if not re.search(r'\([^)]+,\s*\d{4}\)', nearby_text):
                context_start = max(0, match.start() - 50)
                context_end = min(len(content), match.end() + 50)
                context = content[context_start:context_end]
                opportunities.append({
                    'position': match.start(),
                    'term': match.group(),
                    'suggested_citation': citation,
                    'context': context
                })

    # Sort by position
    opportunities.sort(key=lambda x: x['position'])

    return opportunities

def main():
    manuscript_dir = Path("D:/code/github/llm_history/manuscript")

    # Process all chapters
    for chapter_dir in sorted(manuscript_dir.glob("*/"):
        if chapter_dir.is_dir() and not chapter_dir.name.startswith("00-") and not chapter_dir.name.startswith("99-"):
            print(f"\n{'='*60}")
            print(f"Chapter: {chapter_dir.name}")
            print('='*60)

            for md_file in chapter_dir.glob("*.md"):
                print(f"\nFile: {md_file.name}")
                opportunities = find_citation_opportunities(md_file)

                if opportunities:
                    print(f"Found {len(opportunities)} potential citation locations:\n")
                    for i, opp in enumerate(opportunities[:10], 1):  # Show first 10
                        print(f"{i}. Term: '{opp['term']}'")
                        print(f"   Suggested: {opp['suggested_citation']}")
                        print(f"   Context: ...{opp['context']}...")
                        print()
                else:
                    print("No obvious citation opportunities found.")

if __name__ == "__main__":
    main()
