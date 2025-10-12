#!/usr/bin/env python3
"""
Example script to generate flashcards from NAQT articles.

This script demonstrates how to:
1. Set up configuration
2. Load QBReader data
3. Parse NAQT articles
4. Generate flashcards using an LLM
5. Export results to CSV for Anki import
"""

import os
from functools import partial
from pathlib import Path

import pandas as pd

from anki_qb import (
    initialize_client,
    set_config,
    Config,
    format_ygk_prompts,
    ask_llm,
    read_markdown,
)
from anki_qb.llm import get_qbr_data
from anki_qb.prompts import PROMPT_CHATGPT_SHORT


def main():
    """Generate flashcards from NAQT articles."""

    # 1. Initialize configuration
    print("Initializing configuration...")
    config = Config(
        data_dir=os.getenv("ANKI_QB_DATA_DIR", "data"),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
    )
    set_config(config)
    initialize_client(config.gemini_api_key)

    # Validate that data files exist
    try:
        config.validate()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure you have the required data files in the data/ directory.")
        print("See data/README.md for instructions.")
        return 1

    # 2. Load QBReader data
    print(f"Loading QBReader data from {config.data_dir}...")
    bonuses = pd.read_json(config.bonuses_path, lines=True)
    tossups = pd.read_json(config.tossups_path, lines=True)
    print(f"  Loaded {len(bonuses)} bonuses and {len(tossups)} tossups")

    # 3. Choose a category to process
    # You can change this to any category you have HTML files for
    category = "short_story_authors"
    print(f"\nProcessing category: {category}")

    html_path = config.html_path(category)
    if not html_path.exists():
        print(f"Error: HTML file not found at {html_path}")
        print(f"\nAvailable HTML files in {config.data_dir}:")
        for html_file in config.data_dir.glob("*.html"):
            print(f"  - {html_file.name}")
        return 1

    # 4. Generate prompts
    print("Generating prompts...")
    get_qbr_data_fn = partial(get_qbr_data, bonuses_df=bonuses, tossups_df=tossups)
    prompts = format_ygk_prompts(str(html_path), PROMPT_CHATGPT_SHORT, get_qbr_data_fn)
    print(f"  Generated {len(prompts)} prompts")

    # 5. Generate flashcards for each topic
    print("\nGenerating flashcards...")
    all_flashcards = []

    for i, prompt in enumerate(prompts, 1):
        print(f"  Processing topic {i}/{len(prompts)}...")

        # Ask LLM to generate flashcards
        result = ask_llm(prompt)

        # Parse the markdown table response
        try:
            flashcards_df = read_markdown(result)
            flashcards_df['topic'] = f"{category}_topic_{i}"
            all_flashcards.append(flashcards_df)
            print(f"    Generated {len(flashcards_df)} flashcards")
        except Exception as e:
            print(f"    Error parsing response: {e}")
            continue

    # 6. Combine and sort all flashcards
    if all_flashcards:
        combined_df = pd.concat(all_flashcards, ignore_index=True)

        # Sort by difficulty (if available)
        if 'Difficulty' in combined_df.columns:
            combined_df = combined_df.sort_values('Difficulty')

        # 7. Export to CSV
        output_file = f"flashcards_{category}.csv"
        combined_df.to_csv(output_file, index=False)
        print(f"\n✓ Successfully generated {len(combined_df)} flashcards!")
        print(f"✓ Saved to: {output_file}")
        print(f"\nYou can now import this CSV file into Anki.")

        # Show some statistics
        if 'Difficulty' in combined_df.columns:
            print("\nFlashcard distribution by difficulty:")
            print(combined_df['Difficulty'].value_counts().sort_index())

        return 0
    else:
        print("\nNo flashcards were generated. Please check your data files and try again.")
        return 1


if __name__ == "__main__":
    exit(main())
