# Russian Source Verification

Use this reference before synthesizing Russian or mixed RU/EN literature.

## Required Metadata

For every source, capture:

- `source_language`: `ru`, `en`, or `mixed`;
- `source_system`: Scopus, Web of Science, Crossref, OpenAlex, eLIBRARY, РИНЦ, CyberLeninka, user-provided, or local corpus;
- bibliographic fields: authors, title, venue, year, volume/issue, pages, DOI/URL when verified;
- access status: full text, abstract only, metadata only, inaccessible;
- verification label: `peer_reviewed_verified`, `partially_verified`, `non_peer_reviewed`, `inaccessible`, or `unverified`.

## Russian Source Rules

- eLIBRARY record existence does not prove ВАК status.
- РИНЦ presence does not prove peer review or methodological quality.
- CyberLeninka open access does not prove peer-review status.
- DOI must be checked against the source or a trusted index.
- Missing pages, issue, city, publisher, or DOI stay `metadata_missing`.

## Blocking Conditions

Do not use a source as evidence when:

- the source cannot be found;
- the claim requires full text but only metadata is available;
- journal status is asserted but not verified;
- DOI or pages are guessed;
- two similar citations appear merged into one reference.
