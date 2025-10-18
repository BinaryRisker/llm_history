---
concept_id: multi-head-attention
concept_name_zh: 多头注意力机制
concept_name_en: Multi-Head Attention
category: architecture
difficulty: intermediate
introduced: 2017
paper: "Attention is All You Need (Vaswani et al., 2017)"
related_concepts: [self-attention, transformer, attention-mechanism, parallel-computation]
---

# 多头注意力机制 (Multi-Head Attention)

## 什么是多头注意力？

**多头注意力 (Multi-Head Attention)** 是Self-Attention的增强版，通过**多个并行的注意力"视角"**同时关注不同方面的信息。

**核心思想**: 一个人看问题可能片面，多个专家从不同角度看更全面。

### 类比理解

想象你在评估一篇文章的质量：

**单头注意力 (Self-Attention)**:
```
一个评委从一个角度评价:
- 只看语法正确性
问题: 忽略了内容深度、逻辑连贯、文采等方面
```

**多头注意力 (Multi-Head Attention)**:
```
8个评委从不同角度同时评价:
- 评委1: 语法正确性
- 评委2: 逻辑连贯性
- 评委3: 内容深度
- 评委4: 文采修辞
- 评委5: 论据充分性
- 评委6: 结构完整性
- 评委7: 创新性
- 评委8: 实用价值

最终得分: 综合所有评委意见
结果: 更全面、更准确的评价
```

### 实际例子

**句子**: "The animal didn't cross the street because it was too tired."

**单头注意力**:
- 只能从一个角度理解"it"指代谁
- 可能只关注距离近的词

**多头注意力** (8个头):
```
Head 1: 语法关系
→ "it" 主语 → 动词 "was" → 形容词 "tired"

Head 2: 语义关联
→ "it" 与 "animal" 语义相关度高 (0.9)
→ "it" 与 "street" 语义相关度低 (0.1)

Head 3: 位置距离
→ "it" 距离 "animal" 较远 (10 tokens)
→ "it" 距离 "street" 较近 (4 tokens)

Head 4: 逻辑推理
→ "tired" (疲惫) → 通常修饰生物
→ "animal" 可以疲惫，"street" 不会疲惫

Head 5-8: 其他语言学特征
→ 词性、语态、时态、上下文...

综合判断: "it" = "animal" (置信度 95%)
```

**优势**: 即使某个头错误判断，其他头可以纠正。

---

## 为什么需要多头？为什么重要？

### 1. 表示子空间 (Representation Subspaces)

**核心洞察**: 语言理解需要同时关注多种特征

**问题**: 单个Self-Attention只能学习一种模式

```
例子: "bank" (银行/河岸)

单头注意力:
- 只能学习一种消歧策略
- 比如: 只看名词搭配
  - "bank account" → 金融机构 ✅
  - "river bank" → 可能误判 ❌

多头注意力:
- Head 1: 名词搭配 ("account", "loan")
- Head 2: 动词搭配 ("deposit", "flow")
- Head 3: 形容词修饰 ("financial", "steep")
- Head 4: 上下文主题 (金融 vs 地理)

综合4个头 → 准确消歧
```

### 2. 捕捉多样化关系

**语言中的多维关系**:

```
句子: "昨天下午，李华在图书馆给我打了电话。"

Head 1 - 时间关系:
"昨天下午" → "打了电话" (时间修饰)

Head 2 - 主谓关系:
"李华" → "打了电话" (施事者)

Head 3 - 地点关系:
"在图书馆" → "打了电话" (地点状语)

Head 4 - 动宾关系:
"打了" → "电话" (动词-宾语)

Head 5 - 指代关系:
"我" ← 对话目标

Head 6 - 句式结构:
完整句式识别

Head 7-8 - 其他特征:
语气、情感倾向等
```

**单头**: 只能捕捉其中1-2种关系
**多头**: 同时捕捉所有关系，理解更全面

### 3. 鲁棒性 (Robustness)

**集成学习效应**:

```
类比: 为什么随机森林比单棵决策树好？
→ 多个模型投票，减少单个模型错误影响

多头注意力:
- 8个头同时工作
- 如果Head 2出错，其他7个头可以纠正
- 平均效应降低方差，提升稳定性
```

### 4. 并行计算效率

**关键优势**: 多头不是串行，而是**并行**

```
错误理解: Head 1 → Head 2 → Head 3 → ... (串行)
正确理解: Head 1, 2, 3, ..., 8 同时计算 (并行)

计算时间:
单头: T
8头并行: T (相同！因为GPU并行)

信息量:
单头: 1x
8头: 8x (8倍信息)

效率提升: 8倍信息，同样时间 → 性价比极高
```

---

## 如何工作？（技术机制）

### 多头注意力的三个步骤

#### Step 1: 投影到多个子空间

**核心操作**: 将输入投影成多组 Query, Key, Value

