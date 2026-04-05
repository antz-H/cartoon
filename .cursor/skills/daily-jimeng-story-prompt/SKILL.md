---
name: daily-jimeng-story-prompt
description: Builds daily 即梦/JiMeng image prompts for the fixed-character ink picture-book series 墨团与芽仔, writes `作品/{序号} {标题}.md`, and enforces topic constraints (微小但重要、共鸣优先忌任务感、非鸡汤留白、轻悖论/口语留白可选). Use when the user runs /daily-jimeng-story-prompt, asks to continue the story arc, generate today's page prompt, 续写绘本一页, or assemble prompts from the arc file and template.
---

# Daily JiMeng Story Prompt

## Purpose

Fixed-character daily page workflow: read continuity → draft one drawable beat → fill the prompt template → optional bottom caption → save under `作品/`.

Does **not** cover 选图、去水印、后期修图 unless the user asks separately.

## Before you write beats or captions

**Read [reference.md](reference.md)** for: 选题参考与约束、连续性规则、留白规则（含参考语感）、本页情节标准、输出模板、模板文件路径、边界。

## Inputs

- Arc: `墨团与芽仔-一周情节.md`（或当前主线情节文档）
- Guide: `即梦绘本Prompt总结.md`
- Prior pages: `作品/*.md`
- Prompt structure: `reference/Prompt-template.md` — 路径解析见 [reference.md](reference.md)「Prompt 模板路径」

若多份情节文档并存，取**最能代表当前正序**的一份。

## Workflow

1. **读连续性**：情节顺序、角色锚点、最近一页发生了什么；明确承接与未决情绪。
2. **写今日一拍**：先过 reference **「共鸣优先 · 忌任务感」** 快检，再落笔。须符合 **选题约束**，但**禁止**为凑「微小」「克制」而硬拗停步、对称构图或金句式深意。单场景、可画；`主题` / `深意` 可省略或极短——若写出来像教案小结则删掉，只保留 **本页情节**（**本页情节**直接用于拼装）。忌与上一页同动作、同机位、同套话（见 reference **禁止套层推进**）。
3. **拼完整正向 prompt**：按模板五段顺序；留白段与模板一致，勿自改结构。
4. **留白文案**：若留白段供后期配文，按 reference **留白规则** 写一句或两短句；勿让模型渲染长中文。
5. **写入 `作品/{两位序号} {标题}.md`**：与弧文件序号、标题对齐；节名顺序固定：

   `[角色固定段]` → `[画风段]` → `[留白指令段]`（含后期排版说明）→ `[本页情节]`（以 `竖版内页。` 起）→ `[质量词：高清、宣纸质感]`

   只写当页文件，勿覆盖无关页。

6. **聊天回复**：连续性说明 2～4 行 + 默认完整输出结构见 [reference.md](reference.md)「默认输出结构」；注明 **已写入** 路径。

## Examples

- 触发语与完整范例：[examples.md](examples.md)
- `examples.md` 内「模板」指本 skill 下 `reference/Prompt-template.md`（路径规则见 reference.md）

## Quick checklist

- [ ] 已读 reference 选题 + 留白 + **共鸣优先 · 忌任务感**
- [ ] 本页一件小事、可画，且带 **体感或具体破绽**（非空泛「安静克制」）
- [ ] 拼装顺序与模板一致
- [ ] 作品 md 五段齐全
