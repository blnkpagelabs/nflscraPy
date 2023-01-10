from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.1.3' 
DESCRIPTION = "Datasets and Scraping Functions for NFL Data"

LONG_DESCRIPTION = """
This package was inspired by the creators of nflscrapR and nflfastR and the tremendous influence they have had on the open-source NFL community

The functionality of nflscraPy was designed to allow Python users to easily ingest boxscore and seasonal data from publicly available resourses, in particular, Pro Football Reference

Hopefully this package builds upon the availabilty of open-source resources for the football and data analytics community
"""

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="nflscraPy", 
        version=VERSION,
        license="MIT License",
        url = "https://github.com/blnkpagelabs/nflscraPy",
        author="Tyler Durden",
        author_email="blankpagelabs@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "beautifulsoup4>=4.11.1",
            "bs4>=0.0.1",
            "certifi>=2022.12.7",
            "charset-normalizer>=2.1.1",
            "idna>=3.4",
            "numpy>=1.24.1",
            "pandas>=1.5.2",
            "python-dateutil>=2.8.2",
            "pytz>=2022.7",
            "requests>=2.28.1",
            "six>=1.16.0",
            "soupsieve>=2.3.2.post1",
            "urllib3>=1.26.13",
        ],
        keywords=[
            'python', 
            'scraper',
            'NFL Data',
            'Pro Football Reference',
            'Sports Reference',
            'fiveThirtyEight',
        ],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
        ]
)