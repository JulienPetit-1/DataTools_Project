import pandas as pd

class Core:

    def __init__(self, players):
        index_with_nan = players.index[players.isnull().any(axis=1)]
        players.drop(index_with_nan,0, inplace=True)
        self.Players = players

    def roi_top_players(self):
        '''
            Sorted the player list by ROI from the top
                    
            :return: List of all players sorted by ROI descending
            :rtype: list(dict)
        '''
        return self.Players.sort_values(by=['ROI'], ascending=False).to_dict("records")

    def roi_bottom_players(self):
         '''
	        Sorted the player list by ROI from the bottom
            
	        :return: List of all players sorted by ROI ascending
	        :rtype: list(dict) 
        '''
        return self.Players.sort_values(by=['ROI'], ascending=True).to_dict("records")

    def average__player_roi(self):
         '''
	        Sorted the player list by ROI's mean
            
            :return: List of all players sorted by ROI's mean
            :rtype: list(dict)
        '''
        return round(float(self.Players['ROI'].mean(), 2)).to_dict("records")

    def points_top_players(self):

        '''
            Sorted the player list by goals
                    
            :return: List of all players sorted by goals
            :rtype: list(dict)
        '''
        return self.Players.sort_values(by=['Goals'], ascending=False).to_dict("records")
        
    def players_by_status(self, status):
        '''
            Sorted the player list by status
                    
            :return: List of all players sorted by status
            :rtype: list(dict)
        '''
        return self.Players[self.Players['Status'].str.match(status)].to_dict("records")

    def roi_filter_by_position(self, position, number = 10):
        '''
            Sorted the player's ROI by position
                    
            :return: List of all players sorted by position and ROI
            :rtype: list(dict)
        '''
        return self.Players[self.Players['Position'].str.match(position)].sort_values(by=['ROI'], ascending=False)[:number].to_dict("records")

    def points_filter_by_position(self, position, number = 10):
        '''
            Sorted the player's points by position
                    
            :return: List of all players sorted by position and points
            :rtype: list(dict)
        '''
        return self.Players[self.Players['Position'].str.match(position)].sort_values(by=['Goals'], ascending=False)[:number].to_dict("records")

    def team_list(self):
        '''
            Prepare the team list by grouping the players with their position
                    
            :return: Number of players in the teams
            :rtype: integer
        '''
        return self.Players.groupby('Club')['Position'].count()

    def player_list(self):
        '''
            Display all the players with their informations
                    
            :return: List of all players informations
            :rtype: List(dict)
        '''
        return self.Players.to_dict("records")

    def build_team_by_roi(self, budget = 100, count_limit = 2, gk = 2, df = 5, md = 5, atk = 3):

        '''
            Build the final team with all the previous informations
                    
            :param budget: Budget to allow for the team
            :type budget: integer
            :param count_limit: Number of stars for the team
            :type count_limit: integer
            :param gk: Number of goalkeepers
            :type gk: integer
            :param df: Number of defenders
            :type df: integer
            :param md: Number of midfielders
            :type md: integer
            :param atk: Number of attackers
            :type atk: integer

            :return: List of all players choosen for the final team
            :rtype: list(dict)
        '''
        
        money_team = []
        final_team = []
        i = 0
        budget = budget
        injured = self.players_by_status('injuried')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Attacker': atk}
        y = {'Goalkeeper': 410, 'Defender': 300, 'Midfielder': 50, 'Attacker': -190}
        x = {'Goalkeeper': 410, 'Defender': 300, 'Midfielder': 50, 'Attacker': -190}
        teams = self.team_list()
        for player in self.points_top_players():
            
            if len(money_team) < count_limit and player not in injured and budget >= player['Cost'] and positions[player['Position']] > 0 and teams[player['Club']] > 0:
                money_team.append(player)
                budget -= player['Cost']
                positions[player['Position']] = positions[player['Position']] - 1
                teams[player['Club']] = teams[player['Club']] - 1
            else:
                for player in self.roi_top_players():

                    if player not in money_team and budget >= player['Cost'] and positions[player['Position']] > 0 and teams[player['Club']] > 0 :
                        money_team.append(player)
                        budget -= player['Cost']
                        positions[player['Position']] = positions[player['Position']] - 1
                        teams[player['Club']] = teams[player['Club']] - 1
        for player in money_team:
            i = i + 1
            player['ROI'] = round(float(player['ROI']), 2)
            player['y'] = y[player['Position']]
            player['x'] = (600/len(money_team))*i*3 -400
            final_team.append(player)

        total_points = sum([item['Goals'] for item in money_team])
        print('Budget: ' + str(round(budget, 2)))
        print('OnzeDeLegende picked the following team:')
        print('Points: ' + str(total_points))
        return final_team