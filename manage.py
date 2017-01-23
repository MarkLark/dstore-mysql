#!/usr/bin/python
import pyman

menu = pyman.Main( "DStore-MySQL - Manager", [
    pyman.Doc(),
    pyman.PyPi(),
    pyman.NoseTest(),
    pyman.Git(),
    pyman.Actions.Exit()
])
menu.cli()