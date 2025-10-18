# Chapter Template Contract

**Version**: 1.0
**Purpose**: Standard structure for all book chapters
**Applies To**: All files in `manuscript/` directory

---

## File Structure

```markdown
---
# YAML Frontmatter (required)
chapter_number: [integer]
title: "[Chinese title]"
title_en: "[English title]"
period: "[YYYY-YYYY]"
status: draft | reviewed | final
word_count: [integer]
key_events:
  - [event-id-1]
  - [event-id-2]
key_organizations:
  - [org-id-1]
  - [org-id-2]
technical_concepts:
  - [concept-id-1]
  - [concept-id-2]
anecdote_count: [integer]
created_date: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# Chapter [N]: [Title in Chinese]

## 引言 (Introduction)
[2-3 paragraphs setting context, connecting to previous chapter]

## [Main Section 1]
[Content with technical explanations, timeline events, citations]

### [Subsection 1.1]
[Detailed content]

## [Main Section 2]
[Content continues...]

### 💡 轶事：[Anecdote Title] (Optional Anecdote Callout)
[Anecdote content with verification status if needed]

## [Main Section 3]
[Content continues...]

## 小结 (Summary)
[2-3 paragraphs summarizing key developments, setting up next chapter]

---

**本章要点** (Key Takeaways):
- [Key point 1]
- [Key point 2]
- [Key point 3]

**参考文献** (Chapter References):
[List inline citations used in this chapter]
```

---

## Required Elements

### 1. YAML Frontmatter
**Mandatory Fields**:
- `chapter_number`: Sequential integer (1-11)
- `title`: Chinese chapter title
- `title_en`: English chapter title
- `period`: Time period covered (format: "YYYY-YYYY" or "YYYY-MM to YYYY-MM")
- `status`: One of: draft, reviewed, final
- `word_count`: Integer count of Chinese characters (updated after major edits)
- `created_date`: ISO 8601 date (YYYY-MM-DD)
- `last_updated`: ISO 8601 date (YYYY-MM-DD)

**Optional Fields** (populate if applicable):
- `key_events`: Array of event IDs covered in chapter
- `key_organizations`: Array of organization IDs featured
- `technical_concepts`: Array of concept IDs explained
- `anecdote_count`: Number of anecdotes included

### 2. Chapter Title (H1)
- Format: `# Chapter [N]: [Title]`
- Must match frontmatter `title` field
- Only one H1 per file

### 3. Introduction Section (引言)
- Required first section after title
- 2-3 paragraphs
- Purpose:
  - Establish context for this chapter
  - Connect to previous chapter's ending
  - Preview what's coming in this chapter

### 4. Main Content Sections (H2)
- At least 3-5 main sections per chapter
- Use descriptive headings (avoid generic "Section 1", "Section 2")
- Each section focuses on one major theme, event, or organization

### 5. Subsections (H3, H4)
- Use H3 for major subsections
- Use H4 for detailed breakdowns
- Maximum depth: H4 (don't go deeper)

### 6. Summary Section (小结)
- Required last section before backmatter
- 2-3 paragraphs
- Purpose:
  - Recap key developments covered
  - Emphasize significance
  - Transition to next chapter

### 7. Key Takeaways Box
- Bulleted list (3-5 items)
- Distill chapter's most important points
- Written in accessible language

### 8. Chapter References
- List all inline citations used in chapter
- Follow bibliography format from citations contract
- Links to full bibliography in backmatter

---

## Content Guidelines

### Technical Explanations
**Format**:
```markdown
### [Technical Concept Name]

**什么是[概念]？** (What is [Concept]?)
[Accessible explanation for non-experts, 2-3 paragraphs]

**为什么重要？** (Why It Matters)
[Significance and impact, 1-2 paragraphs]

**类比** (Analogy, optional):
[Helpful comparison if concept is complex]

参见：[Reference to source]
```

**Requirements**:
- Explain on first use (90% of technical terms, SC-004)
- Accessible to readers with basic technical literacy (FR-008)
- Prioritize conceptual accuracy over mathematical precision (assumptions section)

### Timeline Events
**Format**:
```markdown
### [Event Title] (YYYY-MM-DD)

[Description of what happened, 2-3 paragraphs]

**主要贡献** (Key Contributions):
- [Innovation 1]
- [Innovation 2]

**影响** (Impact):
[How this enabled future developments]

参考：[Citation]
```

### Anecdotes
**Format**:
```markdown
### 💡 轶事：[Anecdote Title]

[Story content, 1-2 paragraphs]

[If unverified: ⚠️ **注**：此信息未经官方证实，来源于业界传闻。
Note: This information is unverified and based on industry reports.]

---
```

**Requirements**:
- Relevant to surrounding content (User Story 4, Scenario 1)
- Clear demarcation from main text (callout box, horizontal rules)
- Verification status marked if unverified (FR-010)
- Smooth transition back to main narrative (User Story 4, Scenario 3)

### Citations
**Inline Format**: `(Author, Year)` or `(作者, Year)`

**Examples**:
```markdown
根据Google的论文 (Vaswani et al., 2017)，Transformer架构...
According to Google's paper (Vaswani et al., 2017), the Transformer architecture...

OpenAI在博客中宣布 (Radford, 2018) GPT-1的发布...
OpenAI announced in their blog (Radford, 2018) the release of GPT-1...
```

**Requirements**:
- 80%+ of major claims cited (SC-008)
- Format consistent across all chapters (FR-013)

### Cross-References
**Format**:
```markdown
这一突破为后来的ChatGPT奠定了基础（参见[第6章](../04-chatgpt-mainstream/chatgpt-launch.md)）。
This breakthrough laid the foundation for ChatGPT (see [Chapter 6](../04-chatgpt-mainstream/chatgpt-launch.md)).

如[第2章](../01-foundation/attention-mechanism.md)所述，自注意力机制...
As described in [Chapter 2](../01-foundation/attention-mechanism.md), the self-attention mechanism...
```

---

## Validation Checklist

**Before marking chapter as `status: reviewed`**:

- [ ] Frontmatter complete and accurate
- [ ] Word count between 8,000-12,000 characters
- [ ] Introduction connects to previous chapter
- [ ] Summary sets up next chapter
- [ ] 90%+ technical terms explained on first use
- [ ] Major claims cited (80%+ with references)
- [ ] Anecdotes marked with verification status
- [ ] Cross-references valid (links work)
- [ ] Consistent voice and tone with other chapters
- [ ] No orphaned H1, H2, H3 headers (each must have content)
- [ ] Key takeaways box present with 3-5 items

**Before marking chapter as `status: final`**:

- [ ] Beta reader feedback incorporated
- [ ] Fact-checking complete for all claims
- [ ] References verified and accessible
- [ ] Narrative flow validated
- [ ] Anecdote frequency consistent with other chapters

---

## Version History

**v1.0** (2025-10-17): Initial contract based on data model and research decisions
