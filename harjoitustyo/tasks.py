from invoke import task

@task
def foo(ctx):
    print("bar")

@task
def start(ctx):
    ctx.run("python src/main.py")

@task
def test(ctx):
    ctx.run("coverage run --branch -m pytest")

@task
def coverage_report(ctx):
    ctx.run("coverage run --branch --omit='*/ei_kaytossa_vanha.py' -m pytest")
    ctx.run("coverage report -m --omit='*/ei_kaytossa_vanha.py'")
    ctx.run("coverage html --omit='*/ei_kaytossa_vanha.py'")

@task
def lint(ctx):
    ctx.run("pylint --ignore=main.py,ei_kaytossa_vanha.py  src")

@task
def format_for_lint(ctx):
    ctx.run("autopep8 --in-place --recursive src")