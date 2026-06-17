# RU Venue Example: Dissertation Council Review

Request:

```text
Проведи предварительную рецензию главы диссертации и автореферата перед диссертационным советом: проверь научную новизну, положения на защиту и ответы на замечания.
```

Expected skill: `akademicheskii-retsenzent`

Routing:

- Russian dissertation council context routes to the Russian reviewer adapter.
- Stable venue marker: диссертационный совет.
- Review criteria differ from a journal article review even when ВАК publications are also mentioned.
- The reviewer remains read-only unless the user explicitly asks for revision drafting.

Expected checks:

- evaluate dissertation council criteria: novelty, defended propositions, methodological validity, reliability, theoretical/practical significance, and publication alignment;
- distinguish comments on the dissertation text, автореферат, and publication package;
- require traceability for every reviewer concern and preserve concern IDs through revision;
- require page/section evidence before marking any issue `addressed`;
- use `needs_evidence` when the response letter claims a fix but the manuscript location is missing.
