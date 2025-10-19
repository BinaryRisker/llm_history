#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Validation Script for LLM History Chronicle
Combines T159 (word counts), T160 (citations), T161 (cross-references)
Task: T161a

Usage:
    python validate_all.py              # Run all validations
    python validate_all.py --words      # Run only word count validation
    python validate_all.py --citations  # Run only citation validation
    python validate_all.py --links      # Run only cross-reference validation
    python validate_all.py --quick      # Run quick validation (summary only)
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(".")
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
CLAUDEDOCS_DIR = PROJECT_ROOT / "claudedocs"

# ============================================================================
# T159: Word Count Validation
# ============================================================================

def count_chinese_chars(text):
    """
    Count Chinese characters in text (same logic as validate_word_counts.py).
    Excludes markdown syntax and frontmatter.
    """
    # Remove markdown frontmatter (YAML between --- markers)
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL | re.MULTILINE)

    # Remove markdown links but keep link text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove markdown image syntax
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)

    # Remove markdown headings markers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove markdown bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)

    # Count Chinese characters (including punctuation)
    chinese_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]', text)

    return len(chinese_chars)

def validate_word_counts(quick=False):
    """Validate chapter word counts (T159)."""
    print("\n" + "="*70)
    print("WORD COUNT VALIDATION - T159")
    print("="*70 + "\n")

    target_min = 9000
    target_max = 13500

    # Define exact chapter list (same as validate_word_counts.py)
    chapters = [
        ("第1章", "manuscript/01-foundation/transformer-revolution.md"),
        ("第2章", "manuscript/01-foundation/early-applications.md"),
        ("第3章", "manuscript/02-gpt-era/scaling-up.md"),
        ("第4章", "manuscript/02-gpt-era/google-response.md"),
        ("第5章", "manuscript/03-alignment/rlhf-chatgpt.md"),
        ("第6章", "manuscript/04-chatgpt-revolution/chatgpt-launch.md"),
        ("第7章", "manuscript/05-global-race-2023/ai-race-2023.md"),
        ("第8章", "manuscript/05-global-race-2023/meta-llama.md"),
        ("第9章", "manuscript/06-chinese-ai/chinese-development.md"),
        ("第10章", "manuscript/07-multimodal-era/2024-breakthroughs.md"),
        ("第11章", "manuscript/08-present/2025-present.md"),
    ]

    results = []
    total_chars = 0
    in_range_count = 0

    for chapter_num, file_path in chapters:
        chapter_path = Path(file_path)
        try:
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
                char_count = count_chinese_chars(content)
                total_chars += char_count

                in_range = target_min <= char_count <= target_max
                if in_range:
                    in_range_count += 1
                    status = "PASS"
                else:
                    status = "WARN"

                results.append({
                    'file': chapter_path.name,
                    'chars': char_count,
                    'in_range': in_range,
                    'status': status
                })

                if not quick:
                    print(f"[{status}] {chapter_path.name}: {char_count:,} chars")
        except Exception as e:
            print(f"[ERROR] {chapter_path.name}: {e}")

    # Summary
    print(f"\nTotal chapters: {len(results)}")
    print(f"In range ({target_min:,}-{target_max:,}): {in_range_count}/{len(results)}")
    print(f"Total characters: {total_chars:,}")
    print(f"Target range: 100,000-150,000")

    if total_chars < 100000:
        print(f"WARNING: Below minimum by {100000 - total_chars:,} chars")
    elif total_chars > 150000:
        print(f"WARNING: Above maximum by {total_chars - 150000:,} chars")
    else:
        print("PASS: Total within target range")

    return {
        'total_chars': total_chars,
        'in_range_count': in_range_count,
        'total_chapters': len(results),
        'passed': total_chars >= 100000 and total_chars <= 150000
    }

# ============================================================================
# T160: Citation Format Validation
# ============================================================================

VALID_CITATION_PATTERNS = [
    r'\([A-Z][a-zA-Z\s&]+,\s*\d{4}\)',  # (Author, Year)
    r'\([A-Z][a-zA-Z\s&]+\s+et\s+al\.,\s*\d{4}\)',  # (Author et al., Year)
    r'\([A-Z][a-zA-Z\s&]+\s+&\s+[A-Z][a-zA-Z\s]+,\s*\d{4}\)',  # (Author1 & Author2, Year)
]

PROBLEMATIC_PATTERNS = [
    (r'\([A-Z][a-zA-Z\s&]+\s+\d{4}\)', "Missing comma between author and year"),
    (r'\[[A-Z][a-zA-Z\s&]+,\s*\d{4}\]', "Wrong bracket type (should be parentheses)"),
    (r'\([A-Z][a-zA-Z\s&]+\.\s*\d{4}\)', "Period instead of comma"),
]

def find_all_citations(content):
    """Find all potential citations in content."""
    citation_pattern = r'\([A-Z][^\)]{0,100}(?:19|20)\d{2}\)'
    return re.finditer(citation_pattern, content)

