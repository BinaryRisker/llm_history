#!/usr/bin/env python3
"""
Consistency Validation Script (T154-T158)

Validates:
- Narrative voice consistency (T154)
- Tone consistency per constitution (T155)
- Chapter structure consistency (T156)
- Terminology consistency (T157)
- Term usage patterns (T158)
"""

import re
from pathlib import Path
from collections import defaultdict, Counter

def get_chapter_files():
    """Get all main chapter files (exclude frontmatter and backmatter)"""
    manuscript_dir = Path("D:/code/github/llm_history/manuscript")

    chapters = []
    for pattern in [
        "01-foundation/*.md",
        "02-gpt-era/*.md",
        "03-alignment/*.md",
        "04-chatgpt-revolution/*.md",
        "05-global-race-2023/*.md",
        "06-chinese-ai/*.md",
        "07-multimodal-era/*.md",
        "08-present/*.md",
    ]:
        for filepath in manuscript_dir.glob(pattern):
            if filepath.stem != "chapter-template":
                chapters.append(filepath)

    return sorted(chapters)

def check_chapter_structure(filepath):
    """T156: Validate chapter structure consistency"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = {
        "filename": filepath.name,
        "has_frontmatter": bool(re.search(r'^---\n.*?\n---', content, re.DOTALL | re.MULTILINE)),
        "has_intro": "引言" in content or "引言 (" in content,
        "has_summary": "小结" in content or "小结 (" in content,
        "has_key_takeaways": "本章要点" in content or "要点 (" in content,
        "has_related_resources": "相关资源" in content,
        "has_glossary_link": "术语表" in content and "glossary.md" in content,
    }

    return results

def check_terminology_patterns(filepath):
    """T157, T158: Check terminology consistency"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count different terms for language model
    llm_variants = {
        "大语言模型": len(re.findall(r'大语言模型', content)),
        "语言模型": len(re.findall(r'(?<!大)语言模型', content)),
        "LLM": len(re.findall(r'\bLLM\b', content)),
        "大模型": len(re.findall(r'大模型', content)),
    }

    # Check for other terminology variations
    transformer_variants = {
        "Transformer": len(re.findall(r'\bTransformer\b', content)),
        "transformer": len(re.findall(r'\btransformer\b', content)),
        "Transformer架构": len(re.findall(r'Transformer架构', content)),
    }

    return {
        "filename": filepath.name,
        "llm_variants": llm_variants,
        "transformer_variants": transformer_variants,
    }

