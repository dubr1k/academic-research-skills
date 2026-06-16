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
- separate РИНЦ presence from ВАК compliance;
- provide issue locations and required fixes;
- do not rewrite the manuscript inside the review.
