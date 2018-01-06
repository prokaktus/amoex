import sys
import os
from setuptools import setup
from amoex import __version__


if sys.version_info[0] < 3:
    sys.exit("Python2 is not supported")


description = """
Asyncio MOEX Python API
"""


setup(
    name="amoex",
    url="https://github.com/prokaktus/amoex",
    version=__version__,
    description=description.strip(),
    author="Filipenko Maxim",
    author_email="mfilipenko@yandex.ru",
    packages=[
        'amoex'
    ],
    install_requires=['aiohttp', 'toolz'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
