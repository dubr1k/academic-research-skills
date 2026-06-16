# RU Research Example: Russian Source Verification Depth

Request:

```text
Проверь подборку русских источников для литературного обзора: часть есть в eLIBRARY, часть на CyberLeninka, у двух ссылок нет страниц и DOI. Нужно понять, что можно использовать как доказательство, а что оставить как непроверенное.
```

Expected skill: `akademicheskoe-issledovanie`

Routing:

- Russian research task with source verification as the primary deliverable.
- Russian context controls eLIBRARY, РИНЦ, CyberLeninka, DOI, and ГОСТ metadata handling.
- The output can stay in Russian, but the source matrix must preserve machine-readable status fields.

Expected checks:

- separate eLIBRARY record presence, РИНЦ indexing, current ВАК status, and peer-review evidence;
- treat CyberLeninka as an access channel, not as proof of peer review;
- classify every source as `verified_current`, `partially_verified`, `not_verified`, `inaccessible`, or `rejected`;
- mark missing issue, pages, DOI, city, publisher, or journal status as `metadata_missing`;
- keep unresolved `not_verified` fields visible in the handoff and final caveats.

