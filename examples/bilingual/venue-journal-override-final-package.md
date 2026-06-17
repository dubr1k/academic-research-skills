# Bilingual Venue Example: Journal Override Final Package

Request:

```text
Собери финальный bilingual package для российского журнала: статья на русском, English title/abstract/keywords, список литературы по APA из guidelines журнала, плюс проверка ГОСТ-конфликта.
```

Expected skill: `akademicheskii-konveer`

Routing:

- Russian venue with bilingual deliverables routes to the Russian pipeline adapter.
- `final_package_mode: bilingual` because Russian manuscript files and English-facing metadata are both required.
- APA is the final citation style only if the journal override is evidenced by author guidelines.

Expected checks:

- carry `output_language: ru`, `source_language`, `citation_style: journal_override`, and `final_package_mode: bilingual` through finalization;
- record Citation Style Decision: default ГОСТ, journal override APA, final style APA, and evidence source;
- include Russian manuscript, English title/abstract/keywords, bibliography style decision, disclosures, and submission checklist;
- run Stage 4.5 final integrity before final package assembly;
- do not revert the bibliography to ГОСТ or drop English metadata because the venue is Russian.
