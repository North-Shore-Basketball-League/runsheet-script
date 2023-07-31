import json
from pathlib import Path


class Printing:
    def __init__(self):
        pass

    class formatting:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def print_new(self):
        print("\n")

    def print_inline(self, str):
        print("    "+str, end="")
        self.backline()

    def backline(self):
        print('\r', end="")

    def welcome(self):
        versionPath = Path(__file__).parent / "version.json"
        version = "Unknown version"

        if versionPath.exists():
            with versionPath.open() as f:
                version = json.loads(versionPath.read_text(
                    encoding="UTF-8"))["version"]

        versionStr = f"{self.formatting.UNDERLINE}{self.formatting.OKCYAN}Running Version: {version}{self.formatting.ENDC}"

        print(f'''


    
    ███╗   ██╗███████╗██████╗ ██╗     
    ████╗  ██║██╔════╝██╔══██╗██║     
    ██╔██╗ ██║███████╗██████╔╝██║     
    ██║╚██╗██║╚════██║██╔══██╗██║     
    ██║ ╚████║███████║██████╔╝███████╗
    ╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝


    {self.formatting.HEADER}{self.formatting.OKBLUE}Starting to extract this weeks runsheet and scoresheets!{self.formatting.ENDC}
    {versionStr}

''')
