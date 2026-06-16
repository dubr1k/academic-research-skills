# Bilingual Example: Mixed Source Verification Handoff

Request:

```text
Собери source-verification handoff для русских статей из CyberLeninka/eLIBRARY и англоязычных Scopus papers. Итоговый обзор будет на английском, но русские названия источников не переводить.
```

Expected skill: `akademicheskoe-issledovanie`

Routing:

- Mixed RU/EN corpus with Russian and international source systems.
- Russian context controls local verification; international output constraints control the later synthesis.
- Source language and output language are separate fields.

Expected checks:

- preserve `source_language` and `source_system` for every source;
- keep CyberLeninka as an access channel and Scopus/eLIBRARY/РИНЦ as separate status signals;
- mark unresolved DOI, pages, issue, journal status, or source match as `metadata_missing` or `not_verified`;
- state which sources can support claims now and which need more evidence before synthesis;
- do not silently translate Russian titles, merge similar citations, or treat index presence as claim support.

