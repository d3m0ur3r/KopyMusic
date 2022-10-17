﻿# KopyMusic (***WORK IN PROGRESS***)

KopyMusic is a CLI file transfer script. It's fairly simple but effective. The main purpose of KopyMusic is to copy music
from one folder to another without overwriting existing files.

It does a set comparison between chosen folders and copies them.

### Windows installation:

### Linux installation:

    $ python3 -m pip install -r requirements.txt  
    $ python3 main.py

### General info:

KopyMusic uses sftp for network transfers and all default ports (22)
KopyMusic can transfer all kinds of files, not just music files.

### Usage examples:

**-u john -r 192.168.1.200/Music -l C:\Users\john\Music\ -t**

**-u john -r 192.168.1.200/Music -l C:\Users\john\Music\ --reverse -t**

**-r C:/MyMusic -l $HOME/Music -t**

**-r C:/MyMusic -l $HOME/Music --mirror -t**

