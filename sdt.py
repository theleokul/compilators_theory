#!/usr/bin/env python3

import argparse
import re

import pandas as pd

import grammatic as g

# Parse args
parser = argparse.ArgumentParser(description='Syntax driven translator')
parser.add_argument('-s', '--seq', type=str, default='a+b*c*(d-e)#', help='Sequence to translate')
args = parser.parse_args()
seq = args.seq

# Remove all spaces
seq = re.sub(r'\s', '', seq)

# Insert termination letter to make algorithm works
if seq[-1] != '#':
    seq += '#'


def iterate_through_grams(seq, seq_i):
    for gram_i, gram in enumerate(g.grams):
        if gram.process_sdt(seq, seq_i, gram_i):
            return True
    return False


def main():
    for seq_i, let in enumerate(seq):
        # let - current symbol (R)

        while True:
            if iterate_through_grams(seq, seq_i):
                continue
            else:
                break

        g.steps.append([g.stack, seq[seq_i], seq[seq_i+1:], '-', g.pol_not])
        g.stack += let

    df = pd.DataFrame(g.steps, columns=['stack', 'cur_let', 'seq_rest', 'rule_i', 'pol_not'])

    with pd.option_context('display.max_rows', None):
        print(df)


if __name__ == '__main__':
    main()
