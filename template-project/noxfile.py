import nox


nox.options.sessions = ("lint", "mypy", "safety", "black", "typeguard", "test")

locations = ["src", "tests", "noxfile.py"]
package = "template-project"


def install_with_constraints(session, *args, **kwargs):
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + "/reqs.txt"

        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={filename}",
            external=True,
        )
        session.install(f"--constraint={filename}", *args, **kwargs)


@nox.session()
def test(session):
    pytest_args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "coverage[toml]",
        "pytest",
        "pytest-cov",
    )
    session.run("pytest", *pytest_args)


@nox.session()
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
        "flake8-rst-docstrings",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session()
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session()
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session()
def safety(session):
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + "/reqs.txt"
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={filename}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={filename}", "--full-report")


@nox.session()
def typeguard(session):
    args = session.posargs or []
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session()
def docs(session):
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinx-rtd-theme",
    )
    session.run("sphinx-build", "-W", "docs", "docs/_build")
