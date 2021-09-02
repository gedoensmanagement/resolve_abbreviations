#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hunspell import Hunspell
# Initialize the dictionary object. hunspell_data_dir is the
# directory of the two dictionary files "la_LA.aff" and "la_LA.dic":
h = Hunspell('la_LA', hunspell_data_dir='hunspell-la')

# Check a list of words:
words = ["amamus", "credo", "asdf", "wrong!", "spes"]
for word in words:
    print(word, h.spell(word))