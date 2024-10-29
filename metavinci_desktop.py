import os
from pathlib import Path
from subprocess import run, Popen, PIPE, STDOUT

BRAND = "HEAVYMETA®"
VERSION = "0.01"
ABOUT = f"""
Command Line Interface for {BRAND} Standard NFT Data
Version: {VERSION}
ALL RIGHTS RESERVED 2024
"""
VERSION = "0.01"

FILE_PATH = Path(__file__).parent
HOME = os.path.expanduser('~')
METAVINCI_PATH = os.path.join(HOME, '.metavinci')
METAVINCI_INSTALL = "curl -L https://raw.githubusercontent.com/inviti8/metavinci/main/install.sh | bash"
METAVINCI_BIN = os.path.join(METAVINCI_PATH, 'bin', 'metavinci')

def _run_command(cmd):
      process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
      output, error = process.communicate()

      if process.returncode != 0:  
        print("Command failed with error:", error.decode('utf-8'))
      else:
        print(output.decode('utf-8'))

if __name__ == "__main__":
    print(f"{BRAND} {VERSION}")

    if not os.path.exists(METAVINCI_PATH):
        print("metavinci not installed, installing...")
        _run_command(METAVINCI_INSTALL)
    else:
        _run_command(METAVINCI_BIN)