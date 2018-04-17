# lazy-linux
Amalgam of tools to make a *nix user live easy

Why type a long line of command every time you want to get something done?
Even doing a `history | grep something` gets repetitive.
So, over course of time like all linux user I have ended up writing up small and large scripts/programs to automate routine tasks.

  - [gchrome](#gchrome)
  - [pretty-html.py](#pretty-html)
	

---

## gchrome

A shell script designed to run google chrome.
The default data directory for google chrome is: `$HOME/.config/google-chrome`
	
However, doing all web-browsing from the same profile can be problematic. Despite the ability of google chrome to create individual user from it's own root folder, it is just not enough. 
	

---
## pretty-html

bs4 pretty-printer. Everyonce in a while I end up having to reformat html for one reason or another. This is my quick and dirty solution. tidy can do a better job I suppose but I like my pretty printer!!!

`python pretty-html -i input.html <output>` # output can be a file or be left empty (or -) for stdout.

Alternatively,
	`cat file.html | python pretty-html.py > outfile`
