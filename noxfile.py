import nox


@nox.session(
    venv_backend="uv",
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
)
def tests(session) -> None:
    session.run("uv", "run", "pytest", "tests/")


# @nox.session
# def lint(session):
#     session.install("ruff")
#     session.run("ruff", "check", "--fix")


# @nox.session
# def format(session):
#     session.install("ruff")
#     session.run("ruff", "format")
