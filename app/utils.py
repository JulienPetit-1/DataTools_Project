import pandas as pd
import os
from app.core import Core
from app.scrapping import Scrapping

class Application:

    Players = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "saves", "players.csv"))

    def team(self, parameters):
        core = Core(self.Players)
        return core.get_money_team_objects()
    
    def refresh(self):
        scrap = Scrapping()
        print("Refreshed") 