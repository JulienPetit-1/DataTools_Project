import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class Scrapping:

    def get_links_to_players(root_html):
        '''
            Extract players links from URL_PLAYER_LISTE
            
            :param root_html: BeautifulSoup Element that contains all players links
            :type root_html: bs4.BeautifulSoup
            :return: List of all players links in the page
            :rtype: list(str)
        '''
        players_links = []

        for link in root_html.find_all('a'): 
            ref = str(link.get("href"))
            if '/players/' in ref:
                players_links.append(ref)
                players_links = list(set(players_links))
        return players_links


    def extract_player_info(player_html):
        '''
            Extract players infos from URL PLAYER HTML

            :param player_html: BeautifulSoup Element that contains players infos
            :type player_html: bs4.element.Tag
            :return:
                - player_name: name of the player
                - player_club: club of the player
                - player_role: position of the player
                - player_cost: cost of the player
                - player_goals: number of goals 
                - player_time: minutes played of the player
                - player_matchs: number of matchs 
                - player_red_cards: number of red cards of the players
                - player_points: number of points (goals number multiply by 5)
                - player_ROI : return of investment for the player (points divide by cost)
                
            :rtype: tuple(string, string, string, string, string, string, string, string, string, string)
        '''
        
        player_name = player_html.find('h1').text
        player_club = player_html.find('td', {"class":"team"}).text
        player_role = player_html.find('dd', {"data-position":"position"}).text
        try:
            player_cost = float(player_html.find('td', {"class":"type"}).text[1:].replace("€","").replace("M",""))
        except:
            player_cost = np.nan
        player_goals = int(player_html.find('td', {"class":"number statistic goals available"}).text)
        player_time = int(player_html.find('td', {"class":"number statistic game-minutes available"}).text)
        player_match = int(player_html.find('td', {"class":"number statistic appearances available"}).text)
        player_red_cards = int(player_html.find('td', {"class":"number statistic red-cards available"}).text)
        try:
            player_ROI = player_goals / player_cost * 10
        except:
            player_ROI = player_cost

        return player_name, player_club, player_cost, player_role, player_goals, player_time, player_match, player_red_cards, player_ROI


    def add_players_list(self):
        req = Request('https://int.soccerway.com/players/topscorers/', headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        player_list = self.get_links_to_players(soup)

        links = [ player_list[0], 'https://int.soccerway.com/players/transfers/' ]
        for link in links:
            players = []
            for link in self.get_links_to_players(soup):
                try:
                    new_link= 'https://int.soccerway.com' + link
                    req = Request(new_link, headers={'User-Agent': 'Mozilla/5.0'})
                    webpage = urlopen(req).read()
                    soup = BeautifulSoup(webpage, 'html.parser')
                    result = extract_player_info(soup)
                    players.append(result)
                    print(result)
                except: 
                    next

        return players
    
    def __init__(self):
        players = self.add_players_list()
        return pd.DataFrame(data=list(set(players)), columns = ['Name', 'Club', 'Cost', 'Position', 'Goals', 'Minutes played', 'Matchs', 'Red Cards', 'ROI'])