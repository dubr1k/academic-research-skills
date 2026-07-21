# Literature Matrix Template

| citation_key | Source language | Source system | Bibliographic record | Search date/bounds | Nearest prior work | Cache/live status | ref_retrieval_method | read_scope / PDF preflight | Current status evidence | Verification label | Claim supported | Limitations |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | ru/en/mixed | eLIBRARY/РИНЦ/CyberLeninka/Scopus/etc. | Authors, title, venue, year, issue, pages, DOI/URL | Date, databases, queries, languages | Citation key or explicit none-found-within-search | fresh/stale/live-revalidated | API/manual_pdf/web/local | intended vs actual scope; sidecar verdict | Database/list checked, date/recency, unresolved status evidence | verified_current / peer_reviewed_verified / partially_verified / not_verified / non_peer_reviewed / inaccessible / unverified | Specific claim, not a broad topic | Missing metadata, access limits, status caveat |

## ГОСТ Draft Entry

```text
Автор А. А. Название статьи // Название журнала. - Год. - Т. X, N Y. - С. xx-yy. - DOI: ...
```

## Notes

- Replace unknown fields with `metadata_missing`.
- Keep Russian titles in Russian unless translation is requested.
- Keep English titles in English unless the target venue requires translation or transliteration.
- Keep `not_verified` identifiers and status claims visible until they are resolved.
- Treat CyberLeninka as an access channel and record the journal/index status separately.
- Do not move a source into final bibliography until required fields are verified or explicitly marked `metadata_missing`.
- Do not use stale cache, abstract-only access, or missing PDF preflight as page-level claim support.
- Treat novelty as search-bounded; preserve the nearest prior work and all search limits.
