import nox
import nox_uv
import argparse

nox.options.default_venv_backend = "uv"
nox.options.sessions = []


@nox_uv.session(
    python=["3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["dev"],
)
def tests(session: nox.Session) -> None:
    """
    Runs tests using specified python version.

    Usage:
    $ nox -s tests

    Reference:
    - https://edward-jazzhands.github.io/posts/python-testing-with-nox-and-uv/
    """
    session.run("pytest", *session.posargs)


@nox_uv.session(uv_groups=["dev"])
def lint(session: nox.Session) -> None:
    """
    Checks for linting errors in codebase using ruff.

    Usage:
    $ nox -s lint
    """
    session.run("ruff", "check")


@nox_uv.session(uv_groups=["dev"])
def format(session: nox.Session) -> None:
    """
    Checks for linting errors in codebase using ruff.

    Usage:
    $ nox -s format
    """
    session.run("ruff", "format")


@nox_uv.session(uv_groups=["dev"])
def release(session: nox.Session) -> None:
    """
    Kicks off an automated release process by creating and pushing a new tag.

    Invokes bump-my-version with the positional argument setting the version.

    Usage:
    $ nox -s release -- [major|minor|patch|pre_l]

    Reference:
    - https://nox.thea.codes/en/stable/cookbook.html
    """
    parser = argparse.ArgumentParser(
        description="Release a semver version.",
    )
    parser.suggest_on_error = True
    parser.add_argument(
        "release",
        type=str,
        nargs="?",
        help="The type of semver release to make.",
        choices={"major", "minor", "patch", "pre_l"},
        default="pre_l",
    )
    args: argparse.Namespace = parser.parse_args(args=session.posargs)

    release: str = args.release

    session.log(f"Bumping the {release!r} version.")
    session.run("bump-my-version", "show", "current_version")
    session.run("bump-my-version", "show", "--increment", release, "new_version")

    confirm = input(
        f"You are about to bump the {release!r} release. Are you sure? [y/n]: "
    )

    if confirm.lower().strip() != "y":
        session.error(f"You said no when prompted to bump the {release!r} release.")

    session.run("bump-my-version", "bump", release)

    session.log("Pushing the new tag")
    session.run("git", "push", external=True)
    session.run("git", "push", "--tags", external=True)


if __name__ == "__main__":
    nox.main()
