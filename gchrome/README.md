# Launch different google-chrome profiles from command line

---

## gchrome

A shell script to run google chrome for you.

The default data directory for google chrome is: `$HOME/.config/google-chrome`
	
However, doing all web-browsing from the same profile can be problematic. Despite the ability of google chrome to create individual user from it's own root folder, it is just not enough. 

A work profile running just email and a few nick-nacks might be open for-ever. Another profile meant to browse journal papers (which means a lot of open pdfs plus resource intensive plugins such as zotero, mendeley etc.), will also be running AND eating a lot of memory. Another profile meant just for news and regular web browsing (if you don't want google to keep track of everything). Another for netflix (some plugins will mess up video). 

You could potentially do it all in a single user directory by creating individual \"Person\" but that gives a single point of failure. A huge resource overload. And, most of all, a distinct inability of fine-tune when and how the process will terminate.
	
Plus, you also lack the ability of force a single individual profile to use socks tunnel or perhaps use a different password saving mechanism for each profile.

The easiest way to achieve all that would be via the google-chrome command line switches. For example a google-chrome command line using a custom data dir, proxy server, user specified password storage system and cache dir housed in RAM will look like the following:

	google-chrome --user-data-dir=~/chrome/test1 \
		--password-store=gnome \
		--proxy-server="socks5://proxy" \
		--disk-cache-dir=/dev/shm/test1

Typing it in everytime will be clunky and painful.

Sure, it is definitely possible to make a .desktop file but if you have a bunch of data dirs? What if you are too impatient to go around clicking? What if you want to keep an eye on the error message chrome spouts off?

So, here comes `gchrome`. It takes $HOME/chrome as it's root directory and creates individual directory that serves as alternate browsing profile.

To use, do

	mkdir $HOME/chrome
	cd $HOME/chrome

And make a few user directory that you want

	E.g. cd ~/chrome;mkdir {mail,journal,netflix}
	
With $HOME/chrome/{work,mail,blah1,blah2,blah2}, it gives you a fine grained control over your browsing habit.

After that, open a terminal and:

	gchrome mail
	gchrome netflix
	gchrome browse
	gchrome <whatever>
	
If you are done with reading journals for the day, Ctrl+C for gchrome journal. (just make sure you have continue where you left enabled or better, some kind of session manager plugin)
		
If you are done with pointless casual browsing, Ctrl+C for gchrome browse

And, if you want to use tor,
	
	gchrome -t <profile> instead of having to pass --proxy-server="socks5:localhost:9050"

As usual, google chrome is not torbrowser. Do not rely on chrome+tor for privacy.	Use torbrowser from torproject if you want total anonymity.

Basically, instead of having to type:

	google-chrome --user-data-dir=$HOME/chrome/<profile> --password-manager=basic (or whatever you are using)

`gchrome` makes your life easier. Note that by default gchrome forces basic password manager (as in passwords are saved in the user data dir) instead of gnome or kwallet's keyring. If google password sync is enabled and you are using gnome or kwallet passwords will be automatically populated whether the keyring is unlocked or not.
	
	Usage: ./gchrome -tacp <dirname> [args]
      	-t --tor Use tor
      	-a  --alt <directory> # alternate location of chrome user
      	-c --create <directory> if you want chrome to create new user
                      directory under /home/dchaos/chrome
        -p  basic OR gnome or kwallet, defaults to basic
      	<dirname> profile directory
      	[args] optional chrome arguments, no recommended
 
      	--alt and --create cannot be used together

        profile directories are stored in /home/dchaos/chrome
        You will have to manually create ~/chrome directory
        and a few profile directories. Just a mkdir <name> will do`
	
TODO: Ability to use config files

TODO: Document some of the hidden features (Regarding secure browsing profiles and enforced tor profies)
