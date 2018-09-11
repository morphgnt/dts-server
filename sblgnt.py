#!/usr/bin/env python3

import glob

for filename in glob.glob("../sblgnt/*-morphgnt.txt"):
    output_filename = "data/" + filename[10:]
    prev_bcv = None
    with open(filename) as f:
        with open(output_filename, "w") as g:
            for line in f:
                parts = line.strip().split()
                bcv = parts[0]
                text = parts[3]
                if bcv != prev_bcv:
                    if prev_bcv:
                        print(file=g)
                    print(bcv, end=" ", file=g)
                    prev_bcv = bcv
                print(text, end=" ", file=g)
            print(file=g)
