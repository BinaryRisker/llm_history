---
concept_id: few-shot-learning
concept_name_zh: 少样本学习
concept_name_en: Few-Shot Learning
category: capability
difficulty: intermediate
introduced: 2020
paper: "Language Models are Few-Shot Learners (Brown et al., 2020)"
related_concepts: [in-context-learning, prompting, zero-shot, meta-learning, gpt-3]
---

# 少样本学习 (Few-Shot Learning)

## 什么是少样本学习？

**少样本学习 (Few-Shot Learning)** 是指AI模型仅通过极少量示例（通常2-10个）就能学会新任务的能力，无需重新训练或微调。

**核心思想**: 像人类一样，"看几个例子就明白"。

**革命性意义**: 打破了传统机器学习"数据饥渴"的困境。

### 类比理解

想象教小孩识别新事物：

**传统机器学习 (需要大量样本)**:
```
目标: 识别长颈鹿

方法: 展示10,000张长颈鹿照片
训练: 反复学习数天
结果: 终于学会

问题:
- 需要大量标注数据
- 训练耗时
- 每个新动物都要重复这个过程
```

**人类学习 (少样本)**:
```
目标: 识别长颈鹿

方法:
大人: "看，这是长颈鹿 🦒"
展示: 2-3张照片

小孩: "哦，长脖子，有斑点的！"
结果: 立即理解，终身记住

优势:
- 只需几个例子
- 理解核心特征
- 泛化能力强
```

**Few-Shot Learning (AI模仿人类)**:
```
目标: 学会情感分类

方法: 给模型展示3个例子
"This movie is great! → Positive"
"This movie is terrible! → Negative"
"I loved this film! → Positive"

新输入: "I hated this movie!"
模型: → Negative ✅

优势: 无需重新训练，立即生效
```

### 实际例子

**GPT-3的Few-Shot能力**:

```
任务: 英译中翻译

Prompt (提示):
"""
sea otter → 海獭
peppermint → 薄荷
plush giraffes → 长毛绒长颈鹿
cheese →
"""

GPT-3输出: "奶酪" ✅

机制:
- 给出3个示例 (Few-Shot)
- 模型理解任务是"英译中"
- 无需任何训练，直接翻译

对比:
传统方法需要: 百万翻译对 + 数天训练
Few-Shot: 3个示例 + 0训练
```

**代码生成示例**:
```
Prompt:
"""
# 计算列表总和
def sum_list(lst):
    return sum(lst)

# 找到列表最大值
def max_list(lst):
    return max(lst)

# 反转字符串
def reverse_string(s):
"""

GPT-3补全:
    return s[::-1]

理解: 从2个示例学会了函数定义模式
```

---

## 为什么重要？为什么革命性？

### 传统机器学习的困境

**问题1: 数据饥渴**
```
监督学习需求:
- 图像分类: 10,000+ 标注图片
- 文本分类: 50,000+ 标注文本
- 机器翻译: 1,000,000+ 句对

瓶颈:
- 标注成本高昂 ($0.1-10/样本)
- 领域专家稀缺 (医疗、法律)
- 小众任务无法获得足够数据
```

**问题2: 任务特化**
```
传统模型:
每个任务训练一个专门模型

问题:
新任务 = 重新收集数据 + 重新训练
→ 开发周期长（周到月）
→ 成本高
→ 无法快速适应
```

### Few-Shot Learning的突破

**1. 数据效率革命**

```
传统:
情感分类 → 需要10,000标注样本

Few-Shot (GPT-3):
情感分类 → 需要3-10示例
→ 数据需求减少1000倍！

成本对比:
传统: $10,000 (标注) + $1,000 (训练)
Few-Shot: $0 (无标注) + $0 (无训练)
```

**实证结果** (GPT-3论文):
| 任务 | 传统监督 | Few-Shot GPT-3 |
|------|---------|---------------|
| TriviaQA | 10K样本 → 68% | 64-shot → 71% |
| SuperGLUE | 全量数据 → 89% | 32-shot → 71% |

**2. 快速任务适配**

```
传统开发周期:
定义任务 → 收集数据 (2周) → 标注 (1周) → 训练 (1天) → 评估
总计: ~3周

Few-Shot周期:
定义任务 → 写3-10个示例 (10分钟) → 测试
总计: ~10分钟

速度提升: 3000倍
```

**3. 长尾任务可行性**

```
传统方法无法处理的任务:
- 小众语言翻译 (缺乏平行语料)
- 特定领域分类 (如医学亚专科)
- 即兴创意任务 (如"用莎士比亚风格写代码注释")

Few-Shot可以:
给几个示例 → 模型理解 → 完成任务
→ 使"无法做"变成"可以做"
```

**4. 通用智能展现**

```
传统AI: "窄AI"
每个任务一个专门模型

Few-Shot AI: "通用AI"雏形
一个模型适应数千种任务

哲学意义:
类似人类智能 - 举一反三能力
→ AGI (通用人工智能) 的重要一步
```

