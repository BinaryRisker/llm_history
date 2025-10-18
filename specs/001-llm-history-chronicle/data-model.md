# Data Model: LLM History Chronicle Book

**Feature**: LLM History Chronicle Book
**Branch**: `001-llm-history-chronicle`
**Date**: 2025-10-17
**Purpose**: Define entities, relationships, and schema for book content structure

---

## Overview

This data model defines the conceptual structure for organizing and managing the book's content. While this is a documentation project (not a database-backed system), the entities represent the key information structures that must be consistently maintained across the manuscript.

---

## Core Entities

### 1. Chapter

Represents a major section of the book covering a period or theme in LLM history.

**Attributes**:
- `chapter_id` (string): Unique identifier (e.g., "01-foundation", "04-chatgpt-revolution")
- `chapter_number` (integer): Sequential number (1-11)
- `title` (string): Chapter title in Chinese and English
- `period` (string): Time period covered (e.g., "2017-2018", "2023-2024")
- `word_count` (integer): Character count (target: 8,000-12,000 Chinese characters)
- `status` (enum): draft | reviewed | final
- `key_events` (array): List of timeline event IDs covered in chapter
- `key_organizations` (array): List of organization IDs featured in chapter
- `technical_concepts` (array): List of concept IDs explained in chapter
- `anecdote_count` (integer): Number of anecdotes included
- `created_date` (date): Initial draft date
- `last_updated` (date): Most recent modification

**Relationships**:
- Contains multiple Sections (1:N)
- References multiple Timeline Events (M:N)
- Covers multiple Organizations (M:N)
- Explains multiple Technical Concepts (M:N)
- Includes multiple Anecdotes (1:N)

**Validation Rules**:
- `word_count` should be between 8,000-12,000 characters (FR-007 consistency requirement)
- At least 60% of chapters must contain anecdotes (SC-005)
- Each chapter must have clear opening and closing that connect to adjacent chapters (User Story 1, Scenario 2)

**File Location**: `manuscript/{chapter_id}/`

---

### 2. Section

Represents a subsection within a chapter focusing on a specific topic or event.

**Attributes**:
- `section_id` (string): Unique identifier (e.g., "01-foundation-transformer")
- `chapter_id` (string): Parent chapter reference
- `title` (string): Section heading
- `level` (integer): Heading level (2-4, H2-H4 in Markdown)
- `content` (markdown): Section body text
- `word_count` (integer): Character count
- `references` (array): Citation IDs used in this section

**Relationships**:
- Belongs to one Chapter (N:1)
- May reference multiple Timeline Events (M:N)
- May reference multiple Technical Concepts (M:N)
- Contains multiple References (1:N)

**Validation Rules**:
- Section titles must be descriptive enough for navigation (FR-015)
- Technical terms must be explained on first use (FR-008, SC-004: 90%+ of terms explained)

**File Organization**: Content embedded in parent chapter Markdown file with H2/H3/H4 headings

---

### 3. Timeline Event

Represents a significant milestone in LLM development history.

**Attributes**:
- `event_id` (string): Unique identifier (e.g., "transformer-paper-2017", "chatgpt-launch-2022")
- `date` (date): Event date (YYYY-MM-DD format)
- `title` (string): Event name/description in Chinese and English
- `organization_id` (string): Primary organization responsible
- `event_type` (enum): paper_publication | model_release | product_launch | company_announcement | technical_breakthrough
- `significance_level` (enum): critical | major | notable | minor
- `description` (string): Brief summary of the event
- `impact` (string): Why this event matters, what it enabled
- `verification_status` (enum): highly_verified | verified | single_source | reported | disputed
- `sources` (array): List of reference IDs supporting this event
- `causal_connections` (array): List of event IDs this enabled/was enabled by
- `technical_concepts` (array): List of concept IDs introduced or used
- `chapter_id` (string): Primary chapter where event is covered

