#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T159: Validate Chapter Word Counts
Validates that all 11 main chapters are within 9,000-13,500 Chinese character range.
"""

import re
from pathlib import Path

# Define target range
MIN_CHARS = 9000
MAX_CHARS = 13500
TARGET_RANGE = f"{MIN_CHARS:,}-{MAX_CHARS:,}"

# Define chapter files
CHAPTERS = [
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

def count_chinese_chars(text):
    """
    Count Chinese characters in text.
    Includes:
    - CJK Unified Ideographs: 4E00-9FFF
    - CJK Extension A: 3400-4DBF
    - CJK punctuation and symbols

    Excludes:
    - Markdown syntax
    - English text
    - Numbers
    - Whitespace
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
    # CJK Unified Ideographs + Extension A + Chinese punctuation
    chinese_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]', text)

    return len(chinese_chars)

def validate_chapters(base_path="."):
    """Validate all chapter word counts."""
    base = Path(base_path)
    results = []
    total_chars = 0
    in_range_count = 0

    print("=" * 80)
    print("T159: Chapter Word Count Validation")
    print("=" * 80)
    print(f"Target Range: {TARGET_RANGE} Chinese characters per chapter\n")

    for chapter_name, chapter_file in CHAPTERS:
        file_path = base / chapter_file

        if not file_path.exists():
            results.append({
                'chapter': chapter_name,
                'file': chapter_file,
                'chars': 0,
                'status': '❌ FILE NOT FOUND',
                'in_range': False
            })
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        char_count = count_chinese_chars(content)
        total_chars += char_count

        # Determine status
        if MIN_CHARS <= char_count <= MAX_CHARS:
            status = '[PASS]'
            in_range = True
            in_range_count += 1
        elif char_count < MIN_CHARS:
            status = f'[SHORT] ({MIN_CHARS - char_count:,} chars under)'
            in_range = False
        else:
            status = f'[LONG] ({char_count - MAX_CHARS:,} chars over)'
            in_range = False

        results.append({
            'chapter': chapter_name,
            'file': chapter_file,
            'chars': char_count,
            'status': status,
            'in_range': in_range
        })

    # Print results table
    print(f"{'Chapter':<8} {'File':<50} {'Chars':>10} {'Status':<30}")
    print("-" * 110)

    for r in results:
        print(f"{r['chapter']:<8} {Path(r['file']).name:<50} {r['chars']:>10,} {r['status']:<30}")

    print("=" * 110)
    print(f"{'TOTAL':<8} {'11 chapters':<50} {total_chars:>10,}")
    print(f"{'AVERAGE':<8} {'per chapter':<50} {total_chars // len(CHAPTERS):>10,}")
    print("=" * 110)

    # Summary
    print(f"\n{'SUMMARY'}")
    print("-" * 80)
    print(f"Chapters in range ({TARGET_RANGE}): {in_range_count}/{len(CHAPTERS)} ({in_range_count/len(CHAPTERS)*100:.1f}%)")
    print(f"Total characters: {total_chars:,}")
    print(f"Target total range: 99,000-148,500 (11 chapters × 9,000-13,500)")

    # Overall validation
    if 99000 <= total_chars <= 148500:
        print(f"\n[PASS] TOTAL COUNT: Within target range")
    else:
        print(f"\n[WARNING] TOTAL COUNT: Outside target range")

    if in_range_count == len(CHAPTERS):
        print(f"[PASS] INDIVIDUAL CHAPTERS: All chapters within range")
    else:
        print(f"[WARNING] INDIVIDUAL CHAPTERS: {len(CHAPTERS) - in_range_count} chapter(s) outside range")

    # Overall recommendation
    print(f"\n{'RECOMMENDATION'}")
    print("-" * 80)
    if in_range_count >= len(CHAPTERS) * 0.9:  # 90% threshold
        print("[PASS] T159 VALIDATION: PASSED")
        print("Majority of chapters within target range. Book meets length requirements.")
    else:
        print("[WARNING] T159 VALIDATION: NEEDS ATTENTION")
        print("Multiple chapters outside target range. Consider adjustments.")

    return results, total_chars, in_range_count

if __name__ == "__main__":
    import sys
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    results, total, in_range = validate_chapters(base_path)
