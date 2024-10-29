import shutil
import subprocess
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("version", help="The version of this installer")
parser.add_argument("--linux", help="copy executable to deb build folder", action="store_true")
parser.add_argument("--mac", help="copy executable to dmg build folder", action="store_true")
args = parser.parse_args()

bin_name = 'metavinci_desktop'

# get current working directory
cwd = Path.cwd()
build_dir = cwd / "build"
dist_dir = cwd / "dist"
release_dir = cwd / "release"

release_linux_dir = release_dir / "linux"
release_mac_dir    = release_dir / "mac"    

src_bin = dist_dir / bin_name

def _clean_dir(dir):
    print(f"Cleaning {dir}")
    # check if build dir exists, if not create it
    if not dir.exists():
        dir.mkdir()
    else: # delete all files inside the directory
        for item in dir.iterdir():
            if item.is_file():
                item.unlink()
            else:
                shutil.rmtree(item)

# source files
src_file1 = cwd / 'metavinci_desktop.py'
src_icon = cwd / f'{bin_name}.png'

_clean_dir(build_dir)
_clean_dir(dist_dir)

shutil.rmtree(build_dir)
shutil.rmtree(dist_dir)

print("Building binary...")
# build the python script into an executable using PyInstaller
subprocess.run(['pyinstaller', '--onefile', str(cwd / src_file1.name)], check=True)

if args.linux:
    # target directories for the build folder and files
    pkg_dir = cwd / f'metavinci_desktop_{args.version}'
    deb_dir = pkg_dir / 'DEBIAN'
    usr_dir = pkg_dir / 'usr'
    bin_dir = usr_dir / 'bin'
    share_dir = usr_dir / 'share'
    app_dir = share_dir  / 'applications'
    icon_dir = share_dir / 'icons'
    hicolor_dir = icon_dir / 'hicolor'
    icon_size_dir = hicolor_dir / '512x512'
    icon_apps_dir = icon_size_dir / 'apps'

    src_ctrl = cwd / 'linux' / 'control'
    dest_ctrl = deb_dir / 'control'

    src_desktop = cwd / 'linux' / 'metavinci.desktop'
    dest_desktop = app_dir / 'metavinci.desktop'

    dest_bin = bin_dir / bin_name

    deb = cwd / f'metavinci_desktop_{args.version}.deb'
    dest_deb = release_linux_dir / f'metavinci-desktop_{args.version}_amd64.deb'

    
    # clean the build folder
    _clean_dir(pkg_dir)
    _clean_dir(release_dir)

    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)

    print("Creating build folders...")
    #build build directories
    if not release_dir.exists():
        release_dir.mkdir()

    if not release_linux_dir.exists():
        release_linux_dir.mkdir()

    if not pkg_dir.exists():
        pkg_dir.mkdir()

    if not deb_dir.exists():
        deb_dir.mkdir()
    
    if not usr_dir.exists():
        usr_dir.mkdir()
    
    if not bin_dir.exists():
        bin_dir.mkdir()

    if not share_dir.exists():
        share_dir.mkdir()
    
    if not app_dir.exists():
        app_dir.mkdir()

    if not icon_dir.exists():
        icon_dir.mkdir()

    if not hicolor_dir.exists():
        hicolor_dir.mkdir()

    if not icon_size_dir.exists():
        icon_size_dir.mkdir()

    if not icon_size_dir.exists():
        icon_size_dir.mkdir()
    
    if not icon_apps_dir.exists():
        icon_apps_dir.mkdir()

    if deb.is_file():
        deb.unlink()

    dest_icon = icon_apps_dir / f'{bin_name}.png'

    # copy source files to the build folder
    shutil.copy(src_ctrl, dest_ctrl)
    shutil.copy(src_desktop, dest_desktop)
    shutil.copy(src_bin,  dest_bin)
    shutil.copy(src_icon,  dest_icon)

    print("Building debian package...")
    subprocess.run(['dpkg-deb', '--build', str(pkg_dir)])
    print("Package created: " + str(deb))
    shutil.move(str(deb), str(dest_deb))
    
