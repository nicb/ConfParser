#!/usr/bin/env python
#
# $Id: setup.py 555 2006-05-07 23:37:13Z nicb $
#
from distutils.core import setup
from string import strip

revision = "$Revision: 555 $"

setup(name="ConfParser",
	  version=strip(revision[10:-1]),
      description="Generic Configuration Parser Class",
	  author="Nicola Bernardini",
	  author_email="nic.bern@tiscali.it",
	  url="http://www.nicolabernardini.info/src/python",
	  packages=['ConfParser'], 
)

