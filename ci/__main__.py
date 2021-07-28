import subprocess

import click


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

@cli.command(name="isort", help="Run isort")
def black():
    """ Run isort on the codebase"""
    cmd = ["python", "-m", "isort", "."]
    cproc = subprocess.run(cmd)
    rc = cproc.returncode
    if rc is not None and rc != 0:
        click.echo(cproc.stdout)
        click.echo(cproc.stderr)
        raise click.ClickException("Failed isort")

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

if __name__ == "__main__":
    cli(prog_name="python -m ci")
