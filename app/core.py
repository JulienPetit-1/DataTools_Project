import pandas as pd

class Core:

    def __init__(self, players):
        index_with_nan = players.index[players.isnull().any(axis=1)]
        players.drop(index_with_nan,0, inplace=True)
        self.Players = players

    def roi_top_players(self):
        return self.Players.sort_values(by=['ROI'], ascending=False).to_dict("records")

    def roi_bottom_players(self):
        return self.Players.sort_values(by=['ROI'], ascending=True).to_dict("records")

    def average__player_roi(self):
        return round(float(self.Players['ROI'].mean(), 2)).to_dict("records")

    def points_top_players(self):
        return self.Players.sort_values(by=['Goals'], ascending=False).to_dict("records")
        
    def players_by_status(self, status):
        return self.Players[self.Players['Status'].str.match(status)].to_dict("records")

    def roi_filter_by_position(self, position, number = 10):
        return self.Players[self.Players['Position'].str.match(position)].sort_values(by=['ROI'], ascending=False)[:number].to_dict("records")

    def points_filter_by_position(self, position, number = 10):
        return self.Players[self.Players['Position'].str.match(position)].sort_values(by=['Goals'], ascending=False)[:number].to_dict("records")

    def team_list(self):
        return self.Players.groupby('Club')['Position'].count()

    def player_list(self):
        return self.Players.to_dict("records")

    def build_team_by_roi(self, budget = 100, count_limit = 2, gk = 2, df = 5, md = 5, atk = 3):
        money_team = []
        final_team = []
        budget = budget
        injured = self.players_by_status('injuried')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Attacker': atk}
        y = {'Goalkeeper': 410, 'Defender': 300, 'Midfielder': 50, 'Attacker': -190}
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
        pos = None
        i = 0
        for player in money_team:
            player['ROI'] = round(float(player['ROI']), 2)
            player['y'] = y[player['Position']]
            if pos is not player['Position'] : 
                i = 1
                pos = player['Position']
            else:
                i = i + 1
            row_team = sum(value['Position'] == pos for value in money_team)
            player['x'] = (i/(row_team+1))* 600 - 300
            final_team.append(player)

        total_points = sum([item['Goals'] for item in money_team])
        print('Budget: ' + str(round(budget, 2)))
        print('Points: ' + str(total_points))
        return final_team