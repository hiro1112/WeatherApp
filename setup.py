from setuptools import setup

APP = ['weather.py']
DATA_FILES = ['icon', 'primary_area.xml', 'data.tmp']
OPTIONS = {
        'argv_emulation': True,
        'iconfile': 'weather.icns',
        'plist': {
            'PyRuntimeLocations': [
                '@executable_path/../Frameworks/libpython3.7.dylib',
                '/Users/hiroki/.pyenv/versions/3.7.7/lib/libpython3.7.dylib'
                ],
            'LSUIElement': True,
                 }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
