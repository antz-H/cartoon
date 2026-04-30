---
name: jimeng-motuan-xhs-daily
description: 墨团与芽仔每日即梦→小红书稿：读 memory+近页定主题，五段拼即梦 prompt，落盘作品 md，评分后合并写入 memory
when_to_use: /jimeng-motuan-xhs-daily, 每日即梦小红书稿, 墨团与芽仔, 即梦prompt, 生图, 小红书绘本稿, 主题—标题—prompt—记记忆
---

# JiMeng · 墨团与芽仔 · 每日小红书稿

## 先读

1. **[references/memory-protocol.md](references/memory-protocol.md)**：memory.md 覆写哲学、槽位合并、0～10 询问、写入闸门
2. **[references/iteration-rubric.md](references/iteration-rubric.md)**：落盘前 A/B/C 自检表
3. **[references/xhs-and-tone.md](references/xhs-and-tone.md)**：标题字数、正文气质、缩略图自检
4. **[references/Prompt-template.md](references/Prompt-template.md)**：五段拼装与留白版式原文

钉尾、模型常漏留白等：**按需**查阅仓库根目录 `即梦绘本Prompt总结.md`（§4.4、§2.4）。

## 默认输入（仓库根 `cartoon/`）

- `memory.md`：跨轮原则与偏好（**≤300字、原则级合并覆写、非案情台账**）
- `作品/*.md`：取最近 2～3 篇扫本页情节与留白，防同构
- 前一日数据反馈（可选）：用户消息里粘贴的曝光/点击率等；**弱信号**微调，写入 memory 时只保留蒸馏原则
- 若用户另有 memory 路径：以用户消息为准

## Workflow（顺序固定）

### 1. 定主题

- 用 memory + 近页（及用户弧/大纲，若有）对齐：上一拍未决、情绪走向、重复母题
- 本拍须**单场景、可画、小具体**；与墨团（沉、稳、墨）与芽仔（小、灵、笋）行为动机一致
- 过 [xhs-and-tone.md](references/xhs-and-tone.md) 信息流自检：相对近页至少变一项（天色/机位/道具/身体关系）
- 同步成稿**选型理由**，须在步骤 3 落盘为 `## 主题与选型理由`

### 2. 定小红书主标题

- **3～10 汉字**，白话自解释；规则见 [xhs-and-tone.md](references/xhs-and-tone.md)
- **不**进入即梦正向 prompt

### 3. 生成即梦正向 Prompt（**必须落盘 .md**）

- **落盘前强制**：按 [iteration-rubric.md](references/iteration-rubric.md) A+B 自检；不过线则只改文字再跑一轮（最多两轮静默修订）；仍卡壳→聊天说明，**禁止**谎称已写入
- 五段顺序：`[角色固定段]` → `[画风段]` → `[留白指令段]`（四选一）→ `[本页情节]`（**以`竖版内页。`起笔**，不重复画风段）→ `[质量词]`
- 钉尾按 `即梦绘本Prompt总结.md` §4.4 在整段末尾追加
- **落盘**：新建 `作品/{两位序号} {白话标题}.md`，序号 = 现有最大 +1，勿覆盖已有
- **文件三节（顺序固定）**：
  1. `## 主题与选型理由`：至少覆盖 ①承接上拍/未决 ②相对近页改了哪项 ③与 memory 对齐或张力 ④为何可画 ⑤墨团/芽仔动机各一句
  2. `## 小红书主标题`：一行 3～10 字
  3. `## 即梦正向 Prompt`：完整 prompt（代码围栏包裹，含钉尾）
- **可选**追加：留白对白、对白释义、发布包装——遵守 [xhs-and-tone.md](references/xhs-and-tone.md)；留白对白默认使用**方言**（不限地域，有特色即可），规则见 [xhs-and-tone.md](references/xhs-and-tone.md)「对白方言」一节
- 聊天中给出**可复制完整 prompt**，标注「以下为即梦粘贴区」，写明已落盘路径

### 4. 询问（评分 + memory）

- 短列表汇总：主题、主标题、本拍要点、未决钩子
- **必须**依次询问两段（原文见 [memory-protocol.md](references/memory-protocol.md)「询问」）：
  1. 即梦 prompt 有效性 **0～10**（衡量控图/出图帮助，非小红书配文）
  2. 是否并入 `memory.md` 滚动总结 ≤300 字？回复 **是/否**
- **停止**，等用户回复；**不得**在用户确认前写入 memory

### 5. 用户确认「是」之后

- 过 [iteration-rubric.md](references/iteration-rubric.md) 节 C 闸门
- 按 [memory-protocol.md](references/memory-protocol.md)：读旧版 → A/B/C 槽位合并 → 具象扫描 → 整文件重写 `memory.md`（≤300 字，C/B 为主，A 一句类型化）
- 用户 0～10 分转写进 C 区（高分强化一条、低分避坑一条）
- 回复说明已重写、路径、约 X 字/300

## 交付块

1. 连续性 2～4 行（完整选型理由在 md 中）
2. 主题一句
3. 主标题（3～10 汉字）
4. 即梦正向 prompt（完整可复制）+ 已落盘路径
5. （按需）留白对白 / 对白释义 / 发布包装
6. 0～10 评分 + 是否并入 memory 询问（原文以 memory-protocol 为准）
