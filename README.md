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
│   ├── llm.py             # LLM interaction (Gemini)
│   ├── formatters.py      # Data formatting utilities
│   └── text_utils.py      # Text normalization
├── data/                  # Data files (you add these)
│   ├── qbreader/          # QBReader database
│   │   ├── bonuses.json
│   │   └── tossups.json
│   └── ygk/               # NAQT "You Gotta Know" HTML files
│       └── *.html
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

### 3. Configure LLM API Keys

This project uses the [llm](https://llm.datasette.io/) package, which supports multiple LLM providers.

Set up API keys for your preferred provider:

```bash
# For OpenAI (GPT models)
llm keys set openai

# For Anthropic (Claude models)
llm keys set anthropic

# For Google (Gemini models)
llm keys set gemini

# List available models
llm models
```

See the [llm documentation](https://llm.datasette.io/en/stable/setup.html) for more providers and setup details. Another option is to use a `.env` file to store your API and then pass it to scripts with `uv run`.

```bash
uv run --env-file .env -- bin/generate-flashcards.py --category [...]
```

## Usage

### Generate Flashcards (CLI)

The main way to use this project is via the `bin/generate-flashcards.py` script:

```bash
# List all available categories
uv run bin/generate-flashcards.py --list-categories

# Generate flashcards for a single category
uv run bin/generate-flashcards.py --category short_story_authors

# Generate for all categories (this will take a while!)
uv run bin/generate-flashcards.py --all

# Use a specific model
uv run bin/generate-flashcards.py --category modern_poets --model claude-3-5-sonnet

# Choose a different prompt style
uv run bin/generate-flashcards.py --category american_novels --prompt short

# Specify output directory
uv run bin/generate-flashcards.py --category ancient_philosophers --output my_flashcards/
```

**Available options:**
- `--category CATEGORY` - Process a specific YGK category
- `--all` - Process all available categories
- `--model MODEL` - LLM model to use (default: gpt-4o-mini)
- `--prompt {frequency,short,detailed}` - Prompt style (default: frequency)
- `--output DIR` - Output directory (default: output/)
- `--list-categories` - List all available categories
- `-v, --verbose` - Verbose output

Output CSV files can be imported directly into Anki.

### Python API Example

```python
import pandas as pd
from functools import partial
from anki_qb import (
    set_config,
    Config,
    format_ygk_prompts,
    ask_llm,
    read_markdown,
)
from anki_qb.llm import get_qbr_data
from anki_qb.prompts import PROMPT_CHATGPT_SHORT

# 1. Initialize configuration
config = Config(data_dir="data")
set_config(config)

# 2. Load QBReader data
bonuses = pd.read_json(config.bonuses_path, lines=True)
tossups = pd.read_json(config.tossups_path, lines=True)

# 3. Parse NAQT article and generate prompts
category = "short_story_authors"  # Example category
html_path = config.html_path(category)

# Create a function to get QBR data with loaded dataframes
get_qbr_data_fn = partial(get_qbr_data, bonuses_df=bonuses, tossups_df=tossups)

# Generate prompts for all topics in the article
prompts_with_metadata = format_ygk_prompts(str(html_path), PROMPT_CHATGPT_SHORT, get_qbr_data_fn)

# 4. Generate flashcards for first topic
prompt, metadata = prompts_with_metadata[0]
result = ask_llm(prompt)

# 5. Parse markdown table
flashcards_df = read_markdown(result)
flashcards_df = flashcards_df.sort_values("Difficulty")

# 6. Export to CSV for Anki import
flashcards_df.to_csv("flashcards.csv", index=False)
```

### Available Prompt Styles

The package includes several prompt templates in `anki_qb.prompts`:

- **`frequency`** (Default) - `PROMPT_FREQUENCY_FOCUSED` - Focuses on high-frequency clues that appear most often in actual quiz bowl questions. No difficulty ratings, just Question/Answer pairs. **Recommended for most users.**
- **`short`** - `PROMPT_CHATGPT_SHORT` - Concise prompt with difficulty ratings (1-5)
- **`detailed`** - `PROMPT_CHATGPT` - Detailed version with extensive examples and difficulty ratings

Legacy prompts also available:
- `PROMPT_ADIL` - Original Quiz Bowl-specific prompt with difficulty ratings
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

### Install Dev Dependencies

Development tools (pytest, ruff, ipdb, ipython) are in a separate dependency group:

```bash
uv sync --group dev
```

### Running Tests
```bash
uv run --group dev pytest
```

### Code Formatting
```bash
uv run --group dev ruff check src/
uv run --group dev ruff format src/
```

## Data Sources

- **NAQT "You Gotta Know"**: https://www.naqt.com/you-gotta-know/
- **QBReader**: Database of Quiz Bowl questions (tossups and bonuses)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
