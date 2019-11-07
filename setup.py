from setuptools import setup

setup(
    name='macstats',
    version='0.1',
    author_email='mm@mxs.de',
    app=['main.py'],
    setup_requires=[
        'py2app',
        'pyobjc-framework-cocoa',
        'psutil',
        'pillow',
    ],
)
