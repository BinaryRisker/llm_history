#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-Reference Validator for LLM History Chronicle
Validates all internal links and cross-references across manuscript chapters
Task: T161
"""

import os
import re
from pathlib import Path

# Project root
PROJECT_ROOT = Path(".")

# Manuscript directory
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"

# Common reference patterns
MARKDOWN_LINK_PATTERN = r'\[([^\]]+)\]\(([^\)]+)\)'
SECTION_ANCHOR_PATTERN = r'#[a-z0-9-]+'

def find_all_links(content):
    """Find all markdown links in content."""
    return re.findall(MARKDOWN_LINK_PATTERN, content)

def validate_file_reference(source_file, target_path):
    """Validate if a file reference exists."""
    # Handle absolute vs relative paths
    source_dir = source_file.parent

    # If target is just an anchor (#section), it's valid (local section)
    if target_path.startswith('#'):
        return True, "Local section reference"

    # If target is external URL, skip validation
    if target_path.startswith('http://') or target_path.startswith('https://'):
        return True, "External URL (not validated)"

    # Resolve relative path
    if target_path.startswith('/'):
        # Absolute from project root
        target_file = PROJECT_ROOT / target_path.lstrip('/')
    else:
        # Relative to source file
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

def get_line_number(content, position):
    """Get line number for a position in content."""
    return content[:position].count('\n') + 1

def validate_chapter_references(chapter_path):
    """Validate all cross-references in a chapter file."""
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

    links = find_all_links(content)
    valid_count = 0
    invalid_count = 0
    issues = []

    for link_text, link_path in links:
        is_valid, message = validate_file_reference(chapter_path, link_path)

        # Find line number (approximate)
        link_pattern = re.escape(f"[{link_text}]({link_path})")
        match = re.search(link_pattern, content)
        line_num = get_line_number(content, match.start()) if match else 0

        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            issues.append({
                'line': line_num,
                'text': link_text,
                'path': link_path,
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
    print("CROSS-REFERENCE VALIDATION - T161")
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
        result = validate_chapter_references(chapter_path)

        if 'error' in result:
            print(f"[ERROR] {result['file']}: {result['error']}")
            continue

        total_valid += result['valid_count']
        total_invalid += result['invalid_count']

        if result['invalid_count'] > 0:
            chapters_with_issues.append(result)
            print(f"[WARNING] {result['file']}: {result['invalid_count']} broken link(s)")
        else:
            print(f"[PASS] {result['file']}: {result['valid_count']} link(s) valid")

    # Summary
    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total links found: {total_valid + total_invalid}")
    print(f"Valid links: {total_valid}")
    print(f"Broken links: {total_invalid}")
    print(f"Chapters with broken links: {len(chapters_with_issues)}")
    print()

    # Detailed issues
    if chapters_with_issues:
        print("=" * 70)
        print("DETAILED ISSUES")
        print("=" * 70)
        print()

        for chapter in chapters_with_issues:
            print(f"File: {chapter['file']}")
            print(f"Broken links: {len(chapter['issues'])}")
            print()

            for issue in chapter['issues']:
                print(f"  Line {issue['line']}: [{issue['text']}]({issue['path']})")
                print(f"  Problem: {issue['issue']}")
                print()

        # Save detailed report
        report_path = Path("claudedocs/validation_t161_cross_references.txt")
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("CROSS-REFERENCE VALIDATION REPORT - T161\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total links: {total_valid + total_invalid}\n")
            f.write(f"Valid: {total_valid}\n")
            f.write(f"Broken: {total_invalid}\n")
            f.write(f"Chapters with issues: {len(chapters_with_issues)}\n\n")
            f.write("=" * 70 + "\n")
            f.write("DETAILED ISSUES\n")
            f.write("=" * 70 + "\n\n")

            for chapter in chapters_with_issues:
                f.write(f"File: {chapter['file']}\n")
                f.write(f"Broken links: {len(chapter['issues'])}\n\n")

                for issue in chapter['issues']:
                    f.write(f"  Line {issue['line']}: [{issue['text']}]({issue['path']})\n")
                    f.write(f"  Problem: {issue['issue']}\n\n")

        print(f"Detailed report saved to: {report_path}")
        print()

        # Validation result
        print("=" * 70)
        if total_invalid == 0:
            print("[PASS] All cross-references are valid")
        else:
            print(f"[FAIL] {total_invalid} broken link(s) need fixing")
        print("=" * 70)
    else:
        print("[PASS] All cross-references link correctly!")
        print("=" * 70)

if __name__ == "__main__":
    main()