**Relationships**:
- Owned by one Organization (N:1)
- Covered in one or more Chapters (M:N)
- Introduces/uses multiple Technical Concepts (M:N)
- Supported by multiple References (M:N)
- Connected to other Timeline Events (M:N, causal graph)

**Validation Rules**:
- Must have at least one source reference (FR-013, SC-008: 80%+ citations)
- Date must be within 2017-2025 range (FR-017)
- `significance_level: critical` events must be included (SC-002: 50+ significant events)
- Causal connections must form valid directed acyclic graph (no circular causality)

**File Location**: `assets/timelines/events/{event_id}.md` or embedded in timeline files

---

### 4. Organization

Represents a company or research institution contributing to LLM development.

**Attributes**:
- `organization_id` (string): Unique identifier (e.g., "openai", "google-deepmind", "baidu")
- `name` (string): Official name in Chinese and English
- `country` (string): Primary country/region
- `founded_date` (date): Organization founding date (if relevant to LLM work)
- `key_researchers` (array): Names of prominent researchers/leaders
- `strategic_approach` (string): Brief description of organization's strategy/philosophy
- `major_contributions` (array): List of event IDs for key contributions
- `timeline_start` (date): When organization began LLM work
- `timeline_end` (date): null (ongoing) or end date if ceased operations
- `logo_url` (string): Optional path to organization logo

**Relationships**:
- Responsible for multiple Timeline Events (1:N)
- Mentioned in multiple Chapters (M:N)
- Develops multiple Models (1:N)

**Validation Rules**:
- Each major organization (OpenAI, Google, Meta, Anthropic, Baidu, Alibaba) must have 3+ documented contributions (SC-003)
- Coverage must fairly represent global contributions (FR-006, constraints section: balance constraint)

**File Location**: `research/organizations/{organization_id}.md`

---

### 5. Technical Concept

Represents a key innovation or technical principle in LLM development.

**Attributes**:
- `concept_id` (string): Unique identifier (e.g., "self-attention", "scaling-laws", "rlhf")
- `name` (string): Concept name in Chinese and English
- `aliases` (array): Alternative names/abbreviations
- `introduced_date` (date): When concept first appeared
- `innovators` (array): Researchers who introduced the concept
- `organization_id` (string): Organization where developed (if applicable)
- `explanation_accessible` (markdown): Non-technical explanation for general audience
- `explanation_technical` (markdown): More detailed technical explanation (optional)
- `significance` (string): Why this concept matters, what problems it solved
- `examples` (array): Practical examples or analogies
- `first_chapter_appearance` (string): Chapter ID where concept is first explained
- `related_concepts` (array): List of related concept IDs
- `references` (array): Key papers or sources explaining this concept

**Relationships**:
- Introduced by one Organization (N:1, optional)
- Used in multiple Timeline Events (M:N)
- Explained in one or more Chapters (M:N, first appearance is special)
- Related to other Technical Concepts (M:N)
- Supported by multiple References (M:N)

**Validation Rules**:
- Must be explained on first use in accessible language (FR-008, SC-004: 90%+)
- Must include significance/impact explanation (FR-012)
- Accessible explanation must be understandable to readers with basic technical literacy (User Story 3)
- Analogies must accurately represent concepts (User Story 3, Scenario 4)

**File Location**: `manuscript/99-backmatter/glossary.md` (consolidated) or inline in chapters

---

### 6. Model

Represents a specific LLM or architecture.

**Attributes**:
- `model_id` (string): Unique identifier (e.g., "gpt-3", "bert-base", "llama-2-70b")
- `name` (string): Model name
- `release_date` (date): Public release or paper publication date
- `organization_id` (string): Developing organization
- `parameter_count` (string): Model size (e.g., "175B parameters")
- `architecture_type` (string): Base architecture (e.g., "Transformer decoder", "BERT encoder")
- `key_capabilities` (array): Notable capabilities or features
- `innovations` (array): List of concept IDs for technical innovations introduced
- `predecessor_model_id` (string): Previous model this builds on (if applicable)
- `successor_model_id` (string): Next model in the series (if applicable)
- `chapter_id` (string): Chapter where model is primarily discussed

