from setuptools import setup
import os


with open('README.md', 'r') as file:
    readme = file.read()

with open('requirements.txt', 'r') as file:
    requirements = file.read().splitlines()

version = {}
with open(os.path.join('cqapi', 'version.py'), 'r') as file:
    exec(file.read(), version)

setup(
    name='cqapi',
    version=version['__version__'],
    description='A Conquery REST API library.',
    long_description=readme,
    packages=['cqapi'],
    install_requires=[
        'aiohttp==3.5.4'
    ],
)

