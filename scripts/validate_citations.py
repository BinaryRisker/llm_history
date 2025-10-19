#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Citation Format Validator for LLM History Chronicle
Validates (Author, Year) citation format across all manuscript chapters
Task: T160
"""

import os
import re
from pathlib import Path

# Manuscript directory
MANUSCRIPT_DIR = Path("manuscript")

# Citation patterns
VALID_CITATION_PATTERNS = [
    r'\([A-Z][a-zA-Z\s&]+,\s*\d{4}\)',  # (Author, Year)
    r'\([A-Z][a-zA-Z\s&]+\s+et\s+al\.,\s*\d{4}\)',  # (Author et al., Year)
    r'\([A-Z][a-zA-Z\s&]+\s+&\s+[A-Z][a-zA-Z\s]+,\s*\d{4}\)',  # (Author1 & Author2, Year)
]

PROBLEMATIC_PATTERNS = [
    (r'\([A-Z][a-zA-Z\s&]+\s+\d{4}\)', "Missing comma between author and year"),  # (Author Year)
    (r'\[[A-Z][a-zA-Z\s&]+,\s*\d{4}\]', "Wrong bracket type (should be parentheses)"),  # [Author, Year]
    (r'\([A-Z][a-zA-Z\s&]+\.\s*\d{4}\)', "Period instead of comma"),  # (Author. Year)
]

def find_all_citations(content):
    """Find all potential citations in content."""
    # Match patterns like (Something, YYYY) or (Something YYYY)
    citation_pattern = r'\([A-Z][^\)]{0,100}(?:19|20)\d{2}\)'
    return re.finditer(citation_pattern, content)

def validate_citation(citation_text):
    """Check if citation matches valid format."""
    # Check valid patterns
    for pattern in VALID_CITATION_PATTERNS:
        if re.fullmatch(pattern, citation_text):
            return True, "Valid format"

    # Check problematic patterns
    for pattern, issue in PROBLEMATIC_PATTERNS:
        if re.fullmatch(pattern, citation_text):
            return False, issue

    # If no match, it's an unknown format
    return False, "Unknown citation format"

def get_line_number(content, position):
    """Get line number for a position in content."""
    return content[:position].count('\n') + 1

def validate_chapter_citations(chapter_path):
    """Validate all citations in a chapter file."""
    try:
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            'file': chapter_path.name,
            'error': f"Failed to read file: {e}",
            'valid_count': 0,
            'invalid_count': 0,
            'issues': []
        }

    citations = find_all_citations(content)
    valid_count = 0
    invalid_count = 0
    issues = []

    for match in citations:
        citation_text = match.group(0)
        is_valid, message = validate_citation(citation_text)
        line_num = get_line_number(content, match.start())

        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            issues.append({
                'line': line_num,
                'citation': citation_text,
                'issue': message
            })

    return {
        'file': chapter_path.name,
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'issues': issues
    }

def main():
    print("=" * 70)
    print("CITATION FORMAT VALIDATION - T160")
    print("=" * 70)
    print()

    # Get all markdown files in manuscript directory
    chapter_files = []
    for root, dirs, files in os.walk(MANUSCRIPT_DIR):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                chapter_files.append(Path(root) / file)

    chapter_files.sort()

    print(f"Found {len(chapter_files)} chapter files to validate")
    print()

    total_valid = 0
    total_invalid = 0
    chapters_with_issues = []

    # Validate each chapter
    for chapter_path in chapter_files:
        result = validate_chapter_citations(chapter_path)

        if 'error' in result:
            print(f"[ERROR] {result['file']}: {result['error']}")
            continue

        total_valid += result['valid_count']
        total_invalid += result['invalid_count']

        if result['invalid_count'] > 0:
            chapters_with_issues.append(result)
            print(f"[WARNING] {result['file']}: {result['invalid_count']} invalid citation(s)")
        else:
            print(f"[PASS] {result['file']}: {result['valid_count']} citation(s) valid")

    # Summary
    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total citations found: {total_valid + total_invalid}")
    print(f"Valid citations: {total_valid}")
    print(f"Invalid citations: {total_invalid}")
    print(f"Chapters with issues: {len(chapters_with_issues)}")
    print()

    # Detailed issues
    if chapters_with_issues:
        print("=" * 70)
        print("DETAILED ISSUES")
        print("=" * 70)
        print()

        for chapter in chapters_with_issues:
            print(f"File: {chapter['file']}")
            print(f"Issues: {len(chapter['issues'])}")
            print()

            for issue in chapter['issues']:
                print(f"  Line {issue['line']}: {issue['citation']}")
                print(f"  Problem: {issue['issue']}")
                print()

        # Save detailed report
        report_path = Path("claudedocs/validation_t160_citations.txt")
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("CITATION FORMAT VALIDATION REPORT - T160\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total citations: {total_valid + total_invalid}\n")
            f.write(f"Valid: {total_valid}\n")
            f.write(f"Invalid: {total_invalid}\n")
            f.write(f"Chapters with issues: {len(chapters_with_issues)}\n\n")
            f.write("=" * 70 + "\n")
            f.write("DETAILED ISSUES\n")
            f.write("=" * 70 + "\n\n")

            for chapter in chapters_with_issues:
                f.write(f"File: {chapter['file']}\n")
                f.write(f"Issues: {len(chapter['issues'])}\n\n")

                for issue in chapter['issues']:
                    f.write(f"  Line {issue['line']}: {issue['citation']}\n")
                    f.write(f"  Problem: {issue['issue']}\n\n")

        print(f"Detailed report saved to: {report_path}")
        print()

        # Validation result
        print("=" * 70)
        if total_invalid == 0:
            print("[PASS] All citations follow correct format")
        else:
            print(f"[FAIL] {total_invalid} citation(s) need correction")
        print("=" * 70)
    else:
        print("[PASS] All citations follow correct (Author, Year) format!")
        print("=" * 70)

if __name__ == "__main__":
    main()
