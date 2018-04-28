+ ### 2to3

pretty-html.py is mostly python 3. Make sure it is completely 3 and get rid of from `future import` etc.

+ ### bs4 dependency

pretty-html depends on bs4. Get rid of it? regex, regex and some more regex. Will that be faster? And sometimes bs4 might not be available anyway.
