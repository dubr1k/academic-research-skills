# Russian Source Verification

Use this reference before synthesizing Russian or mixed RU/EN literature.

## Required Metadata

For every source, capture:

- `source_language`: `ru`, `en`, or `mixed`;
- `source_system`: Scopus, Web of Science, Crossref, OpenAlex, eLIBRARY, РИНЦ, CyberLeninka, user-provided, or local corpus;
- bibliographic fields: authors, title, venue, year, volume/issue, pages, DOI/URL when verified;
- access status: full text, abstract only, metadata only, inaccessible;
- verification label: `verified_current`, `peer_reviewed_verified`, `partially_verified`, `non_peer_reviewed`, `inaccessible`, `not_verified`, or `unverified`.
- current status evidence: exact database/list/source checked, date or recency marker when available, and unresolved evidence needed.

## Source Verification Ladder

Use this verification ladder before synthesis:

| Label | Use when | Required action |
|---|---|---|
| `verified_current` | The source exists, bibliographic fields match, and the claimed status is current. | May use as evidence if it supports the claim. |
| `peer_reviewed_verified` | Peer-review or journal status is verified, but current list status is not the main claim. | Use with status caveat if ВАК/РИНЦ currency is relevant. |
| `partially_verified` | Source exists, but one or more fields/status claims remain unresolved. | Carry `metadata_missing` and ask for or search missing evidence. |
| `not_verified` | Source, DOI, journal status, or citation fields are only user-provided or shape-plausible. | Do not use as support until verified. |
| `inaccessible` | The source likely exists, but needed full text or metadata cannot be accessed. | Use only for existence/context, not claim support. |
| `non_peer_reviewed` | Source is confirmed but not peer-reviewed or not scholarly. | Use only as object of analysis or low-weight context. |
| `unverified` | Verification has not been attempted or evidence is too weak to classify. | Block final bibliography and evidence claims. |

## Russian Source Rules

- eLIBRARY record existence does not prove ВАК status.
- РИНЦ presence does not prove peer review or methodological quality.
- CyberLeninka open access does not prove peer-review status.
- DOI must be checked against the source or a trusted index.
- Missing pages, issue, city, publisher, or DOI stay `metadata_missing`.
- Scopus/Web of Science indexing does not prove that a Russian venue requirement is satisfied.
- A current ВАК-list claim needs current list evidence; old screenshots, user memory, and eLIBRARY cards are not enough.
- In mixed corpora, `source_language` follows the source, while output language follows the user's deliverable request.

## Blocking Conditions

Do not use a source as evidence when:

- the source cannot be found;
- the claim requires full text but only metadata is available;
- journal status is asserted but not verified;
- DOI or pages are guessed;
- two similar citations appear merged into one reference.
- `source_language` or `source_system` is dropped during synthesis;
- CyberLeninka availability is treated as peer-review proof;
- a shape-valid DOI is accepted without resolver or publisher evidence.

## Handoff Requirements

Every source-verification handoff must preserve:

- final verification label;
- `metadata_missing` fields;
- `not_verified` identifiers or status claims;
- access channel vs index status;
- claim support verdict;
- evidence still needed before final ГОСТ/APA/IEEE/Vancouver/Chicago bibliography.