---

## 如何工作？（In-Context Learning）

### 核心机制: 上下文学习

**关键发现**: Few-Shot不是"学习"，而是"推理"

```
传统学习:
更新模型参数 → 固化知识

Few-Shot:
模型参数不变 → 从上下文推断任务
→ 称为"In-Context Learning" (上下文学习)
```

### Few-Shot Prompt结构

**标准格式**:
```
[示例1]: input1 → output1
[示例2]: input2 → output2
...
[示例N]: inputN → outputN
[查询]: input_query →

模型补全: output_query
```

**具体示例 (翻译)**:
```
sea otter → 海獭
peppermint → 薄荷
plush giraffes → 长毛绒长颈鹿

cheese → [模型输出: 奶酪]
```

### N-Shot术语

**0-Shot (Zero-Shot)**: 无示例，只有任务描述
```
Translate English to Chinese:
cheese → [模型输出: 奶酪]
```

**1-Shot (One-Shot)**: 1个示例
```
sea otter → 海獭
cheese → [模型输出: 奶酪]
```

**Few-Shot**: 通常2-10个示例
```
(如上3-shot示例)
```

**Many-Shot**: >10个示例 (通常10-100)
```
研究发现: 通常3-10个示例后性能提升饱和
→ Few-Shot已经足够
```

### 为什么Few-Shot有效？

**理论1: 大规模预训练的涌现能力**
```
小模型 (<1B参数): Few-Shot能力弱
大模型 (>10B参数): Few-Shot能力开始出现
超大模型 (>100B参数): Few-Shot能力强大

GPT-3实验:
GPT-3 Small (125M): Few-Shot几乎无效
GPT-3 Medium (1.3B): Few-Shot开始有效
GPT-3 Large (6.7B): Few-Shot较好
GPT-3 (175B): Few-Shot接近监督学习

结论: Few-Shot是模型规模的涌现能力
```

**理论2: 元学习 (Meta-Learning)**
```
预训练过程隐式学习:
"如何从示例中学习模式"

海量预训练数据中包含无数"示例 → 任务"模式
→ 模型学会识别这种模式
→ 推理时应用这种能力
```

**理论3: 模式匹配**
```
模型在预训练时见过类似模式:

训练数据中:
"...apple is a fruit, banana is a fruit, orange is a..."

推理时识别:
"sea otter → 海獭" 类似于 "English → Chinese"
→ 继续这个模式
```

---

## 历史发展

### 2018年之前: 小规模Few-Shot

**传统Few-Shot Learning**:
- 计算机视觉领域 (图像分类)
- 小规模模型 (<100M参数)
- 专门设计的元学习算法 (MAML, Prototypical Networks)

**局限**: 需要专门训练，泛化性差

### 2018-2019: 预训练模型的雏形

**GPT-1 (2018-06)**:
```
发现: 预训练模型可以zero-shot完成某些任务
例子: 文本生成、简单问答

但: Zero-Shot性能仍远低于监督学习
Few-Shot能力: 几乎没有
```

**GPT-2 (2019-02)**:
```
规模: 1.5B参数 (比GPT-1大10倍)

发现: Zero-Shot能力显著提升
- 无监督翻译
- 阅读理解
- 文本摘要

Few-Shot: 开始出现，但不稳定
→ "Zero-Shot是未来"的信念
```

### 2020年5月: 🔴 GPT-3定义Few-Shot时代

**GPT-3 (Brown et al., 2020)**:
```
规模: 175B参数 (比GPT-2大116倍)

革命性发现: Few-Shot性能接近甚至超越监督学习！

核心贡献:
1. 系统研究0-shot, 1-shot, few-shot性能
2. 证明: 示例数量 ↑ → 性能 ↑ (符合规律)
3. 某些任务: Few-Shot > Fine-tuning

论文标题: "Language Models are Few-Shot Learners"
→ 定义新范式
```

**GPT-3实证结果**:
```
TriviaQA (问答):
Few-Shot (64示例): 71.2%
Fine-tuned SOTA: 68.0%
→ Few-Shot首次超越微调！

SuperGLUE (综合任务):
Few-Shot: 71.8%
微调基线: 89.8%
→ 仍有差距，但已接近

意义: 证明Few-Shot可行，不只是玩具
```

### 2020-2022: Few-Shot成为标准能力

**GPT-3 API (2020-06)**:
- 开发者广泛使用Few-Shot
- Prompt Engineering兴起
- Few-Shot成为主流应用方式

**PaLM (Google, 2022-04)**:
- 540B参数
- Few-Shot能力进一步提升
- Chain-of-Thought Few-Shot推理

