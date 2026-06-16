# RU Paper Example: ГОСТ Source Types

Request:

```text
Оформи список литературы по ГОСТ: журнальная статья, монография, автореферат диссертации, доклад конференции и веб-страница. У части источников нет страниц, города и даты обращения.
```

Expected skill: `akademicheskaya-statya`

Routing:

- Russian writing and citation-formatting task.
- ГОСТ is the requested default, but every entry must be typed before formatting.
- Missing metadata must remain visible instead of being guessed.

Expected checks:

- classify each entry as journal article, monograph, dissertation abstract, conference paper, or web source;
- apply the matching ГОСТ pattern only after source type is identified;
- mark missing pages, issue, city, publisher, institution, page count, DOI, URL, or access date as `metadata_missing`;
- keep Russian and English titles in their source language unless the journal requires translation or transliteration;
- do not invent bibliographic fields to make the list look complete.

