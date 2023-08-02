from importlib.util import find_spec
from pathlib import Path
import requests
from github import Github


def checkImports(packages):
    for module in packages:
        package, link = module

        if find_spec(package) is not None:
            continue

        downloadPath = Path(__file__).parent / package

        print(package, "not found")
        print(link)

        github = Github()
        contents = github.get_repo(link).get_contents()
