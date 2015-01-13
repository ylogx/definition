from distutils.core import setup

add_keywords = dict(
    entry_points = {
        'console_scripts': ['definition = definition.definition:main'],
    },
)

setup(
        name='definition',
        description='Definition fetcher from 5 online dictionaries',
        version='0.0.2',
        packages=['definition'],
        license='GPLv3+',
        author='Shubham Chaudhary',
        author_email='me@shubhamchaudhary.in',
        url='https://github.com/shubhamchaudhary/definition',
        long_description=open('README.txt').read(),
        **add_keywords
)

