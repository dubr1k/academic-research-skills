# Bilingual Example: CyberLeninka And Scopus Corpus

Request:

```text
Сравни статьи из CyberLeninka и Scopus по теме онлайн-обучения, итог нужен для English article.
```

Expected skill: `akademicheskoe-issledovanie`

Routing:

- Mixed RU/EN corpus with Russian and international source systems.
- Research skill keeps source metadata while the final synthesis targets an English article.

Expected checks:

- preserve `source_language` and `source_system`;
- treat CyberLeninka as access context, not automatic peer-review proof;
- keep access channel, index status, and claim support as separate fields;
- carry `metadata_missing` and `not_verified` source fields into the English synthesis handoff;
- use international output constraints for the final article;
- do not translate titles or quotations unless requested.
