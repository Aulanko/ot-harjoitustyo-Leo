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
    ctx.run("coverage run --branch -m pytest")
    ctx.run("coverage report -m")
    ctx.run("coverage html")