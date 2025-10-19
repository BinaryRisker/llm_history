# 格式转换设置指南
# Format Conversion Setup Guide

**目的 | Purpose**: 将Markdown书稿转换为PDF、ePub和HTML格式以供发布和分发
**版本 | Version**: 1.0
**创建日期 | Created**: 2025-10-19

---

## 概览 | Overview

本书使用Markdown格式撰写，需要转换为多种格式以满足不同阅读需求：

| 格式 | 用途 | 目标读者 |
|------|------|---------|
| **PDF** | 打印出版、正式分发 | 需要固定排版的读者 |
| **ePub** | 电子阅读器、移动阅读 | Kindle、iPad等设备用户 |
| **HTML** | 在线阅读、网站发布 | Web浏览器用户 |

---

## 工具选择 | Tool Selection

### 推荐工具: Pandoc

**Pandoc** 是功能强大的文档转换工具，支持多种格式互转。

**安装 Pandoc**:
```bash
# Windows (使用Chocolatey)
choco install pandoc

# Or download from https://pandoc.org/installing.html

# 验证安装
pandoc --version
```

**为什么选择Pandoc**:
- ✅ 支持Markdown → PDF/ePub/HTML
- ✅ 处理中文内容良好
- ✅ 支持自定义模板和样式
- ✅ 命令行工具，易于自动化
- ✅ 开源免费

---

## T173: PDF转换设置

### 基础PDF转换

**最简单的转换命令**:
```bash
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.pdf \
  --toc \
  --number-sections \
  --metadata title="大语言模型编年史" \
  --metadata author="[Your Name]" \
  --pdf-engine=xelatex
```

### 中文字体支持

**问题**: 默认LaTeX引擎不支持中文字符

**解决方案**: 使用XeLaTeX引擎 + 中文字体

**安装中文字体支持**:
```bash
# 安装TeX Live (包含XeLaTeX)
# Windows: https://www.tug.org/texlive/windows.html
# 下载并安装texlive-full

# 验证XeLaTeX
xelatex --version
```

**创建PDF配置文件**: `config/pdf-metadata.yaml`

```yaml
---
title: "大语言模型编年史：从Transformer到ChatGPT的AI革命"
title-en: "Chronicle of Large Language Models: The AI Revolution from Transformer to ChatGPT"
author: "[Your Name]"
date: "2025年11月"
lang: zh-CN
documentclass: book
geometry:
  - margin=2.5cm
  - papersize=a5
fontsize: 11pt
mainfont: "Noto Serif CJK SC"  # 中文衬线字体
sansfont: "Noto Sans CJK SC"   # 中文无衬线字体
monofont: "Noto Sans Mono CJK SC"  # 等宽字体
CJKmainfont: "Noto Serif CJK SC"
linestretch: 1.5
toc: true
toc-depth: 2
number-sections: true
colorlinks: true
linkcolor: blue
urlcolor: blue
---
```

**高质量PDF转换命令**:
```bash
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.pdf \
  --metadata-file=config/pdf-metadata.yaml \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  --highlight-style=tango \
  -V geometry:margin=2.5cm \
  -V CJKmainfont="Noto Serif CJK SC"
```

### PDF自定义样式

**创建LaTeX模板**: `config/pdf-template.latex`

```latex
\documentclass[$if(fontsize)$$fontsize$,$endif$]{$documentclass$}

% 中文支持
\usepackage{xeCJK}
\setCJKmainfont{Noto Serif CJK SC}

% 页面布局
\usepackage[margin=2.5cm]{geometry}

% 标题样式
\usepackage{titlesec}
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries}{\chaptertitlename\ \thechapter}{20pt}{\Huge}

% 页眉页脚
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\leftmark}
\fancyhead[LO]{\rightmark}

% 代码高亮
\usepackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single
}

% 超链接
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue]{hyperref}

\begin{document}

$body$

\end{document}
```

**使用自定义模板**:
```bash
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.pdf \
  --template=config/pdf-template.latex \
  --metadata-file=config/pdf-metadata.yaml \
  --pdf-engine=xelatex
```

### 封面页设置

**创建封面文件**: `manuscript/00-frontmatter/cover.md`

```markdown
---
title: |
  大语言模型编年史
  Chronicle of Large Language Models
subtitle: |
  从Transformer到ChatGPT的AI革命
  The AI Revolution from Transformer to ChatGPT
author: "[Your Name]"
date: "2025年11月"
---

\thispagestyle{empty}

\vspace*{\fill}

\begin{center}
\Huge \textbf{大语言模型编年史}

\LARGE Chronicle of Large Language Models

\vspace{1cm}

\Large 从Transformer到ChatGPT的AI革命

\large The AI Revolution from Transformer to ChatGPT

\vspace{2cm}

\normalsize [Your Name] 著

\vspace{1cm}

2025年11月
\end{center}

\vspace*{\fill}

\newpage
```

