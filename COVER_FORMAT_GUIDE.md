# 封面格式转换指南

## 问题说明

SVG 格式的封面在不同格式中的兼容性：
- ✅ **HTML**: 完美显示
- ⚠️ **ePub**: 部分阅读器支持
- ⚠️ **PDF**: XeLaTeX 处理 SVG 有限制

## 解决方案：转换为 PNG

### 方法1：使用 Python 脚本（推荐）

1. 安装依赖：
```bash
pip install cairosvg
```

2. 运行转换脚本：
```bash
python scripts/convert-covers-to-png.py
```

3. 更新封面引用：
```bash
# 编辑 manuscript/00-frontmatter/cover.md
# 将 cover-5-complex.svg 改为 cover-5-complex.png

# 编辑 config/epub-metadata.yaml
# 将 cover-5-complex.svg 改为 cover-5-complex.png
```

4. 重新生成：
```bash
.\scripts\build-all.ps1
```

### 方法2：在线转换

1. 访问在线转换工具：
   - https://cloudconvert.com/svg-to-png
   - https://convertio.co/zh/svg-png/

2. 上传封面文件：
   - `assets/images/cover-5-complex.svg`

3. 设置参数：
   - 宽度：1600 像素
   - 高度：自动（保持比例）
   - 质量：最高

4. 下载转换后的 PNG

5. 保存为：
   - `assets/images/cover-5-complex.png`

6. 按照方法1的步骤3-4完成

### 方法3：使用 Inkscape

1. 用 Inkscape 打开 SVG 文件

2. 文件 → 导出 PNG

3. 设置：
   - 宽度：1600 像素
   - DPI：300

4. 导出保存

## 验证封面是否正确包含

### 检查 ePub
```bash
unzip -l output/llm-history-chronicle.epub | grep cover

# 应该看到：
# EPUB/media/cover-5-complex.png  (或 .svg)
# EPUB/text/cover.xhtml
```

### 检查 PDF
```bash
# 打开 PDF，第一页应该是封面
start output/llm-history-chronicle.pdf
```

### 检查 HTML
```bash
# 打开 HTML，顶部应该显示封面
start output/llm-history-chronicle.html
```

## 当前状态

当前使用的是 **SVG 格式**封面：
- HTML: ✅ 正常显示
- ePub: ⚠️ 需要支持 SVG 的阅读器（如 Calibre）
- PDF: ⚠️ 可能无法正确渲染

**建议**：转换为 PNG 格式以获得最佳兼容性。
