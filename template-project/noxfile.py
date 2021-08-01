import nox


nox.options.sessions = ("lint", "test")

locations = ["src", "tests", "noxfile.py"]


@nox.session()
def test(session):
    pytest_args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *pytest_args)


@nox.session()
def lint(session):
    args = session.posargs or locations
    session.install(
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
    session.install("black")
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
        session.install("safety")
        session.run("safety", "check", f"--file={filename}", "--full-report")
