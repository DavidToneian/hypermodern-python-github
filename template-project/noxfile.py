import nox


nox.options.sessions = ("lint", "test")

locations = ["src", "tests", "noxfile.py"]


def install_with_constraints(session, *args, **kwargs):
    import tempfile

    with tempfile.TemporaryDirectory as tmpdir:
        filename = tmpdir + "/reqs.txt"

        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
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
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


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