```
原始输入: X (维度 512)

单头注意力:
Q = X · W_Q  (512 → 512)
K = X · W_K  (512 → 512)
V = X · W_V  (512 → 512)

多头注意力 (8 heads):
对于每个 head i:
Q_i = X · W_Q^i  (512 → 64)
K_i = X · W_K^i  (512 → 64)
V_i = X · W_V^i  (512 → 64)

总共: 8 sets of (Q, K, V)
每个head的维度: 512/8 = 64 (降维)
```

**类比**:
```
原图像 (512维特征) → 分解成8个专门视角 (每个64维)
- 视角1: 颜色信息
- 视角2: 纹理信息
- 视角3: 形状信息
- ...
```

#### Step 2: 并行计算各头的注意力

```
对于每个 head i (并行执行):

Attention_i = Softmax(Q_i · K_i^T / √d_k) · V_i

结果:
Attention_1: (seq_len, 64)
Attention_2: (seq_len, 64)
...
Attention_8: (seq_len, 64)
```

**每个头独立计算**:
- 有自己的参数 W_Q^i, W_K^i, W_V^i
- 学习不同的特征模式
- 关注不同的词语关系

#### Step 3: 拼接并融合

```
拼接 (Concatenate):
MultiHead = Concat(Attention_1, ..., Attention_8)
维度: (seq_len, 8 * 64) = (seq_len, 512)

线性变换 (融合):
Output = MultiHead · W_O
维度: (seq_len, 512) → (seq_len, 512)
```

**融合作用**:
- 整合8个头的信息
- 学习如何组合不同视角
- 恢复原始维度

### 完整流程图

```
输入 X (seq_len, 512)
        ↓
    [分裂投影]
   ↙  ↓  ↓  ↘
Head1 Head2 ... Head8  (并行)
 (64) (64)    (64)
   ↓   ↓       ↓
 Attn1 Attn2 ... Attn8
   ↓   ↓       ↓
    [拼接融合]
        ↓
  输出 (seq_len, 512)
```

---

## 为什么8个头？（设计选择）

### Transformer原论文的设计

**参数设置**:
- 模型维度: d_model = 512
- 头数: h = 8
- 每头维度: d_k = d_v = 512/8 = 64

**设计权衡**:

```
头数少 (如 2头):
优势: 每头维度大 (256)，表达能力强
劣势: 视角少，多样性不足

头数多 (如 32头):
优势: 视角多，多样性丰富
劣势: 每头维度小 (16)，表达能力弱

8头 = 甜蜜点:
- 足够的多样性
- 足够的表达能力
- 计算效率高 (GPU友好)
```

### 不同模型的选择

| 模型 | 头数 | 模型维度 | 每头维度 | 设计理由 |
|------|------|----------|----------|----------|
| **Transformer Base** | 8 | 512 | 64 | 平衡性能和效率 |
| **BERT Base** | 12 | 768 | 64 | 保持每头64维 |
| **BERT Large** | 16 | 1024 | 64 | 更多视角 |
| **GPT-2** | 12-25 | 768-1600 | 64 | 模型越大头越多 |
| **GPT-3** | 96 | 12288 | 128 | 超大模型，128维/头 |

**趋势**: 模型越大，头数越多，但每头维度保持稳定 (64-128)

---

## 多头注意力学到了什么？

### 实证研究发现

**可视化研究** (Transformer论文附录):

```
Head 1: 学习句法关系
- 主谓关系: 主语 → 动词
- 动宾关系: 动词 → 宾语

Head 2: 学习位置邻近
- 关注相邻词语
- 局部依赖模式

Head 3: 学习远距离依赖
- 跨句子引用
- 长距离指代

Head 4: 学习固定搭配
- 成语、短语
- 常见词组

Head 5: 学习稀有模式
- 低频词关系
- 特殊语法结构

Head 6-8: 混合模式
- 多种特征组合
- 复杂交互
```

### 具体例子分析

**句子**: "The animal didn't cross the street because it was too tired."

**BERTology研究结果**:

```
Layer 5, Head 3:
强烈关注代词解析
→ "it" 指向 "animal" (权重 0.87)

Layer 8, Head 11:
关注因果关系
→ "because" 连接两个子句

Layer 10, Head 2:
关注否定词作用域
→ "didn't" 作用于 "cross"

Layer 12, Head 7:
综合语义理解
→ "tired" 解释 "didn't cross" 的原因
```

**发现**: 不同层的不同头分工明确，层次化理解

---

## 优势与局限

### ✅ 优势

1. **多样性**: 同时捕捉多种语言学特征
2. **鲁棒性**: 多个头投票，减少错误
3. **并行性**: 所有头并行计算，无额外时间成本
4. **可解释性**: 可视化不同头学到的模式

### ⚠️ 局限

