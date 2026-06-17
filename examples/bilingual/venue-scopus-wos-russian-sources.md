# Bilingual Venue Example: Scopus/WoS Article With Russian Sources

Request:

```text
На русском помоги проверить русские источники для English article в Scopus/WoS журнал: часть источников из eLIBRARY, часть из CyberLeninka, итоговая статья на английском.
```

Expected skill: `akademicheskoe-issledovanie`

Routing:

- Russian interaction language plus international Scopus/WoS output routes to the Russian research adapter with international output constraints.
- `output_language: en` for the article plan or source matrix notes intended for the English manuscript.
- `source_language: [ru, en]` must survive the handoff to writing.

Expected checks:

- classify Russian sources by source_system: eLIBRARY, РИНЦ, ВАК, CyberLeninka, DOI, publisher, Scopus, WoS, or other;
- preserve original Russian titles and add translated/transliterated fields only if the target style requires them;
- distinguish CyberLeninka access copies from peer-reviewed publisher records;
- flag sources whose English-language reference entry needs transliteration, translation, or missing metadata review;
- do not infer Scopus/WoS suitability from Russian index status or silently translate source titles without a separate field.
