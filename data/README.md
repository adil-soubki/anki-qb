# Data Directory

This directory contains your Quiz Bowl data files organized in subdirectories.

## Directory Structure

```
data/
├── qbreader/          # QBReader database files
│   ├── bonuses.json
│   └── tossups.json
└── ygk/               # NAQT "You Gotta Know" HTML files
    └── *.html
```

## Required Files

### 1. QBReader Database Files (`qbreader/` subdirectory)

Two JSON files from the QBReader database in JSON lines format:

- **qbreader/bonuses.json** - Bonus questions (one JSON object per line)
- **qbreader/tossups.json** - Tossup questions (one JSON object per line)

Each file should have one JSON object per line with the following structure:

**bonuses.json** (example line):
```json
{
  "leadin_sanitized": "This author wrote...",
  "parts_sanitized": ["Part 1 text", "Part 2 text", "Part 3 text"],
  "answers_sanitized": ["Answer 1", "Answer 2", "Answer 3"]
}
```

**tossups.json** (example line):
```json
{
  "question_sanitized": "This work features...",
  "answer_sanitized": "The Great Gatsby"
}
```

### 2. NAQT "You Gotta Know" HTML Files (`ygk/` subdirectory)

Downloaded HTML files from NAQT's "You Gotta Know" series should follow this naming pattern:

```
https___www_naqt_com_you_gotta_know_<category>_html.html
```

For example:
- `ygk/https___www_naqt_com_you_gotta_know_short_story_authors_html.html`
- `ygk/https___www_naqt_com_you_gotta_know_british_monarchs_html.html`
- `ygk/https___www_naqt_com_you_gotta_know_works_of_horror_fiction_html.html`

## How to Obtain the Files

### QBReader Data

Visit the QBReader website or API to download the question database. The data should be in JSON lines format where each line is a valid JSON object.

### NAQT Articles

Visit https://www.naqt.com/you-gotta-know/ to view the articles.

The original notebook included an AppleScript for scraping these articles from Safari. However, you can also:
1. Manually download the HTML files using your browser's "Save Page As" feature
2. Use a web scraping tool of your choice (respecting NAQT's terms of service)
3. Use the provided AppleScript (macOS only) from the original notebook

**Note**: Make sure you have permission to use this content and respect NAQT's copyright and terms of service.

## File Structure

Once you've added all files, your data directory should look like:

```
data/
├── README.md (this file)
├── qbreader/
│   ├── bonuses.json
│   ├── tossups.json
│   └── ... (other QBReader files)
└── ygk/
    ├── https___www_naqt_com_you_gotta_know_short_story_authors_html.html
    ├── https___www_naqt_com_you_gotta_know_british_monarchs_html.html
    └── ... (more HTML files)
```

## .gitignore

The data files are gitignored by default to avoid committing large files and potentially copyrighted content.
