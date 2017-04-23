#!/usr/bin/env python
"""
Config is a user interactive setup for webhook shims.

Shims.ini can then be referenced by the shims for pre-configured parameters.
"""

__author__ = "John Dias"
__email__ = "diasj@vmware.com"
__license__ = "Apache v2"
__verion__ = "1.0"

import logging
import sys
import os
import ConfigParser
##########################
# Menus
##########################

# Main Menu
def main_menu(choices):
    os.system('clear')
    print "Select a shim number to configure:"
    for n, c in enumerate(choices):
        print("{} - {}".format(n, c))
    choice = raw_input(" Select (Q to end)>> ")
    if choice.lower == "q":
        return
    return(choice)



settings = ConfigParser.ConfigParser()
settings
settings.read('./shims.ini')

confSections = settings.sections()

menu_selection = main_menu(confSections)
print menu_selection
