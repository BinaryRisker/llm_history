#!/usr/bin/env python3
"""
Extract all inline citations from manuscript chapters
Format: (Author, Year) or (作者, 年份)
"""

import re
import glob
from pathlib import Path
from collections import defaultdict

def extract_citations_from_file(filepath):
    """Extract all citations from a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for (Author, Year) or (Author et al., Year)
    # Supports both English and Chinese authors
    patterns = [
        r'\(([A-Z][a-zA-Z\s]+(?:\set\sal\.)?),\s*(\d{4})\)',  # English: (Author, Year) or (Author et al., Year)
        r'\(([一-龥]+),\s*(\d{4})\)',  # Chinese: (作者, 年份)
        r'\(([A-Z][a-zA-Z\s]+(?:\set\sal\.)?\s*&\s*[A-Z][a-zA-Z\s]+),\s*(\d{4})\)',  # (Author1 & Author2, Year)
    ]

    citations = []
    for pattern in patterns:
        matches = re.findall(pattern, content)
        citations.extend([(author.strip(), year) for author, year in matches])

    return citations

def main():
    manuscript_dir = Path("D:/code/github/llm_history/manuscript")

    # Skip backmatter references and template files
    skip_files = ['references.md', 'chapter-template.md']

    # Collect all citations
    all_citations = defaultdict(set)
    file_citations = {}

    for md_file in sorted(manuscript_dir.rglob("*.md")):
        if md_file.name in skip_files:
            continue

        citations = extract_citations_from_file(md_file)
        if citations:
            file_citations[md_file.relative_to(manuscript_dir)] = citations
            for author, year in citations:
                all_citations[f"{author}, {year}"].add(str(md_file.relative_to(manuscript_dir)))

    # Print results
    print("=" * 80)
    print("INLINE CITATIONS EXTRACTION REPORT")
    print("=" * 80)
    print()

    print(f"Total unique citations found: {len(all_citations)}")
    print()

    print("CITATIONS BY FILE:")
    print("-" * 80)
    for filepath, citations in sorted(file_citations.items()):
        print(f"\n{filepath}:")
        unique_cites = sorted(set([f"({author}, {year})" for author, year in citations]))
        for cite in unique_cites:
            print(f"  - {cite}")

    print()
    print("=" * 80)
    print("ALL UNIQUE CITATIONS (sorted):")
    print("-" * 80)
    for citation in sorted(all_citations.keys()):
        files = ", ".join(sorted(all_citations[citation]))
        print(f"({citation})")
        print(f"  Found in: {files}")

    # Export to text file for easy reference
    output_file = Path("D:/code/github/llm_history/extracted_citations.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("EXTRACTED INLINE CITATIONS\n")
        f.write("=" * 80 + "\n\n")
        for citation in sorted(all_citations.keys()):
            f.write(f"({citation})\n")

    print(f"\n\nCitations also exported to: {output_file}")
    print()

    # Count total citations
    total_count = sum(len(cites) for cites in file_citations.values())
    print(f"Total citation instances: {total_count}")
    print(f"Unique citations: {len(all_citations)}")

if __name__ == "__main__":
    main()
