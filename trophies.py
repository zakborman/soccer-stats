import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from unidecode import unidecode

def check_country(country):
    if country == "english" or country == "spanish" or country == "italian" or country == "german" or country == "french":
        return True
    elif country == "dutch" or country == "portuguese" or country == "brazilian" or country == "argentinian":
        return True
    else:
        return False

def players():
    urls = ["https://www.transfermarkt.us/premier-league/erfolgreichstespieler/wettbewerb/GB1", # England
            "https://www.transfermarkt.us/laliga/erfolgreichstespieler/wettbewerb/ES1", # Spain
            "https://www.transfermarkt.us/serie-a/erfolgreichstespieler/wettbewerb/IT1", # Italy
            "https://www.transfermarkt.us/bundesliga/erfolgreichstespieler/wettbewerb/L1", # Germany
            "https://www.transfermarkt.us/ligue-1/erfolgreichstespieler/wettbewerb/FR1", # France
            "https://www.transfermarkt.us/eredivisie/erfolgreichstespieler/wettbewerb/NL1", # Netherlands
            "https://www.transfermarkt.us/liga-nos/erfolgreichstespieler/wettbewerb/PO1", # Portugal
            "https://www.transfermarkt.us/campeonato-brasileiro-serie-a/erfolgreichstespieler/wettbewerb/BRA1", # Brazil
            "https://www.transfermarkt.us/superliga/erfolgreichstespieler/wettbewerb/AR1N", # Argentina
            "https://www.transfermarkt.us/uefa-champions-league/erfolgreichstespieler/pokalwettbewerb/CL", # Champions League
            "https://www.transfermarkt.us/copa-libertadores/erfolgreichstespieler/pokalwettbewerb/CLI"] # Copa Libertadores
    
    stats_df = pandas.DataFrame(columns = ["Player", "Nation", "Pos", "FIFA", "BDOR", "UEFA", 
                                           "WC", "NC", "NSC", "IC", "CC", "CSC", "L", "C", "SC", "LC", "YC", "O", "Total"])
    
    position_dict = {"Left Winger": "LW", "Centre-Forward": "CF", "Second Striker": "SS", "Right Winger": "RW", 
                     "Left Midfield": "LM", "Attacking Midfield": "AM", "Central Midfield": "CM", "Defensive Midfield": "DM", "Right Midfield": "RM",
                     "Left-Back": "LB", "Sweeper": "SW", "Centre-Back": "CB", "Right-Back": "RB", 
                     "Goalkeeper": "GK"}
    
    driver = webdriver.Edge('./msedgedriver')
    trophy_driver = webdriver.Edge('./msedgedriver')

    for url in urls:
        driver.get(url)
        time.sleep(1)
        entries = driver.find_elements(By.CSS_SELECTOR, "#yw1 > table > tbody > tr")
        for entry in entries:
            profile = entry.find_element(By.CSS_SELECTOR, "td:nth-child(1) > table > tbody > tr:nth-child(1) > td.hauptlink > a")
            link = profile.get_attribute("href").split("/profil")
            trophy_driver.get(link[0] + "/erfolge" + link[1])
            time.sleep(1)
            
            try:
                trophy_driver.switch_to.frame("sp_message_iframe_910281")
                reject_button = trophy_driver.find_element(By.CSS_SELECTOR, "#notice > div.message-component.message-row.mobile-reverse > div:nth-child(1) > button")
                print(reject_button.text)
                reject_button.click()
                trophy_driver.switch_to.default_content()
            except:
                print("no popup")

            player = profile.get_attribute("title")
            if (player[:4] == "Sir "):
                player = player[4:]
            print(player)
            
            try:
                nation = trophy_driver.find_element(By.CSS_SELECTOR, "#main > main > header > div.data-header__info-box > div > ul:nth-child(1) > li:nth-child(3) > span").text
            except:
                time.sleep(100)
                trophy_driver.get(link[0] + "/erfolge" + link[1])
                time.sleep(1)
                nation = trophy_driver.find_element(By.CSS_SELECTOR, "#main > main > header > div.data-header__info-box > div > ul:nth-child(1) > li:nth-child(3) > span").text

            try:
                position = position_dict[trophy_driver.find_element(By.CSS_SELECTOR, "#main > main > header > div.data-header__info-box > div > ul:nth-child(2) > li:nth-child(2) > span").text]
            except:
                continue

            fifa_poty = 0
            ballon_dor = 0
            uefa_poty = 0

            world_cup = 0
            national_cup = 0
            national_supercup = 0

            intercontinental_cup = 0
            continental_cup = 0
            continental_supercup = 0

            league = 0
            cup = 0
            supercup = 0
            league_cup = 0

            youth_cup = 0
            olympics = 0

            total = 0

            titles = trophy_driver.find_elements(By.CSS_SELECTOR, "h2.content-box-headline")
            print(len(titles), "titles")
            for title in titles:
                print(title.text)
                if title.text == "ALL TITLES":
                    continue
                header = unidecode(title.text).strip().lower().split("x ")
                count = int(header[0])
                comp = unidecode(header[1]).lower()
                print(count, comp)

                if comp == "the best fifa men's player":
                    fifa_poty += count
                elif comp == "winner ballon d'or":
                    ballon_dor += count
                elif comp == "uefa best player in europe":
                    uefa_poty += count
                
                elif comp == "world cup winner":
                    world_cup += count
                
                elif comp == "european champion":
                    national_cup += count
                elif comp == "copa america winner":
                    national_cup += count
                elif comp == "confederations cup winner":
                    national_cup += count
                elif comp == "winner uefa nations league":
                    national_cup += count

                elif comp == "conmebol-uefa cup of champions winner":
                    national_supercup += count
                
                elif comp == "fifa club world cup winner":
                    intercontinental_cup += count
                elif comp == "intercontinental cup winner":
                    intercontinental_cup += count
                
                elif comp == "champions league winner":
                    continental_cup += count
                elif comp == "european champion clubs' cup winner":
                    continental_cup += count
                elif comp == "uefa cup winner":
                    continental_cup += count
                elif comp == "europapokal der pokalsieger sieger":
                    continental_cup += count
                elif comp == "inter-cities fairs cup winner":
                    continental_cup += count
                elif comp == "copa libertadores winner":
                    continental_cup += count
                elif comp == "copa sudamericana winner":
                    continental_cup += count
                
                elif comp == "uefa supercup winner":
                    continental_supercup += count
                elif comp == "recopa sudamericana winner":
                    continental_supercup += count
                
                elif "champion" in comp and check_country(comp.split(" champion")[0]):
                    league += count
                
                elif "cup winner" in comp and check_country(comp.split(" cup winner")[0]):
                    cup += count
                elif comp == "english fa cup winner":
                    cup += count

                elif "super cup winner" in comp and check_country(comp.split(" super cup winner")[0]):
                    supercup += count
                elif comp == "campeon supercopa argentina" or comp == "winner supercopa do brasil":
                    supercup += count

                elif "league cup winner" in comp and check_country(comp.split(" league cup winner")[0]):
                    league_cup += count
                elif comp == "winner copa de la liga profesional":
                    league_cup += count
            
                elif "under-" in comp:
                    youth_cup += count
                elif comp == "olympic medalist":
                    olympics += count

            total += fifa_poty + ballon_dor + uefa_poty + world_cup + national_cup + national_supercup + intercontinental_cup + continental_cup + continental_supercup
            total += league + cup + supercup + league_cup + youth_cup + olympics

            trophy_dict = {"Player": player, "Nation": nation, "Pos": position, "FIFA": fifa_poty, "BDOR": ballon_dor, "UEFA": uefa_poty, 
                            "WC": world_cup, "NC": national_cup, "NSC": national_supercup, "IC": intercontinental_cup, "CC": continental_cup, "CSC": continental_supercup, "L": league, "C": cup, "SC": supercup, "LC": league_cup, "YC": youth_cup, "O": olympics, "Total": total}
            
            stats_df = stats_df.append(trophy_dict, ignore_index = True)
    stats_df.drop_duplicates().to_csv("trophies/players.csv")
    return stats_df

players()
