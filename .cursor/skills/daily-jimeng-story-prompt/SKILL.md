---
name: daily-jimeng-story-prompt
description: Generates a daily JiMeng illustration prompt from ongoing story materials for a fixed-character picture book series, and writes the assembled prompt to `作品/{序号} {标题}.md`. Use when the user wants to continue a story arc, derive today's plot from prior plot files, produce a complete 即梦/即梦AI image prompt from `reference/Prompt-template.md`, or save page prompts as work documents under `作品/`.
---

# Daily JiMeng Story Prompt

## Purpose

This skill is for a fixed-character illustrated story workflow.

It helps the agent do these steps:

1. Read existing story materials and infer a coherent "today's plot" that continues prior beats.
2. Build a full JiMeng image prompt by filling the structure in `reference/Prompt-template.md`.
3. Write one short sentence for the whitespace/text area when the template's `[留白指令段]` implies a caption or bottom text.
4. **Persist the assembled prompt into a `作品/` markdown file** that matches the numbering and short title from the story arc (for example `作品/05 驻足.md`), using the same section headings as sibling files under `作品/`.

This skill does **not** handle image selection, watermark removal, or post-processing unless the user asks separately.

## Default Inputs

Use these sources first when they exist:

- `reference/Prompt-template.md`: the master prompt structure for this skill
- story arc files such as `墨团与芽仔-一周情节.md`
- related prompt guidance such as `即梦绘本Prompt总结.md`
- any existing `作品/*.md` files for page-specific wording or continuity

If multiple story files exist, prefer the most recent file that clearly represents the current canonical sequence.

## Workflow

Follow this order every time:

### 1. Read continuity before writing

Read the relevant story documents and extract:

- the current plot sequence
- recurring emotional arc
- fixed character identities
- visual continuity constraints
- what has already happened most recently

Before drafting today's plot, briefly determine:

- what changed in the last scene
- what emotional beat is still unresolved
- what kind of next beat feels continuous rather than repetitive

### 2. Generate today's plot beat

Write one new scene that can naturally follow the latest established scene.

Requirements:

- preserve both fixed characters' identity, scale, and relationship
- keep the emotional tone restrained, quiet, and picture-book suitable
- avoid repeating the exact same physical action as the immediately previous scene
- prefer progression through mood, distance, gesture, environment, or perspective
- keep the scene visually drawable in a single still image
- preserve continuity with prior motifs when useful

When useful, output today's plot in three parts:

- `主题`
- `深意`
- `本页情节`

The `本页情节` should be the most directly usable source for prompt assembly.

### 3. Assemble the full JiMeng prompt

Read `reference/Prompt-template.md` and follow its structure exactly.

Use this assembly logic:

1. fixed character segment
2. style segment
3. today's plot segment
4. whitespace/layout segment
5. quality terms

Do not rewrite the template into a different structure unless the user explicitly asks.

When the chosen whitespace/layout variant is meant to hold a short line of text, also generate a matching caption sentence for that page.

### 4. Write the work document (`作品/*.md`)

After the prompt is complete, **write or update** the page file under `作品/`:

- **Naming**: `作品/{两位序号} {标题}.md` where the序号 and标题 align with `墨团与芽仔-一周情节.md` (or the active arc), e.g. `05 驻足.md`. Use two-digit prefixes `01`–`09` to match existing files.
- **Section order** (same labels as other `作品/*.md` files):

  1. `[角色固定段]` — full text from template / prior pages
  2. `[画风段]` — same unless the day needs a special variant (e.g. sunrise color note on day 3)
  3. `[留白指令段]` — chosen variant from `reference/Prompt-template.md`, plus any **后期排版** notes for the `留白文案` (do not ask the image model to render readable long text; keep captions for post layout when possible)
  4. `[本页情节]` — start with `竖版内页。` then the scene paragraph
  5. `[质量词：高清、宣纸质感]` — quality block

