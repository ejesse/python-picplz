===========
python-picplz
===========
:Info: Python library for picplz service
:Author: Jesse Emery (http://github.com/ejesse)

Status
=====
Pretty alpha. You can make unauthenticated requests to get users and user's pics. You can authenticate, but no secured methods are implemented yet (although it will let you know if your API key works).

About
=====
python-picplz is a Python library for interfacing with the `Picplz API <http://sites.google.com/site/picplzapi>`_.

Installation
============

Pip:

    pip install python-picplz. 

Otherwise, you can download the source from `GitHub <http://github.com/ejesse/python-picplz>`_ and run:: 

    python setup.py install

Dependencies
============
- Simplejson 2.1.5

Examples
========
To do anything, first create an API instance::

    from picplz.api import PicplzAPI
    api = PicplzAPI()

Getting a user::

    user = api.get_user(username='ejesse')

Getting a pic by id::

    pic = api.get_pic(id=1534270)

Getting a pic by its longurl_id::

    pic = api.get_pic(longurl_id='rm789')

Getting a pic by its shorturl_id::

    pic = api.get_pic(shorturl_id='Q2s5')

Getting all of a user's pics::

    pics = api.get_pics(user=user)

Or::

    pics = user.fetch_all_pics()

Contributing
============
The source is available on `GitHub <http://github.com/ejesse/python-picplz>`_ - to
contribute to the project, fork it on GitHub and send a pull request, all
contributions and suggestions are welcome!
