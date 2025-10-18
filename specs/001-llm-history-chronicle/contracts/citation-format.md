# Citation Format Contract

**Version**: 1.0
**Purpose**: Standardize citation and reference formatting across the book
**Applies To**: All manuscript files, bibliography, and references

---

## Citation Style Overview

**Primary Style**: Informal Author-Year format (适合科普读物 / suitable for popular science)
**Bibliography**: Full references in backmatter with alphabetical ordering
**Language Handling**: Bilingual support for Chinese and English sources

---

## Inline Citations

### Format Rules

**Single Author**:
```markdown
Chinese: (作者姓名, Year)
English: (Lastname, Year)

Examples:
据OpenAI的报告 (Altman, 2023)，GPT-4的训练...
According to OpenAI's report (Altman, 2023), GPT-4 training...
```

**Two Authors**:
```markdown
Chinese: (作者1 & 作者2, Year)
English: (Lastname1 & Lastname2, Year)

Examples:
根据研究 (Brown & Mann, 2020)...
According to research (Brown & Mann, 2020)...
```

**Three or More Authors**:
```markdown
Chinese: (第一作者 et al., Year)
English: (First Author et al., Year)

Examples:
Transformer架构 (Vaswani et al., 2017) 提出了...
The Transformer architecture (Vaswani et al., 2017) proposed...
```

**Corporate/Organization Author**:
```markdown
(Organization Name, Year)

Examples:
OpenAI发布的技术报告 (OpenAI, 2023) 显示...
OpenAI's technical report (OpenAI, 2023) shows...

根据百度研究院的报告 (Baidu Research, 2021)...
According to Baidu Research's report (Baidu Research, 2021)...
```

**Chinese Authors**:
```markdown
Use full Chinese name or pinyin based on source language

Examples:
李彦宏的演讲 (李彦宏, 2019) 中提到...
In Li Yanhong's speech (李彦宏, 2019)...

Or romanized if source is English:
(Li, 2019)
```

### Multiple Citations

**Same Parentheses**:
```markdown
多项研究 (Vaswani et al., 2017; Devlin et al., 2018; Radford et al., 2019) 表明...
Multiple studies (Vaswani et al., 2017; Devlin et al., 2018; Radford et al., 2019) show...
```

### Page Numbers or Sections (Optional)

**When Quoting or Referencing Specific Section**:
```markdown
正如论文所述："attention is all you need" (Vaswani et al., 2017, p. 6)
As stated in the paper: "attention is all you need" (Vaswani et al., 2017, p. 6)
```

---

## Bibliography Format

**Location**: `manuscript/99-backmatter/references.md`

**Organization**:
1. Alphabetical by author lastname (or organization name)
2. Grouped by type (optional): Papers, Articles, Books, Blogs, Interviews
3. Both Chinese and English sources in same list

### Academic Papers

**Format**:
```
Author(s). (Year). Title. Conference/Journal. DOI/URL

Example:
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All You Need. *Advances in Neural Information Processing Systems (NeurIPS) 30*. https://arxiv.org/abs/1706.03762

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *arXiv preprint arXiv:1810.04805*. https://arxiv.org/abs/1810.04805
```

**Chinese Papers**:
```
中文作者. (Year). 论文标题. 会议/期刊. URL

Example:
李彦宏, 王海峰, 吴华. (2019). ERNIE: Enhanced Representation through Knowledge Integration. 《中国人工智能学术年会》. https://arxiv.org/abs/1904.09223
```

### Blog Posts / Articles

**Format**:
```
Author(s). (Year, Month Day). Title. *Blog/Publication Name*. URL

Example:
Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018, June 11). Improving Language Understanding by Generative Pre-Training. *OpenAI Blog*. https://openai.com/research/language-unsupervised

Altman, S. (2023, March 14). GPT-4. *OpenAI Blog*. https://openai.com/research/gpt-4
```

### Company Announcements

**Format**:
```
Company Name. (Year, Month Day). Announcement Title. URL

Example:
OpenAI. (2022, November 30). Introducing ChatGPT. https://openai.com/blog/chatgpt

Google. (2023, February 6). An important next step on our AI journey. https://blog.google/technology/ai/bard-google-ai-search-updates/

百度. (2019, March 16). 百度正式发布ERNIE 1.0. https://...
```

### Books

**Format**:
```
Author(s). (Year). *Book Title* (Edition if applicable). Publisher.

Example:
Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
```

### Interviews / Videos

**Format**:
```
Interviewee Name. (Year, Month Day). Interview/Video Title. *Platform/Publication*. URL

Example:
Hinton, G. (2023, May 1). Geoffrey Hinton on AI's Future. *CBS 60 Minutes*. https://www.youtube.com/watch?v=...

Sam Altman. (2023, March 16). Interview on GPT-4 Development. *Lex Fridman Podcast*. https://...
```

### Tweets / Social Media

**Format**:
```
@Username. (Year, Month Day). Tweet text [Tweet]. Twitter/X. URL

Example:
@sama. (2022, November 30). ChatGPT is now available [Tweet]. Twitter. https://twitter.com/sama/status/...
```

---

## Verification Status Markings

For sources with uncertain credibility or unverified claims, add notation:

### In Text

**Verified Information**:
```markdown
官方发布显示 (OpenAI, 2023) GPT-4拥有...
Official release shows (OpenAI, 2023) GPT-4 has...
```

