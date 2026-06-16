# Bilingual Example: Russian Journal With APA Override

Request:

```text
Пишу статью для российского журнала из перечня ВАК. Редакция требует список литературы в APA, а основной текст и аннотация на русском. Помоги подготовить citation plan и package checklist.
```

Expected skill: `akademicheskaya-statya`

Routing:

- Russian venue and Russian interaction language route to the Russian writing adapter.
- The journal override makes APA the final citation style instead of default ГОСТ.
- ВАК/РИНЦ venue constraints remain active even when bibliography style is APA.

Expected checks:

- record default style, journal override, final style, and evidence for the APA requirement;
- flag ГОСТ vs APA as a style conflict resolved by the journal author guidelines;
- preserve Russian manuscript requirements: title, abstract, keywords, ВАК/РИНЦ checks, disclosure placeholders;
- ask for the author guidelines before final formatting if they are not provided;
- do not silently convert the bibliography back to ГОСТ.