def validate_citation(citation_text):
    """Check if citation matches valid format."""
    for pattern in VALID_CITATION_PATTERNS:
        if re.fullmatch(pattern, citation_text):
            return True, "Valid format"
    for pattern, issue in PROBLEMATIC_PATTERNS:
        if re.fullmatch(pattern, citation_text):
            return False, issue
    return False, "Unknown citation format"

def validate_citations(quick=False):
    """Validate citation formats (T160)."""
    print("\n" + "="*70)
    print("CITATION FORMAT VALIDATION - T160")
    print("="*70 + "\n")

    chapter_files = []
    for root, dirs, files in os.walk(MANUSCRIPT_DIR):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                chapter_files.append(Path(root) / file)

    chapter_files.sort()

    total_valid = 0
    total_invalid = 0
    chapters_with_issues = []

    for chapter_path in chapter_files:
        try:
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            if not quick:
                print(f"[ERROR] {chapter_path.name}: {e}")
            continue

        citations = find_all_citations(content)
        valid_count = 0
        invalid_count = 0
        issues = []

        for match in citations:
            citation_text = match.group(0)
            is_valid, message = validate_citation(citation_text)

            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'line': line_num,
                    'citation': citation_text,
                    'issue': message
                })

        total_valid += valid_count
        total_invalid += invalid_count

        if invalid_count > 0:
            chapters_with_issues.append({
                'file': chapter_path.name,
                'valid_count': valid_count,
                'invalid_count': invalid_count,
                'issues': issues
            })
            if not quick:
                print(f"[WARNING] {chapter_path.name}: {invalid_count} invalid citation(s)")
        elif valid_count > 0 and not quick:
            print(f"[PASS] {chapter_path.name}: {valid_count} citation(s) valid")

    print(f"\nTotal citations: {total_valid + total_invalid}")
    print(f"Valid: {total_valid}")
    print(f"Invalid: {total_invalid}")

    if total_invalid == 0:
        print("[PASS] All citations in valid format")
    else:
        print(f"[WARN]  {total_invalid} citation(s) need correction")

    return {
        'total_valid': total_valid,
        'total_invalid': total_invalid,
        'passed': total_invalid == 0
    }

# ============================================================================
# T161: Cross-Reference Validation
# ============================================================================

MARKDOWN_LINK_PATTERN = r'\[([^\]]+)\]\(([^\)]+)\)'

def find_all_links(content):
    """Find all markdown links in content."""
    return re.findall(MARKDOWN_LINK_PATTERN, content)

def validate_file_reference(source_file, target_path):
    """Validate if a file reference exists."""
    source_dir = source_file.parent

    # Local section references are valid
    if target_path.startswith('#'):
        return True, "Local section reference"

    # External URLs - skip validation
    if target_path.startswith('http://') or target_path.startswith('https://'):
        return True, "External URL (not validated)"

    # Resolve relative path
    if target_path.startswith('/'):
        target_file = PROJECT_ROOT / target_path.lstrip('/')
    else:
        target_file = source_dir / target_path

    # Remove anchor if present
    if '#' in str(target_file):
        target_file = Path(str(target_file).split('#')[0])

    # Normalize path
    try:
        target_file = target_file.resolve()
    except:
        return False, f"Invalid path: {target_path}"

    # Check if file exists
    if target_file.exists():
        return True, "Valid file reference"
    else:
        return False, f"File not found: {target_path}"

def validate_cross_references(quick=False):
    """Validate all cross-references (T161)."""
    print("\n" + "="*70)
    print("CROSS-REFERENCE VALIDATION - T161")
    print("="*70 + "\n")

    chapter_files = []
    for root, dirs, files in os.walk(MANUSCRIPT_DIR):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                chapter_files.append(Path(root) / file)

    chapter_files.sort()

    total_valid = 0
    total_invalid = 0
    chapters_with_issues = []

    for chapter_path in chapter_files:
        try:
            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            if not quick:
                print(f"[ERROR] {chapter_path.name}: {e}")
            continue

        links = find_all_links(content)
        valid_count = 0
        invalid_count = 0
        issues = []

        for link_text, link_path in links:
            is_valid, message = validate_file_reference(chapter_path, link_path)

            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                # Find line number
                link_pattern = re.escape(f"[{link_text}]({link_path})")
                match = re.search(link_pattern, content)
                line_num = content[:match.start()].count('\n') + 1 if match else 0

                issues.append({
                    'line': line_num,
                    'text': link_text,
                    'path': link_path,
                    'issue': message
                })

        total_valid += valid_count
        total_invalid += invalid_count

        if invalid_count > 0:
            chapters_with_issues.append({
                'file': chapter_path.name,
                'valid_count': valid_count,
                'invalid_count': invalid_count,
                'issues': issues
            })
            if not quick:
                print(f"[WARNING] {chapter_path.name}: {invalid_count} broken link(s)")
        elif valid_count > 0 and not quick:
            print(f"[PASS] {chapter_path.name}: {valid_count} link(s) valid")

    print(f"\nTotal links: {total_valid + total_invalid}")
    print(f"Valid: {total_valid}")
    print(f"Broken: {total_invalid}")

    # Note about documentation examples
    if total_invalid > 0:
        # Check if broken links are in documentation files
        doc_files = ['chapter-template.md', 'index.md']
        doc_issues = sum(1 for ch in chapters_with_issues if ch['file'] in doc_files)
        real_issues = total_invalid - doc_issues

        if real_issues == 0 and doc_issues > 0:
            print("[INFO]  All broken links are in documentation examples (intentional)")
            print("[PASS] All chapter cross-references valid")
        else:
            print(f"[WARN]  {total_invalid} broken link(s) need fixing")
    else:
        print("[PASS] All cross-references valid")

    return {
        'total_valid': total_valid,
        'total_invalid': total_invalid,
        'passed': total_invalid == 0 or all(ch['file'] in ['chapter-template.md', 'index.md'] for ch in chapters_with_issues)
    }

