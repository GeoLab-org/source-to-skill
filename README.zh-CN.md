<p align="center">
  <img src="assets/logo.svg" alt="source-to-skill logo" width="112">
</p>

# source-to-skill

[![CI](https://github.com/GeoLab-org/source-to-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/GeoLab-org/source-to-skill/actions/workflows/ci.yml)

[English](README.md) | **简体中文**

收藏夹不是知识库。能被调用，才更接近能力。

你可能收藏过很多“以后一定会看”的长视频，听过当时很炸的播客，读过方法论很强的书。收藏那一刻，它们看起来都很有用。可真正开始做事时，它们常常只剩下一种模糊印象：我好像看过。

`source-to-skill` 就是为这个断层做的。

它是一个早期开源编译器，用来把高价值内容转成最小可用的能力系统更新：一条笔记、一段证据、一个能力种子、一个聚焦能力，或者一次对已有能力的更新建议。

内容默认不是能力。内容先成为证据、增量或种子。只有稳定、可迁移、经过测试的方法，才应该升级成可调用的能力。

它不是总结器。

摘要告诉你内容讲了什么。能力让 AI 在真实任务里调用这套方法。一个好的能力系统还应该知道：新内容是在确认旧方法、修正旧方法、反驳旧方法，还是已经超越旧方法。

目标不是制造更多笔记，而是让有用的方法活得足够久，久到智能体可以调用它、质疑它、继续改进它。

![Source to Skill flow](assets/hero-diagram.svg)

## 为什么做

大多数 AI 工具回答的是第一个问题：

> 这段内容讲了什么？

`source-to-skill` 想问的是更有用的那个问题：

> 这段内容能不能改进一个智能体真的会用的方法？

这个差别很重要。一个好的总结，仍然可能只是把内容困在笔记里。一个有用的能力，应该改变智能体在下一个真实任务里的行为。

高价值内容里可能包含框架、原则、判断标准、反例、案例和操作步骤。一个好的能力应该把这些方法保留下来，同时保留证据、边界和清楚的输出契约。

RAG 帮智能体检索知识。Skills 帮智能体带着知识行动。  
所以能力需要的不只是文本，而是可复用判断、证据、适用范围和行为约束。它也需要维护：新内容应该先和已有能力匹配，而不是马上制造更多文件。

`source-to-skill` 在写文件前先做准备度判断。弱内容不应该被包装成看起来很自信的假方法论。相似内容也通常应该先成为证据、修正建议或待确认更新，而不是直接变成新能力。

说白了：

```text
不要把每份内容都变成能力。
不要把每个想法都变成新文件。
找到稳定的方法，保留证据，只在通过审查后进化已有能力系统。
```

## 什么时候用

当你有一份内容，觉得它太有价值，不该继续躺在收藏夹里；但又太危险，不能盲目升级成智能体行为时，可以用 `source-to-skill`。

适合：

- 一个真正讲清操作方法的长视频
- 一期有可复用判断的播客或访谈
- 一本有清晰框架的书、一门课、一组文章
- 一篇能修正已有规则的技术或商业博客
- 一组包含流程、检查项或失败模式的资料

不太适合：

- 只需要看一次的新闻
- 没有操作方法的鸡血内容
- 很短的观点碎片
- 缺少上下文的一次性会议记录
- 无法用证据验证的内容

真正有用的时刻，是一份内容不再只是“我看过的东西”，而变成“我的智能体下次能调用的方法”。

## 为什么不是总结

总结压缩内容。能力组织行动。

普通总结可能会说：

> 这场访谈认为，产品需要清晰定位、理解用户、建立差异化。

但一个能力应该让方法变得可用：

- 什么时候使用这个定位框架
- 先收集哪些信息
- 如何比较竞品叙事
- 如何测试差异是否能被用户感知
- 哪些原文证据支持这个方法
- 这个方法不适合什么场景

边界很重要：不要把所有内容都包装成知识，也不要一篇内容生成一个能力。让有价值的内容去修正、挑战和进化已有能力系统。

## 什么内容值得变成能力

一份内容比较适合蒸馏，当它包含：

- 可复用判断
- 可重复步骤
- 决策规则
- 案例或例子
- 清楚边界
- 可迁移场景
- 足够审查的证据

通常不适合的内容：

- 新闻
- 观点碎片
- 鸡血内容
- 浅层 listicle
- 一次性会议上下文
- 没结构的个人笔记

不是所有内容都值得变成能力。这个保守判断本身就是产品的一部分。

## 从“内容堆积”到“能力增量”

长期方向不是“一份内容，一个能力”。

一篇博客、一场访谈、一个长视频，不应该默认生成一个新能力。否则能力会越来越多、越来越重复、越来越难路由，最后变成另一个混乱的知识库。

每份内容应该先判断它和已有能力系统的关系：

| 关系 | 含义 | 推荐动作 |
| --- | --- | --- |
| 重复 | 已有能力已经覆盖了 | 忽略，或记录为弱参考 |
| 证据 | 支持已有规则，提供更好的例子或原话 | 增加证据，不改核心指导 |
| 修正 | 让已有规则更准确 | 提出定向更新 |
| 冲突 | 和已有规则冲突 | 合并前先问用户 |
| 新能力 | 有稳定方法，且无法归入已有能力 | 创建新的小型/完整能力 |

新内容应该先成为增量：证据、修正、冲突或种子。只有稳定、可复用、经过测试的模式，才应该成为独立能力。

## 能力如何进化

目标中的进化流程：

```text
内容
  -> 提取候选方法
  -> 匹配已有能力
  -> 判断关系：重复 / 证据 / 修正 / 冲突 / 新能力
  -> 生成更新建议
  -> 在关键决策点询问用户
  -> 运行第一性原理测试和对抗式审查
  -> 带着证据和更新记录合并
  -> 运行评估
```

比如，一篇新文章和已有 `product-positioning` 能力重叠。工具不应该再创建一个定位能力，而应该提出：

```text
匹配到已有能力：
- product-positioning-skill (72% overlap)

建议动作：
- 修正

潜在冲突：
- 已有规则：早期产品应该从窄定位开始。
- 新内容：早期产品可能需要先获得更广泛的公共注意，再逐步收窄。

建议合并方式：
- 把早期定位视为临时表达层，而不是固定战略。
- 把新内容作为证据和边界案例加入。
```

用户再决定：合并、保留为冲突，还是拒绝。

## 第一性原理与对抗式审查

能力进化需要免疫系统。

`source-to-skill` 不应该只问“这份内容听起来有没有用”。它应该从两个方向挑战每一次能力生成或更新：

1. **第一性原理测试**：这个更新是否仍然服务核心问题、核心方法和核心使用场景？还是只是在加入好看的噪音？
2. **对抗式审查**：这条指导会在哪里失败、过度泛化、和已有规则冲突，或者伪装成比实际证据更充分？

第一性原理测试负责问：

- 这个能力到底帮智能体做什么？
- 这条新规则是否真的服务这个核心任务？
- 它是方法的一部分，还是只是一个好看的观点？
- 换一份内容、一个作者、一个场景后，它还能成立吗？

对抗式审查负责问：

- 有什么反例会击穿这条规则？
- 它和已有能力有没有冲突？
- 它是不是把局部案例包装成通用方法？
- 证据是否足够，还是 AI 自己补全了作者没说的话？
- 适用边界、失败条件、不要使用的场景是否清楚？

更新核心指导之前，应该先通过这些检查。否则它应该留在证据、待确认笔记、冲突记录或已拒绝更新里。

详见 [docs/review-gates.md](docs/review-gates.md)。

## 示例

输入：

一场 90 分钟的产品定位访谈。

普通总结可能会输出：

> 嘉宾认为产品需要清晰定位、理解用户、建立差异化。

`source-to-skill` 会先判断这套方法是否已经属于某个已有能力。如果它确实是一个新方法，才可能编译成：

```text
product-positioning-skill/
  SKILL.md
  cheatsheet.md
  references/evidence.md
  evals/smoke-questions.md
  eval-report.md
```

生成或更新后的能力应该能帮助智能体：

- 评估一个产品想法
- 识别模糊定位
- 比较不同竞品叙事
- 提出更好的用户访谈问题
- 压力测试上市叙事

## 输出等级

![Output levels](assets/output-levels.svg)

| 等级 | 输出 | 什么时候用 |
|---|---|---|
| 0 | 丢弃 | 内容太薄、本地化太强或噪音太多 |
| 1 | 笔记 | 有信息，但没什么可复用判断 |
| 2 | 能力种子 | 有候选判断，但不足以成为独立能力 |
| 3 | 小型能力 | 主题聚焦，有足够规则和证据 |
| 4 | 完整能力 | 内容系统、结构完整、可独立成为工具包 |

`source-to-skill` 不会把每份内容都升级成完整能力。普通会议可能只值得做笔记；短视频可能只有一个种子；博客可能只是修正一条已有规则；书、课程、文章系列或高密度专家访谈，才可能成为真正的能力工具包。

未来的进化层还应该包括：

- 证据：支持已有判断，但不改核心方法
- 修正：修正或精确化已有能力
- 冲突：和已有能力冲突，需要用户确认

## 安装

从 GitHub 安装：

```bash
python -m pip install "source-to-skill @ git+https://github.com/GeoLab-org/source-to-skill.git@v0.2.0"
source-to-skill --version
```

开发模式安装：

```bash
git clone https://github.com/GeoLab-org/source-to-skill.git
cd source-to-skill
python -m pip install -e .
source-to-skill --version
```

## 使用

运行 demo：

```bash
source-to-skill demo --out out/demo
```

完整命令见 [docs/commands.md](docs/commands.md)，示例流程见
[examples/README.md](examples/README.md)，案例行为见
[docs/case-studies.md](docs/case-studies.md)。

先分析：

```bash
source-to-skill analyze examples/article.md
```

分析远程文章：

```bash
source-to-skill analyze https://example.com/article
```

分析本地 EPUB：

```bash
source-to-skill analyze path/to/book.epub
```

构建推荐产物：

```bash
source-to-skill build examples/article.md --level auto --out out
```

检查生成能力的证据：

```bash
source-to-skill eval-skill out/review-playbook --json
```

强制生成能力种子：

```bash
source-to-skill build examples/meeting-transcript.md --level seed --out out
```

把弱内容折叠进已有能力：

```bash
source-to-skill fold examples/meeting-transcript.md ~/.codex/skills/design-review
```

清洗转写文本后再评分：

```bash
source-to-skill clean-transcript examples/meeting-transcript.vtt \
  --out out/clean-meeting.md \
  --title "Meeting Transcript"

source-to-skill analyze out/clean-meeting.md
```

用已安装的 Whisper 兼容命令行工具转写音频：

```bash
source-to-skill transcribe-audio recording.m4a \
  --out out/recording.vtt \
  --model base
```

把长内容切成可分别评分的主题段：

```bash
source-to-skill split-source out/clean-meeting.md --out out/topics
```

构建或折叠某个有用片段：

```bash
source-to-skill build-segment out/topics 2 --level seed --out out
source-to-skill fold-segment out/topics 2 ~/.codex/skills/design-review
```

## 评分内容

v0 评分器是透明的，会看：

- 内容深度
- 章节结构
- 判断或规则语言
- 可迁移线索
- 例子和证据
- 明显的对话噪音

它不是客观真理判断，而是一个质量门槛：让弱输入更难被包装成强方法论。

小型能力和完整能力会自动生成 `eval-report.md`，用来比较核心指导和 `references/evidence.md`。也可以手动运行 `source-to-skill eval-skill`。

证据很重要，因为生成的能力不应该悄悄发明原内容没支持过的方法。目标不是生成一个看起来有用的产物，而是生成一个人能审查、智能体能使用、并且不丢失来源边界的东西。

## 示例报告

```text
Skill Readiness: 85/100
Recommended output: Mini Skill

Why:
- Structure: clear sectioning and list structure
- Actionability: many rule-like phrases
- Evidence: examples are visible

Caution:
- Short sources usually make better seeds than standalone full skills
```

## 项目状态

这是一个早期项目。

目标不是把每个文件都包装成假方法论，而是做一个谨慎的编译器，能够判断：

- 这份内容太弱
- 这份内容只应该成为笔记
- 这份内容有几个有用种子
- 这份内容包含一个聚焦方法
- 这份内容足够成为完整能力工具包
- 这份内容应该更新已有能力，而不是创建新能力
- 这份内容和已有能力冲突，需要人工审查

当前版本支持本地 UTF-8 文本、Markdown、简单 HTML、本地 EPUB、单页远程文本/HTML URL、转写文本清洗，以及通过外部 Whisper 兼容命令行工具做可选音频转写。它也可以把长内容切分成可分别评分的主题候选。

PDF、网站爬取、浏览器渲染页面和更完整的视频工作流，留给后续采集插件。当前第一任务是把“是否值得变成能力”的判断做准。

当前命令行工具已经可以构建能力产物，也可以把弱内容折叠进已有能力。上面描述的进化层是下一阶段产品方向：内容到增量、能力匹配、第一性原理测试、对抗式审查、用户确认更新和能力回归检查。

## 设计原则

- 不要从每个输入生成完整能力
- 如果内容应该修正已有能力，就不要创建新能力
- 一次性上下文和可复用规则要分开
- 弱能力优先做种子
- 保留证据
- 冲突是审查项，不是自动合并项
- 每次重大更新都要过第一性测试：核心问题、方法、使用场景和边界
- 改核心指导前先做对抗式审查
- 生成产物要小到人可以读、可以审

更多文档：

- [docs/philosophy.md](docs/philosophy.md)
- [docs/output-levels.md](docs/output-levels.md)
- [docs/scoring.md](docs/scoring.md)
- [docs/intake.md](docs/intake.md)
- [docs/transcripts.md](docs/transcripts.md)
- [docs/audio.md](docs/audio.md)
- [docs/splitting.md](docs/splitting.md)
- [docs/demo.md](docs/demo.md)
- [docs/evaluation.md](docs/evaluation.md)
- [docs/review-gates.md](docs/review-gates.md)

## 路线图

见 [ROADMAP.md](ROADMAP.md)。

## 更新记录

见 [CHANGELOG.md](CHANGELOG.md)。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。一句话：改进门槛，不要让弱内容看起来比它实际更强。

## 许可证

MIT