1. **参数量**: 相比单头增加参数 (但每头维度降低，总量相当)
2. **计算复杂度**: O(n² · d) 复杂度，与头数无关但与序列长度平方相关
3. **冗余性**: 部分头可能学到相似模式，存在冗余
4. **设计复杂**: 头数、每头维度需要精心设计

---

## 与单头注意力对比

| 特性 | 单头注意力 | 多头注意力 |
|------|-----------|-----------|
| **表示能力** | 单一视角 | 多视角融合 |
| **鲁棒性** | 依赖单一模式 | 多模式互补 |
| **参数量** | d² | h · (d/h)² ≈ d² (相当) |
| **计算时间** | T | T (并行无额外成本) |
| **可解释性** | 单一模式难解释 | 多头可分别解释 |
| **性能** | 基线 | 显著提升 (论文+2-3 BLEU) |

---

## 历史发展与演进

### 2017: 多头注意力诞生

**Transformer论文** (Vaswani et al., 2017):
- 首次提出Multi-Head Attention
- 8 heads, 512 model dim
- 机器翻译任务SOTA

**关键洞察**:
> "Multi-head attention allows the model to jointly attend to information
> from different representation subspaces at different positions."
>
> "多头注意力允许模型从不同位置的不同表示子空间联合关注信息。"

### 2018-2019: 广泛应用

**BERT** (2018-10):
- 12 heads (Base), 16 heads (Large)
- 证明多头在NLU任务的有效性

**GPT-2** (2019-02):
- 12-25 heads (随模型规模)
- 多头在生成任务的成功

**T5** (2019-10):
- 系统研究头数影响
- 发现8-16头是甜蜜点

### 2019-2020: 多头机制优化

**问题**: 多头是否存在冗余？

**Analyzing Multi-Head Self-Attention** (Voita et al., 2019):
- 剪枝研究: 部分头可删除而不影响性能
- 发现: 不同头确实学习不同功能
- 某些头特化于特定任务（位置、句法、稀有词）

**Multi-Query Attention** (Shazeer, 2019):
- 所有头共享 Key 和 Value，只有 Query 独立
- 参数减少，推理加速
- 性能轻微下降

### 2020-至今: 架构变体

**Grouped-Query Attention** (GQA, 2023):
- Multi-Head 和 Multi-Query 的折中
- 头分组共享 K, V
- Llama 2等模型采用

**Multi-Query Transformer**:
- 推理时显著加速
- KV Cache大小减少

**Sparse Multi-Head Attention**:
- 不是所有头都关注所有位置
- 降低O(n²)复杂度

---

## 实际应用

### 1. 机器翻译

**多头的作用**:
```
源语言: "我昨天在图书馆看书"
目标语言: "I read books in the library yesterday"

Head 1: 对齐词语 ("我" → "I")
Head 2: 语序重排 ("昨天" → 句尾)
Head 3: 时态转换 ("看" → "read" 过去时)
Head 4: 介词处理 ("在" → "in")
Head 5-8: 其他语言学特征
```

### 2. 文本理解 (BERT)

**不同层的头的专业化**:
```
低层 (Layer 1-4):
- Head 学习词法和句法
- 词性、依存关系

中层 (Layer 5-8):
- Head 学习语义关系
- 实体识别、共指消解

高层 (Layer 9-12):
- Head 学习任务特定特征
- 情感分类、问答推理
```

### 3. 代码理解

**GitHub Copilot / CodeBERT**:
```
代码: "for i in range(len(arr)):"

Head 1: 语法结构 (for循环)
Head 2: 变量作用域 (i的范围)
Head 3: 函数调用 (range, len)
Head 4: 数据流 (arr的使用)
Head 5: 编程模式识别
```

---

## 相关概念

1. **Self-Attention (自注意力)**: 多头注意力的基础单元
2. **Transformer**: 首次使用多头注意力的架构
3. **Attention Mechanism (注意力机制)**: 更广泛的注意力家族
4. **Representation Subspace (表示子空间)**: 多头学习的理论基础
5. **Multi-Query Attention**: 多头注意力的高效变体
6. **Grouped-Query Attention**: 多头和多查询的折中

---

## 参考资料

**核心论文**:
- **[vaswani2017]** Vaswani, A., et al. (2017). Attention is All You Need. *NeurIPS 2017*. https://arxiv.org/abs/1706.03762

**深入研究**:
- Voita, E., et al. (2019). Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned. https://arxiv.org/abs/1905.09418
- Michel, P., et al. (2019). Are Sixteen Heads Really Better than One? https://arxiv.org/abs/1905.10650
- Shazeer, N. (2019). Fast Transformer Decoding: One Write-Head is All You Need. https://arxiv.org/abs/1911.02150

**可视化工具**:
- BertViz: https://github.com/jessevig/bertviz (可视化BERT的多头注意力)

---

**概念卡片版本**: 1.0
**创建日期**: 2025-10-17
**最后更新**: 2025-10-17
**维护者**: LLM History Chronicle Project
