"""Setup generator file."""
from setuptools import setup, find_packages
import sys

with open("README.md", "r") as f:
    long_description = f.read()

requirements = open("requirements.txt").read().splitlines()
packages = find_packages()
# packages.remove("tests")

setup(
    name='paymium',
    packages=packages,
    version='1.0',
    description='Paymium API',
    author='mouuff',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='arnaudalies.py@gmail.com',
    url='https://github.com/mouuff/PyPaymium',
    keywords=['tool', 'api', 'paymium', 'bot', 'pypaymium'],
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Software Development'
                 ],
    install_requires=requirements,
    include_package_data=True
)
