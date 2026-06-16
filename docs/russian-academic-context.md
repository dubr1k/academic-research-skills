# Russian Academic Context

This guide defines the Russian academic expectations that the adapter layer must preserve across research, writing, review, and pipeline workflows.

## Scope

Use Russian context rules when a request mentions any of these signals:

- ГОСТ Р 7.0.5-2008 or local bibliography rules;
- ВАК, РИНЦ, eLIBRARY, CyberLeninka, dissertation council, автореферат, ВКР;
- Russian journal submission, Russian department requirements, or Russian-language manuscript;
- mixed RU/EN corpus where Russian source systems affect verification.

The target venue controls academic conventions. The user's language controls interaction language unless the user asks otherwise.

## Source Verification

Classify Russian and mixed sources before synthesis:

| Label | Meaning | Allowed use |
|---|---|---|
| `peer_reviewed_verified` | Journal/source status and metadata are checked. | Main evidence. |
| `partially_verified` | Source exists, but issue/pages/DOI/status are incomplete. | Use with caveat. |
| `non_peer_reviewed` | Conference notes, institutional pages, gray literature, or non-refereed material. | Context only unless task requires it. |
| `inaccessible` | Metadata exists, but full text cannot be checked. | Do not use for precise claims. |
| `unverified` | User-provided or found citation cannot be confirmed. | Do not treat as evidence. |

For eLIBRARY and РИНЦ, distinguish article existence from journal quality. A record in eLIBRARY is not by itself proof that the journal is ВАК-listed, peer-reviewed, or methodologically strong.

For CyberLeninka, treat open access as access status, not as peer-review status. Check journal, year, issue, pages, authors, and DOI separately.

## Anti-Hallucination Rules

- Do not invent DOI, issue, pages, publisher, city, or journal status.
- Mark missing metadata as `metadata_missing`, not as an approximate value.
- Do not merge two similar Russian references into one citation.
- Do not translate titles inside bibliography unless the target style requires translation or transliteration.
- Keep source-language quotations unchanged unless the user asks for translation.

## ГОСТ Bibliography Checklist

For article entries, require at least:

- author names;
- article title;
- journal title;
- year;
- volume/issue when available;
- page range;
- DOI or URL only if verified.

Typical pattern:

```text
Автор А. А. Название статьи // Название журнала. - Год. - Т. X, N Y. - С. xx-yy. - DOI: ...
```

For books, require:

- author or editor;
- title;
- city;
- publisher;
- year;
- page count or cited pages when available.

Typical pattern:

```text
Автор А. А. Название книги. - Город: Издательство, Год. - N с.
```

If a journal has its own ГОСТ variant, follow the journal instructions and state the variant.

## ВАК/РИНЦ Review Criteria

For Russian journal or dissertation-facing review, explicitly evaluate:

- scientific novelty;
- theoretical significance;
- practical significance;
- reliability and validity of results;
- fit with specialty passport, if provided;
- sufficiency and quality of bibliography;
- method-to-claim alignment;
- absence of unsupported broad claims;
- compliance with journal or dissertation council requirements.

Do not equate РИНЦ presence with ВАК compliance. If the user needs ВАК status, require the current journal list or an official source.

## Russian Academic Style Risks

Flag these patterns when they weaken the text:

- `в современном мире` without concrete time frame;
- `актуальность темы обусловлена` without evidence;
- `трудно переоценить роль` as unsupported emphasis;
- `проблемы и перспективы` without a defined corpus;
- `комплексный подход` without components;
- `повышение эффективности` without an efficiency metric;
- repeated throat-clearing such as `в данной статье рассматривается`.

When flagging cliches, preserve useful disciplinary terms and only revise wording that hides a claim, method, or evidence gap.

## Mixed RU/EN Workflows

For mixed corpora:

- keep `source_language` in literature matrices;
- keep `source_system` such as Scopus, Web of Science, eLIBRARY, РИНЦ, CyberLeninka;
- route by task and target venue, not by the presence of one Russian or English source;
- use international citation style when the target is Scopus/IEEE/APA/Vancouver;
- use ГОСТ when the target is a Russian journal, department, or dissertation council.

## Response Traceability

For reviewer response and re-review, maintain a traceability table:

| Reviewer comment | Author response | Manuscript location | Status | Residual risk |
|---|---|---|---|---|
| Required change or concern. | What changed or why not. | Section/page/paragraph. | `addressed`, `partially_addressed`, `not_addressed`, `unverifiable`. | Remaining issue. |

Do not accept author response as proof. Verify the revised manuscript text.

## Quality Fixture Coverage

Lightweight eval fixtures should cover these recurring risks:

- ГОСТ bibliography gaps such as missing pages, issue, city, publisher, or verified DOI;
- source hallucination through fake DOI, merged references, or invented metadata;
- Russian academic cliche patterns that hide relevance, method, evidence, or contribution gaps;
- ВАК/РИНЦ conflation, especially treating eLIBRARY or РИНЦ presence as ВАК compliance;
- revision traceability failures where reviewer response is accepted without manuscript evidence.
