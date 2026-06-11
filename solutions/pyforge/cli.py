import typer
from dataclasses import asdict
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .analysis import analyze, top_funded, funding_by_category
from .io.readers import read_file
from .io.writers import export
from .pipeline import run_pipeline, add_funding_tier, normalize_country

app = typer.Typer(
    name="pyforge",
    help="PyForge — Startup Data Analyzer CLI",
    add_completion=False,
)

console = Console()


@app.command()
def load(
    file_path: str = typer.Argument(..., help="Path to CSV or JSON file"),
):
    """Load and display startup data from a file."""
    path = Path(file_path)
    startups = read_file(path)

    table = Table(title=f"Startups from {path.name}")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Funding", style="green", justify="right")
    table.add_column("Employees", justify="right")
    table.add_column("Country")
    table.add_column("Profitable", justify="center")

    for s in startups:
        table.add_row(
            str(s.id),
            s.name,
            s.category,
            f"${s.funding_usd:,.0f}",
            str(s.employees),
            s.country,
            "Yes" if s.is_profitable else "No",
        )

    console.print(table)
    console.print(f"\n[bold]{len(startups)} startups loaded.[/bold]")


@app.command()
def stats(
    file_path: str = typer.Argument(..., help="Path to data file"),
):
    """Show analysis statistics."""
    startups = read_file(file_path)
    result = analyze(startups)

    console.print("\n[bold underline]Analysis Results[/bold underline]\n")
    console.print(f"  Total startups: [bold]{result.total_startups}[/bold]")
    console.print(f"  Total funding: [green]${result.total_funding:,.0f}[/green]")
    console.print(f"  Average funding: [green]${result.avg_funding:,.0f}[/green]")
    console.print(f"  Average employees: [cyan]{result.avg_employees}[/cyan]")
    console.print(
        f"  Profitable: [bold]{result.profitable_count}[/bold] "
        f"({result.profitable_percentage:.1f}%)"
    )

    console.print("\n[bold]By Category:[/bold]")
    for cat, count in sorted(result.categories.items()):
        console.print(f"  {cat}: {count}")

    top = top_funded(startups, 5)
    console.print("\n[bold]Top 5 Funded:[/bold]")
    for i, s in enumerate(top, 1):
        console.print(f"  {i}. {s.name} — [green]${s.funding_usd:,.0f}[/green]")

    by_cat = funding_by_category(startups)
    console.print("\n[bold]Funding by Category:[/bold]")
    for cat, total in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
        console.print(f"  {cat}: [green]${total:,.0f}[/green]")


@app.command()
def convert(
    input_path: str = typer.Argument(..., help="Source file path"),
    output_path: str = typer.Argument(
        ..., help="Destination file path (.csv, .json, or .md)"
    ),
):
    """Convert data between formats (CSV, JSON, Markdown)."""
    startups = read_file(input_path)
    export(startups, output_path)
    console.print(
        f"[green]Done.[/green] Exported {len(startups)} startups to {output_path}"
    )


@app.command()
def pipeline(
    file_path: str = typer.Argument(..., help="Path to data file"),
):
    """Run the data processing pipeline."""
    startups = read_file(file_path)
    raw_data = [asdict(s) for s in startups]

    console.print("[bold]Running pipeline...[/bold]\n")
    console.print("  Step 1: Reading records...")
    console.print("  Step 2: Validating with Pydantic...")
    console.print("  Step 3: Applying transformations...")

    results = run_pipeline(
        raw_data,
        transformations=[add_funding_tier, normalize_country],
    )

    console.print(
        f"\n[green]Done.[/green] Pipeline completed: "
        f"{len(results)} valid records processed."
    )

    tiers: dict[str, int] = {}
    for r in results:
        tier = r.get("funding_tier", "Unknown")
        tiers[tier] = tiers.get(tier, 0) + 1

    console.print("\n[bold]Funding Tier Distribution:[/bold]")
    for tier, count in sorted(tiers.items()):
        console.print(f"  {tier}: {count}")
