# Indentation

Indentation will always be tab `\t`. 

To quote linux kernel coding style, 
`Tabs are 8 characters, and thus indentations are also 8 characters. There are heretic movements that try to make indentations 4 (or even 2!) characters deep, and that is akin to trying to define the value of PI to be 3.`

If you are behind times and haven't read the linux kernel coding style, [read here ](https://www.kernel.org/doc/html/v4.10/process/coding-style.html)
This will remain true for both shell script and python scripts found here. Use of space to indent code will be considered `heresy`.

Use the .editorconfig file if your ide supports it (it should) or the vim modeline. If you are using emacs, you already know how to handle yourself.

Visit [yapf in github](https://github.com/google/yapf) and see `USE_TABS` to for how to beautify python code with tab as indentation character.

However, instead of running a code beautifier, it is generally better to rely on your editor (or IDE) to swap spaces with tab. `yapf` is a bit complicated and might worsen things.

Just sensible PEP-8 compliant coding with a single exception. USE_TABS. Spaces are for heretics. `pylint` your code before `git push`.



# POSIX standard

shebang line `#!/bin/sh`. Default system shell in debian is dash, fedora is bash. To make *.sh work in both environment, we shall adhere to the POSIX standard instead of being lazy and adopting the feature rich bash. Minimal might be painful but it works. Other flavors of linux might not even chose dash or bash. Complying with POSIX means *.sh will work with them (most likely).


