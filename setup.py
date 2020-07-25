from setuptools import setup, find_packages

# Load the README file.
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='music-scraper',

    author='Justin Yum',

    author_email='justinyum98@gmail.com',

    # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
    version='0.1.0',

    description='A Python application for grabbing music data.',

    long_description=long_description,

    long_description_content_type='text/markdown',

    # Dependencies
    install_requires=[
        'requests>=2.22.0',
        'beautifulsoup4>=4.9.1',
    ],

    keywords='music',

    python_requires='>=3.7'
)
