# Bilingual Example: Russian Journal With APA Override

Request:

```text
Пишу статью для российского журнала из перечня ВАК. Редакция требует список литературы в APA, а основной текст и аннотация на русском. Помоги подготовить citation plan и package checklist.
```

Expected skill: `akademicheskaya-statya`

Routing:

- Russian venue and Russian interaction language route to the Russian writing adapter.
- The requested APA style is retained; Russian language and ВАК do not establish a competing ГОСТ requirement.
- ВАК/РИНЦ venue constraints remain active even when bibliography style is APA.

Expected checks:

- record requested style, journal override, final style, and evidence for the APA requirement;
- do not flag an invented ГОСТ vs APA conflict; identify a mismatch only if a separate verified requirement actually conflicts;
- preserve Russian manuscript requirements: title, abstract, keywords, ВАК/РИНЦ checks, disclosure placeholders;
- ask for the author guidelines before final formatting if they are not provided;
- do not silently convert the bibliography back to ГОСТ.