**思维链 (Chain-of-Thought, CoT)**:
```
标准Few-Shot:
Q: 15个苹果，吃掉5个，剩几个？
A: 10个

CoT Few-Shot:
Q: 15个苹果，吃掉5个，剩几个？
A: 让我想想，15 - 5 = 10。所以剩10个。

发现: 展示"思考过程"的示例 → 性能大幅提升
复杂推理准确率: 20% → 60%
```

### 2022-至今: Few-Shot与其他范式融合

**ChatGPT (2022-11)**:
- RLHF + Few-Shot
- 用户对话中的Few-Shot
- 实时学习用户偏好 (会话内Few-Shot)

**GPT-4 (2023-03)**:
- 更强Few-Shot能力
- 多模态Few-Shot (图像+文本示例)

**Claude, Gemini**:
- 所有主流LLM支持Few-Shot
- Few-Shot成为标准交互方式

---

## Few-Shot的优势与局限

### ✅ 优势

1. **数据效率**: 减少数据需求1000倍
2. **零训练成本**: 无需GPU训练，立即可用
3. **快速迭代**: 10分钟完成任务适配
4. **长尾任务**: 使小众任务可行
5. **通用智能**: 接近人类学习方式

### ⚠️ 局限

1. **性能上限**:
   ```
   Few-Shot: 70-80%准确率
   Fine-tuning: 85-95%准确率
   → 关键任务仍需微调
   ```

2. **示例依赖**:
   ```
   示例质量 → 直接影响性能
   - 示例不当 → 性能大幅下降
   - 示例选择是技巧，需要经验
   ```

3. **上下文长度限制**:
   ```
   GPT-3: 4K tokens上下文
   → 能放的示例数量有限 (~20个)
   → 复杂任务可能示例不够
   ```

4. **不稳定性**:
   ```
   示例顺序、措辞变化 → 性能波动
   同样内容，不同表述 → 结果不同
   → 需要Prompt Engineering技巧
   ```

5. **知识局限**:
   ```
   Few-Shot无法学习新知识
   只能重新组合已有知识
   → 专业领域仍需微调
   ```

---

## Few-Shot vs 其他范式

| 范式 | 数据需求 | 训练成本 | 性能 | 适用场景 |
|------|---------|---------|------|---------|
| **从零训练** | 10K-1M | 天-周 | 最高 | 大规模任务 |
| **Fine-tuning** | 1K-10K | 小时-天 | 高 | 特定任务优化 |
| **Few-Shot** | 2-20 | 零 | 中-高 | 快速原型,长尾任务 |
| **Zero-Shot** | 0 | 零 | 中 | 探索性任务 |

**选择建议**:
```
关键生产任务 → Fine-tuning
快速验证 → Few-Shot
探索新任务 → Zero-Shot
资源充足且数据多 → 从零训练
```

---

## Prompt Engineering技巧

### 技巧1: 示例选择

**质量 > 数量**:
```
3个好示例 > 10个平庸示例

好示例特征:
- 覆盖任务核心模式
- 多样性 (不要太相似)
- 清晰明确
```

### 技巧2: 示例格式

**一致性很重要**:
```
好:
Q: xxx
A: yyy

Q: xxx
A: yyy

差:
Q: xxx
Answer: yyy

Question: xxx
A: yyy
→ 格式不一致导致性能下降
```

### 技巧3: 任务描述

**清晰指令 + 示例**:
```
Translate English to Chinese:

sea otter → 海獭
peppermint → 薄荷
cheese →

比单纯示例效果更好
```

### 技巧4: Chain-of-Thought

**复杂任务展示思考过程**:
```
Q: 鸡蛋12个装一盒，买了5盒，吃掉8个，剩多少？
A: 5盒 = 5 × 12 = 60个。吃掉8个，60 - 8 = 52个。
答案: 52个。

(展示推理过程 → 模型学会推理)
```

---

## 相关概念

1. **In-Context Learning (上下文学习)**: Few-Shot的机制
2. **Prompting (提示工程)**: Few-Shot的应用技巧
3. **Zero-Shot Learning**: 0示例的特例
4. **Meta-Learning (元学习)**: Few-Shot的理论基础
5. **Chain-of-Thought**: Few-Shot推理增强
6. **Instruction Tuning**: 与Few-Shot互补的方法

---

## 参考资料

**核心论文**:
- **[brown2020]** Brown, T., et al. (2020). Language Models are Few-Shot Learners. https://arxiv.org/abs/2005.14165 (GPT-3)

**Few-Shot增强**:
- Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. https://arxiv.org/abs/2201.11903
- Kojima, T., et al. (2022). Large Language Models are Zero-Shot Reasoners. https://arxiv.org/abs/2205.11916

**理论研究**:
- Min, S., et al. (2022). Rethinking the Role of Demonstrations: What Makes In-Context Learning Work? https://arxiv.org/abs/2202.12837

---

**概念卡片版本**: 1.0
**创建日期**: 2025-10-17
**最后更新**: 2025-10-17
**维护者**: LLM History Chronicle Project
