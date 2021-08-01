import nox


@nox.session()
def tests(session):
    pytest_args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *pytest_args)


@nox.session()
def lint(session):
    args = session.posargs or ["src", "tests", "noxfile.py"]
    session.install("flake8")
    session.run("flake8", *args)
