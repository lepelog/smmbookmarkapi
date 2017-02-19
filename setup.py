from setuptools import setup

with open("smmbookmarkapi/.version") as f:
    version = f.read().strip()

setup(
    name='smmbookmarkapi',
    version=version,
    packages=['smmbookmarkapi'],
    include_package_data=False,
    install_requires=['requests>=2.12.3']
)
