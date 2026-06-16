# Bilingual Example: Russian Prompt For Scopus/APA

Request:

```text
На русском помоги подготовить outline статьи для Scopus по академической мотивации студентов, стиль APA, источники английские.
```

Expected skill: `akademicheskaya-statya`

Routing:

- User interaction is Russian.
- Target venue and citation style are international.
- Russian skill is used for planning and explanation, while APA and Scopus constraints are preserved.

Expected checks:

- do not switch to ГОСТ because the prompt is Russian;
- keep APA output constraints explicit;
- use international source priority;
- mark manuscript/output language separately from interaction language.
