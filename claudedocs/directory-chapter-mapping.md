# 目录和章节更新映射表

生成时间: 2025-10-18

## 目录映射

| 旧目录名 | 新目录名 | 状态 |
|---------|---------|------|
| 03-parallel-developments | (删除) | 空目录已删除 |
| 03-alignment-breakthrough | 03-alignment | 已重命名 |
| 04-chatgpt-mainstream | 04-chatgpt-revolution | 已重命名 |
| 04-global-competition | 05-global-race-2023 | 已重命名 |
| 05-global-competition | (合并到 05-global-race-2023) | 文件已移动 |
| 05-multimodal-agent | 07-multimodal-era | 已重命名 |
| 06-recent-developments | 08-present | 已重命名 |
| - | 06-chinese-ai | 新建目录 |

## 完整目录结构

```
manuscript/
├── 00-frontmatter/
├── 01-foundation/
├── 02-gpt-era/
├── 03-alignment/
├── 04-chatgpt-revolution/
├── 05-global-race-2023/
├── 06-chinese-ai/
├── 07-multimodal-era/
├── 08-present/
└── 99-backmatter/
```

## 章节和文件映射

### Phase 3: User Story 1 (Core Timeline)

| 任务 | 原路径 | 新路径 | 章节号 | 状态 |
|-----|--------|--------|--------|------|
| T040 | 04-chatgpt-mainstream/rlhf-innovation.md | 03-alignment/rlhf-chatgpt.md | 5 | ✅ 已存在(合并) |
| T043 | 04-chatgpt-mainstream/chatgpt-launch.md | 04-chatgpt-revolution/chatgpt-launch.md | 6 | ✅ 已更新 |
| T047 | 05-global-competition/openai-anthropic.md | 05-global-race-2023/gpt4-claude.md | 7 | ⏳ 待创建 |
| T048 | 05-global-competition/meta-llama.md | 05-global-race-2023/meta-llama.md | 8 | ✅ 已更新 |
| T051 | 06-recent-developments/2024-breakthroughs.md | 07-multimodal-era/2024-breakthroughs.md | 10 | ✅ 已更新 |
| T052 | 06-recent-developments/2025-present.md | 08-present/2025-present.md | 11 | ✅ 已更新 |

### Phase 4: User Story 2 (Company Tracking)

| 任务 | 原路径 | 新路径 | 章节号 | 状态 |
|-----|--------|--------|--------|------|
| T073 | 05-global-competition/chinese-ai-development.md | 06-chinese-ai/chinese-development.md | 9 | ⏳ 待创建 |

## 需要更新的文件

### 规格文档
- [ ] specs/001-llm-history-chronicle/tasks.md
- [ ] specs/001-llm-history-chronicle/plan.md
- [ ] specs/001-llm-history-chronicle/data-model.md
- [ ] specs/001-llm-history-chronicle/quickstart.md
- [ ] specs/001-llm-history-chronicle/contracts/chapter-template.md

### 手稿文件
- [ ] manuscript/chapter-template.md
- [ ] manuscript/99-backmatter/glossary.md

### 时间线文件
- [ ] assets/timelines/overall-timeline.md
- [ ] assets/timelines/events/*.md (多个事件卡片)

## 更新规则

1. **T002**: 更新为新的目录列表
2. **T040**: 改为 `03-alignment/rlhf-chatgpt.md`（文件已存在，原计划创建 rlhf-innovation.md 已合并）
3. **T043**: 改为 `04-chatgpt-revolution/chatgpt-launch.md`
4. **T047**: 改为 `05-global-race-2023/gpt4-claude.md`（待创建）
5. **T048**: 改为 `05-global-race-2023/meta-llama.md`
6. **T051**: 改为 `07-multimodal-era/2024-breakthroughs.md`
7. **T052**: 改为 `08-present/2025-present.md`
8. **T073**: 改为 `06-chinese-ai/chinese-development.md`

## 章节编号最终确认

| 章节号 | 目录 | 文件 | 标题 | 时间段 |
|--------|------|------|------|--------|
| 1 | 01-foundation | transformer-revolution.md | Transformer革命 | 2017 |
| 2 | 01-foundation | early-applications.md | 早期应用 | 2018 |
| 3 | 02-gpt-era | scaling-up.md | 规模扩大 | 2019-2020 |
| 4 | 02-gpt-era | google-response.md | Google的回应 | 2019-2022 |
| 5 | 03-alignment | rlhf-chatgpt.md | RLHF突破 | 2021-2022 |
| 6 | 04-chatgpt-revolution | chatgpt-launch.md | ChatGPT发布 | 2022-11 |
| 7 | 05-global-race-2023 | ai-race-2023.md | 2023全球竞赛 | 2023 |
| 8 | 05-global-race-2023 | meta-llama.md | Meta开源 | 2023-2024 |
| 9 | 06-chinese-ai | chinese-development.md | 中国AI发展 | 待创建 |
| 10 | 07-multimodal-era | 2024-breakthroughs.md | 多模态突破 | 2024 |
| 11 | 08-present | 2025-present.md | 2025现状 | 2025 |
