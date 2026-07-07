# Review Gates

`source-to-skill` should not only generate skill artifacts. It should protect
the skill system from attractive but weak updates.

The long-term rule is:

```text
source -> delta -> review gates -> user decision -> skill evolution
```

A source should become a new skill only when it survives the same pressure that
would be applied to an update of an existing skill.

## When To Run The Gates

Run these gates when a source might:

- create a Mini Skill or Full Skill
- change `## Core Guidance` in an existing skill
- add a new decision rule, workflow, checklist, or framework
- resolve or introduce a contradiction
- change when a skill should or should not be used

The gates are lighter for notes, seeds, and evidence-only updates. They are
strict for anything that changes agent behavior.

## Gate 1: First-Principles Review

The first-principles review asks whether the proposed guidance still serves the
core job of the skill.

Review questions:

| Question | Pass signal | Fail signal |
| --- | --- | --- |
| What job should this skill help an agent do? | The job is concrete and task-shaped | The job is a vague topic or content category |
| What is the core method? | The method has steps, checks, or decisions | The method is only a theme or opinion |
| Does the new source strengthen that method? | It clarifies, narrows, or supports the method | It adds attractive but unrelated content |
| Is the method transferable? | It can work across sources, authors, or cases | It only describes one local anecdote |
| What is the boundary? | The skill says when not to use the method | The skill implies universal usefulness |

Chinese shorthand:

```text
第一性原理测试：
这个 skill 到底帮 agent 做什么？
这条规则是否真的服务这个核心任务？
它是方法的一部分，还是只是一个好看的观点？
换一个 source / 作者 / 场景后，它还能成立吗？
```

## Gate 2: Adversarial Review

The adversarial review tries to break the proposed guidance before it becomes
persistent behavior.

Review questions:

| Attack | Question | Required response |
| --- | --- | --- |
| Counterexample | What example would make this rule fail? | Add a boundary, exception, or reject the rule |
| Contradiction | Does this conflict with existing guidance? | Ask the user or record a contradiction |
| Overgeneralization | Is a local case being turned into a universal rule? | Narrow the claim |
| Evidence gap | Did the source actually support this claim? | Add evidence or delete the claim |
| Use-case drift | Does this make the skill solve a different problem? | Split, reject, or create a separate seed |
| Unsafe merge | Could this update make the agent worse in common tasks? | Keep as pending until reviewed |

Chinese shorthand:

```text
对抗式审查：
有什么反例会击穿这条规则？
它和已有 skill 有没有冲突？
它是不是把局部案例包装成通用方法？
证据是否足够，还是 AI 自己补全了作者没说的话？
适用边界、失败条件、不要使用的场景是否清楚？
```

## Relationship Decisions

After both gates, classify the source relationship:

| Decision | Use when | Action |
| --- | --- | --- |
| `duplicate` | The source repeats known guidance | Do not update core guidance |
| `evidence` | The source supports an existing rule | Add to evidence only |
| `refinement` | The source improves precision | Propose a targeted edit |
| `contradiction` | The source conflicts with a rule | Ask the user before merging |
| `new_skill` | The source has a stable method outside existing skills | Create a new skill |
| `reject` | The source is noisy, unsupported, or misleading | Record or discard |

## User Review Gate

Do not ask the user to review everything. Ask only at decision points:

- accepting a contradiction
- rewriting core guidance
- creating a new skill instead of updating an old one
- promoting a seed into a Mini Skill or Full Skill
- changing `use_when` / `do_not_use_when`

Useful prompt shape:

```text
This source overlaps with `product-positioning-skill`.

Recommended action: refinement

Conflict:
- Existing guidance: early products should start with narrow positioning.
- New source: early products may need broad public attention before narrowing.

Suggested merge:
- Treat early positioning as a temporary expression layer, not a fixed strategy.

Choose:
1. merge as refinement
2. keep as contradiction
3. add as evidence only
4. reject
5. create a separate skill seed
```

## Review Report Template

Use this shape for future `evolution/pending-updates/` artifacts:

```md
# Skill Update Review

Source:
Target skill:
Recommended relationship:

## Extracted Method Candidates

## First-Principles Review

Core job:
Core method:
Transferability:
Boundary:
Pass / fail:

## Adversarial Review

Counterexamples:
Contradictions:
Overgeneralization risk:
Evidence gaps:
Use-case drift:
Unsafe merge risk:
Pass / fail:

## Proposed Change

## Evidence To Add

## User Decision Needed

## Final Decision
```

## Completion Rule

A proposed update is not ready to merge until:

- each new guidance claim has evidence
- boundaries and failure cases are stated
- contradictions are reviewed by a human
- the target skill still has one clear job
- evaluation or regression questions have been updated when behavior changes

If any of these are missing, keep the update pending.