- **Do not** replace unrelated existing work files; create only the file for the current day or the day the user specified.
- In chat, still give a short confirmation with the **file path** and optionally paste the same content if the user wants to copy without opening the file.

### 5. Keep continuity explicit

When you output the result, include a short continuity note explaining:

- which prior day or prior beat today's scene follows
- what changed compared with the previous scene
- why this scene is the natural next image

Keep the note short, usually 2 to 4 lines.

## Story Continuity Rules

Use these rules when inventing today's scene:

- continuity is more important than novelty
- novelty should come from progression, not from introducing random new elements
- each daily scene should feel like one step on the same emotional line
- do not let characters become exaggerated, overly cute, noisy, comedic, or melodramatic unless the user explicitly changes style
- prefer calm visual storytelling over abstract explanation
- prefer one central action and one clear emotional implication
- preserve the Chinese ink-wash picture book tone

Good progression examples:

- from first noticing to tentative approach
- from facing each other to moving in the same direction
- from physical closeness to emotional recognition
- from shared landscape to shared rhythm
- from separation tension to reconnection

Avoid:

- repeating "holding hands" or the same pose on adjacent days
- adding busy props that weaken the minimalist composition
- breaking established scale or character design
- making the image read like anime poster art, cinematic blockbuster art, or 3D render

## Whitespace Caption Rule

If the template's `[留白指令段]` suggests top or bottom reserved text space, write one optional sentence that can be placed there.

This sentence should:

- match the image content directly
- feel calm and comfortable
- avoid chicken-soup phrasing, slogans, preaching, or forced uplift
- avoid explaining the whole moral
- sound natural in a picture book
- usually stay within one short sentence

Preferred qualities:

- gentle
- specific
- understated
- slightly thoughtful, but not heavy

Good examples:

- `雨细下来，路就慢了一点。`
- `它们没有说话，只把脚步放在了一起。`
- `天亮的时候，山也像刚醒。`

Avoid examples:

- `只要一起前行，终会迎来属于自己的光。`
- `所有相遇，都是命运最好的安排。`
- `哪怕世界寒冷，陪伴也会治愈一切。`

## Output Format

Default to this format unless the user requests something else:

```markdown
今日情节

主题：...

深意：...

本页情节：
...

留白文案：
...

完整即梦 Prompt

...

连续性说明

- 承接：...
- 变化：...
- 原因：...

**已写入**：`作品/{两位序号} {标题}.md`
```

If the user only asks for the final prompt, still do the continuity reasoning internally and return:

- `本页情节`
- `留白文案`
- `完整即梦 Prompt`

## Writing Standard For `本页情节`

The `本页情节` should usually:

- describe a single scene
- specify action and environment together
- imply emotion without over-explaining it
- remain concise enough to embed into the final prompt
- stay visually concrete

Preferred style:

- restrained
- lyrical but not flowery
- image-first
- suitable for direct generation

## If Inputs Are Incomplete

If the story continuity is unclear, do not invent a completely new arc immediately.

Instead:

1. infer the most likely current position from recent files
2. state the assumption briefly
3. generate one conservative next beat that is easy to revise

If `reference/Prompt-template.md` is missing, ask the user for the template or fall back to the latest known prompt structure only after saying that you are doing so.

## Examples

For full worked examples, see [examples.md](examples.md).

### Example trigger requests

- "根据前几天情节生成今天的画面"
- "读取故事文档，续写今天这一页，并给我完整即梦 prompt"
- "按模板生成今天的生图 prompt"
- "给墨团与芽仔继续出今天这一张"

### Example behavior

Given a recent scene about "雾中回望", a good next beat would usually be a restrained reconnection scene rather than a dramatic reunion speech.

After producing the prompt for day 5, write `作品/05 驻足.md` with the five sections above.

## Boundaries

This skill currently stops at prompt generation.

Do not claim that the image has been generated, selected, or edited unless the user separately asks for those steps and the needed tools are available.
