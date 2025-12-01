from invoke import task

@task
def foo(ctx):
    print("bar")

@task
def start(ctx):
    ctx.run("python src/main.py")

@task
def test(ctx):
    ctx.run("coverage run --branch --omit='*/test_analyze.py' -m pytest")

@task
def coverage_report(ctx):
    ctx.run('coverage run --branch --omit="*/ei_kaytossa_vanha.py,src/main.py,src/visual.py" -m pytest')
    ctx.run('coverage report -m --omit="*/ei_kaytossa_vanha.py,src/main.py,src/visual.py"')
    ctx.run('coverage html --omit="*/ei_kaytossa_vanha.py,src/main.py,src/visual.py"')

@task
def lint(ctx):
    ctx.run("pylint --ignore=ei_kaytossa_vanha.py,finance_api.py  src")

@task
def format_for_lint(ctx):
    ctx.run("autopep8 --in-place --recursive src")