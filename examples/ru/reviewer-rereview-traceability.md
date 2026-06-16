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

- classify every comment as `addressed`, `partially_addressed`, `not_addressed`, or `needs_evidence`;
- require page/section-level evidence before marking any comment `addressed`;
- keep residual risks visible for `partially_addressed` items;
- mark promised but unlocated fixes as `needs_evidence`;
- keep journal-index status separate from manuscript quality if venue claims appear in the response.
