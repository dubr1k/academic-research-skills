# RU Venue Example: ВАК Journal Submission Package

Request:

```text
Подготовь submission package для статьи в журнал из перечня ВАК: основной текст на русском, список литературы по требованиям журнала, аннотация и сведения об авторах.
```

Expected skill: `akademicheskaya-statya`

Routing:

- Russian journal venue and ВАК signal route to the Russian writing adapter.
- Default citation style is ГОСТ unless the journal author guidelines define a journal override.
- The task is final-package preparation, not source search, unless missing metadata is found.

Expected checks:

- confirm the current ВАК venue requirement and ask for the journal author guidelines before final formatting;
- record Citation Style Decision: default ГОСТ, journal override if present, final style, and evidence;
- preserve Russian manuscript components: title, abstract, keywords, funding/COI/ethics statements, author information, and submission checklist;
- keep `metadata_missing` for pages, issue, publisher, DOI, or access date until evidence is provided;
- do not fabricate bibliographic metadata or silently force ГОСТ when the journal override requires APA, IEEE, Vancouver, Chicago, or a local style sheet.
