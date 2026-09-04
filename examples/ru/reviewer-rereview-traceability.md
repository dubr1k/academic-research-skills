# RU Reviewer Example: Re-Review Traceability

Request:

```text
Проверь, закрыли ли авторы замечания рецензента после доработки. Есть исходная рецензия, response letter и новая версия статьи с номерами страниц.
```

Expected skill: `akademicheskii-retsenzent`

Routing:

- Russian re-review task with original comments, author responses, and revised manuscript evidence.
- The reviewer verifies the manuscript text instead of accepting the response letter as proof.
- The output must keep machine-readable status values.

Expected checks:

- classify every comment in persuasion-blind Phase 2A as `FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `MADE_WORSE`, or `CANNOT_VERIFY`;
- require page/section-level manuscript evidence before marking any comment `FULLY_ADDRESSED`;
- keep `residual_gap` and its magnitude visible for `PARTIALLY_ADDRESSED` items;
- mark promised but unlocated fixes as `CANNOT_VERIFY`, then compare the response letter only in Phase 2B;
- keep journal-index status separate from manuscript quality if venue claims appear in the response.
