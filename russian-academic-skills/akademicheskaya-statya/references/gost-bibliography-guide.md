# ГОСТ Bibliography Guide

Use this guide for Russian article, dissertation chapter, and ВАК/РИНЦ submissions when the venue does not provide stricter local rules.

## Source Type Decision

Identify the source type before formatting. Do not force every Russian source
into a journal article pattern.

Supported source types:

- journal article;
- monograph;
- dissertation abstract;
- conference paper;
- web source.

If the source type is uncertain, mark `source_type_uncertain` and ask for the
missing bibliographic evidence before final formatting.

## Journal Article Entry

Required fields:

- authors;
- article title;
- journal title;
- year;
- volume and issue when available;
- page range;
- DOI or URL only when verified.

Pattern:

```text
Автор А. А. Название статьи // Название журнала. - Год. - Т. X, N Y. - С. xx-yy. - DOI: ...
```

## Monograph Entry

Required fields:

- author or editor;
- title;
- city;
- publisher;
- year;
- page count or cited pages.

Pattern:

```text
Автор А. А. Название книги. - Город: Издательство, Год. - N с.
```

## Dissertation Abstract Entry

Required fields:

- author;
- dissertation abstract title;
- degree type or specialty when known;
- city;
- institution;
- year;
- page count.

Pattern:

```text
Автор А. А. Название: автореф. дис. ... - Город, Год. - N с.
```

## Conference Paper Entry

Required fields:

- authors;
- paper title;
- conference title;
- city or venue when available;
- year;
- page range;
- publisher or organizer when required by the journal.

Pattern:

```text
Автор А. А. Название доклада // Название конференции. - Город, Год. - С. xx-yy.
```

## Web Source Entry

Required fields:

- author or organization;
- page title;
- site title or publisher;
- URL;
- access date when required;
- publication/update date when available.

Pattern:

```text
Автор/Организация. Название страницы. - URL: ... (дата обращения: DD.MM.YYYY).
```

## Journal Override

Default to ГОСТ Р 7.0.5-2008 for Russian context only when the venue does not
give stricter instructions. A journal override wins over the default.

When a Russian journal requests APA, IEEE, Vancouver, Chicago, or another local
variant:

- preserve the explicit journal override;
- state the conflict between default ГОСТ and the requested style;
- request or use the journal author guidelines for final formatting;
- do not silently convert back to ГОСТ;
- keep Russian venue constraints separate from citation-style constraints.

## Integrity Rules

- Do not invent DOI, pages, issue, city, publisher, or page count.
- If metadata is incomplete, mark it as `metadata_missing`.
- If a journal requires a local ГОСТ variant, follow the journal instructions and state that variant.
- If a journal override requires APA, IEEE, Vancouver, or Chicago, follow that style while preserving Russian venue requirements.
