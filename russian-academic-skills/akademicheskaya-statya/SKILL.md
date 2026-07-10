---
name: akademicheskaya-statya
description: "Русскоязычный academic paper writing skill для Opencode. Используйте для планирования, структуры, черновика, аннотации, литературного обзора, ревизии, ответа рецензентам, проверки цитирования, ГОСТ/APA/IEEE/Vancouver оформления и disclosure научной статьи. Адаптировано из imbad0202/academic-research-skills под русский язык и Opencode task()."
version: "3.15.0-ru.1"
last_updated: "2026-07-10"
status: "active-russian-adapter"
data_access_level: "user_materials_and_verified_sources"
task_type: "writing"
depends_on:
  - "akademicheskoe-issledovanie"
upstream_snapshot: "ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c"
upstream_version: "v3.15.0"
upstream_date: "2026-07-08"
---

# Академическая статья

Русскоязычная адаптация идей `academic-paper` из `imbad0202/academic-research-skills` для Opencode. Skill помогает спланировать, написать, переработать и оформить научную статью или главу диссертации.

Источник адаптации: https://github.com/imbad0202/academic-research-skills
Upstream snapshot: `ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c` (`v3.15.0`, 2026-07-08).
Лицензия источника: Creative Commons Attribution-NonCommercial 4.0 International, Copyright (c) 2026 Cheng-I Wu.

Локальные материалы:

- `agents/gost_citation_agent.md` - агент проверки ГОСТ bibliography, citation consistency и пакета ВАК-статьи.
- `references/gost-bibliography-guide.md` - ГОСТ bibliography guide для статей и книг.
- `templates/vak-article-package.md` - шаблон пакета ВАК-статьи: аннотация, структура, checks.

## Когда использовать

Используйте skill, если пользователь просит:

- написать научную статью, главу, conference paper, policy brief;
- составить план, структуру, outline, IMRaD;
- написать аннотацию, abstract, keywords;
- подготовить литературный обзор как раздел статьи;
- переработать черновик или ответить рецензентам;
- проверить цитирование и список литературы;
- конвертировать стиль цитирования или формат;
- подготовить AI disclosure, funding, COI, author contribution.

Русские триггеры: `написать статью`, `научная статья`, `план статьи`, `структура статьи`, `аннотация`, `ключевые слова`, `литературный обзор`, `методология`, `обсуждение`, `ответ рецензентам`, `переработать статью`, `проверить цитаты`, `оформить по ГОСТ`, `оформить по APA`, `ВАК`, `РИНЦ`, `диссертация`, `ВКР`.

Не используйте этот skill для первичного исследования без задачи написать статью - загрузите `akademicheskoe-issledovanie`. Для независимой критической рецензии готового текста используйте `akademicheskii-retsenzent`.

## Режимы

| Режим | Когда | Итог |
|---|---|---|
| `plan` | Нужно подумать над статьей, но не писать сразу | Paper Blueprint, структура, аргумент, план источников |
| `outline-only` | Нужен только подробный план | Outline + evidence map + word allocation |
| `full` | Нужен полный черновик | Draft с разделами, цитированием, limitations и disclosure |
| `abstract-only` | Нужна аннотация | Русская и/или английская аннотация + keywords |
| `lit-review` | Нужен раздел обзора литературы | Тематический обзор + research gap |
| `revision` | Есть черновик и замечания | Revised draft + response-to-reviewers план |
| `revision-coach` | Есть хаотичные review comments | Revision Roadmap, приоритеты, R->A->C матрица |
| `citation-check` | Нужно проверить цитирование | Citation Audit Report |
| `format-convert` | Нужно изменить стиль/формат | ГОСТ/APA/IEEE/Vancouver/Chicago или MD/LaTeX/DOCX инструкции |
| `disclosure` | Нужно заявление об использовании AI | Venue-specific disclosure paragraph |

Если пользователь сомневается, начинайте с `plan`.

## Mode spectrum

- fidelity: `citation-check`, `format-convert`, `abstract-only`, `disclosure` - строгий шаблон и минимум творческих решений;
- balanced: `full`, `outline-only`, `revision-coach` - структура плюс экспертное письмо;
- originality: `plan` - сократическое планирование и поиск вклада до черновика.

