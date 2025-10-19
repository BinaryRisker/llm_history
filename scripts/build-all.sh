#!/bin/bash

# 生成所有格式的自动化脚本
# Build All Formats - Bash Script
# 修复版本：使用正确的章节顺序

set -e  # 遇到错误立即退出

echo "========================================="
echo "大语言模型编年史 - 格式转换"
echo "LLM History Chronicle - Format Conversion"
echo "========================================="
echo ""

# 检查 Pandoc 是否安装
if ! command -v pandoc &> /dev/null; then
    echo "❌ 错误: Pandoc 未安装"
    echo "请从 https://pandoc.org/installing.html 下载安装"
    exit 1
fi

echo "✅ Pandoc 已安装: $(pandoc --version | head -1)"

# 创建输出目录
mkdir -p output

# 正确的章节顺序（按时间线和逻辑顺序）
MD_FILES=(
    # 前言
    "manuscript/00-frontmatter/preface.md"
    "manuscript/00-frontmatter/reading-guide.md"
    "manuscript/00-frontmatter/acknowledgments.md"

    # 第1章：Transformer革命 (2017)
    "manuscript/01-foundation/transformer-revolution.md"

    # 第2章：预训练范式 (2018)
    "manuscript/01-foundation/early-applications.md"

    # 第3章：规模化探索 (2019-2020)
    "manuscript/02-gpt-era/scaling-up.md"

    # 第4章：Google战略回应 (2019-2022)
    "manuscript/02-gpt-era/google-response.md"

    # 第5章：RLHF与ChatGPT (2021-2022)
    "manuscript/03-alignment/rlhf-chatgpt.md"

    # 第6章：ChatGPT发布 (2022-11)
    "manuscript/04-chatgpt-revolution/chatgpt-launch.md"

    # 第7章：2023 AI竞赛
    "manuscript/05-global-race-2023/ai-race-2023.md"

    # 第8章：Meta开源战略
    "manuscript/05-global-race-2023/meta-llama.md"

    # 第9章：中国AI发展
    "manuscript/06-chinese-ai/chinese-development.md"

    # 第10章：多模态时代 (2024)
    "manuscript/07-multimodal-era/2024-breakthroughs.md"

    # 第11章：2025现状
    "manuscript/08-present/2025-present.md"

    # 附录
    "manuscript/99-backmatter/glossary.md"
    "manuscript/99-backmatter/references.md"
    "manuscript/99-backmatter/index.md"
)

echo "📚 包含章节数: ${#MD_FILES[@]}"
echo ""

# 1. 生成 HTML
echo ""
echo "[1/3] 生成 HTML..."
pandoc "${MD_FILES[@]}" \
  -o output/llm-history-chronicle.html \
  --standalone \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --css=config/html-style.css \
  --metadata title="大语言模型编年史" \
  --metadata author="AI History Chronicler"

if [ -f "output/llm-history-chronicle.html" ]; then
    HTML_SIZE=$(du -h output/llm-history-chronicle.html | cut -f1)
    echo "✅ HTML 生成成功: output/llm-history-chronicle.html ($HTML_SIZE)"
else
    echo "❌ HTML 生成失败"
fi

# 2. 生成 ePub
echo ""
echo "[2/3] 生成 ePub..."
pandoc "${MD_FILES[@]}" \
  -o output/llm-history-chronicle.epub \
  --metadata-file=config/epub-metadata.yaml \
  --toc \
  --toc-depth=2 \
  --css=config/epub-style.css

if [ -f "output/llm-history-chronicle.epub" ]; then
    EPUB_SIZE=$(du -h output/llm-history-chronicle.epub | cut -f1)
    echo "✅ ePub 生成成功: output/llm-history-chronicle.epub ($EPUB_SIZE)"
else
    echo "❌ ePub 生成失败"
fi

# 3. 生成 PDF（如果有 XeLaTeX）
echo ""
echo "[3/3] 生成 PDF..."

if command -v xelatex &> /dev/null; then
    pandoc "${MD_FILES[@]}" \
      -o output/llm-history-chronicle.pdf \
      --metadata-file=config/pdf-metadata.yaml \
      --pdf-engine=xelatex \
      --toc \
      --number-sections \
      -V CJKmainfont="Noto Serif CJK SC"

    if [ -f "output/llm-history-chronicle.pdf" ]; then
        PDF_SIZE=$(du -h output/llm-history-chronicle.pdf | cut -f1)
        echo "✅ PDF 生成成功: output/llm-history-chronicle.pdf ($PDF_SIZE)"
    else
        echo "❌ PDF 生成失败"
    fi
else
    echo "⚠️  XeLaTeX 未安装，跳过 PDF 生成"
    echo "   安装说明: https://www.tug.org/texlive/"
fi

# 显示生成文件信息
echo ""
echo "========================================="
echo "生成文件信息:"
echo "========================================="
ls -lh output/llm-history-chronicle.* 2>/dev/null || echo "没有找到生成的文件"

echo ""
echo "✅ 格式转换完成！"
echo "✅ 章节顺序已修复（按时间线正确排序）"
echo "查看详细报告: output/FORMAT_CONVERSION_REPORT.md"
