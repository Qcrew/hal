# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["hal"]

package_data = {"": ["*"]}

install_requires = [
    "Pint>=0.19.2,<0.20.0",
    "loguru>=0.6.0,<0.7.0",
    "notion-client>=1.0.0,<2.0.0",
    "numpy>=1.22.3,<2.0.0",
    "pyserial>=3.5,<4.0",
    "slack-bolt>=1.13.1,<2.0.0",
]

entry_points = {"console_scripts": ["hal = hal.main:main"]}

setup_kwargs = {
    "name": "hal",
    "version": "2.1.1",
    "description": "Monitor lab instruments in real-time with a Notion frontend",
    "long_description": None,
    "author": "qcrew",
    "author_email": "general.qcrew@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.10,<4.0",
}


setup(**setup_kwargs)
