# twitter-follow-bot
A tool for automatically following a bunch of Twitter accounts

## Installation:

Install Python 3: https://www.python.org/downloads/  
Install Selenium: `pip install selenium`

## Set up:

Enter all the information in the `config.ini` file.  
All the handles of the Twitter accounts to be followed must be in a _CSV_ file in the format shown in the `input.csv` file.

## Running the script:

Make sure that the input csv file is in the same directory as of the script and the `config.ini` file. Then run the script from command-line like the following  
```terminal
sumit@HAL9000:~/Documents/twitter-follow-bot$ python3 twitter-bot.py 
[?] The filename of the csv: input.csv
Following user: defcon
Following user: github
```
