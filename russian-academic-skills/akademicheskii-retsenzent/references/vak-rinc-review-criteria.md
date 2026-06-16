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
- Апробация/publications: visible only if provided; missing evidence is `needs_evidence`.
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

- Fatal methodology or fabricated-source issues block `Accept`.
- Unsupported novelty blocks strong recommendation.
- A review must include issue location, severity, why it matters, and required fix.
- In re-review, a comment cannot be marked resolved without page/section-level manuscript evidence.

## Re-Review Status Taxonomy

Use only these status values:

| Status | Definition | Evidence requirement |
|---|---|---|
| `addressed` | The revised manuscript closes the concern. | Page/section/paragraph evidence is present. |
| `partially_addressed` | The revision closes part of the concern but leaves a residual issue. | Evidence and residual risk are both stated. |
| `not_addressed` | The manuscript does not change or the change does not answer the concern. | Missing or contradictory manuscript evidence is stated. |
| `needs_evidence` | The response claims a fix but the revised manuscript location is missing, inaccessible, or too vague. | Request exact page/section evidence before closure. |
