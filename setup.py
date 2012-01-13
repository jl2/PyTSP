from setuptools import setup

APP = ['viewtsp.py']
OPTIONS = {'argv_emulation': True,"includes": ["sip", "PyQt4"]}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
