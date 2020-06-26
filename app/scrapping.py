from urllib.request import Request, urlopen
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime


class Scrapping:

    links_scrap = [ 'https://int.soccerway.com/players/topscorers/', 'https://int.soccerway.com/players/transfers/']

    def get_html_from_page(self, link):

        '''
            Extract html code from a choosen web site

            Get HTML from web page and parse it.

            :param page_link: link of the webpage we want to scrap
            :type page_link: string
            :return: BeautifulSoup object (HTML parsed)
            :rtype: bs4.BeautifulSoup
        '''
        
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        
        return soup
    

    def get_links_to_players(self, root_html):
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

    def extract_player_info(self, player_html):
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
                - player_status: status of the player
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
            player_diff_days = (datetime.today() - datetime.strptime(player_html.find('td', {"class":"enddate"}).text, '%d/%m/%y')).days
        except:
            player_diff_days = np.nan
            
        if player_diff_days > 30:
            player_status = "available"
        elif player_diff_days < 0:
            player_status = "injuried"
        else:
            player_status = "doubtful"
            
        try:
            player_ROI = player_goals / player_cost * 10
        except:
            player_ROI = player_cost

        for link in player_html.find_all('img'): 
            ref = link.get("src")
            if '/players/' in ref:
                player_image = ref

        return player_name, player_club, player_cost, player_role, player_goals, player_time, player_match, player_red_cards, player_status, player_ROI, player_image


    def add_players_list(self):
        '''
            Add players infos to a list

            :return: players : list of the player's informations

            :rtype: ArrayList
        '''
    
        players = []
        
        for i in self.links_scrap:
            soup = self.get_html_from_page(i)
            links = self.get_links_to_players(soup)
            for link in links:
                try:
                    new_link= 'https://int.soccerway.com' + link
                    soup_player = self.get_html_from_page(new_link)
                    result = self.extract_player_info(soup_player)
                    players.append(result)
                    print(result)
                except: 
                    next

        return players
    
    def __init__(self):
        players = self.add_players_list()
        return pd.DataFrame(data=list(set(players)), columns = ['Name', 'Club', 'Cost', 'Position', 'Goals', 'Minutes_played', 'Matchs', 'Red_Cards', 'Status', 'ROI', 'Asset'])