def check_narrative_voice(filepath):
    """T154, T155: Check narrative voice and tone"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for marketing language (should avoid)
    marketing_terms = [
        "blazingly fast", "blazing fast", "革命性的突破",
        "100% secure", "absolutely", "magnificent", "完美无缺",
        "史无前例", "空前绝后",
    ]

    found_marketing = []
    for term in marketing_terms:
        if term in content.lower() or term in content:
            count = content.lower().count(term.lower())
            found_marketing.append((term, count))

    # Check tone markers (should have balance)
    professional_markers = {
        "研究表明": len(re.findall(r'研究表明', content)),
        "数据显示": len(re.findall(r'数据显示', content)),
        "根据": len(re.findall(r'根据', content)),
        "据": len(re.findall(r'据.*报告', content)),
    }

    engaging_markers = {
        "有趣的是": len(re.findall(r'有趣的是', content)),
        "值得注意的是": len(re.findall(r'值得注意的是', content)),
        "令人惊讶": len(re.findall(r'令人惊讶', content)),
        "想象一下": len(re.findall(r'想象一下', content)),
    }

    return {
        "filename": filepath.name,
        "marketing_language": found_marketing,
        "professional_markers": professional_markers,
        "engaging_markers": engaging_markers,
        "total_professional": sum(professional_markers.values()),
        "total_engaging": sum(engaging_markers.values()),
    }

def main():
    print("=" * 80)
    print("CONSISTENCY VALIDATION REPORT (T154-T158)")
    print("=" * 80)
    print()

    chapters = get_chapter_files()
    print(f"Analyzing {len(chapters)} chapters...")
    print()

    # T156: Chapter Structure Consistency
    print("=" * 80)
    print("T156: CHAPTER STRUCTURE CONSISTENCY")
    print("=" * 80)
    print()

    structure_issues = []
    for chapter in chapters:
        result = check_chapter_structure(chapter)

        missing = []
        if not result["has_frontmatter"]:
            missing.append("Frontmatter")
        if not result["has_intro"]:
            missing.append("引言")
        if not result["has_summary"]:
            missing.append("小结")
        if not result["has_key_takeaways"]:
            missing.append("要点")
        if not result["has_related_resources"]:
            missing.append("相关资源")
        if not result["has_glossary_link"]:
            missing.append("术语表链接")

        if missing:
            structure_issues.append((result["filename"], missing))
            print(f"[ISSUE] {result['filename']}")
            print(f"  Missing: {', '.join(missing)}")
        else:
            print(f"[OK] {result['filename']} - Complete structure")

    print()
    if structure_issues:
        print(f"Structure Issues: {len(structure_issues)} chapters need attention")
    else:
        print("[PASS] All chapters have consistent structure")

    # T157, T158: Terminology Consistency
    print()
    print("=" * 80)
    print("T157-T158: TERMINOLOGY CONSISTENCY")
    print("=" * 80)
    print()

    llm_term_usage = defaultdict(int)
    transformer_term_usage = defaultdict(int)

    for chapter in chapters:
        result = check_terminology_patterns(chapter)

        # Aggregate counts
        for term, count in result["llm_variants"].items():
            llm_term_usage[term] += count
        for term, count in result["transformer_variants"].items():
            transformer_term_usage[term] += count

    print("LLM Terminology Usage Across All Chapters:")
    for term, count in sorted(llm_term_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {term}: {count} occurrences")

    print()
    print("Transformer Terminology Usage:")
    for term, count in sorted(transformer_term_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {term}: {count} occurrences")

    print()
    print("Analysis:")
    if llm_term_usage["LLM"] > llm_term_usage["大语言模型"]:
        print("  [WARNING] More English 'LLM' than Chinese '大语言模型' - consider consistency")
    elif llm_term_usage["大语言模型"] > llm_term_usage["LLM"] * 2:
        print("  [PASS] Chinese-first principle maintained for '大语言模型'")
    else:
        print("  ~ Balanced usage of '大语言模型' and 'LLM'")

    # T154-T155: Narrative Voice and Tone
    print()
    print("=" * 80)
    print("T154-T155: NARRATIVE VOICE AND TONE CONSISTENCY")
    print("=" * 80)
    print()

    marketing_violations = []
    tone_imbalance = []

    for chapter in chapters:
        result = check_narrative_voice(chapter)

        if result["marketing_language"]:
            marketing_violations.append((result["filename"], result["marketing_language"]))

        # Check balance (should have some professional AND some engaging)
        total_prof = result["total_professional"]
        total_eng = result["total_engaging"]

        if total_prof == 0:
            tone_imbalance.append((result["filename"], "No professional markers"))
        elif total_eng == 0:
            tone_imbalance.append((result["filename"], "No engaging markers"))
        elif total_prof > total_eng * 5:
            tone_imbalance.append((result["filename"], "Too formal (5:1 ratio)"))

        # Print summary
        print(f"{result['filename']}:")
        print(f"  Professional markers: {total_prof}")
        print(f"  Engaging markers: {total_eng}")
        if result["marketing_language"]:
            print(f"  [WARNING] Marketing language: {result['marketing_language']}")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    if marketing_violations:
        print(f"[WARNING] Marketing Language Issues: {len(marketing_violations)} chapters")
        for filename, violations in marketing_violations:
            print(f"  - {filename}: {violations}")
        print()

    if tone_imbalance:
        print(f"[WARNING] Tone Balance Issues: {len(tone_imbalance)} chapters")
        for filename, issue in tone_imbalance:
            print(f"  - {filename}: {issue}")
        print()

    if not marketing_violations and not tone_imbalance:
        print("[PASS] All chapters maintain consistent professional yet engaging tone")
        print()

    print("OVERALL ASSESSMENT:")
    print(f"  Structure Issues: {len(structure_issues)}")
    print(f"  Marketing Language: {len(marketing_violations)}")
    print(f"  Tone Imbalance: {len(tone_imbalance)}")
    print()

    if structure_issues == 0 and not marketing_violations and not tone_imbalance:
        print("[PASS] EXCELLENT: Excellent consistency across all dimensions")
    elif len(structure_issues) + len(marketing_violations) + len(tone_imbalance) <= 3:
        print("[PASS] GOOD: Minor issues, overall good consistency")
    else:
        print("[WARNING] NEEDS ATTENTION: Multiple consistency issues detected")

    print()
    print("=" * 80)
    print("Report complete. See details above for specific issues.")
    print("=" * 80)

if __name__ == "__main__":
    main()
