# RU Reviewer Example: ВАК/РИНЦ Pre-Submission Review

Request:

```text
Отрецензируй статью перед отправкой в журнал РИНЦ и проверь, выглядит ли она достаточно сильной для ВАК.
```

Expected skill: `akademicheskii-retsenzent`

Routing:

- Russian peer-review task with РИНЦ and ВАК signals.
- Review stays read-only unless the user explicitly asks for revision writing.

Expected checks:

- evaluate novelty, theoretical significance, practical significance, reliability, bibliography, and method-to-claim alignment;
- separate journal-index status (`current_vak`, `rinc_indexed`, `elibrary_record`, `not_verified`) from manuscript quality;
- distinguish ВАК article, dissertation council, and international journal review criteria when the user provides the context;
- provide issue locations and required fixes;
- require page/section-level traceability before any reviewer comment is marked resolved;
- do not rewrite the manuscript inside the review.
