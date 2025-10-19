#!/usr/bin/env python3
"""
Add timeline cross-references to all chapters
"""
import re
import os

# Define chapters and their specific related resources
chapters = {
    "manuscript/04-chatgpt-revolution/chatgpt-launch.md": {
        "resources": [
            "📅 [完整时间线](../../assets/timelines/overall-timeline.md) - ChatGPT革命完整时间线",
            "🏢 [公司对比时间线](../../assets/timelines/company-timelines/comparison.md) - 2023全球AI竞赛",
            "📄 [ChatGPT事件卡片](../../assets/timelines/events/chatgpt-launch-2022.md) - ChatGPT发布详细分析",
            "🏢 [OpenAI组织档案](../../research/organizations/openai.md) - OpenAI产品化战略"
        ]
    },
    "manuscript/05-global-race-2023/ai-race-2023.md": {
        "resources": [
            "📅 [完整时间线](../../assets/timelines/overall-timeline.md) - 2023 AI竞赛完整时间线",
            "🏢 [公司对比时间线](../../assets/timelines/company-timelines/comparison.md) - GPT-4/Claude/Gemini并行发展",
            "📄 [GPT-4事件卡片](../../assets/timelines/events/gpt4-launch-2023.md) - GPT-4详细分析",
            "🏢 [Anthropic组织档案](../../research/organizations/anthropic.md) - Anthropic AI安全理念"
        ]
    },
    "manuscript/05-global-race-2023/meta-llama.md": {
        "resources": [
            "📅 [完整时间线](../../assets/timelines/overall-timeline.md) - Meta开源战略时间线",
            "🏢 [公司对比时间线](../../assets/timelines/company-timelines/comparison.md) - 开源vs闭源竞争",
            "📄 [LLaMA事件卡片](../../assets/timelines/events/llama-release-2023.md) - LLaMA发布与泄露事件",
            "🏢 [Meta组织档案](../../research/organizations/meta.md) - Meta开源AI战略"
        ]
    },
    "manuscript/06-chinese-ai/chinese-development.md": {
        "resources": [
            "📅 [完整时间线](../../assets/timelines/overall-timeline.md) - 中国AI发展完整时间线",
            "🏢 [公司对比时间线](../../assets/timelines/company-timelines/comparison.md) - 中西方AI并行发展",
            "🏢 [百度组织档案](../../research/organizations/baidu.md) - 百度战略转型",
            "🏢 [阿里组织档案](../../research/organizations/alibaba.md) - 阿里开源生态"
        ]
    },
    "manuscript/07-multimodal-era/2024-breakthroughs.md": {
        "resources": [
            "📅 [完整时间线](../../assets/timelines/overall-timeline.md) - 2024多模态突破时间线",
            "🏢 [公司对比时间线](../../assets/timelines/company-timelines/comparison.md) - 2024全球竞争格局"
        ]
    },
    "manuscript/08-present/2025-present.md": {
        "resources": [
            "📅 [完整时间线](../../assets/timelines/overall-timeline.md) - 2025最新发展时间线",
            "🏢 [公司对比时间线](../../assets/timelines/company-timelines/comparison.md) - 当前竞争态势"
        ]
    }
}

def add_references_to_chapter(filepath, resources):
    """Add related resources section before the --- separator after 小结"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has "相关资源"
    if "**相关资源**" in content or "**Related Resources**" in content:
        print(f"[OK] {filepath} already has references, skipping")
        return

    # Find the pattern: 小结 section followed by --- separator
    # We want to insert before the ---
    pattern = r'(## 小结.*?)\n\n---'

    def replacement(match):
        summary_content = match.group(1)
        resources_text = "\n\n**相关资源** (Related Resources):\n"
        for resource in resources:
            resources_text += f"- {resource}\n"
        resources_text += "\n---"
        return summary_content + resources_text

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[OK] Added references to {filepath}")
    else:
        print(f"[ERROR] Pattern not found in {filepath}")

def main():
    print("Adding timeline cross-references to chapters...\n")
    for filepath, config in chapters.items():
        if os.path.exists(filepath):
            add_references_to_chapter(filepath, config["resources"])
        else:
            print(f"[ERROR] File not found: {filepath}")

    print("\n[OK] Done! All references added.")

if __name__ == "__main__":
    main()
