# RU Research Example: ГОСТ/ВАК Literature Review

Request:

```text
Сделай обзор литературы по цифровой трансформации высшего образования для статьи ВАК. Нужны русские и англоязычные источники, список по ГОСТ.
```

Expected skill: `akademicheskoe-issledovanie`

Routing:

- Russian request with ВАК and ГОСТ requirements.
- Mixed corpus is allowed, but source language and source system must be tracked.
- Russian context controls bibliography verification.

Expected checks:

- classify sources as `peer_reviewed_verified`, `partially_verified`, `non_peer_reviewed`, `inaccessible`, or `unverified`;
- use `verified_current` only when the current source/status evidence is actually checked;
- keep unresolved DOI, issue, pages, and journal status as `not_verified` or `metadata_missing`;
- distinguish eLIBRARY record presence from ВАК or peer-review status;
- do not invent DOI, issue, pages, or publisher;
- return a literature matrix with `source_language` and `source_system`.
