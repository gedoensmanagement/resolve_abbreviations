#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Provide the lines as a list:
lines = ["Prędicamus Christū",
         "Prædicamus Christum",
         "antiquum quum equum aequum"]

# Provide the regex patterns and the corresponding replacements
# as a list of lists:
replacement_table = [["æ", "ae"],
                     ["ę", "ae"],
                     ["ū", "um"],
                     # make sure to use a raw string (r"PATTERN") here:
                     [r"\bquum\b", "cum"]] 

# Loop through the lines:
for line in lines:
    print("raw:   ", line)

    # Loop through the items in the replacement_table dictionary
    # to apply all the predefined search and replace operations:
    for pattern, replacement in replacement_table:
        line = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
    print("cooked:", line, "\n")