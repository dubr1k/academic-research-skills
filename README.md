# Русские академические skills для Claude Code и Opencode

[![Upstream](https://img.shields.io/badge/upstream-Imbad0202%2Facademic--research--skills-blue)](https://github.com/Imbad0202/academic-research-skills)
[![Snapshot](https://img.shields.io/badge/snapshot-v3.12.0%20%2F%20175f79b-lightgrey)](https://github.com/Imbad0202/academic-research-skills/commit/175f79bcca4467949fa94e410c25823bd574f687)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

Русскоязычная адаптация идей из [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills) для научной работы в Claude Code и Opencode.

Этот fork сохраняет upstream-проект и добавляет отдельный пакет [`russian-academic-skills/`](russian-academic-skills/) с четырьмя skills:

| Skill | Назначение | Типичный результат |
|---|---|---|
| `akademicheskoe-issledovanie` | Research, поиск источников, обзор литературы, fact-check, systematic review | Research brief, матрица источников, claim-check таблица, PRISMA-style протокол |
| `akademicheskaya-statya` | План, структура, черновик, аннотация, оформление и revision научной статьи | Paper blueprint, outline, draft, revision roadmap, disclosure |
| `akademicheskii-retsenzent` | Независимая рецензия, peer review, methodology check, re-review | Review report, editorial decision, major/minor issues, roadmap правок |
| `akademicheskii-konveer` | Полный цикл research -> paper -> review -> revision -> finalization | Стадийный pipeline с checkpoint-ами и integrity gates |

Оригинальная upstream-документация доступна в исходном репозитории: [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills).

> Это не официальный перевод upstream. Это русскоязычная адаптация для Claude Code / Opencode workflows. Автор upstream: Cheng-I Wu. Лицензия источника: CC BY-NC 4.0.

---

## Зачем это нужно

Обычные LLM-подсказки для академической работы часто ломаются одинаково: модель выдумывает источники, делает обзор литературы без search strategy, пишет статью до проверки claims, дает слишком мягкую рецензию или превращает русский научный текст в набор канцелярских AI-клише.

Эти skills задают агенту более строгий workflow:

- отделять research, writing, review и full pipeline;
- проверять источники до синтеза;
- явно маркировать подтвержденное, спорное и непроверенное;
- не выдумывать DOI, журналы и библиографические записи;
- использовать ГОСТ/APA/IEEE/Vancouver/Chicago по запросу;
- учитывать ВАК, РИНЦ, eLIBRARY, CyberLeninka и русскоязычные требования;
- проводить рецензию через severity, location, why it matters и required fix;
- не скрывать limitations, funding, COI и AI disclosure.

Главный принцип inherited from upstream: AI is your copilot, not the pilot.

---

## Быстрая установка для Claude Code

```bash
git clone https://github.com/<your-github>/academic-research-skills.git
cd academic-research-skills
mkdir -p ~/.claude/skills
cp -R russian-academic-skills/* ~/.claude/skills/
```

Добавьте routing в `~/.claude/CLAUDE.md`:

```markdown
## Русские академические skills

Перед ответом на академические запросы в русском или английском языке загружай matching skill.

| Intent | Skill |
|---|---|
| Поиск источников, research, literature review, fact-check | `akademicheskoe-issledovanie` |
| Написание статьи, план, структура, черновик, abstract, оформление | `akademicheskaya-statya` |
| Рецензия, peer review, methodology check, pre-submission review | `akademicheskii-retsenzent` |
| Полный цикл или 2+ academic intents сразу | `akademicheskii-konveer` |

Если skill registry в текущей сессии не видит новые skills, прочитай `~/.claude/skills/<skill>/SKILL.md` напрямую и следуй ему.
```

Перезапустите Claude Code или начните новую сессию, чтобы registry увидел новые skills.

---

## Быстрая установка для Opencode

```bash
git clone https://github.com/<your-github>/academic-research-skills.git
cd academic-research-skills
mkdir -p ~/.config/opencode/skills
cp -R russian-academic-skills/* ~/.config/opencode/skills/
```

Добавьте routing в `~/.config/opencode/AGENTS.md` или project-level `AGENTS.md`:

```markdown
## Русские академические skills

Перед ответом, планированием, поиском, письмом или делегацией проверяй текущий запрос пользователя на academic intent.

| Intent | Skill | Триггеры |
|---|---|---|
| Source search, research, literature review, fact-check | `akademicheskoe-issledovanie` | `исследование`, `найди источники`, `обзор литературы`, `fact-check`, `systematic review` |
| Academic writing, paper plan, draft, abstract, formatting | `akademicheskaya-statya` | `напиши статью`, `научная статья`, `план статьи`, `аннотация`, `оформи по ГОСТ` |
| Review, peer review, methodology check | `akademicheskii-retsenzent` | `рецензия`, `отрецензируй`, `проверь статью`, `peer review`, `methodology check` |
| Full pipeline or multiple academic intents | `akademicheskii-konveer` | `полный цикл`, `от темы до статьи`, `research to paper`, `full pipeline` |

Правила выбора: один intent -> соответствующий skill; 2+ intents -> `akademicheskii-konveer`; узкий one-step запрос не превращай в полный конвейер. Если registry кэширован и не видит новый skill, прочитай `~/.config/opencode/skills/<skill>/SKILL.md` напрямую.
```

---

## Как выбирать skill

### 1. Исследование и источники

Загружайте `akademicheskoe-issledovanie`, если пользователь пишет:

```text
Найди источники по теме X.
Сделай обзор литературы.
Проверь эти claims и DOI.
Собери systematic review protocol.
Помоги сузить исследовательский вопрос.
```

Режимы: `socratic`, `quick`, `full`, `lit-review`, `fact-check`, `systematic-review`, `review`.

### 2. Написание статьи

Загружайте `akademicheskaya-statya`, если пользователь пишет:

```text
Напиши план статьи.
Собери структуру IMRaD.
Напиши аннотацию и keywords.
Переработай черновик по замечаниям.
Оформи список литературы по ГОСТ.
```

Skill не должен выдумывать источники. Если корпуса литературы нет, сначала нужен research step.

### 3. Рецензирование

Загружайте `akademicheskii-retsenzent`, если пользователь пишет:

```text
Отрецензируй статью перед отправкой.
Проверь методологию и статистику.
Смоделируй peer review.
Проверь, закрыты ли замечания после revision.
```

Рецензент read-only по отношению к рукописи: он выдает critique и roadmap, но не переписывает статью, пока пользователь явно не просит revision mode.

### 4. Полный конвейер

Загружайте `akademicheskii-konveer`, если пользователь пишет:

```text
Проведи полный цикл от темы до статьи.
Сделай research to paper.
Подготовь публикацию с нуля.
Есть черновик и замечания, доведи до финальной версии.
```

Конвейер определяет entry point и ведет по стадиям: Research -> Write -> Integrity -> Review -> Revise -> Re-review -> Final Integrity -> Finalize -> Process Summary.

---

## Примеры запросов

```text
Сделай быстрый обзор литературы по применению LLM в оценивании студенческих работ. Нужны 8-12 надежных источников и ограничения доказательств.
```

Ожидаемый routing: `akademicheskoe-issledovanie`, режим `lit-review` или `quick`.

```text
Я хочу писать про ИИ в образовании, но тема слишком широкая. Помоги сузить исследовательский вопрос.
```

Ожидаемый routing: `akademicheskoe-issledovanie`, режим `socratic`.

```text
На основе research brief сделай структуру статьи для журнала ВАК.
```

Ожидаемый routing: `akademicheskaya-statya`, режим `plan` или `outline-only`.

```text
Отрецензируй рукопись как строгий reviewer: найди major issues, methodology risks и desk-reject signals.
```

Ожидаемый routing: `akademicheskii-retsenzent`, режим `full`.

```text
У меня есть тема и список источников. Проведи полный цикл до публикационного пакета.
```

Ожидаемый routing: `akademicheskii-konveer`.

---

## Отличия от upstream

Upstream `academic-research-skills` — большой Claude Code plugin/suite с командами `/ars-*`, агентами, схемами, lint-скриптами и многоязычной документацией.

Этот fork добавляет компактный русскоязычный слой:

- русские trigger phrases;
- routing для Claude Code и Opencode;
- Opencode-style orchestration через `task()` вместо Claude-style agent references;
- ГОСТ/ВАК/РИНЦ/eLIBRARY/CyberLeninka considerations;
- русский anti-AI-cliche check;
- отдельный full-pipeline skill для выбора стадии и передачи материалов между research, writing и review.

---

## Обновление от upstream

Адаптация зафиксирована на snapshot:

```text
175f79bcca4467949fa94e410c25823bd574f687
v3.12.0, 2026-06-08
```

Если upstream обновился:

1. подтяните upstream changes;
2. проверьте изменения в `deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`;
3. вручную перенесите релевантные идеи в `russian-academic-skills/*/SKILL.md`;
4. обновите строку `Upstream snapshot` в каждом русском skill;
5. проверьте routing examples в этом README.

---

## Лицензия и attribution

Оригинальный проект:

```text
Academic Research Skills
Author: Cheng-I Wu
Repository: https://github.com/Imbad0202/academic-research-skills
License: Creative Commons Attribution-NonCommercial 4.0 International
Copyright (c) 2026 Cheng-I Wu
```

Эта адаптация распространяется на условиях, совместимых с upstream license: **CC BY-NC 4.0**. Некоммерческое использование, распространение и адаптация разрешены при сохранении attribution и указании изменений.

Attribution format:

```text
Based on Academic Research Skills by Cheng-I Wu
https://github.com/Imbad0202/academic-research-skills
Russian Claude Code / Opencode adaptation: this fork
```

Не используйте этот fork для коммерческих целей без отдельного разрешения правообладателя upstream.

---

## Проверка после установки

После копирования skills и routing rules попробуйте четыре запроса:

```text
Найди источники для обзора литературы по теме X.
Напиши план научной статьи по теме X.
Отрецензируй эту статью перед отправкой.
Проведи полный цикл от темы до статьи.
```

Ожидаемое поведение: агент должен загрузить соответствующий skill или, если registry кэширован, прочитать `SKILL.md` напрямую и следовать его протоколу.
