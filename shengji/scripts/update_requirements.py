import subprocess


def run():
    subprocess.call('pip-compile --upgrade requirements/global.in --output-file requirements/global.txt'.split())
    subprocess.call('pip-compile --upgrade requirements/dev.in --output-file requirements/dev.txt'.split())
    subprocess.call('pip-sync requirements/global.txt requirements/dev.txt'.split())
