bin/pelican content --theme-path themes/Flex -s publishconf.py
rsync -e "ssh -p 22" -P -rvzc --include tags --cvs-exclude --delete "output"/ "$USER@itconsense.com:/var/www/html/blog"