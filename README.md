# playscrape

Scrape the Wayback Machine for archived PlaysTV content.

If found, videos will be downloaded in 720p (the only resolution available for most content) to a directory specified (current directory if unspecified) and organized into folders by game name.

## Requirements

- Python 3
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](http://docs.python-requests.org/en/master/)
- [Waybackpy](https://pypi.org/project/waybackpy/)

## Installation

1. Clone the project

   `git clone https://github.com/bheinks/playscrape.git`

2. Install required dependencies

   Poetry: `poetry install`

   Pip: `pip install requirements.txt`

## Usage
```
usage: playscrape.py [-h] username [path]

positional arguments:
  username    PlaysTV username
  path        video save location (default: current directory)
```
