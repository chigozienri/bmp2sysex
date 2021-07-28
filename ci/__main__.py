import click
import subprocess


@click.group()
def cli():
    pass


@cli.command(name="test", help="Run the tests")
def test():
    cmd = [
        "python",
        "-X",
        "faulthandler",
        "-m",
        "unittest",
        "discover",
        "--buffer",
        "-s",
        "tests",
    ]

    cproc = subprocess.run(cmd)
    rc = cproc.returncode
    if rc is not None and rc != 0:
        click.echo(cproc.stdout)
        click.echo(cproc.stderr)
        raise click.ClickException("Failed tests")


@cli.command(name="flake8", help="Run flake8")
def flake8():
    """ Run flake8 on the codebase"""
    cmd = ["python", "-m", "flake8", "."]
    cproc = subprocess.run(cmd)
    rc = cproc.returncode
    if rc is not None and rc != 0:
        click.echo(cproc.stdout)
        click.echo(cproc.stderr)
        raise click.ClickException("Failed flake8")


@cli.command(name="black", help="Run black")
def black():
    """ Run black on the codebase"""
    cmd = ["python", "-m", "black", "--line-length", "79", "."]
    cproc = subprocess.run(cmd)
    rc = cproc.returncode
    if rc is not None and rc != 0:
        click.echo(cproc.stdout)
        click.echo(cproc.stderr)
        raise click.ClickException("Failed black")


if __name__ == "__main__":
    cli(prog_name="python -m ci")
