from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from pyforge.analysis import analyze, funding_by_category, top_funded
from pyforge.io.readers import read_file
from pyforge.io.writers import export
from pyforge.pipeline import add_funding_tier, normalize_country, run_pipeline

app = typer.Typer(name="pyforge", help="PyForge — Startup Data Analyzer")
console = Console()


def _funding(v: float) -> str:
    return f"${v:,.0f}"


@app.command()
def load(file_path: str = typer.Argument(..., help="Path to CSV or JSON file")):
    """Load and display startups from a file."""
    try:
        startups = read_file(file_path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    table = Table(title=f"Startups — {Path(file_path).name}", show_lines=False)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Name", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Funding", justify="right", style="green")
    table.add_column("Employees", justify="right")
    table.add_column("Country")
    table.add_column("Profitable", justify="center")

    for s in startups:
        table.add_row(
            str(s.id),
            s.name,
            s.category,
            _funding(s.funding_usd),
            str(s.employees),
            s.country,
            "[green]Yes[/green]" if s.is_profitable else "[red]No[/red]",
        )

    console.print(table)
    console.print(f"[dim]{len(startups)} startups loaded.[/dim]")


@app.command()
def stats(file_path: str = typer.Argument(..., help="Path to CSV or JSON file")):
    """Show complete analysis for a startup dataset."""
    try:
        startups = read_file(file_path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    result = analyze(startups)

    # Summary panel
    console.rule("[bold]Summary[/bold]")
    console.print(f"  Total startups:    {result.total_startups}")
    console.print(f"  Total funding:     {_funding(result.total_funding)}")
    console.print(f"  Avg funding:       {_funding(result.avg_funding)}")
    console.print(f"  Avg employees:     {result.avg_employees}")
    console.print(f"  Profitable:        {result.profitable_count} ({result.profitable_percentage:.1f}%)")

    # By category
    console.rule("[bold]By Category[/bold]")
    cat_table = Table(show_header=True)
    cat_table.add_column("Category", style="cyan")
    cat_table.add_column("Count", justify="right")
    cat_table.add_column("Total Funding", justify="right", style="green")
    fbc = funding_by_category(startups)
    for cat, count in sorted(result.categories.items(), key=lambda x: -x[1]):
        cat_table.add_row(cat, str(count), _funding(fbc.get(cat, 0.0)))
    console.print(cat_table)

    # Top 5 funded
    console.rule("[bold]Top 5 Funded[/bold]")
    top_table = Table(show_header=True)
    top_table.add_column("Name", style="bold")
    top_table.add_column("Category", style="cyan")
    top_table.add_column("Funding", justify="right", style="green")
    top_table.add_column("Country")
    for s in top_funded(startups, n=5):
        top_table.add_row(s.name, s.category, _funding(s.funding_usd), s.country)
    console.print(top_table)


@app.command()
def convert(
    input_path: str = typer.Argument(..., help="Source file (.csv or .json)"),
    output_path: str = typer.Argument(..., help="Destination file (.csv, .json, or .md)"),
):
    """Convert a startup file between CSV, JSON, and Markdown formats."""
    try:
        startups = read_file(input_path)
        export(startups, output_path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    console.print(
        f"[green]Converted[/green] {len(startups)} startups: "
        f"[dim]{input_path}[/dim] → [bold]{output_path}[/bold]"
    )


@app.command()
def pipeline(file_path: str = typer.Argument(..., help="Path to CSV or JSON file")):
    """Run the enrichment pipeline (funding tier + country normalization)."""
    try:
        startups = read_file(file_path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    from dataclasses import asdict
    raw = [asdict(s) for s in startups]
    records = run_pipeline(raw, transformations=[add_funding_tier, normalize_country])

    # Show enriched table
    table = Table(title="Pipeline Output", show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Funding Tier", style="magenta")
    table.add_column("Country")
    table.add_column("Funding", justify="right", style="green")

    for r in records:
        table.add_row(
            r["name"],
            r["category"],
            r.get("funding_tier", "—"),
            r["country"],
            _funding(r["funding_usd"]),
        )
    console.print(table)

    # Tier distribution
    console.rule("[bold]Tier Distribution[/bold]")
    tier_counts: dict[str, int] = {}
    for r in records:
        tier = r.get("funding_tier", "Unknown")
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    dist_table = Table(show_header=True)
    dist_table.add_column("Tier", style="magenta")
    dist_table.add_column("Count", justify="right")
    dist_table.add_column("Percentage", justify="right")
    total = len(records)
    tier_order = ["Pre-seed", "Seed", "Series A", "Series B", "Series C+"]
    for tier in tier_order:
        count = tier_counts.get(tier, 0)
        if count:
            dist_table.add_row(tier, str(count), f"{count / total * 100:.1f}%")
    console.print(dist_table)
    console.print(f"[dim]{total} records processed.[/dim]")
