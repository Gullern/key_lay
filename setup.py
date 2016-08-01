#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'name': 'key_lay',
	'description': '',
	'version': '0.1',
	'url': 'https://github.com/Gullern/key_lay',
	'author': 'Jan Gulla, Odd Cappelen',
	'author_email': 'jangu@stud.ntnu.no, odd.cappelen@gmail.com',
	'packages': ['key_lay']
}

setup(**config)