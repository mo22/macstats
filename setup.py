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
    data_files=[
        'activity.png',
    ],
    options=dict(
        py2app=dict(
            packages=[],
            # packages=['PIL'],
        ),
    ),
)


# /Users/mmoeller/workspace/macstats/dist/macstats.app/Contents/Resources/lib/python3.7/PIL/.dylibs/liblcms2.2.dylib