# ============================================================================
# Main Batch Validation
# ============================================================================

def run_all_validations(args):
    """Run all or selected validations."""
    print("\n" + "="*70)
    print("BATCH VALIDATION - LLM History Chronicle")
    print("Tasks: T159 (Word Counts) + T160 (Citations) + T161 (Cross-References)")
    print("="*70)

    results = {}

    # Determine which validations to run
    run_all = not (args.words or args.citations or args.links)

    if run_all or args.words:
        results['word_counts'] = validate_word_counts(quick=args.quick)

    if run_all or args.citations:
        results['citations'] = validate_citations(quick=args.quick)

    if run_all or args.links:
        results['cross_references'] = validate_cross_references(quick=args.quick)

    # Overall summary
    print("\n" + "="*70)
    print("OVERALL VALIDATION SUMMARY")
    print("="*70)

    all_passed = True

    if 'word_counts' in results:
        status = "[PASS] PASS" if results['word_counts']['passed'] else "[WARN]  WARN"
        print(f"Word Counts (T159): {status}")
        all_passed = all_passed and results['word_counts']['passed']

    if 'citations' in results:
        status = "[PASS] PASS" if results['citations']['passed'] else "[FAIL] FAIL"
        print(f"Citations (T160): {status}")
        all_passed = all_passed and results['citations']['passed']

    if 'cross_references' in results:
        status = "[PASS] PASS" if results['cross_references']['passed'] else "[WARN]  WARN"
        print(f"Cross-References (T161): {status}")
        all_passed = all_passed and results['cross_references']['passed']

    print("="*70)

    if all_passed:
        print("[PASS] All validations passed!")
    else:
        print("[WARN]  Some validations require attention")

    # Save summary report
    if not args.quick:
        save_summary_report(results)

    return 0 if all_passed else 1

def save_summary_report(results):
    """Save validation summary to file."""
    CLAUDEDOCS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = CLAUDEDOCS_DIR / f"validation_batch_summary_{timestamp}.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("BATCH VALIDATION SUMMARY\n")
        f.write("="*70 + "\n\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if 'word_counts' in results:
            f.write("Word Counts (T159):\n")
            f.write(f"  Total characters: {results['word_counts']['total_chars']:,}\n")
            f.write(f"  Chapters in range: {results['word_counts']['in_range_count']}/{results['word_counts']['total_chapters']}\n")
            f.write(f"  Status: {'PASS' if results['word_counts']['passed'] else 'WARN'}\n\n")

        if 'citations' in results:
            f.write("Citations (T160):\n")
            f.write(f"  Valid citations: {results['citations']['total_valid']}\n")
            f.write(f"  Invalid citations: {results['citations']['total_invalid']}\n")
            f.write(f"  Status: {'PASS' if results['citations']['passed'] else 'FAIL'}\n\n")

        if 'cross_references' in results:
            f.write("Cross-References (T161):\n")
            f.write(f"  Valid links: {results['cross_references']['total_valid']}\n")
            f.write(f"  Broken links: {results['cross_references']['total_invalid']}\n")
            f.write(f"  Status: {'PASS' if results['cross_references']['passed'] else 'WARN'}\n\n")

    print(f"\nSummary report saved to: {report_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Batch validation for LLM History Chronicle (T161a)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_all.py              # Run all validations
  python validate_all.py --words      # Run only word count check
  python validate_all.py --citations  # Run only citation check
  python validate_all.py --links      # Run only cross-reference check
  python validate_all.py --quick      # Quick summary without details
        """
    )

    parser.add_argument('--words', action='store_true', help='Run only word count validation (T159)')
    parser.add_argument('--citations', action='store_true', help='Run only citation validation (T160)')
    parser.add_argument('--links', action='store_true', help='Run only cross-reference validation (T161)')
    parser.add_argument('--quick', action='store_true', help='Quick mode (summary only, no details)')

    args = parser.parse_args()

    return run_all_validations(args)

if __name__ == "__main__":
    sys.exit(main())
