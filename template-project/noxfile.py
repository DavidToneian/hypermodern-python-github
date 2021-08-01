import nox

@nox.session()
def tests(session):
    pytest_args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *pytest_args)
