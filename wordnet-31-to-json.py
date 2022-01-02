#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import json
import os
import fnmatch

def find(directory, pattern):
    filelist = []

    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                filelist.append(filename)

    filelist.sort()
    return filelist

def load_json(filename):

    try:
        with open(filename, 'r') as fh:
            entry = json.load(fh)
            return entry

    except:
        print(f"Unable to load {filename}")
        return None


def main():

    print("Read individual jsons and produce a single json")
    terms = []

    output_folder = 'produced'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in find('downloaded/', '*.json'):
        entry = load_json(filename)

        if entry is None:
            continue

        entry = entry[0]
        term = {}
        term['id'] = entry['id']
        term['subject'] = entry['subject']

        if 'cat' in entry['foreign']:
            term['ca'] = entry['foreign']['cat']

        terms.append(term)
    
    with open(f'{output_folder}/terms.json', 'w') as outfile:
        json.dump(terms, outfile, indent=4, ensure_ascii=False)

    with open(f'{output_folder}/words.txt', 'w') as outfile:
        for term in terms:
            outfile.write(f"{term}\n")

    with open(f'{output_folder}/synset_ids_31.txt', 'w') as outfile:
        for term in terms:
            outfile.write(f"{term['id']} - {term['subject']}\n")

    print(f"Written {len(terms)}")

if __name__ == "__main__":
    main()