---

## T174: ePub转换设置

### 基础ePub转换

**ePub格式优势**:
- 可重排布局，适应不同屏幕尺寸
- 支持Kindle、Apple Books、Google Play Books
- 内嵌字体，确保中文显示

**基础转换命令**:
```bash
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.epub \
  --toc \
  --toc-depth=2 \
  --epub-cover-image=assets/cover.jpg \
  --metadata title="大语言模型编年史" \
  --metadata author="[Your Name]" \
  --metadata lang=zh-CN
```

### ePub元数据配置

**创建ePub元数据**: `config/epub-metadata.yaml`

```yaml
---
title: "大语言模型编年史：从Transformer到ChatGPT的AI革命"
creator:
  - role: author
    text: "[Your Name]"
language: zh-CN
rights: "© 2025 [Your Name]. All rights reserved."
publisher: "[Publisher Name or Self-Published]"
date: "2025-11-01"
description: |
  一部全面记录大语言模型发展历史的编年史，从2017年Transformer论文到2025年的ChatGPT时代，
  涵盖技术创新、公司竞争和行业变革的完整故事。
subject:
  - "人工智能"
  - "大语言模型"
  - "ChatGPT"
  - "深度学习"
  - "科技历史"
---
```

**高质量ePub转换**:
```bash
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.epub \
  --metadata-file=config/epub-metadata.yaml \
  --toc \
  --toc-depth=2 \
  --epub-cover-image=assets/cover.jpg \
  --epub-embed-font=fonts/NotoSerifCJKsc-Regular.otf \
  --epub-embed-font=fonts/NotoSerifCJKsc-Bold.otf \
  --css=config/epub-style.css
```

### ePub样式定制

**创建CSS样式**: `config/epub-style.css`

```css
/* ePub样式表 */

body {
  font-family: "Noto Serif CJK SC", serif;
  line-height: 1.8;
  font-size: 1.1em;
  margin: 1em;
}

h1, h2, h3, h4 {
  font-family: "Noto Sans CJK SC", sans-serif;
  color: #2c3e50;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
}

h1 {
  font-size: 2em;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.3em;
}

h2 {
  font-size: 1.6em;
  color: #34495e;
}

code {
  font-family: "Noto Sans Mono CJK SC", monospace;
  background-color: #f4f4f4;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

pre {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1em;
  overflow-x: auto;
}

blockquote {
  border-left: 4px solid #3498db;
  padding-left: 1em;
  margin-left: 0;
  font-style: italic;
  color: #555;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* 表格样式 */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 0.6em;
  text-align: left;
}

th {
  background-color: #3498db;
  color: white;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* 图片 */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
}
```

### ePub封面设计

**封面图片要求**:
- 尺寸：1600×2400 像素（推荐）
- 格式：JPG或PNG
- 文件大小：< 2MB
- 中文标题清晰可读

**生成封面** (使用Canva或Photoshop):
1. 创建1600×2400画布
2. 添加书名、副标题、作者名
3. 添加相关图标（AI、神经网络等）
4. 保存为`assets/cover.jpg`

---

## T175: HTML转换设置

### 基础HTML转换

**HTML格式优势**:
- 在线阅读，无需下载
- 搜索引擎友好
- 支持交互元素（折叠、导航）
- 易于分享和引用

**单页HTML转换**:
```bash
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.html \
  --standalone \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --css=config/html-style.css \
  --metadata title="大语言模型编年史" \
  --metadata author="[Your Name]"
```

### HTML样式定制

**创建HTML CSS**: `config/html-style.css`

