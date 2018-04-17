#!/usr/bin/python
#
###############################################################################
# Copyright (C) 2018 by Sabin Katila (sabin@sabink.org)                       #
# Released under the terms of GPLv3                                           #
# <http://www.gnu.org/licenses/                                               #
# You are free to use, modify and/or redistribute as per the terms of GPL v3  #
#                                                                             #
###############################################################################
from __future__ import print_function

import sys, os
import argparse
from contextlib import contextmanager

from bs4 import BeautifulSoup


@contextmanager
def outw(ofile, force=False):
	"""
	Write output to file or stdout
	"""
	# when outfile is not stdout
	if not os.path.exists(ofile):
		# If file does not exists, it is all good
		outf = open(ofile, "w")
	else:
		# only when outfile exists
		if os.path.isfile(ofile) and force:
			sys.stderr.write("output file " + ofile +
				" already exists, overwritting!!!\n")
		else:
			error_m = "exists"
			if os.path.isdir(ofile): error_m = "is a directory"
			sys.stderr.write("Outfile " + error_m +
				"!!! Cowardly quitting!!!\n")
			sys.exit(1)
	#print("OKAY we are writing output to: ", ofile)
	try:
		outf = open(ofile, "wb")
		yield outf
	finally:
		outf.close()

def main():
	"""
	Parse html and pretty print
	"""
	parser = argparse.ArgumentParser()

	parser.add_argument(
			"-i", "--input-file",
			dest="input",
			help="Input file",
			required=False,
			default='-'
			)

	parser.add_argument(
			"output",
			help="Output file, use - or just skip for stdout",
			nargs='?',
			default="-"
			)

	parser.add_argument(
			"-f", "--force",
			action="store_true",
			default=False,
			help="Output file, if present will be overwritten"
			)

	args = parser.parse_args()

	infile = args.input
	outfile = args.output
	#print("%s \n %s" % (infile, outfile))
	if infile != '-' and not os.path.isfile(infile):
		msg = "does not exist"
		if os.path.isdir(infile): msg = "is a directory"
		sys.stderr.write("Input file " +  msg +  " Check again!!!\n")
		sys.exit(1)


	# now that infile and outfile checks are done, let's get started

	if infile == '-':
		inf = [i for i in sys.stdin]
	else:
		inf = [i for i in open(infile, "r")]
	inlines = ''.join(inf)
	soup = BeautifulSoup(inlines, "lxml")
	pr = soup.prettify()
	if outfile == '-':
		sys.stdout.write(pr)
	else:
		with outw(outfile, force=args.force) as o:
			o.write(pr.encode('utf-8'))

if __name__ == '__main__':
	main()

# vim: autoindent tabstop=4 shiftwidth=4 noexpandtab softtabstop=4 filetype=python
