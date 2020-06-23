from app.core import Core
from app.scrapping import Scrapping

class Application:
    def team(self, parameters):
        return parameters
        core = Core()
        return core.get_money_team_objects()
    
    def refresh(self):
        scrap = Scrapping()
        scrap.run()
        print("Refreshed") 