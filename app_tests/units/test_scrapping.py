import unittest
 
class TestScrapping(unittest.TestCase):
    def test_extract_players_info():
        # Assign
        test_link = f"https://int.soccerway.com/players/paul-pogba/177208/"
        html = Scrapping.get_html_from_page(test_link) 
        expected_output = ('P. Pogba', 'Manchester United', 105.0, 'Midfielder', 0, 627, 9, 0, 'doubtful', 0.0, 'https://secure.cache.images.core.optasports.com/soccer/players/18x18/420221.png')
 
        # Acts
        output = Scrapping.extract_players_info(html)
 
        # Assert
        assert expected_output == output