**Reported/Unverified**:
```markdown
据报道 (TechCrunch, 2023) OpenAI正在开发...
⚠️ 注：此信息未经官方确认
---
Reportedly (TechCrunch, 2023) OpenAI is developing...
⚠️ Note: This information is unverified
```

**Disputed Facts**:
```markdown
关于GPT-4的训练成本存在不同说法：
- 来源A (The Information, 2023) 估计为1亿美元
- 来源B (SemiAnalysis, 2023) 估计为2亿美元
官方未披露确切数字。
---
Training costs for GPT-4 are disputed:
- Source A (The Information, 2023) estimates $100M
- Source B (SemiAnalysis, 2023) estimates $200M
Official figures not disclosed.
```

### In Bibliography

**Verified Academic/Official Sources**: No special marking

**Industry Reports** (may lack peer review):
```
⚠️ SemiAnalysis. (2023, June). GPT-4 Architecture and Cost Analysis. https://...
[Industry report - not peer reviewed]
```

**Unverified Rumors**:
```
⚠️ Anonymous Source. (2023). Claim about [X]. *Tech Forum*.
[Unverified - included for completeness]
```

---

## Special Cases

### ArXiv Preprints

**Format**: Include arXiv ID for tracking
```
Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., & Liu, P. J. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer. *arXiv preprint arXiv:1910.10683*. https://arxiv.org/abs/1910.10683
```

### Technical Reports

**Format**: Include report number if available
```
OpenAI. (2023). GPT-4 Technical Report (Tech. Rep.). https://arxiv.org/abs/2303.08774
```

### Conference Papers

**Format**: Include conference name and year
```
Brown, T., Mann, B., Ryder, N., et al. (2020). Language Models are Few-Shot Learners. *Advances in Neural Information Processing Systems (NeurIPS) 33*. https://arxiv.org/abs/2005.14165
```

### GitHub Repositories

**Format**:
```
Author/Organization. (Year). Repository Name (Version/Release if applicable). GitHub. URL

Example:
Meta AI. (2023). LLaMA: Open and Efficient Foundation Language Models (v2). GitHub. https://github.com/facebookresearch/llama
```

---

## Bibliography Organization Example

```markdown
# References

## Academic Papers

**B**

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Amodei, D. (2020). Language Models are Few-Shot Learners. *Advances in Neural Information Processing Systems (NeurIPS) 33*. https://arxiv.org/abs/2005.14165

**D**

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *arXiv preprint arXiv:1810.04805*. https://arxiv.org/abs/1810.04805

**V**

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All You Need. *Advances in Neural Information Processing Systems (NeurIPS) 30*. https://arxiv.org/abs/1706.03762

## Company Publications & Blogs

**G**

Google. (2023, February 6). An important next step on our AI journey. *Google Blog*. https://blog.google/technology/ai/bard-google-ai-search-updates/

**O**

OpenAI. (2022, November 30). Introducing ChatGPT. *OpenAI Blog*. https://openai.com/blog/chatgpt

OpenAI. (2023). GPT-4 Technical Report. *arXiv preprint arXiv:2303.08774*. https://arxiv.org/abs/2303.08774

## Chinese Sources

**李 (Li)**

李彦宏. (2019). ERNIE技术白皮书. 百度研究院. https://...

**百度 (Baidu)**

百度. (2019, March 16). 百度正式发布ERNIE 1.0. https://...

## Interviews & Media

Altman, S. (2023, March 16). Interview on GPT-4 Development. *Lex Fridman Podcast*. https://...

Hinton, G. (2023, May 1). Geoffrey Hinton on AI's Future. *CBS 60 Minutes*. https://www.youtube.com/watch?v=...
```

---

## Tools & Automation

### Citation Validation

**Manual Checklist**:
- [ ] All inline citations have corresponding bibliography entry
- [ ] All bibliography entries are cited at least once
- [ ] Author names consistent across all mentions
- [ ] Years match between inline and bibliography
- [ ] URLs accessible (check quarterly)

**Automated Checks** (scripts):
```bash
# Find all citations in manuscript
grep -r "\([A-Z][a-z]* et al\., [0-9]\{4\}\)" manuscript/

# Find bibliography entries
grep "^[A-Z]" manuscript/99-backmatter/references.md

# Cross-reference citations with bibliography
# [Custom script needed]
```

### Citation Count Tracking

Target: 80%+ of major claims cited (SC-008)

**Script Output**:
```
Chapter 1: 45 claims, 38 citations (84% ✅)
Chapter 2: 52 claims, 40 citations (77% ⚠️)
...
Total: 450 claims, 380 citations (84% ✅)
```

---

## Common Mistakes to Avoid

❌ **Inconsistent author names**:
```
(Vaswani, 2017) vs (Vaswani et al., 2017)
[Use "et al." if 3+ authors]
```

❌ **Missing citations for major claims**:
```
GPT-3拥有1750亿参数。[Needs citation]
GPT-3 has 175 billion parameters. [Needs citation]

✅ Correct:
GPT-3拥有1750亿参数 (Brown et al., 2020)。
GPT-3 has 175 billion parameters (Brown et al., 2020).
```

❌ **Broken URLs**:
```
Check all URLs quarterly, update if moved
```

❌ **Citation without bibliography entry**:
```
(Smith, 2021) in text but no Smith 2021 in bibliography
```

❌ **Mixing citation styles**:
```
Avoid footnotes, endnotes, or numbered references [1]
Stick to Author-Year format
```

---

## Version History

**v1.0** (2025-10-17): Initial citation format contract
