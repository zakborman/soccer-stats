import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def season(first=1956, last=2025):
    driver = webdriver.Firefox(service=Service('/usr/bin/geckodriver'), options=Options())

    df = pd.DataFrame(columns=["Season", "Player", "Position", "Age", "Nationality", "Club", "League", "Matches", "Goals", "Assists", "G/A"])
    
    league_countries = ["Spain", "Italy", "England", "Germany", "Portugal", "Netherlands", "France"]
    positions = range(1,15)
    url_1 = "https://www.transfermarkt.com/scorer/topscorer/statistik/2024/plus/0/galerie/0?saison_id="
    url_3 = "&filter=0&yt0=Show"

    driver.get("https://www.transfermarkt.com")
    time.sleep(2)

    # Wait for iframe to be present and switch to it
    iframe = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='Iframe title']"))
    )
    driver.switch_to.frame(iframe)

    # Now try to find and click the button
    button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept & continue']"))
    )
    button.click()

    driver.switch_to.default_content()
    time.sleep(2)
    
    for season in range(first-1, last):
        print(str(season) + "-" + str(season+1)[2:])

        for position in positions: 
            if season >= 1992:
                url_2 = f"{season}&selectedOptionKey=6&land_id=0&altersklasse=&ausrichtung=&spielerposition_id={position}"
            else:
                url_2 = f"{season}&selectedOptionKey=5&land_id=0&altersklasse=&ausrichtung=&spielerposition_id={position}"
            
            driver.get(url_1 + url_2 + url_3)
            time.sleep(2)
            
            # Wait for the table to load
            try: 
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.items"))
                )
            except:
                continue

            # Get only the visible rows (they have 'odd' or 'even' class)
            visible_rows = driver.find_elements(By.CSS_SELECTOR, "table.items tbody tr.odd, table.items tbody tr.even")
            
            for element in visible_rows:
                player = element.find_element(By.XPATH, ".//table//tr//td[2]/a").text
                main_position = element.find_element(By.CSS_SELECTOR, "td:nth-child(2) table tbody tr:nth-child(2) td").text
                age = element.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                nationality = element.find_element(By.CSS_SELECTOR, "td:nth-child(4) img").get_attribute("title")
                
                try: 
                    club = element.find_element(By.CSS_SELECTOR, "td:nth-child(5) table tbody tr td:nth-child(2) a").text
                    league = element.find_element(By.CSS_SELECTOR, "td:nth-child(5) table tbody tr:nth-child(2) td a").text
                    league_country = element.find_element(By.CSS_SELECTOR, "td:nth-child(5) table tbody tr:nth-child(2) td img").get_attribute("title")
                    
                    if league_country not in league_countries:
                        continue
                    
                    league = league_country + " " + league

                except:
                    club = "Multiple clubs"
                    league = "N/A"

                matches = element.find_element(By.CSS_SELECTOR, "td:nth-child(6) a").text
                goals = element.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
                assists = element.find_element(By.CSS_SELECTOR, "td:nth-child(8)").text
                ga = element.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text

                # exceptions
                if player == "Neymar":
                    main_position = "Left Winger"

                ga_dict = {
                    "Season": season+1,
                    "Player": player,
                    "Position": main_position,
                    "Age": age,
                    "Nationality": nationality,
                    "Club": club,
                    "League": league,
                    "Matches": matches,
                    "Goals": goals,
                    "Assists": assists,
                    "G/A": ga
                }

                df.loc[len(df)] = ga_dict
                print(main_position, player)
    driver.close()
    df.drop_duplicates(subset=["Season", "Player", "Position", "Age", "Nationality", "Club", "League"]).to_csv("goal_contributions_season.csv", index=False)

def season_gk(first=1956, last=2025):
    driver = webdriver.Firefox()

    df = pd.DataFrame(columns=["Season", "Player", "Nationality", "Matches", "Clean Sheets", "Goals Conceded"])



def year(first, last):
    driver = webdriver.Firefox()

    df = pd.DataFrame(columns=["Year", "Player", "Position", "Nationality", "Matches", "Goals", "Assists", "G/A"])
    
    for year in range(first, last+1):
        if year > 1992:
            url = f"https://www.transfermarkt.com/spieler-statistik/jahrestorschuetzen/statistik/stat/plus/0/galerie/0?jahr={year}&selectedOptionKey=6&monatVon=01&monatBis=12&altersklasse=&land_id=&ausrichtung=alle&spielerposition_id=alle&art=2"
        else:
            url = f"https://www.transfermarkt.com/spieler-statistik/jahrestorschuetzen/statistik/stat/plus/0/galerie/0?jahr={year}&selectedOptionKey=5&monatVon=01&monatBis=12&altersklasse=&land_id=&ausrichtung=alle&spielerposition_id=alle&art=2"
        driver.get(url)
        time.sleep(2)
        
        if year == first:
            # Wait for iframe to be present and switch to it
            iframe = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='Iframe title']"))
            )
            driver.switch_to.frame(iframe)

            # Now try to find and click the button
            button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept & continue']"))
            )
            button.click()

            driver.switch_to.default_content()
            time.sleep(2)
        
        # Wait for the table to load
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.items"))
        )

        # Get only the visible rows (they have 'odd' or 'even' class)
        visible_rows = driver.find_elements(By.CSS_SELECTOR, "table.items tbody tr.odd, table.items tbody tr.even")

        print(year)
        
        for element in visible_rows:
            player = element.find_element(By.CSS_SELECTOR, "td:nth-child(2) table tbody tr td:nth-child(2) a").text
            position = element.find_element(By.CSS_SELECTOR, "td:nth-child(2) table tbody tr:nth-child(2) td").text
            nationality = element.find_element(By.CSS_SELECTOR, "td:nth-child(4) img").get_attribute("title")
            matches = element.find_element(By.CSS_SELECTOR, "td:nth-child(6) a").text
            goals = element.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
            assists = element.find_element(By.CSS_SELECTOR, "td:nth-child(8)").text
            ga = element.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text

            ga_dict = {
                "Year": year,
                "Player": player,
                "Position": position,
                "Nationality": nationality,
                "Matches": matches,
                "Goals": goals,
                "Assists": assists,
                "G/A": ga
            }

            df.loc[len(df)] = ga_dict
            print(player)
    driver.close()
    df.to_csv("goal_contributions_year.csv", index=False)

season()