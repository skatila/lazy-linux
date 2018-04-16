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
	
A work profile running just email and a few nick-nacks might have to be up and running for-ever. Another profile meant to browse journal papers (which means a lot of open pdfs), will also be running AND eating a lot of memory. Another profile meant just for news. Another for netflix. You could potentially use it all in a single profile but that will create a huge memory overhead.
	
So, here comes gchrome. It takes $HOME/chrome as it's root directory and creates individual directory that serves as alternate browsing profile.

To use, do
	mkdir $HOME/chrome;cd $HOME/chrome
And make a few user directory that you want
	E.g. cd ~/chrome;mkdir {mail,journal,netflix}
	
With $HOME/chrome/{work,mail,blah1,blah2,blah2}, it gives you a fine grained control over your browsing habits.
	
If you are done with reading journals for the day, Ctrl+C for gchrome journal. (just make sure you have continue where you left enabled or better, some kind of session manager plugin)
		
If you are done with pointless casual browsing, Ctrl+C for gchrome browse
	
And, if you want to use tor,
	
	gchrome -t <profile> instead of having to pass --proxy-server="socks5:localhost:9050"
As usual, google chrome is not torbrowser. Do not rely on chrome+tor for privacy.	Use torbrowser from torproject if you want total anonymity.

Basically, instead of having to type
	google-chrome --user-data-dir=$HOME/chrome/<profile> --password-manager=basic (or whatever you are using)
gchrome makes your life easier.
	
	Usage: ./gchrome -tacp <dirname> [args]
      	-t --tor Use tor
      	-a  --alt <directory> # alternate location of chrome user
      	-c --create <directory> if you want chrome to create new user
                      directory under /home/dchaos/chrome
      	<dirname> profile directory
      	[args] optional chrome arguments, no recommended
 
      	--alt and --create cannot be used together

        profile directories are stored in /home/dchaos/chrome
        You will have to manually create ~/chrome directory
        and a few profile directories. Just a mkdir <name> will do`
	

---
## pretty-html

bs4 pretty-printer. Everyonce in a while I end up having to reformat html for one reason or another. This is my quick and dirty solution. tidy can do a better job I suppose but I like my pretty printer!!!

`python pretty-html -i input.html <output>` # output can be a file or be left empty (or -) for stdout.

Alternatively,
	`cat file.html | python pretty-html.py > outfile`
