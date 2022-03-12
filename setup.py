from setuptools import find_packages, setup

setup(
    name='datastructures',
    version='0.0.1',
    packages=find_packages(),
    entrypoints={
        'console_scripts': [
            'foo=src.main:main',
        ],
    },
)
