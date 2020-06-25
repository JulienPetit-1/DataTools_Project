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

    def get_money_team_objects(self, budget = 100, count_limit = 2, gk = 2, df = 5, md = 5, atk = 3):
        money_team = []
        budget = budget
        injured = self.players_by_status('injuried')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Attacker': atk}
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
        return money_team

    def build_team_by_roi(self, budget = 100, count_limit = 2, gk = 2, df = 5, md = 5, atk = 3):
        money_team = []
        budget = budget
        injured = self.players_by_status('injuried')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Attacker': atk}
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
                        
        final_team = [(item['Name'], item['Position'], item['Cost']) for item in money_team]
        total_points = sum([item['Goals'] for item in money_team])
        print('Budget: ' + str(round(budget, 2)))
        print('OnzeDeLegende picked the following team:')
        print('GK: '), print([(item[0], item[2]) for item in final_team if item[1] == "Goalkeeper"])
        print('DF: '), print([(item[0], item[2]) for item in final_team if item[1] == "Defender"])
        print('MD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Midfielder"])
        print('ATK: '), print([(item[0], item[2])  for item in final_team if item[1] == "Attacker"])
        print('Points: ' + str(total_points))
        return money_team

    def build_team_by_points(self, budget = 100, count_limit = 15, gk = 2, df = 5, md = 5, fwd = 3):
        points_team = []
        budget = budget
        injured = self.players_by_status('injuried')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Attacker': atk}
        for player in self.points_top_players():
            if len(points_team) < count_limit and player not in injured and budget >= player['Cost'] and positions[player['Position']] > 0:
                points_team.append(player)
                budget -= player['Cost']
                positions[player['Position']] = positions[player['Position']] - 1
        final_team = [(item['Name'], item['Position'], item['Cost']) for item in points_team]
        total_points = sum([item['Goals']for item in points_team])
        print('Remaining Budget: ' + str(round(budget, 2)))
        print('AVG Joe has picked the following team:')
        print('GK: '), print([(item[0], item[2]) for item in final_team if item[1] == "Goalkeeper"])
        print('DF: '), print([(item[0], item[2]) for item in final_team if item[1] == "Defender"])
        print('MD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Midfielder"])
        print('ATK: '), print([(item[0], item[2])  for item in final_team if item[1] == "Attacker"])
        print('Points: ' + str(total_points))
        return points_team