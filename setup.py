# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hal']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'notion-client>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'hal',
    'version': '2.0.0',
    'description': 'Monitor lab instruments in real-time with a Notion frontend',
    'long_description': None,
    'author': 'qcrew',
    'author_email': 'general.qcrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
