# Anki Quiz Bowl

Generate Anki flashcards from NAQT "You Gotta Know" articles and Quiz Bowl questions using LLM-powered prompts.

## Overview

This project helps Quiz Bowl players study more effectively by:
1. Parsing NAQT's "You Gotta Know" articles to extract key topics and terms
2. Finding related tossup and bonus questions from the QBReader database
3. Using LLMs (Google Gemini) to generate optimized Anki flashcards with difficulty ratings

## Project Structure

```
anki-qb/
├── src/anki_qb/           # Main package
│   ├── __init__.py        # Package exports
│   ├── config.py          # Configuration management
│   ├── parsing.py         # HTML parsing for NAQT articles
│   ├── search.py          # QBReader database search
│   ├── prompts.py         # LLM prompt templates
│   ├── llm.py            # LLM interaction (Gemini)
│   ├── formatters.py     # Data formatting utilities
│   └── text_utils.py     # Text normalization
├── data/                  # Data files (you add these)
│   ├── qbreader/          # QBReader database
│   │   ├── bonuses.json
│   │   └── tossups.json
│   └── ygk/               # NAQT "You Gotta Know" HTML files
│       └── *.html
├── examples/              # Example usage scripts
└── tests/                 # Tests
```

## Setup

### 1. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 2. Set Up Data Files

Place the following files in the `data/` directory:

- **qbreader/bonuses.json** - QBReader bonus questions (JSON lines format)
- **qbreader/tossups.json** - QBReader tossup questions (JSON lines format)
- **ygk/*.html** - Downloaded NAQT "You Gotta Know" articles

See `data/README.md` for more details on obtaining these files.

### 3. Configure API Key

Create a `.env` file from the example template:
```bash
cp .env.example .env
```

Then edit `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your-api-key-here
```

Alternatively, you can set it as an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or pass it directly in your code (see examples).

## Usage

### Running the Example Script

To run the included example script:
```bash
uv run --env-file .env -- examples/generate_flashcards.py
```

This will:
1. Load environment variables from `.env`
2. Parse the example NAQT article
3. Generate flashcards using the LLM
4. Export to CSV for Anki import

### Basic Example (Python Code)

```python
import pandas as pd
from anki_qb import (
    initialize_client,
    set_config,
    Config,
    parse_ygk_page,
    format_ygk_prompts,
    ask_llm,
    read_markdown,
)
from anki_qb.prompts import PROMPT_CHATGPT_SHORT

# 1. Initialize configuration
config = Config(
    data_dir="data",
    gemini_api_key="your-api-key"
)
set_config(config)
initialize_client(config.gemini_api_key)

# 2. Load QBReader data
bonuses = pd.read_json(config.bonuses_path, lines=True)
tossups = pd.read_json(config.tossups_path, lines=True)

# 3. Parse NAQT article and generate prompts
category = "short_story_authors"  # Example category
html_path = config.html_path(category)

# Create a function to get QBR data with loaded dataframes
from functools import partial
from anki_qb.llm import get_qbr_data
get_qbr_data_fn = partial(get_qbr_data, bonuses_df=bonuses, tossups_df=tossups)

# Generate prompts for all topics in the article
prompts = format_ygk_prompts(str(html_path), PROMPT_CHATGPT_SHORT, get_qbr_data_fn)

# 4. Generate flashcards for first topic
result = ask_llm(prompts[0])

# 5. Parse markdown table
flashcards_df = read_markdown(result)
flashcards_df = flashcards_df.sort_values("Difficulty")

# 6. Export to CSV for Anki import
flashcards_df.to_csv("flashcards.csv", index=False)
```

### Available Prompt Templates

The package includes several prompt templates in `anki_qb.prompts`:

- `PROMPT_CHATGPT_SHORT` - Concise, optimized prompt (recommended)
- `PROMPT_CHATGPT` - Detailed version with examples
- `PROMPT_ADIL` - Quiz Bowl-specific with difficulty ratings
- `PROMPT_FNX_18` - Based on spaced repetition best practices
- `PROMPT_LM_SHERLOCK` - Simplified approach

You can also create your own custom prompts using these as templates.

## Features

### Text Normalization
Handles HTML entities, Unicode normalization, fancy quotes, and whitespace cleanup.

### Flexible Parsing
Automatically detects and parses both `<ul>` and `<dl>` formatted NAQT articles.

### Smart Search
Case-insensitive regex search across tossup and bonus questions with automatic term sanitization.

### Difficulty Ratings
Generated flashcards include difficulty ratings (1-5) to help prioritize study:
- 1: Core facts critical for basic understanding
- 2-3: Common and intermediate clues
- 4-5: Advanced "power" clues and specialist knowledge

## Development

### Running Tests
```bash
uv run pytest
```

### Code Formatting
```bash
uv run ruff check src/
uv run ruff format src/
```

## Data Sources

- **NAQT "You Gotta Know"**: https://www.naqt.com/you-gotta-know/
- **QBReader**: Database of Quiz Bowl questions (tossups and bonuses)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
