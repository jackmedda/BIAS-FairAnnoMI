from setuptools import setup, find_packages

import os
from codecs import open

lib_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Get the long description from the README file
with open(os.path.join(lib_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="fair-annomi",
    version="0.1.0",
    description="Demo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["scikit-learn", "sklearn_pandas"]
)
