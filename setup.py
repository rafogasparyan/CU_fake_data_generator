# setup.py
from setuptools import setup, find_packages

setup(
    name='magicgenerator',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'magicgenerator=magicgenerator.magicgenerator:main',
        ],
    },
)
