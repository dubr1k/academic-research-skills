# ВАК/РИНЦ Review Criteria

Use this reference for Russian journal, ВАК, РИНЦ, dissertation council, and pre-submission reviews.

## Journal-Index Status Is Not Manuscript Quality

Record venue/index facts separately from the quality judgment.
Stable marker: journal-index status must never be treated as manuscript quality.

| Field | Meaning | Review use |
|---|---|---|
| `current_vak` | Journal is currently presented by the user as ВАК-listed or official evidence is supplied | Submission-context signal only; still review novelty, rigor, and evidence. |
| `rinc_indexed` | Journal/source has РИНЦ indexing evidence | Indexing signal only; not proof of peer review or manuscript quality. |
| `elibrary_record` | eLIBRARY record exists | Metadata/access signal only; not proof of ВАК status. |
| `international_indexed` | Scopus/Web of Science/other international index evidence is supplied | Venue visibility signal only; not proof of fit or rigor. |
| `not_verified` | Status is claimed but evidence is missing/currentness is unknown | Keep as caveat; do not infer compliance. |
| `not_applicable` | Review is manuscript-only or no venue claim is relevant | Omit venue-based recommendation. |

## Core Criteria

Evaluate explicitly:

- scientific novelty;
- theoretical significance;
- practical significance;
- reliability and validity of results;
- fit with specialty passport when provided;
- bibliography quality and source status;
- method-to-claim alignment;
- clarity of contribution;
- absence of unsupported broad claims.

## Review Context Criteria

### ВАК Article Review

- Novelty: the manuscript states what is new relative to existing literature and Russian specialty context.
- Theoretical significance: concepts, model, classification, or explanation are advanced beyond description.
- Practical significance: application, implementation, policy, or professional use follows from the evidence.
- Reliability: data, methods, sampling, validation, and limitations are sufficient for the claims.
- Specialty passport fit: checked only when the user provides a specialty/passport.
- Bibliography: relevant sources are current enough for the field and source statuses are not conflated.

### Dissertation Council Review

- Dissertation linkage: article contribution maps to dissertation topic, aim, tasks, and positions for defense.
- Апробация/publications: visible only if provided; missing evidence is evidence-state `evidence_missing`, а не re-review verdict.
- Personal contribution: distinguish author contribution from group/project background.
- Reliability and validity: evaluate data provenance, procedure, reproducibility, and limitation handling.
- Specialty passport fit: claims and terminology match the provided specialty area.
- Council-facing risk: note issues that could weaken pre-defense, official opponent review, or council discussion.

### International Journal Review

Stable marker: international journal review.

- Fit/scope: topic, article type, audience, and contribution match the target journal if supplied.
- Originality: contribution is framed for the international field, not only local relevance.
- Method transparency: data, measures, ethics, analysis, limitations, and reproducibility are inspectable.
- Literature integration: Russian and international sources are synthesized rather than listed.
- Claims: conclusions are conservative and supported by results.
- Reporting expectations: data availability, ethics, funding/COI, and AI disclosure are flagged when relevant.

## Venue Caveats

- РИНЦ presence is not ВАК compliance.
- eLIBRARY metadata is not a quality guarantee.
- CyberLeninka access is not a peer-review guarantee.
- If the user needs current ВАК status, require an official list or journal instructions.
- Do not let positive index status override weak manuscript quality.
- Do not let unknown index status become a manuscript-quality criticism.

## Decision Constraints

- Machine decision contract uses only `Accept`, `Minor Revision`, `Major Revision`, or `Reject`; более свободные редакционные формулировки остаются пояснением, а не пятым token.
- Fatal methodology or fabricated-source issues block `Accept`.
- Unsupported novelty blocks strong recommendation.
- A review must include issue location, severity, why it matters, and required fix.
- In re-review, a comment cannot be marked resolved without page/section-level manuscript evidence.

## Role-Scoped Finding Contract

- D1 belongs to methodology; D2 to domain; D3 to Devil's Advocate plus methodology; D4 to perspective; D5/D6 to EIC.
- ВАК/РИНЦ review is an overlay for D2/D6, not an additional panel seat.
- Ineligible dimension: `score: not_assessed` without `abstain_reason`. Eligible but not applicable: `not_assessed` with `abstain_reason`.
- Findings require `severity`, `confidence`, `competence_basis`, and typed anchor `text|table|figure|equation|dataset|absence`; `absence` records inspected scope.
- Empty findings require a `Coverage Receipt`; `Top Blocking Issues` contains 0–3 evidence-backed items.

## Re-Review Status Taxonomy

Use only these status values:

| Status | Definition | Evidence requirement |
|---|---|---|
| `FULLY_ADDRESSED` | The revised manuscript closes the concern against the pre-committed criterion. | Typed page/section/paragraph evidence is present. |
| `PARTIALLY_ADDRESSED` | The revision closes part of the concern but leaves a residual issue. | Evidence, `residual_gap`, and residual magnitude are stated. |
| `NOT_ADDRESSED` | The manuscript does not change or the change does not answer the criterion. | Missing or contradictory manuscript evidence is stated. |
| `MADE_WORSE` | The revision degrades the concern's subject relative to the original manuscript. | Evidence anchors in the original and revised manuscripts are stated. |
| `CANNOT_VERIFY` | Evidence or comparison base is insufficient. | Record a concrete reason and remain fail-closed. |