Не смешивайте режимы без необходимости: если пользователь просит только citation-check, не переписывайте статью.

## Opencode orchestration

Используйте категории по типу работы:

```text
- планирование структуры и аргумента: task(category="writing")
- тяжелая логика методологии или causal claims: task(category="ultrabrain")
- поиск литературы: task(subagent_type="librarian", run_in_background=true)
- проверка локального корпуса: task(subagent_type="explore", run_in_background=true)
- ревизия по комментариям: task(category="writing")
- независимая критика черновика: task(subagent_type="oracle") или skill `akademicheskii-retsenzent`
```

Не используйте Claude-style `@agent`. Все параллельные блоки оформляйте через Opencode task fan-out.

### Phase boundary и write-scope guard (v3.15)

В hook-enabled Claude Code runtime deterministic PreToolUse write-scope guard ограничивает single-phase agents разрешенными deliverables. На Windows он требует Git Bash и рабочий Python; отсутствие Python должно безопасно отключать optional guard, а не блокировать основную prompt-driven работу. В Opencode, Codex и других runtimes без hook сохраняйте те же границы в контракте `task()` и выполняйте post-task diff check после делегации. Guard - дополнительное hardening, а не замена citation/claim audit.

Не разрешайте writing-agent менять review report, source-verification artifacts или pipeline state вне явно переданного write scope. При ambiguous cross-phase input сначала уточните режим.

## Процесс full-режима

### 0. Intake

Перед письмом уточните:

- тип текста: empirical / literature review / theoretical / case study / policy brief / conference paper;
- дисциплина и целевой журнал/конференция;
- язык основного текста;
- стиль цитирования: по умолчанию ГОСТ Р 7.0.5-2008 для русского контекста;
- объем;
- есть ли источники, данные, таблицы, рисунки;
- есть ли требования ВАК, РИНЦ, журнала или кафедры;
- нужны ли LaTeX/DOCX/PDF или достаточно Markdown.

Если пользователь не дает исходных материалов, не выдумывайте литературу. Сначала предложите запустить исследовательский этап.

### 1. Research/Literature

Если источники уже предоставлены, используйте их как основной корпус. Если источников нет, запустите `akademicheskoe-issledovanie` или `librarian` для поиска.

Выход:

- search strategy;
- source corpus;
- literature matrix;
- список проверенных и непроверенных источников.

### 2. Structure

Выберите структуру:

| Тип | Структура |
|---|---|
| empirical | IMRaD: Introduction, Methods, Results, Discussion |
| literature review | тематический обзор + synthesis + gaps |
| theoretical | проблема, теория, критика, расширение, следствия |
| case study | контекст, кейс, данные, анализ, lessons learned |
| policy brief | проблема, evidence, policy options, recommendations |
| conference paper | короткая версия с фокусом на вклад и метод |

Для русского текста используйте разделы:

1. Введение.
2. Обзор литературы.
3. Методология.
4. Результаты.
5. Обсуждение.
6. Заключение.
7. Список литературы.
8. Приложения при необходимости.

### 3. Argument Blueprint

Перед черновиком зафиксируйте:

- главный тезис;
- 3-5 основных claims;
- evidence для каждого claim;
- возможные возражения;
- ограничения;
- что статья добавляет к литературе.

Каждый claim должен иметь источник, данные пользователя или явную пометку `гипотеза/интерпретация`.

### 4. Drafting

Пишите разделами. Для каждого раздела проверяйте:

- цель раздела;
- соответствие outline;
- наличие источников;
- отсутствие неподдержанных обобщений;
- связь с главным тезисом;
- объем относительно плана.

Не используйте шаблонные AI-фразы: `важно отметить`, `в современном мире`, `данная тема является актуальной`, если они не несут фактической нагрузки.

### 5. Citation and Integrity

Проверяйте:

- все in-text citations есть в reference list;
- все reference list entries процитированы;
- DOI добавлен, если известен;
- нет вымышленных источников;
- числовые claims соответствуют источникам;
- старые источники оправданы как foundational или historical.

Для русского ГОСТ-оформления используйте как минимум поля:

```text
Автор(ы). Название статьи // Название журнала. - Год. - Т. X, N Y. - С. xx-yy. - DOI: ...
Автор(ы). Название книги. - Город: Издательство, Год. - N с.
```

