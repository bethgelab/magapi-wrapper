from setuptools import setup
from setuptools import find_packages
from os.path import join, dirname

with open(join(dirname(__file__), "magapi/VERSION")) as f:
    version = f.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    "pandas",
    "requests",
    "setuptools",
    "typing-extensions>=3.7.4.1",
    "tabulate",
]
tests_require = ["pytest>=5.3.5", "pytest-cov>=2.8.1"]



setup(
    name="magapi-wrapper",
    version=version,
    description="Tool to download publications from Microsoft Academic Knowledge API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="Microsoft Academic graph, MAG, Knowledge API, Publications",
    author="Kantharaju Narayanappa",
    author_email="kantharajucn@outlook.com",
    url="https://github.com/bethgelab/magapi-wrapper",
    license="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"testing": tests_require},
    entry_points={
        'console_scripts': ['mag-api=tool.wrapper:main']
    },
    setup_requires = ['flake8'],
)