**Relationships**:
- Developed by one Organization (N:1)
- Uses multiple Technical Concepts (M:N)
- Predecessor/Successor chain with other Models (1:1 each)
- Documented in Timeline Event (1:1)
- Covered in one or more Chapters (M:N)

**Validation Rules**:
- Major models (GPT series, BERT, T5, ChatGPT, etc.) must be covered (FR-002, FR-003, FR-004)
- Release date must be within 2017-2025 (FR-017)
- Relationship to predecessors/successors must be explained (FR-016: causal relationships)

**File Location**: Embedded in chapter content, summarized in timeline files

---

### 7. Anecdote

Represents an interesting story or behind-the-scenes detail.

**Attributes**:
- `anecdote_id` (string): Unique identifier
- `title` (string): Brief title or topic
- `content` (markdown): Story text
- `related_event_id` (string): Timeline event this relates to (if any)
- `related_organization_id` (string): Organization involved
- `verification_status` (enum): confirmed | rumored | speculative
- `sources` (array): Reference IDs for sourcing (if verified)
- `significance` (string): Why this story matters, what it reveals
- `chapter_id` (string): Chapter where anecdote appears
- `word_count` (integer): Length in characters

**Relationships**:
- Related to Timeline Event (N:1, optional)
- Related to Organization (N:1, optional)
- Appears in one Chapter (N:1)
- Supported by References (M:N, required if verified)

**Validation Rules**:
- Must be relevant to surrounding content (User Story 4, Scenario 1)
- Unverified anecdotes must be clearly marked as such (FR-010, User Story 4, Scenario 2)
- Transition back to main narrative must be smooth (User Story 4, Scenario 3)
- Frequency should be consistent across chapters (User Story 4, Scenario 4; SC-005: 60%+ chapters)

**File Location**: Embedded in chapter content with clear demarcation (e.g., sidebar, callout box)

---

### 8. Reference

Represents a citation to source material.

**Attributes**:
- `reference_id` (string): Unique identifier (e.g., "vaswani2017", "radford2018gpt1")
- `reference_type` (enum): paper | article | book | interview | blog | announcement | video
- `authors` (array): Author names (preserve original order)
- `title` (string): Publication/article title
- `publication` (string): Journal, conference, website, or publisher
- `date` (date): Publication date
- `url` (string): Web link (if available)
- `doi` (string): DOI (for academic papers)
- `language` (enum): chinese | english | other
- `access_date` (date): When source was last verified accessible
- `quoted_in` (array): List of chapter IDs or section IDs where cited
- `credibility_tier` (integer): 1 (highest) to 4 (lowest) based on source type

**Relationships**:
- Cited by multiple Chapters/Sections (M:N)
- Supports multiple Timeline Events (M:N)
- Supports multiple Technical Concepts (M:N)
- Supports Anecdotes (M:N, for verified anecdotes)

**Validation Rules**:
- 80%+ of major factual claims must have references (SC-008)
- All Timeline Events must have at least one reference (FR-013)
- Citations must follow (Author, Year) format in text (research.md decision)
- Full bibliography in backmatter (FR-013)

**File Location**: `manuscript/99-backmatter/references.md` (consolidated bibliography)

---

## Entity Relationships Summary

```
Chapter (1) ──────(N) Section
   │
   ├──────(M)────(N) Timeline Event ──────(N)────(1) Organization
   │                      │                             │
   │                      ├──────(M)────(N) Technical Concept
   │                      │
   │                      └──────(M)────(N) Model ─────(N)────(1) Organization
   │
   ├──────(1)────(N) Anecdote ──────(N)────(1) Timeline Event (optional)
   │
   └──────(M)────(N) Reference
```

---

## Metadata Standards

### File Naming Conventions

