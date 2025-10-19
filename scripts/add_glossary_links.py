#!/usr/bin/env python3
"""
Add glossary cross-references to all chapter files
"""

import re
from pathlib import Path

# Chapter-specific glossary terms to highlight
chapter_terms = {
    "01-foundation/early-applications.md": "（GPT、BERT、预训练、微调、迁移学习等）",
    "02-gpt-era/scaling-up.md": "（缩放定律、Few-shot Learning、涌现能力、参数量等）",
    "02-gpt-era/google-response.md": "（T5、TPU、Gemini等）",
    "03-alignment/rlhf-chatgpt.md": "（RLHF、指令微调、对齐等）",
    "04-chatgpt-revolution/chatgpt-launch.md": "（ChatGPT、API、提示工程等）",
    "05-global-race-2023/ai-race-2023.md": "（GPT-4、Claude、Constitutional AI、多模态模型等）",
    "05-global-race-2023/meta-llama.md": "（LLaMA、开源模型、MoE等）",
    "06-chinese-ai/chinese-development.md": "（ERNIE、Qwen、百模大战、ChatGLM、混元、豆包等）",
    "07-multimodal-era/2024-breakthroughs.md": "（Agent、Computer Use、DeepSeek、算法优化等）",
    "08-present/2025-present.md": "（GPT-5、Llama 4、AGI、芯片战、Nvidia Blackwell等）",
}

def add_glossary_link(filepath, terms_hint):
    """Add glossary link to a chapter's Related Resources section"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if glossary link already exists
    if '术语表' in content and '99-backmatter/glossary.md' in content:
        print(f"[OK] {filepath.name}: Glossary link already exists")
        return False

    # Find the Related Resources section
    pattern = r'(\*\*相关资源\*\* \(Related Resources\):.*?)(\n\n---|\n\*\*本章要点\*\*)'

    def add_link(match):
        resources_section = match.group(1)
        end_marker = match.group(2)

        # Add glossary link before the end marker
        glossary_line = f"\n- 📖 [术语表](../../99-backmatter/glossary.md) - 本章技术术语详解{terms_hint}"

        return resources_section + glossary_line + end_marker

    new_content = re.sub(pattern, add_link, content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[UPDATED] {filepath.name}: Added glossary link")
        return True
    else:
        print(f"[SKIP] {filepath.name}: Could not find Related Resources section")
        return False

def main():
    manuscript_dir = Path("D:/code/github/llm_history/manuscript")

    print("Adding glossary cross-references to chapters...")
    print("=" * 60)

    updated_count = 0
    for rel_path, terms in chapter_terms.items():
        filepath = manuscript_dir / rel_path
        if filepath.exists():
            if add_glossary_link(filepath, terms):
                updated_count += 1
        else:
            print(f"✗ {rel_path}: File not found")

    print("=" * 60)
    print(f"Updated {updated_count} out of {len(chapter_terms)} chapters")

if __name__ == "__main__":
    main()
