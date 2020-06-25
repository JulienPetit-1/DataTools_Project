import pandas as pd
import os
from app.core import Core
from app.scrapping import Scrapping

class Application:

    self.Players = pd.read_csv(os.path.join(os.path.abspath(__file__), "saves", "players.csv")))

    def team(self, parameters):
        return parameters
        core = Core(self.players)
        return core.get_money_team_objects()
    
    def refresh(self):
        scrap = Scrapping()
        print("Refreshed") 