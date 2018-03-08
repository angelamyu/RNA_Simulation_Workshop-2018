"""
Parses `spats_tool run` output and creates .seq and .shape files.
See wiki for instructions on how to use. 

Version: 0.0.1
Author: Angela M Yu, 2018

Copyright (C) 2018  Julius B. Lucks, Angela M Yu.
All rights reserved.
Distributed under the terms of the GNU General Public License, see 'LICENSE'.
"""

import getopt
import sys
import re

def parse_spats_dump(file, linkerseq, output_prefix):
    """
    Parses reactivity file and outputs .rho and .seq, stripping off the
    linker sequence.
    """
    try:
        with open(file, 'r') as f:
            f.readline()  # throw out header
            seq = []
            rho = []
            pos = []
            linkerseq = linkerseq.upper().replace('T', 'U')

            for l in f:  # parse through file
                vars = re.split(',', l)
                seq.append(vars[2].upper().replace('T', 'U'))
                rho.append(float(vars[7]))
                pos.append(vars[1])

            #cutoff linker sequence and calculate rhos
            seqstring = "".join(seq)
            if seqstring.endswith(linkerseq):
                seq_cut = seqstring[1:-len(linkerseq)]
            rho_cut = rho[1:-len(linkerseq)]

            # Output files
            try:
                with open(output_prefix+".shape", 'w') as out:
                    out.write("\n".join(["\t".join([str(zi), str(zr)]) for zi, zr in zip(pos[1:], rho_cut)]))
            except EnvironmentError:
                print "Error opening output .rho file: " + output_prefix + ".shape"

            try:
                with open(output_prefix+".seq", "w") as new_seq:
                    line_to_write = ';\n{0}\n%s1'.format(output_prefix+".seq") % (seq_cut)
                    new_seq.write(line_to_write)
            except EnvironmentError:
                print "Error opening output .seq file: " + output_prefix + ".seq"

            return

    except EnvironmentError:
        print "Error opening reactivities file: " + file


def getopts(short_arg_string, long_arg_list):
    """
    Returns a dictionary of command line arguments as defined by short_arg_string and long_arg_list
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_arg_string, long_arg_list)
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    return dict(opts)


if __name__ == '__main__':
    opts = getopts("", ["input=", "linker=", "output_prefix="])
    parse_spats_dump(opts["--input"], opts["--linker"], opts["--output_prefix"])

