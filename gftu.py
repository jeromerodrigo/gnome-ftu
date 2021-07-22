#!/usr/bin/python3

###############################################################
### PROJECT:
### Gnome Flatpak Custom Theme Updater
### SCRIPT:
### gftu.py
### DESCRIPTION:
### Automated custom theme update for Flatpak Apps in Gnome
###
### MAINTAINED BY:
### hkdb <hkdb@3df.io>
### ############################################################

import os, datetime, sys, glob, shutil, string
from pathlib import Path

# Define Version
version = "v00.01"

# Get HomeDir
homedir = str(Path.home())

# Never write same code, make function
def numFolders(path):
    return len([f.path for f in os.scandir(path) if f.is_dir()])


def hasRuntime(path):
    return os.path.isdir(path) == True and numFolders(path) > 0


def copyTheme(runtime_path, namespace, platforms, theme_path):
    for p in platforms:
        dest = runtime_path + "org." + namespace + ".Platform/x86_64/" + p + "/active/files/share/themes/"
        # TODO Handle sudo needed for copying into /var/lib
        command = "cp -R " + theme_path + " " + dest

        print("\nCOPYING TO: ", dest)
        print(command)
        os.system(command)

# Set runtime path
runtime_sys = "/var/lib/flatpak/runtime/"
runtime_local = homedir + "/.local/share/flatpak/runtime/"
runtime = []

print("\nLooking for Flatpak runtime...")

if hasRuntime(runtime_sys):
    runtime.append(runtime_sys)

if hasRuntime(runtime_local):
    runtime.append(runtime_local)

if len(runtime) == 0:
    print("flatpak runtime not found in:" + runtime_local + " or " + runtime_sys)
    exit()

for r in runtime:
    print("flatpak runtime found in:", r)

# Get current theme being used
print("\nIdentifying which theme is currently being used...")
theme = os.popen('gsettings get org.gnome.desktop.interface gtk-theme').read()
theme = theme[1:-2]
print("THEME: " + theme)

# Check what theme folders in flatpak exists
print("\nChecking Flatpak Gnome Platform Dependencies...")
platforms = os.listdir(homedir + "/.local/share/flatpak/runtime/org.gnome.Platform/x86_64/")
for p in platforms:
    print("Gnome " + p)

# Check on where theme exists
orig = ""
print("\nChecking to see where the theme dir is...")
home = os.path.isdir(homedir+"/.local/share/themes/"+theme)
print("HOME: ", home)
if home == True:
    orig = homedir+"/.local/share/themes/"+theme
else:
    system = os.path.isdir("/usr/share/themes/"+theme)
    print("SYSTEM: ", system)
    if system == True:
        orig = "/usr/share/themes/"+theme
    else:
        print("ERROR: No such theme available in the 2 common places to find them. Please move your theme folder to either ~/.local/share/themes/ or /usr/share/themes/ and try again.\n")
        exit()

# copy theme over to all available platforms
print("\nCopying theme to all available platforms...")
for p in platforms:
    print("COPYING TO: ",  p)
    os.system("cp -R " + orig + " " + homedir + "/.local/share/flatpak/runtime/org.gnome.Platform/x86_64/" + p + "/active/files/share/themes/")
    # print("cp -R " + orig + " " + homedir + "/.local/share/flatpak/runtime/org.gnome.Platform/x86_64/" + p + "/active/files/share/themes/")

print("\nDONE...\n")
