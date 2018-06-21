#!/bin/sh
# June 2018
# author: Sabin Katila
#
# Hack job to figure out all missing imports
# Same can be achieved by doing a epydoc .
#
TMP=$(mktemp -d -p $PWD)
find -type f -name "*.py" -print0 | xargs -0 grep -w import | cut -d ':' -f2 > ${TMP}/myimports
cd ${TMP}
cat myimports  | grep ^import | cut -d ' ' -f2 | cut -d '.' -f1  |  sort -u > impor1

cat myimports  | grep ^from | cut -d ' ' -f 2 | cut -d '.' -f1 | sort -u > impor2

cat impor2  impor1 | sort | sed '/^$/'d > ${TMP}/all-import

cat all-import  | sort -u | awk '{printf("import %s\n", $1)}' > import-test.py
# Now look out for the import-error, those are the modules you are missing

pylint import-test.py | grep -i error
echo "ALL FILES WRITTEN TO: " ${TMP}
