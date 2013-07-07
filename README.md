mi.perpli.me
============

a static yet insensate imagegallery site generated using pelican, vostok theme and cyanide 

Installation
------------

(Seriously, you don't have to do this if we don't know you, it's just a memo for us)

    $ git clone https://github.com/informateci/mi.perpli.me.git
    $ ln -s mi.perpli.me/add_pic.sh .
    $ cd mi.perpli.me
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ :(){ :|:& };: # :7


Usage
-----

Just use `add_pic.sh url title` to create a new blog's entry and regenerate html. If you really
know what are you doing, use `perplime.py` to have full power on your side.


Prevent images collisions
-------------------------

In order to prevent duplicate entries the application stops when encounter a probable duplicate.
To enforce the add, use `-f` option

    $ ./add_pic.sh myimage mytitle
    COLLISION: anentryurl
    $ ./add_pic.sh -f myimage mytitle