```css
/* 现代HTML样式 */

:root {
  --primary-color: #3498db;
  --secondary-color: #2c3e50;
  --background-color: #ffffff;
  --text-color: #333333;
  --code-background: #f8f9fa;
  --border-color: #e1e4e8;
}

body {
  font-family: "Noto Serif CJK SC", "Georgia", serif;
  line-height: 1.8;
  color: var(--text-color);
  background-color: var(--background-color);
  max-width: 900px;
  margin: 0 auto;
  padding: 2em;
  font-size: 18px;
}

/* 标题 */
h1, h2, h3, h4, h5, h6 {
  font-family: "Noto Sans CJK SC", "Arial", sans-serif;
  color: var(--secondary-color);
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

h1 {
  font-size: 2.5em;
  border-bottom: 3px solid var(--primary-color);
  padding-bottom: 0.3em;
}

h2 {
  font-size: 2em;
  color: var(--primary-color);
}

h3 {
  font-size: 1.5em;
}

/* 链接 */
a {
  color: var(--primary-color);
  text-decoration: none;
  border-bottom: 1px dotted var(--primary-color);
  transition: all 0.3s ease;
}

a:hover {
  color: #2980b9;
  border-bottom-style: solid;
}

/* 代码 */
code {
  font-family: "Noto Sans Mono CJK SC", "Consolas", monospace;
  background-color: var(--code-background);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
  border: 1px solid var(--border-color);
}

pre {
  background-color: var(--code-background);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 1.2em;
  overflow-x: auto;
  line-height: 1.5;
}

pre code {
  background: none;
  border: none;
  padding: 0;
}

/* 引用块 */
blockquote {
  border-left: 4px solid var(--primary-color);
  padding-left: 1.5em;
  margin-left: 0;
  font-style: italic;
  color: #555;
  background-color: #f9f9f9;
  padding: 1em 1em 1em 1.5em;
  border-radius: 0 4px 4px 0;
}

/* 表格 */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5em 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

th, td {
  border: 1px solid var(--border-color);
  padding: 0.8em;
  text-align: left;
}

th {
  background-color: var(--primary-color);
  color: white;
  font-weight: 600;
}

tr:nth-child(even) {
  background-color: #f8f9fa;
}

tr:hover {
  background-color: #e9ecef;
}

/* 目录 */
#TOC {
  background-color: #f8f9fa;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5em;
  margin-bottom: 2em;
}

#TOC ul {
  list-style-type: none;
  padding-left: 1em;
}

#TOC > ul {
  padding-left: 0;
}

#TOC a {
  border: none;
  font-weight: 500;
}

/* 图片 */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 2em auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* 页脚 */
footer {
  margin-top: 3em;
  padding-top: 2em;
  border-top: 2px solid var(--border-color);
  text-align: center;
  color: #666;
  font-size: 0.9em;
}

/* 响应式设计 */
@media (max-width: 768px) {
  body {
    padding: 1em;
    font-size: 16px;
  }

  h1 {
    font-size: 2em;
  }

  h2 {
    font-size: 1.6em;
  }
}
```

### 多页HTML站点生成

**使用Pandoc + 自定义脚本生成静态网站**:

创建脚本：`scripts/generate-html-site.sh`

```bash
#!/bin/bash

# 生成HTML静态网站

OUTPUT_DIR="output/html-site"
mkdir -p $OUTPUT_DIR

# 生成每章的单独HTML页面
for chapter in manuscript/0{1..8}-*/chapter-*.md; do
    chapter_name=$(basename "$chapter" .md)
    pandoc "$chapter" \
      -o "$OUTPUT_DIR/$chapter_name.html" \
      --standalone \
      --toc \
      --css=../config/html-style.css \
      --template=config/html-template.html
done

# 生成索引页
cat > $OUTPUT_DIR/index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>大语言模型编年史</title>
    <link rel="stylesheet" href="../config/html-style.css">
</head>
<body>
    <h1>大语言模型编年史</h1>
    <h2>从Transformer到ChatGPT的AI革命</h2>

    <nav>
        <h3>目录</h3>
        <ul>
            <li><a href="chapter-01.html">第1章：Transformer革命</a></li>
            <li><a href="chapter-02.html">第2章：早期应用</a></li>
            <li><a href="chapter-03.html">第3章：规模化扩展</a></li>
            <!-- 继续添加所有章节链接 -->
        </ul>
    </nav>
</body>
</html>
EOF

echo "HTML站点生成完成：$OUTPUT_DIR/"
```

---

## 自动化构建脚本

### 一键生成所有格式

创建：`scripts/build-all-formats.sh`

