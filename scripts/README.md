# Scripts 目录说明

本目录包含LLM History Chronicle项目的所有辅助脚本和验证工具。

## 目录结构

```
scripts/
├── README.md                          # 本文档
├── validate_all.py                    # 🔍 批量验证脚本（推荐使用）
├── validate_citations.py              # 引用格式验证（T160）
├── validate_consistency.py            # 一致性验证（T154-T158）
├── validate_cross_references.py       # 交叉引用验证（T161）
├── validate_word_counts.py            # 字数统计验证（T159）
├── add_citations_helper.py            # 引用添加辅助工具
├── add_glossary_links.py              # 术语表链接生成器（T151）
├── add_timeline_references.py         # 时间线引用添加器
├── extract_citations.py               # 引用提取工具
├── fix-manuscript-structure.ps1       # 文件结构修复（PowerShell）
└── fix-manuscript-structure.sh        # 文件结构修复（Bash）
```

## 主要脚本

### 🔍 批量验证脚本（推荐）

**validate_all.py** - 整合T159-T161所有验证

```bash
# 从项目根目录运行

# 运行所有验证
python scripts/validate_all.py

# 快速摘要模式
python scripts/validate_all.py --quick

# 单项验证
python scripts/validate_all.py --words      # 仅字数统计
python scripts/validate_all.py --citations  # 仅引用格式
python scripts/validate_all.py --links      # 仅交叉引用
```

**输出**：
- 控制台显示验证结果
- 生成汇总报告：`claudedocs/validation_batch_summary_YYYYMMDD_HHMMSS.txt`

详细使用说明见：`claudedocs/VALIDATION.md`

## 验证脚本

### validate_word_counts.py (T159)
**用途**: 验证11个章节的中文字符数

```bash
python scripts/validate_word_counts.py
```

- 统计范围：9,000-13,500字符/章
- 总计目标：100,000-150,000字符
- 排除：YAML frontmatter、markdown语法

### validate_citations.py (T160)
**用途**: 验证学术引用格式

```bash
python scripts/validate_citations.py
```

- 支持格式：`(Author, Year)`, `(Author et al., Year)`
- 检测问题：缺失逗号、错误括号、格式不规范
- 报告输出：`claudedocs/validation_t160_citations.txt`

### validate_cross_references.py (T161)
**用途**: 验证所有markdown链接

```bash
python scripts/validate_cross_references.py
```

- 检查内容：内部文件引用、外部URL、本地锚点
- 报告输出：`claudedocs/validation_t161_cross_references.txt`

### validate_consistency.py (T154-T158)
**用途**: 验证文档一致性

```bash
python scripts/validate_consistency.py
```

- 检查项目：
  - T154: 叙事语气一致性
  - T155: 专业与易懂平衡
  - T156: 章节结构规范
  - T157: 术语一致性
  - T158: 术语使用规范

## 辅助脚本

### add_glossary_links.py (T151)
**用途**: 自动添加术语表交叉引用

```bash
python scripts/add_glossary_links.py
```

- 功能：在所有章节的"相关资源"部分添加术语表链接
- 包含：章节特定术语提示

### add_timeline_references.py
**用途**: 添加时间线引用链接

```bash
python scripts/add_timeline_references.py
```

- 功能：在章节中添加时间线可视化引用

### add_citations_helper.py
**用途**: 辅助添加学术引用

```bash
python scripts/add_citations_helper.py
```

- 功能：帮助格式化和插入引用

### extract_citations.py
**用途**: 从章节中提取现有引用

```bash
python scripts/extract_citations.py
```

- 功能：提取所有引用以便统一管理
- 输出：`extracted_citations.txt`

## 修复脚本

### fix-manuscript-structure.*
**用途**: 修复章节文件结构问题

```bash
# Windows PowerShell
.\scripts\fix-manuscript-structure.ps1

# Unix/Linux/Mac
bash scripts/fix-manuscript-structure.sh
```

- 功能：修复文件命名、路径、结构问题

## 使用建议

### 开发工作流

1. **内容修改后**：
   ```bash
   python scripts/validate_all.py --quick
   ```

2. **提交代码前**：
   ```bash
   python scripts/validate_all.py
   ```

3. **Beta测试前**：
   ```bash
   python scripts/validate_all.py
   python scripts/validate_consistency.py
   ```

### 问题排查

如果验证失败：
1. 查看控制台输出找到具体问题
2. 检查 `claudedocs/validation_*.txt` 详细报告
3. 使用单独验证脚本深入分析

### 性能优化

- 使用 `--quick` 快速检查（无详细输出）
- 使用单项验证针对性检查
- 批量修复问题后再运行完整验证

## 报告位置

所有验证报告保存在 `claudedocs/` 目录：

- `validation_t159_word_counts.txt` - 字数统计详细报告
- `validation_t160_citations.txt` - 引用格式详细报告
- `validation_t161_cross_references.txt` - 交叉引用详细报告
- `validation_t154-t158_consistency.txt` - 一致性验证报告
- `validation_batch_summary_*.txt` - 批量验证汇总（带时间戳）

## 维护说明

### 添加新验证

1. 在 `scripts/` 创建新的 `validate_xxx.py`
2. 遵循现有脚本的输出格式
3. 更新 `validate_all.py` 集成新验证
4. 更新本文档

### 脚本命名规范

- `validate_*.py` - 验证脚本
- `add_*.py` - 内容添加辅助脚本
- `extract_*.py` - 内容提取工具
- `fix_*.py` - 修复工具

## 故障排除

### 编码问题
如果遇到Unicode错误，确保使用UTF-8编码：
```bash
export PYTHONIOENCODING=utf-8  # Unix/Linux/Mac
$env:PYTHONIOENCODING="utf-8"  # Windows PowerShell
```

### 路径问题
所有脚本应从项目根目录运行：
```bash
cd /path/to/llm_history
python scripts/validate_all.py
```

### Python版本
要求Python 3.7+：
```bash
python --version  # 检查版本
```

## 联系方式

如有问题或改进建议，请查看项目文档或提交Issue。