Перед форматированием определите тип источника: journal article, monograph,
dissertation abstract, conference paper или web source. Если тип или поля
неполны, используйте `metadata_missing` / `source_type_uncertain`, а не
угадывайте страницы, выпуск, город, издательство, организацию или дату
обращения.

Если российский журнал задает journal override (APA, IEEE, Vancouver, Chicago,
локальный ГОСТ-вариант или собственный style sheet), инструкции журнала имеют
приоритет над default ГОСТ. Явно фиксируйте: default style, override, final
style и источник требования.

Если требуется строгая библиографическая точность, явно скажите, что нужен финальный ручной/библиотечный контроль по требованиям журнала.

### 6. Review and Revision

Перед финализацией выполните самопроверку:

- Originality;
- Methodological Rigor;
- Evidence Sufficiency;
- Argument Coherence;
- Writing Quality;
- Literature Integration;
- Significance and Impact.

Для review comments создайте Revision Roadmap:

| Comment | Category | Severity | Response strategy | Text change | Status |
|---|---|---|---|---|---|

Статусы:

- ACCEPTED;
- PARTIALLY_ACCEPTED;
- REVIEWER_DISAGREE;
- NEEDS_DATA;
- OUT_OF_SCOPE.

Нельзя соглашаться со всеми замечаниями механически. Если рецензент ошибается, аргументируйте отказ доказательно и профессионально.

## Обязательные включения

Для полноценной статьи проверьте наличие:

- limitations;
- data availability statement;
- ethics declaration, если применимо;
- conflict of interest statement;
- funding acknowledgment;
- author contributions/CRediT, если применимо;
- AI disclosure statement, если AI использовался;
- корректный список литературы.

## Качество письма

Требования:

- научный тон без канцелярской пустоты;
- разнообразный ритм предложений и абзацев;
- claims идут до объяснений, а не после длинных вступлений;
- переходы показывают логическую связь, а не просто `кроме того`;
- терминология дисциплины важнее универсального academic style;
- word count в пределах +/-10%, если задан.

### Russian AI-cliche check

Перед финалом удалите или обоснуйте шаблонные обороты:

- `в современном мире`, `в настоящее время`, `на сегодняшний день`, если не указана дата или период;
- `данная тема является актуальной`, если не названы факты актуальности;
- `трудно переоценить роль`, `важнейшее значение`, `необходимо отметить`, если это не несет claim;
- `комплексный подход`, `многогранная проблема`, `широкий спектр`, если не раскрыты компоненты;
- `позволяет повысить эффективность`, если нет метрики эффективности;
- `проблемы и перспективы`, если нет корпуса проблем и критериев перспектив;
- чрезмерные синонимические повторы: `исследование/работа/статья` в каждом предложении.

### Pattern checks

- Throat-clearing: раздел должен начинаться с claim, а не с `В данном разделе рассматривается...`.
- Uniform paragraph length: избегайте одинаковых абзацев по 4-5 предложений.
- Rule-of-three compulsion: не создавайте искусственные тройки аргументов, если структура материала другая.
- Mirror structure: не повторяйте одну синтаксическую рамку в каждом абзаце.
- Hedging discipline: `может`, `вероятно`, `предположительно` нужны только при реальной неопределенности.

## Анти-паттерны

- Выдумывать источники или DOI.
- Писать статью до подтверждения структуры и источников.
- Делать universal claims без доказательств.
- Добавлять новые разделы при revision без разрешения.
- Принимать все review comments без оценки.
- Скрывать limitations.
- Подгонять литературу под готовый тезис.

## Форматы вывода

Для `plan`:

```text
# Paper Blueprint
## Цель и вклад
## Тип статьи
## Research question
## Структура
## Claims and evidence map
## Риски
## Следующие шаги
```

Для `full`:

```text
# Черновик статьи
## Аннотация
## Ключевые слова
## Введение
## Обзор литературы
## Методология
## Результаты
## Обсуждение
## Заключение
## Ограничения
## Disclosure / Funding / COI
## Список литературы
```

Для `revision`:

```text
# Revision Roadmap
# Response to Reviewers
# Revised Sections
# Remaining Limitations
```
