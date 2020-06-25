import pandas as pd
import os
from app.core import Core
from app.scrapping import Scrapping

class Application:

    def __init__(self):
        self.Players = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "saves", "players.csv"))

    def team(self, parameters):
        core = Core(self.Players)
        return core.build_team_by_roi()
    
    def refresh(self):
        self.Players = Scrapping()
        print("Refreshed") 