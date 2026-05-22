from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(
    name="stie",
    help="Space Threat Intelligence Exchange CLI",
)
console = Console()


@app.command()
def submit(
    file: str = typer.Argument(..., help="Path to threat report JSON file"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """Submit a threat report to the exchange."""
    console.print(f"[yellow]Submitting report from {file}...[/yellow]")
    console.print("[red]Not yet implemented[/red]")


@app.command()
def get(
    report_id: str = typer.Argument(..., help="Report ID to retrieve"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """Retrieve a threat report by ID."""
    console.print(f"[yellow]Fetching report {report_id}...[/yellow]")
    console.print("[red]Not yet implemented[/red]")


@app.command()
def list_reports(
    limit: int = typer.Option(50, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset", "-o"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """List threat reports."""
    console.print("[red]Not yet implemented[/red]")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """Search threat reports."""
    console.print(f"[yellow]Searching for: {query}...[/yellow]")
    console.print("[red]Not yet implemented[/red]")


@app.command()
def keygen(
    output: str = typer.Option("stie-key", "--output", "-o", help="Output file prefix"),
):
    """Generate a new Ed25519 key pair."""
    from stie.crypto.keys import generate_key_pair, serialize_private_key, serialize_public_key

    priv, pub = generate_key_pair()
    priv_path = f"{output}.priv.pem"
    pub_path = f"{output}.pub.pem"

    with open(priv_path, "w") as f:
        f.write(serialize_private_key(priv))
    with open(pub_path, "w") as f:
        f.write(serialize_public_key(pub))

    console.print("[green]Generated key pair:[/green]")
    console.print(f"  Private key: {priv_path}")
    console.print(f"  Public key:  {pub_path}")


@app.command()
def sign(
    file: str = typer.Argument(..., help="Report JSON file to sign"),
    key: str = typer.Argument(..., help="Private key PEM file"),
):
    """Sign a threat report."""
    import json

    from stie.crypto.signing import create_signed_envelope

    with open(file) as f:
        report_data = json.load(f)
    with open(key) as f:
        private_key_pem = f.read()
    with open(key.replace(".priv.", ".pub.")) as f:
        public_key_pem = f.read()

    envelope = create_signed_envelope(report_data, private_key_pem, public_key_pem)
    output = file.replace(".json", ".signed.json")
    with open(output, "w") as f:
        json.dump(envelope, f, indent=2)

    console.print(f"[green]Signed report saved to: {output}[/green]")


@app.command()
def verify(
    file: str = typer.Argument(..., help="Signed report file to verify"),
):
    """Verify a signed threat report."""
    import json

    from stie.crypto.signing import verify_signed_envelope

    with open(file) as f:
        envelope = json.load(f)

    valid, fingerprint = verify_signed_envelope(envelope)
    if valid:
        console.print(f"[green]Signature VALID[/green] - Fingerprint: {fingerprint}")
    else:
        console.print("[red]Signature INVALID[/red]")


@app.command()
def peers(
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """List connected peers."""
    console.print("[yellow]Fetching peers...[/yellow]")
    console.print("[red]Not yet implemented[/red]")


@app.command()
def enrich(
    report_id: str = typer.Argument(..., help="Report ID to enrich"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """Enrich a threat report using AI."""
    console.print(f"[yellow]Enriching report {report_id}...[/yellow]")
    console.print("[red]Not yet implemented[/red]")


@app.command()
def qa(
    question: str = typer.Argument(..., help="Question to ask"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """Ask a question about threat reports."""
    console.print(f"[yellow]Asking: {question}...[/yellow]")
    console.print("[red]Not yet implemented[/red]")


@app.command()
def export(
    fmt: str = typer.Option("stix", "--format", "-f", help="Export format (stix, json, csv)"),
    output: str = typer.Option("threats.json", "--output", "-o"),
    server: str = typer.Option("http://localhost:8000", "--server", "-s"),
):
    """Export threat reports."""
    console.print("[red]Not yet implemented[/red]")


def main():
    app()


if __name__ == "__main__":
    main()
