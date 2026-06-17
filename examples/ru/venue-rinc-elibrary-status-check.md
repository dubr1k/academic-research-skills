# RU Venue Example: РИНЦ/eLIBRARY Status Check

Request:

```text
Проверь, можно ли ссылаться на эти русские источники как на РИНЦ-публикации: часть есть в eLIBRARY, часть найдена через CyberLeninka.
```

Expected skill: `akademicheskoe-issledovanie`

Routing:

- Russian source verification task routes to the Russian research adapter.
- РИНЦ, eLIBRARY, CyberLeninka, and journal-index status are verification axes, not writing style decisions.
- Output language remains Russian unless the user requests an English evidence matrix.

Expected checks:

- separate eLIBRARY record presence, РИНЦ indexing, ВАК status, DOI, publisher page, and CyberLeninka access copy;
- require current status evidence for any `rinc_indexed` or ВАК claim;
- mark each source as `verified_current`, `partially_verified`, `not_verified`, `inaccessible`, or `rejected`;
- carry `metadata_missing` for issue, pages, DOI, publisher, or access date gaps;
- do not treat CyberLeninka access as peer-review evidence or eLIBRARY presence as proof of РИНЦ indexing.
