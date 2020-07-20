""" This file contains paths to elements in https://www.isoftbet.com/portfolio/ page """
from collections import namedtuple


GAMES_TOTAL = 115  # total number of games
SEARCH_BOX = 'quicksearch'  # element id

# Generate list of named tuples with games' xpaths to name, play button, image click
Games = namedtuple('Games', 'xpath name_xpath play_btn_xpath image_click_xpath')
GAMES = [Games(f'//*[@id="isotope"]/div[{i}]',
               f'//*[@id="isotope"]/div[{i}]/div/div[2]/a/h4',
               f'//*[@id="isotope"]/div[{i}]/div/div[4]/a',
               f'//*[@id="isotope"]/div[{i}]/div/div[1]/a') for i in range(1, GAMES_TOTAL + 1)]