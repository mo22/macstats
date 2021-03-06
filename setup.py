#!/usr/bin/env python3
from setuptools import setup

setup(
    name='macstats',
    version='0.2',
    author_email='mm@mxs.de',
    app=['main.py'],
    setup_requires=[
        'py2app',
        'pyobjc-framework-cocoa',
        'psutil',
        'pillow',
    ],
    data_files=[
        'activity.png',
    ],
    options=dict(
        py2app=dict(
            packages=['PIL'],
            plist=dict(
                LSUIElement=1,
            ),
        ),
    ),
)
