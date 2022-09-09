#  Copyright (c) 2022, J0J0 Todos

import pathlib
from distutils.util import convert_path

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setup
setup(
    name='beets-dirfields',
    version='1.1',
    description='A beets plugin that adds a field for each directory of its original path on import.',
    author='J0J0 Todos',
    author_email='jt@peek-a-boo.at',
    url='https://github.com/joj0/beets-dirfields',
    license='MIT',
    long_description=README,
    long_description_content_type='text/markdown',
    platforms='ALL',

    include_package_data=True,
    test_suite='test',
    #packages='beetsplug.dirfields',
    packages=find_packages(),

    python_requires='>=3.6',

    install_requires=[
        'beets>=1.4.9',
        'PyYAML'
    ],

    tests_require=[
        'pytest', 'mock', 'six', 'yaml',
    ],

    # Extras needed during testing
    extras_require={
        'tests': [],
    },

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
