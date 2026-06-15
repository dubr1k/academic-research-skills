# Bilingual Routing

This document defines how the fork chooses between upstream English skills and Russian context skills.

## Inputs

Evaluate these signals before loading a skill:

- user request language: `en`, `ru`, or `mixed`;
- requested output language;
- academic task: `research`, `paper`, `review`, or `pipeline`;
- target venue/context: international, Russian journal, ВАК, РИНЦ/eLIBRARY, CyberLeninka, dissertation council;
- citation style: APA, IEEE, Vancouver, Chicago, MLA, ГОСТ;
- corpus language: English sources, Russian sources, or mixed corpus.

Explicit user instructions override automatic language detection.

## Skill Map

| Task | English / international context | Russian context |
|---|---|---|
| Research, source search, literature review, fact-check | `deep-research` | `akademicheskoe-issledovanie` |
| Paper planning, drafting, abstract, revision, formatting | `academic-paper` | `akademicheskaya-statya` |
| Peer review, methodology review, pre-submission review | `academic-paper-reviewer` | `akademicheskii-retsenzent` |
| End-to-end research-to-publication workflow | `academic-pipeline` | `akademicheskii-konveer` |

## Routing Rules

### R1. English international workflow

Use upstream English skills when the request is in English and the venue/context is international.

Examples:

- "Write an APA-style literature review on AI feedback in higher education." -> `academic-paper`
- "Run a full research-to-publication pipeline for an IEEE conference paper." -> `academic-pipeline`

### R2. Russian local workflow

Use Russian skills when the request is in Russian and mentions Russian academic requirements or Russian source systems.

Signals:

- ГОСТ;
- ВАК;
- РИНЦ;
- eLIBRARY;
- CyberLeninka;
- диссертация, автореферат, диссертационный совет;
- российский журнал, кафедра, ВКР.

Examples:

- "Оформи список литературы по ГОСТ для статьи ВАК." -> `akademicheskaya-statya`
- "Проверь статью перед отправкой в журнал РИНЦ." -> `akademicheskii-retsenzent`

### R3. Russian request for international venue

Use Russian skills for interaction and planning, but preserve the requested international output constraints.

Examples:

- "На русском помоги подготовить статью для Scopus, стиль APA." -> `akademicheskaya-statya`, output constraints: APA/international venue.
- "Сделай обзор литературы для англоязычной статьи, источники Scopus/Web of Science." -> `akademicheskoe-issledovanie`, source priority: international databases.

### R4. English request for Russian venue

Use Russian context skills when the academic target is Russian even if the prompt is English.

Examples:

- "Review this paper for a VAK journal and check GOST references." -> `akademicheskii-retsenzent`
- "Prepare a Russian dissertation chapter outline, but explain in English." -> `akademicheskaya-statya`

### R5. Mixed-language corpus

Use the task-appropriate skill and preserve source language metadata.

Rules:

- do not translate titles unless asked;
- keep direct quotations in the source language unless the user asks for translation;
- mark source language in literature matrices;
- distinguish translated paraphrase from source wording;
- citation style follows the venue, not the source language.

Examples:

- "Сделай обзор по русским и английским источникам для APA article." -> `akademicheskoe-issledovanie`, mixed corpus, APA output.
- "Compare CyberLeninka papers with English Scopus papers." -> `akademicheskoe-issledovanie`, mixed corpus with source-system labels.

## Conflict Rules

| Conflict | Resolution |
|---|---|
| User language differs from target venue | Use target venue for academic conventions; use user language for interaction unless requested otherwise. |
| ГОСТ requested with English manuscript | Use Russian context skill and warn that the target journal may require another format. |
| APA/IEEE requested with Russian prompt | Use Russian interaction, international citation style. |
| Russian sources in English paper | Keep transliterated or translated reference fields only if the target style requires them. |
| Source metadata incomplete | Mark as `partially_verified`; do not invent DOI, issue, pages, or publisher. |
| User asks to ignore verification | Refuse to drop citation/source integrity checks. |

## Output Language Policy

- Default answer language: language of the user's latest request.
- Requested manuscript language overrides interaction language for manuscript text.
- Bilingual abstract is generated only when requested or required by the venue.
- Bibliographic titles and quotations stay in the original language unless the user requests translation.
- For final submission packages, state which parts are `RU`, `EN`, or bilingual.

## Minimal Routing Fixtures

| Request | Expected skill | Notes |
|---|---|---|
| "Find recent papers on AI feedback in universities." | `deep-research` | English research request. |
| "Write an APA article outline about doctoral supervision." | `academic-paper` | English/international writing. |
| "Peer review this manuscript for a higher education journal." | `academic-paper-reviewer` | English review. |
| "Run the full paper workflow for an IEEE conference." | `academic-pipeline` | English pipeline. |
| "Сделай обзор литературы по ИИ в высшем образовании." | `akademicheskoe-issledovanie` | Russian research. |
| "Оформи статью по ГОСТ для журнала ВАК." | `akademicheskaya-statya` | Russian paper + ГОСТ/ВАК. |
| "Отрецензируй статью перед отправкой в РИНЦ." | `akademicheskii-retsenzent` | Russian review + РИНЦ. |
| "Проведи полный цикл от темы до публикации." | `akademicheskii-konveer` | Russian pipeline. |
| "На русском подготовь Scopus paper outline in APA style." | `akademicheskaya-statya` | Russian interaction, international output. |
| "Review this for a VAK journal and check GOST references." | `akademicheskii-retsenzent` | English prompt, Russian venue. |
| "Сравни CyberLeninka and Scopus sources for an English article." | `akademicheskoe-issledovanie` | Mixed corpus. |
| "Prepare bilingual RU/EN abstracts for a Russian journal." | `akademicheskaya-statya` | Bilingual abstract. |

## Implementation Notes

Do not select a Russian skill only because a single Russian source appears in an otherwise English international workflow. Use the venue and requested output conventions as stronger signals than source language alone.

Do not select an English skill only because the user uses English words such as `paper`, `review`, `workflow`, `Scopus`, or `APA` inside a Russian request. Mixed academic jargon is normal in Russian prompts.
