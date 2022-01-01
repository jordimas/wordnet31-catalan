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

from urllib.request import Request, urlopen
import os

def read_synset30_ids():
    sysnet_ids = []
    with open('input/wei_cat-30_synset.tsv', 'r') as fh:
        while True:
            line = fh.readline()
            if not line:
                break

            components = line.split("\t")
            identifier = components[0].replace('cat-30-', '')
            sysnet_ids.append(identifier)

    print(f"Read {len(sysnet_ids)} identifiers")
    return sysnet_ids

def get_file(url, filename):
    msg = 'Downloading file \'{0}\' to {1}'.format(url, filename)
    print(msg)

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    infile = urlopen(req)
    output = open(filename, 'wb')
    output.write(infile.read())
    output.close()

def main():
    print("Downloads 3.1 Wordnet database for Catalan WordNet 3.0 synset")

    ids = read_synset30_ids()

    data_folder = 'data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    existed = 0
    downloaded = 0
    for id in ids:
        id = id.strip()
        filename = f"{data_folder}/{id}.json"
        if os.path.isfile(filename):
            existed += 1
            continue 

        url = f"http://wordnet-rdf.princeton.edu/json/pwn30/{id}"
        get_file(url, filename)
        downloaded += 1

    print(f"Existed {existed}, downloaded {downloaded}")

if __name__ == "__main__":
    main()
