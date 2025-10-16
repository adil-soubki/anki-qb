#!/usr/bin/env python3
"""
Generate Anki flashcards from NAQT "You Gotta Know" articles.

This script processes YGK articles and generates flashcards using LLMs,
focusing on high-frequency clues from actual quiz bowl questions.

TODO:
    - Support generating flashcards from a term (or list of terms) that the
      user enters, not just terms that appear in ygk articles.
    - Should then search that term in the qbreader databse and tell the user
      how many hits it gets with some examples.
    - Finally after showing that should ask the user if they want to generate
      flashcards for that term or topic.
"""

import argparse
import os
import sys
from functools import partial
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from anki_qb import (
    Config,
    set_config,
    format_ygk_prompts,
    ask_llm,
    read_markdown,
)
from anki_qb.llm import get_qbr_data
from anki_qb.prompts import PROMPT_FREQUENCY_FOCUSED, PROMPT_CHATGPT_SHORT, PROMPT_CHATGPT

console = Console()


def list_categories(data_dir: Path) -> list[str]:
    """List all available YGK categories."""
    ygk_dir = data_dir / "ygk"
    if not ygk_dir.exists():
        return []

    categories = []
    for html_file in sorted(ygk_dir.glob("*.html")):
        # Extract category from filename
        name = html_file.stem
        if name.startswith("https___www_naqt_com_you_gotta_know_") and name.endswith("_html"):
            category = name.replace("https___www_naqt_com_you_gotta_know_", "").replace("_html", "")
            categories.append(category)

    return categories


def main():
    parser = argparse.ArgumentParser(
        description="Generate Anki flashcards from NAQT 'You Gotta Know' articles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate flashcards for a single category
  %(prog)s --category short_story_authors

  # Generate for all categories
  %(prog)s --all

  # Use a specific model
  %(prog)s --category modern_poets --model claude-3-5-sonnet

  # List available categories
  %(prog)s --list-categories
        """
    )

    parser.add_argument(
        "--category",
        help="YGK category to process (e.g., 'short_story_authors')"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all available YGK categories"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory for CSV files (default: output/)"
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="LLM model to use (default: gpt-4o-mini)"
    )
    parser.add_argument(
        "--prompt",
        choices=["frequency", "short", "detailed"],
        default="frequency",
        help="Prompt style: frequency-focused (default), short, or detailed"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Data directory (default: data/)"
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all available categories and exit"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Initialize configuration
    config = Config(data_dir=str(args.data_dir))
    set_config(config)

    # List categories if requested
    if args.list_categories:
        categories = list_categories(config.data_dir)
        if not categories:
            console.print("[red]No categories found in data/ygk/[/red]")
            return 1

        table = Table(title="Available YGK Categories")
        table.add_column("#", style="cyan")
        table.add_column("Category", style="green")

        for i, cat in enumerate(categories, 1):
            table.add_row(str(i), cat)

        console.print(table)
        console.print(f"\n[bold]Total: {len(categories)} categories[/bold]")
        return 0

    # Validate arguments
    if not args.category and not args.all:
        parser.error("Either --category or --all must be specified")

    if args.category and args.all:
        parser.error("Cannot specify both --category and --all")

    # Select prompt template
    prompt_map = {
        "frequency": PROMPT_FREQUENCY_FOCUSED,
        "short": PROMPT_CHATGPT_SHORT,
        "detailed": PROMPT_CHATGPT,
    }
    prompt_template = prompt_map[args.prompt]

    # Validate data files
    try:
        config.validate()
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\nPlease ensure you have the required data files.")
        console.print("See data/README.md for instructions.")
        return 1

    # Load QBReader data
    console.print(f"[bold]Loading QBReader data from {config.data_dir}...[/bold]")
    bonuses = pd.read_json(config.bonuses_path, lines=True)
    tossups = pd.read_json(config.tossups_path, lines=True)
    console.print(f"  Loaded {len(bonuses):,} bonuses and {len(tossups):,} tossups")

    # Determine categories to process
    if args.all:
        categories = list_categories(config.data_dir)
        if not categories:
            console.print("[red]No categories found![/red]")
            return 1
        console.print(f"\n[bold]Processing all {len(categories)} categories[/bold]")
    else:
        categories = [args.category]

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    # Process each category
    get_qbr_data_fn = partial(get_qbr_data, bonuses_df=bonuses, tossups_df=tossups, model=args.model)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:

        overall_task = progress.add_task(
            "[cyan]Processing categories...",
            total=len(categories)
        )

        for category in categories:
            html_path = config.html_path(category)

            if not html_path.exists():
                console.print(f"[yellow]⚠ Skipping {category}: file not found[/yellow]")
                progress.advance(overall_task)
                continue

            # Generate prompts
            try:
                prompts_with_metadata = format_ygk_prompts(str(html_path), prompt_template, get_qbr_data_fn)
            except Exception as e:
                console.print(f"[red]✗ Error parsing {category}: {e}[/red]")
                progress.advance(overall_task)
                continue

            # Generate flashcards for each topic
            all_flashcards = []
            topic_task = progress.add_task(
                f"[green]  {category}",
                total=len(prompts_with_metadata)
            )

            for i, (prompt, metadata) in enumerate(prompts_with_metadata, 1):
                try:
                    topic_label = metadata["label"]
                    sanitized_term = metadata["sanitized_term"]

                    # Ask LLM to generate flashcards
                    result = ask_llm(prompt, model=args.model)

                    # Parse the markdown table response
                    flashcards_df = read_markdown(result)
                    flashcards_df['category'] = category
                    flashcards_df['topic_name'] = topic_label
                    flashcards_df['topic_number'] = i
                    flashcards_df['search_term'] = sanitized_term
                    all_flashcards.append(flashcards_df)

                    if args.verbose:
                        console.print(f"    Topic {i}/{len(prompts_with_metadata)} ({topic_label}): {len(flashcards_df)} flashcards")

                except Exception as e:
                    if args.verbose:
                        console.print(f"    [yellow]Topic {i}/{len(prompts_with_metadata)} ({topic_label}): Error - {e}[/yellow]")

                progress.advance(topic_task)

            # Save flashcards for this category
            if all_flashcards:
                combined_df = pd.concat(all_flashcards, ignore_index=True)
                output_file = args.output / f"flashcards_{category}.csv"
                combined_df.to_csv(output_file, index=False)
                console.print(f"[green]✓ {category}: {len(combined_df)} flashcards → {output_file}[/green]")
            else:
                console.print(f"[yellow]⚠ {category}: No flashcards generated[/yellow]")

            progress.remove_task(topic_task)
            progress.advance(overall_task)

    console.print("\n[bold green]✓ Done![/bold green]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
