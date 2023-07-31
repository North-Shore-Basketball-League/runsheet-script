from importlib.util import find_spec
import subprocess
from sys import executable


def checkImports(packages):
    for module in packages:
        if find_spec(module) is not None:
            continue

        print(module, "not found")
        subprocess.check_call([executable, "-m", "pip", "install", module])