```bash
#!/bin/bash

# 自动化构建脚本 - 生成PDF, ePub, HTML

set -e  # 遇到错误立即退出

echo "========================================="
echo "大语言模型编年史 - 格式转换"
echo "========================================="
echo ""

# 创建输出目录
mkdir -p output

# 1. 生成PDF
echo "[1/3] 生成PDF..."
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.pdf \
  --metadata-file=config/pdf-metadata.yaml \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  -V CJKmainfont="Noto Serif CJK SC"

echo "✅ PDF生成成功: output/llm-history-chronicle.pdf"
echo ""

# 2. 生成ePub
echo "[2/3] 生成ePub..."
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.epub \
  --metadata-file=config/epub-metadata.yaml \
  --toc \
  --toc-depth=2 \
  --epub-cover-image=assets/cover.jpg \
  --css=config/epub-style.css

echo "✅ ePub生成成功: output/llm-history-chronicle.epub"
echo ""

# 3. 生成HTML
echo "[3/3] 生成HTML..."
pandoc manuscript/**/*.md \
  -o output/llm-history-chronicle.html \
  --standalone \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --css=config/html-style.css

echo "✅ HTML生成成功: output/llm-history-chronicle.html"
echo ""

# 生成文件大小报告
echo "========================================="
echo "生成文件信息："
echo "========================================="
ls -lh output/llm-history-chronicle.* | awk '{print $9, $5}'
echo ""

echo "✅ 所有格式生成完成！"
```

**运行构建**:
```bash
chmod +x scripts/build-all-formats.sh
./scripts/build-all-formats.sh
```

---

## 质量检查清单

### PDF质量检查

- [ ] 中文字符正确显示
- [ ] 目录生成完整
- [ ] 章节编号正确
- [ ] 代码块格式正确
- [ ] 图片清晰显示
- [ ] 页眉页脚正确
- [ ] 超链接可点击
- [ ] 总页数合理（300-450页）

### ePub质量检查

- [ ] 在Kindle Previewer中测试
- [ ] 在Apple Books中测试
- [ ] 封面图片显示正确
- [ ] 目录导航正常
- [ ] 中文字体嵌入成功
- [ ] 章节分页合理
- [ ] 可调整字体大小
- [ ] 代码块不溢出

### HTML质量检查

- [ ] 在Chrome中测试
- [ ] 在Firefox中测试
- [ ] 在Safari中测试
- [ ] 移动端响应式显示
- [ ] 目录锚点跳转正常
- [ ] 代码高亮正确
- [ ] 表格显示完整
- [ ] 打印预览正常

---

## 发布准备

### 文件命名规范

```
llm-history-chronicle-v1.0.pdf
llm-history-chronicle-v1.0.epub
llm-history-chronicle-v1.0.html
```

版本号说明：
- v1.0: 首次正式发布
- v1.1: 小修订（修正错误）
- v2.0: 大改版（新增章节或重大修订）

### 元数据完善

**为所有格式添加完整元数据**:
- 标题（中英文）
- 作者
- 出版日期
- 版权信息
- ISBN（如有）
- 关键词
- 简介

### 分发准备

**PDF**:
- 上传到个人网站
- 分享到GitHub Releases
- 提交到arXiv（如适用）

**ePub**:
- 亚马逊Kindle Direct Publishing
- Apple Books
- Google Play Books
- Kobo
- Gumroad / Leanpub

**HTML**:
- GitHub Pages托管
- 个人域名部署
- Netlify / Vercel部署

---

## 常见问题 | Troubleshooting

### 问题1：中文显示为方框

**原因**: 缺少中文字体或字体未正确指定

**解决**:
```bash
# 下载并安装Noto字体
# https://fonts.google.com/noto/specimen/Noto+Serif+SC

# 在Pandoc命令中指定字体
-V CJKmainfont="Noto Serif CJK SC"
```

### 问题2：PDF生成失败

**原因**: 未安装TeX Live或XeLaTeX

**解决**:
```bash
# 下载安装TeX Live
# Windows: https://www.tug.org/texlive/windows.html

# 验证安装
xelatex --version
```

### 问题3：ePub在Kindle上显示异常

**原因**: Kindle对某些CSS属性支持有限

**解决**:
- 简化CSS，避免复杂样式
- 使用Kindle Previewer测试
- 必要时使用Kindlegen转换为.mobi

### 问题4：HTML文件过大

**原因**: 单页HTML包含全部内容

**解决**:
- 生成多页HTML站点
- 压缩图片
- 使用外部CSS而非内联

---

## 时间估算

**T173 (PDF设置)**: 3-4小时
**T174 (ePub设置)**: 3-4小时
**T175 (HTML设置)**: 2-3小时
**测试和调试**: 4-6小时

**总计**: 12-17小时

---

## 成功标准

✅ **PDF**: 正确显示中文，总页数300-450页，可打印
✅ **ePub**: 在主流阅读器测试通过，字体嵌入成功
✅ **HTML**: 响应式设计，支持主流浏览器
✅ **自动化**: 一键构建脚本正常运行
✅ **质量**: 所有格式通过质量检查清单

---

**本指南确保书稿可转换为多种专业级发布格式。**

**This guide ensures the manuscript can be converted to multiple professional publication formats.**
