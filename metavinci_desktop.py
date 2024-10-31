import os
from pathlib import Path
from subprocess import run, Popen, PIPE, STDOUT
from gifanimus import GifAnimation
from easygui import *

BRAND = "HEAVYMETA®"
VERSION = "0.01"
ABOUT = f"""
Metavinci daemon by {BRAND}
A toolset for Data Standards 
and Metadata visualization
validation and interaction.
Version: {VERSION}
ALL RIGHTS RESERVED 2024
"""
VERSION = "0.01"

FILE_PATH = Path(__file__).parent
HOME = os.path.expanduser('~')
METAVINCI_PATH = os.path.join(HOME, '.metavinci')
METAVINCI_INSTALL = "curl -L https://raw.githubusercontent.com/inviti8/metavinci/main/install.sh | bash"
METAVINCI_BIN = os.path.join(METAVINCI_PATH, 'bin', 'metavinci')
DFX_BIN = os.path.join(HOME, '.local', 'share', 'dfx', 'bin', 'dfx')
LOADING_IMG = os.path.join(FILE_PATH, 'images', 'loading.gif')

def MsgBox(text):
  choices = ["OK"]
  return buttonbox(text, choices=choices)

def InstallBox(text):
  choices = ["INSTALL","CANCEL"]
  return buttonbox(text, choices=choices)

def _node_installed():
  process = Popen('node --version', stdout=PIPE, stderr=PIPE, shell=True)
  process.communicate()

  if process.returncode != 0:  
      return False
  else:
      return True


def _dfx_installed():
  return os.path.isfile(DFX_BIN)

def _run_command(cmd):
      process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
      output, error = process.communicate()

      if process.returncode != 0:  
        return "Command failed with error:", error.decode('utf-8')
      else:
        return output.decode('utf-8')
        

if __name__ == "__main__":
  _run = True

  if not _node_installed():
    MsgBox("Node is not installed, please install")
    _run = False

  if not _dfx_installed():
    MsgBox("Dfx is not installed, please install")
    _run = False

  if _run and not os.path.exists(METAVINCI_PATH):
    print("metavinci not installed, installing...")
    install = InstallBox(f'{ABOUT}')
    if install == 'INSTALL':
      loading = GifAnimation(LOADING_IMG)
      loading.Play()
      _run_command(METAVINCI_INSTALL)
      loading.Stop()
      _run_command(METAVINCI_BIN)
  else:
    if _run:
      _run_command(METAVINCI_BIN)