**Chapters**:
```
manuscript/{part}-{theme}/{chapter-slug}.md
Examples:
- manuscript/01-foundation/transformer-revolution.md
- manuscript/04-chatgpt-revolution/chatgpt-launch.md
- manuscript/07-multimodal-era/2024-breakthroughs.md
```

**Timeline Events**:
```
assets/timelines/events/{event-id}.md
Examples:
- assets/timelines/events/transformer-paper-2017.md
- assets/timelines/events/chatgpt-launch-2022.md
```

**Organizations**:
```
research/organizations/{org-id}.md
Examples:
- research/organizations/openai.md
- research/organizations/baidu.md
```

### Chapter Frontmatter Template

```markdown
---
chapter_number: 1
title: "Transformer革命：注意力机制的诞生"
title_en: "The Transformer Revolution: Birth of Attention Mechanism"
period: "2017-2018"
status: draft
word_count: 10500
key_events:
  - transformer-paper-2017
  - gpt1-release-2018
key_organizations:
  - google-brain
  - openai
technical_concepts:
  - self-attention
  - positional-encoding
anecdote_count: 3
created_date: 2025-10-17
last_updated: 2025-10-17
---

# Chapter 1: Transformer革命：注意力机制的诞生

[Content begins here...]
```

### Timeline Event Template

```markdown
---
event_id: transformer-paper-2017
date: 2017-06-12
title: "《Attention is All You Need》论文发表"
title_en: "Attention is All You Need Paper Published"
organization: google-brain
event_type: paper_publication
significance_level: critical
verification_status: highly_verified
sources:
  - vaswani2017
  - arxiv-1706-03762
causal_connections:
  enables:
    - gpt1-release-2018
    - bert-release-2018
technical_concepts:
  - self-attention
  - multi-head-attention
  - positional-encoding
chapter: 01-foundation
---

## Description
Google Brain团队发表了具有里程碑意义的论文"Attention is All You Need"，提出了Transformer架构...

[Full description...]

## Impact
这一架构完全摒弃了循环神经网络（RNN）和长短期记忆网络（LSTM），为后续所有大型语言模型奠定了基础...

[Impact analysis...]
```

---

## Validation Schema

### Content Quality Checks

**Per Chapter**:
- Word count: 8,000-12,000 characters (target)
- Technical terms: 90%+ explained on first use (SC-004)
- Anecdotes: Present in 60%+ of chapters (SC-005)
- Citations: 80%+ of major claims cited (SC-008)
- Voice consistency: Manual review for tone/style alignment (SC-007)

**Overall Book**:
- Total events: 50+ significant milestones (SC-002)
- Organization coverage: OpenAI, Google, Meta, Anthropic, Baidu, Alibaba each with 3+ contributions (SC-003)
- Timeline completeness: 2017 through October 2025 (FR-017)
- Timeline visualization: At least one comprehensive timeline (SC-006, FR-011)
- Chronological order: Events in sequence with causal connections (FR-016)

### State Transitions

```
Chapter Status Flow:
draft → reviewed → final

Event Verification Flow:
reported → single_source → verified → highly_verified
(or)
reported → disputed → [research] → verified/highly_verified
```

---

## Implementation Notes

**Storage Format**: Git repository with Markdown files
- Human-readable and editable
- Version controlled
- No database required
- Searchable via grep/text search

**Consistency Tools**:
- Automated scripts to check:
  - Chapter word counts
  - Citation format consistency
  - Term usage consistency (glossary matching)
  - Timeline date order
  - Frontmatter schema validation

**Cross-Reference Management**:
- Manual linking via Markdown links: `[Chapter 2](../02-gpt-era/gpt1-breakthrough.md)`
- Search tools to find all references to entities: `grep -r "GPT-3" manuscript/`

---

## Next Steps

1. ✅ Data model defined
2. **→ Contracts**: Define file format specifications, templates, and API-like interfaces
3. **→ Quickstart**: Create writer's guide using this data model
4. **→ Agent Context**: Update context files with this structure
5. **→ Tasks**: Generate implementation tasks based on this model
