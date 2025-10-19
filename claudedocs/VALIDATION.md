# 验证脚本使用指南

## 批量验证脚本（推荐）

**文件**: `validate_all.py`
**任务**: T161a - 整合T159-T161所有验证

### 基本用法

```bash
# 运行所有验证（完整模式）
python validate_all.py

# 快速摘要模式（仅显示结果，无详细信息）
python validate_all.py --quick

# 仅运行字数统计验证
python validate_all.py --words

# 仅运行引用格式验证
python validate_all.py --citations

# 仅运行交叉引用验证
python validate_all.py --links
```

### 输出说明

脚本会生成：
1. **控制台输出**: 显示每项验证的详细结果
2. **汇总报告**: 保存到 `claudedocs/validation_batch_summary_YYYYMMDD_HHMMSS.txt`

### 验证项目

1. **T159 字数统计**: 验证11个章节中文字符数在9,000-13,500范围内
2. **T160 引用格式**: 验证学术引用格式符合 `(Author, Year)` 标准
3. **T161 交叉引用**: 验证所有markdown链接指向存在的文件

## 单独验证脚本

如需单独运行某项验证：

### 字数统计 (T159)
```bash
python validate_word_counts.py
```
- 统计11个主章节的中文字符数
- 排除YAML frontmatter和markdown语法
- 目标：每章9,000-13,500字符，总计100K-150K

### 引用格式 (T160)
```bash
python validate_citations.py
```
- 检查所有章节的学术引用格式
- 支持格式：`(Author, Year)`, `(Author et al., Year)`, `(Author1 & Author2, Year)`
- 生成详细报告到 `claudedocs/validation_t160_citations.txt`

### 交叉引用 (T161)
```bash
python validate_cross_references.py
```
- 验证所有markdown链接
- 检查内部文件引用、外部URL、本地锚点
- 生成详细报告到 `claudedocs/validation_t161_cross_references.txt`

## 验证结果说明

### 状态标识
- `[PASS]` - 验证通过
- `[WARN]` - 警告（可接受但需注意）
- `[FAIL]` - 验证失败（需要修复）

### 常见警告

**字数统计**:
- 某些章节可能略低于或高于目标范围
- 只要总字符数在100K-150K范围内即可接受

**交叉引用**:
- `index.md` 和 `chapter-template.md` 中的示例链接会显示为断链（属于正常）
- 只需关注实际章节文件中的断链

**引用格式**:
- 多引用连接格式（如 `(A, 2019; B, 2020)`）可能不被识别
- 这是合理的学术格式，可手动确认

## 持续集成建议

建议在以下情况运行验证：
1. 完成章节内容修改后
2. 添加新的交叉引用后
3. 提交代码前（确保质量）
4. Beta测试前的最终检查

## 报告位置

所有验证报告保存在 `claudedocs/` 目录：
- `validation_t159_word_counts.txt` - 字数统计详细报告
- `validation_t160_citations.txt` - 引用格式详细报告
- `validation_t161_cross_references.txt` - 交叉引用详细报告
- `validation_batch_summary_*.txt` - 批量验证汇总报告（带时间戳）
