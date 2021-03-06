import codecs

from setuptools import find_packages, setup

import version

setup(
    name="eaas",
    version=version.__version__,
    description="Evaluation as a Service for Natural Language Processing",
    long_description=codecs.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/inspired-co/eaas_client",
    author="Inspired Cognition",
    license="Apache 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "eaas-cli=eaas.eaas_cli:main",
        ],
    },
    install_requires=[
        "nltk>=3.2",
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "pandas",
        "tqdm",
        "requests",
    ],
    include_package_data=True,
)
