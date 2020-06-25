import pandas as pd

class Core:

    def __init__(self, players):
        self.Players = players

    def roi_top_players(self):
        return self.Players.sort_values(by=['ROI'], ascending=False).values.tolist()

    def roi_bottom_players(self):
        return self.Players.sort_values(by=['ROI'], ascending=True).values.tolist()

    def average__player_roi(self):
        return round(float(self.Players['ROI'].mean(), 2)).values.tolist()

    def points_top_players(self):
        return self.Players.sort_values(by=['total_points'], ascending=False).values.tolist()
        
    def players_by_status(self, status):
        return self.Players[self.Players['status'].str.match(status)].values.tolist()

    def roi_filter_by_position(self, position, number = 10):
        return self.Players[self.Players['position'].str.match(position)].sort_values(by=['ROI'], ascending=False)[:number].values.tolist()

    def points_filter_by_position(self, position, number = 10):
        return self.Players[self.Players['position'].str.match(position)].sort_values(by=['total_points'], ascending=False)[:number].values.tolist()

    def team_list(self):
        return self.Players.groupby('team').values.tolist()

    def player_list(self):
        return self.Players.values.tolist()

    def get_money_team_objects(self, budget = 100, count_limit = 2, gk = 2, df = 5, md = 5, fwd = 3):
        money_team = []
        budget = budget
        injured = self.players_by_status('injured')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Forward': fwd}
        teams = { team for team in team_list() }
        for player in self.points_top_players():
            if len(money_team) < count_limit and player not in injured and budget >= player.cost and positions[player.position] > 0 and teams[player.team] > 0:
                money_team.append(player)
                budget -= player.cost
                positions[player.position] = positions[player.position] - 1
                del teams[player.team]
            else:
                for player in self.roi_top_players():
                    if player not in money_team and budget >= player.cost and positions[player.position] > 0 and teams[player.team] > 0:
                        money_team.append(player)
                        budget -= player.cost
                        positions[player.position] = positions[player.position] - 1
                        del teams[player.team]
        final_team = [(item.name, item.position, item.cost) for item in money_team]
        total_points = sum([item.total_points for item in money_team])
        return money_team

    def build_team_by_roi(self, budget = 100, count_limit = 2, gk = 2, df = 5, md = 5, fwd = 3):
        money_team = []
        budget = budget
        injured = self.players_by_status('injured')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Forward': fwd}
        teams = { team:3 for team in team_list() }
        for player in self.points_top_players():
            if len(money_team) < count_limit and player not in injured and budget >= player.cost and positions[player.position] > 0 and teams[player.team] > 0:
                money_team.append(player)
                budget -= player.cost
                positions[player.position] = positions[player.position] - 1
                teams[player.team] = teams[player.team] - 1
            else:
                for player in self.roi_top_players():
                    if player not in money_team and budget >= player.cost and positions[player.position] > 0 and teams[player.team] > 0:
                        money_team.append(player)
                        budget -= player.cost
                        positions[player.position] = positions[player.position] - 1
                        teams[player.team] = teams[player.team] - 1
        final_team = [(item.name, item.position, item.cost) for item in money_team]
        total_points = sum([item.total_points for item in money_team])
        print('Remaining Budget: ' + str(round(budget, 2)))
        print('Your AI has picked the following team:')
        print('GK: '), print([(item[0], item[2]) for item in final_team if item[1] == "Goalkeeper"])
        print('DF: '), print([(item[0], item[2]) for item in final_team if item[1] == "Defender"])
        print('MD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Midfielder"])
        print('FWD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Forward"])
        print('Points: ' + str(total_points))
        return money_team

    def build_team_by_points(self, budget = 100, count_limit = 15, gk = 2, df = 5, md = 5, fwd = 3):
        money_team = []
        budget = budget
        injured = self.players_by_status('injured')
        positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Forward': fwd}
        for player in self.points_top_players():
            if len(money_team) < count_limit and player not in injured and budget >= player.cost and positions[player.position] > 0:
                money_team.append(player)
                budget -= player.cost
                positions[player.position] = positions[player.position] - 1
        final_team = [(item.name, item.position, item.cost) for item in money_team]
        total_points = sum([item.total_points for item in money_team])
        print('Remaining Budget: ' + str(round(budget, 2)))
        print('AVG Joe has picked the following team:')
        print('GK: '), print([(item[0], item[2]) for item in final_team if item[1] == "Goalkeeper"])
        print('DF: '), print([(item[0], item[2]) for item in final_team if item[1] == "Defender"])
        print('MD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Midfielder"])
        print('FWD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Forward"])
        print('Total Fantasy Points: ' + str(total_points))
        return money_team

    def money_team_table(self):
        keys = Player.__table__.columns.keys()
        headers = [keys[3], 'team', keys[4],keys[5], 'points', keys[8], keys[10], 'ROI']
        rows = [[item.name, item.team.name, item.position, item.cost, item.total_points, item.minutes, item.roi] for item in get_money_team_objects()]
        return [headers, rows]