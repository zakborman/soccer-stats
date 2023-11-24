import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

LAST_SEASON = 2023

def summary(URL, first_season, comp, yearly = False, step = 1):
    stats_df = pd.DataFrame(columns = ["Player", "Season", "Age", "Position", "Team", "Apps", "Starts", "Mins", "Goals", "Assists", "MotM", "Rating", "Competition"])
    for year in range(first_season, LAST_SEASON+1, step):
        driver = webdriver.Edge('./msedgedriver')
        driver.get(URL)
        time.sleep(3)
        season = str(year-1) + "/" + str(year)
        format_season = str(year-1) + "-" + str(year)[-2:]
        if(yearly):
            season = str(year)
            if(year >= 2020 and year <= 2023):
                season = str(year-1)
                format_season = str(year) + "-" + str(year+1)[-2:]
        dropdown = Select(driver.find_element(By.ID, "seasons"))
        dropdown.select_by_visible_text(season)
        time.sleep(5)
        try:
            driver.find_elements(By.CSS_SELECTOR, "#sub-navigation > ul > li")[3].find_element(By.CSS_SELECTOR, "a").click()
        except:
            dropdown = Select(driver.find_element(By.ID, "stages"))
            if(comp == "POR Primeira Liga"):
                dropdown.select_by_visible_text("Primeira Liga")
            elif(comp == "UEFA Europa League"):
                dropdown.select_by_visible_text("Europa League Final Stage")
            elif(comp == "ITA Serie A"):
                dropdown.select_by_visible_text("Serie A")
            time.sleep(5)
            driver.find_elements(By.CSS_SELECTOR, "#sub-navigation > ul > li")[3].find_element(By.CSS_SELECTOR, "a").click()
        time.sleep(5)
        driver.find_elements(By.CSS_SELECTOR, '#apps > dd')[1].find_element(By.CSS_SELECTOR, "a").click()
        time.sleep(5)
        page = driver.find_elements(By.CSS_SELECTOR, '#statistics-paging-summary > div > dl.listbox.right > dt > b')[0].text
        page = int(page.split('/')[1].split(' ')[0])
        for i in range(page):
            if i != 0:
                driver.find_element(By.ID, 'next').click()
                time.sleep(5)
            temp_df = pd.DataFrame(columns = ["Player", "Season", "Age", "Position", "Team", "Apps", "Starts", "Mins", "Goals", "Assists", "MotM", "Rating", "Competition"])
            elements = driver.find_elements(By.CSS_SELECTOR, "#player-table-statistics-body tr")
            for element in elements:
                player = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "a")[0].find_elements(By.CSS_SELECTOR, "span")[0].text
                team = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "a")[1].find_elements(By.CSS_SELECTOR, "span")[0].text[:-1]

                age = int(element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "span")[4].text) - (LAST_SEASON - year)
                if(yearly and year >= 2020 and year <= 2022):
                    age += 1

                pos = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "span")[5].text[2:]
                if pos == "Forward":
                    pos = "FW"
                elif pos == "Midfielder":
                    pos = "M(CLR)"
                elif pos == "Defender":
                    pos = "D(CLR)"
                elif pos == "Goalkeeper":
                    pos = "GK"      

                apps = element.find_elements(By.CSS_SELECTOR, "td")[2].text
                if '(' in apps:
                    starts = apps.split('(')[0]
                    subs = apps.split('(')[1].split(')')[0]
                    apps = int(starts) + int(subs)
                else:
                    starts = apps

                mins = element.find_elements(By.CSS_SELECTOR, "td")[3].text
                goals = element.find_elements(By.CSS_SELECTOR, "td")[4].text
                assists = element.find_elements(By.CSS_SELECTOR, "td")[5].text
                motm = element.find_elements(By.CSS_SELECTOR, "td")[11].text
                rating = element.find_elements(By.CSS_SELECTOR, "td")[12].text
                stats_dict = {
                    "Player": player,
                    "Season": format_season,
                    "Age": age,
                    "Position": pos,
                    "Team": team,
                    "Apps": apps,
                    "Starts": starts,
                    "Mins": mins, 
                    "Goals": goals,
                    "Assists": assists, 
                    "MotM": motm,
                    "Rating": rating,
                    "Competition": comp,
                }
                for key in stats_dict:
                    if(stats_dict[key] == "-"):
                        stats_dict[key] = 0
                temp_df.loc[len(temp_df)] = stats_dict
            stats_df = pd.concat([stats_df,temp_df])
        driver.close()
    stats_df.to_csv(comp + ".csv")
    return stats_df

def teams(URL, first_season, comp, yearly = False, step = 1):
    stats_df = pd.DataFrame(columns = ["Team", "Season", "Goals", "SpG", "Yel", "Red", "Pass%", "AerialsWon", "Rating", "Competition"])
    driver = webdriver.Edge('./msedgedriver')
    driver.get(URL)
    for year in range(first_season, LAST_SEASON+1, step):
        time.sleep(3)
        season = str(year-1) + "/" + str(year)
        format_season = str(year-1) + "-" + str(year)[-2:]
        if(yearly):
            season = str(year)
            if(year >= 2020 and year <= 2022):
                format_season = str(year) + "-" + str(year+1)[-2:]
        dropdown = Select(driver.find_element(By.ID, "seasons"))
        dropdown.select_by_visible_text(season)
        time.sleep(5)
        try:
            driver.find_elements(By.CSS_SELECTOR, "#sub-navigation > ul > li")[2].find_element(By.CSS_SELECTOR, "a").click()
        except:
            dropdown = Select(driver.find_element(By.ID, "stages"))
            if(comp == "POR Primeira Liga"):
                dropdown.select_by_visible_text("Primeira Liga")
            elif(comp == "UEFA Europa League"):
                dropdown.select_by_visible_text("Europa League Final Stage")
            time.sleep(5)
            driver.find_elements(By.CSS_SELECTOR, "#sub-navigation > ul > li")[2].find_element(By.CSS_SELECTOR, "a").click()
        time.sleep(5)
        temp_df = pd.DataFrame(columns = ["Team", "Season", "Goals", "SpG", "Yel", "Red", "Pass%", "AerialsWon", "Rating", "Competition"])
        elements = driver.find_elements(By.CSS_SELECTOR, "#top-team-stats-summary-content tr")
        for element in elements:
            team = element.find_elements(By.CSS_SELECTOR, "td")[0].find_element(By.CSS_SELECTOR, "a").text.split(". ")[1]
            goals = element.find_elements(By.CSS_SELECTOR, "td")[1].text
            shots = element.find_elements(By.CSS_SELECTOR, "td")[2].text
            yellows = element.find_elements(By.CSS_SELECTOR, "td")[3].find_elements(By.CSS_SELECTOR, "span")[0].text
            reds = element.find_elements(By.CSS_SELECTOR, "td")[3].find_elements(By.CSS_SELECTOR, "span")[1].text
            #pos = element.find_elements(By.CSS_SELECTOR, "td")[4].text
            pas = element.find_elements(By.CSS_SELECTOR, "td")[5].text
            aerials = element.find_elements(By.CSS_SELECTOR, "td")[6].text
            rating = element.find_elements(By.CSS_SELECTOR, "td")[7].find_element(By.CSS_SELECTOR, "span").text
            stats_dict = {
                "Team": team,
                "Season": format_season,
                "Goals": goals,
                "SpG": shots,
                "Yel": yellows,
                "Red": reds,
                "Pass%": pas,
                "AerialsWon": aerials,
                "Rating": rating,
                "Competition": comp,
            }
            for key in stats_dict:
                if(stats_dict[key] == "-"):
                    stats_dict[key] = 0
            temp_df.loc[len(temp_df)] = stats_dict
        stats_df = pd.concat([stats_df,temp_df])
    stats_df.to_csv("Teams " + comp + ".csv")
    driver.close()
    return stats_df


def nation(driver, URL, first_season, comp, country):
    stats_df = pd.DataFrame(columns = ["Player", "Team", "Age", "Position", "Apps", "Mins", "Rating", "Competition"])
    driver.get(URL)
    time.sleep(3)
    driver.find_elements(By.CSS_SELECTOR, "#sub-navigation > ul > li")[3].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#detailed-statistics-tab > a").click()
    time.sleep(3)
    dropdown = Select(driver.find_element(By.ID, "nationality"))
    try:
        dropdown.select_by_visible_text(country)
    except:
        return
    driver.find_element(By.CSS_SELECTOR, "button.search-button").click()
    time.sleep(3)
    page = driver.find_elements(By.CSS_SELECTOR, '#statistics-paging-detailed > div > dl.listbox.right > dt > b')[0].text
    page = int(page.split('/')[1].split(' ')[0])
    for i in range(page):
        if i != 0:
            try:
                driver.find_element(By.CSS_SELECTOR, 'a#next').click()
            except:
                break
            time.sleep(3)
        temp_df = pd.DataFrame(columns = ["Player", "Team", "Age", "Position", "Apps", "Mins", "Rating", "Competition"])
        elements = driver.find_elements(By.CSS_SELECTOR, "#player-table-statistics-body tr")
        for element in elements:
            player = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "a")[0].find_elements(By.CSS_SELECTOR, "span")[0].text
            if(player == ""):
                continue
            team = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "a")[1].find_elements(By.CSS_SELECTOR, "span")[0].text[:-1]
            age = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "span")[4].text

            pos = element.find_elements(By.CSS_SELECTOR, "td")[0].find_elements(By.CSS_SELECTOR, "span")[5].text[2:]
            if pos == "Forward":
                pos = "FW"
            elif pos == "Midfielder":
                pos = "M(CLR)"
            elif pos == "Defender":
                pos = "D(CLR)"
            elif pos == "Goalkeeper":
                pos = "GK"      

            apps = element.find_elements(By.CSS_SELECTOR, "td")[2].text
            mins = element.find_elements(By.CSS_SELECTOR, "td")[3].text
            rating = element.find_elements(By.CSS_SELECTOR, "td")[8].text

            stats_dict = {
                "Player": player,
                "Team": team,
                "Age": age,
                "Position": pos,
                "Apps": apps,
                "Mins": mins, 
                "Rating": rating,
                "Competition": comp,
            }
            temp_df.loc[len(temp_df)] = stats_dict
        stats_df = pd.concat([stats_df,temp_df])
    return stats_df    


def complete_summary():
    #epl = summary("https://1xbet.whoscored.com/Regions/252/Tournaments/2/", 2023, "ENG Premier League")
    #sll = summary("https://1xbet.whoscored.com/Regions/206/Tournaments/4/", 2023, "ESP La Liga")
    #gb = summary("https://1xbet.whoscored.com/Regions/81/Tournaments/3/", 2023, "GER Bundesliga")
    #isa = summary("https://1xbet.whoscored.com/Regions/108/Tournaments/5/", 2023, "ITA Serie A")
    #fl1 = summary("https://1xbet.whoscored.com/Regions/74/Tournaments/22/", 2023, "FRA Ligue 1")
    #de = summary("https://1xbet.whoscored.com/Regions/155/Tournaments/13/", 2014, "NED Eredivisie")
    #rpl = summary("https://1xbet.whoscored.com/Regions/182/Tournaments/77/", 2014, "RUS Premier League")
    #tsl = summary("https://1xbet.whoscored.com/Regions/225/Tournaments/17/", 2015, "TUR Süper Lig")
    #ppl = summary("https://1xbet.whoscored.com/Regions/177/Tournaments/21/", 2017, "POR Primeira Liga")
    #sp = summary("https://1xbet.whoscored.com/Regions/253/Tournaments/20/", 2021, "SCO Premiership")
    #bpl = summary("https://1xbet.whoscored.com/Regions/22/Tournaments/18/", 2021, "BEL Pro League")
    #pd.concat([epl, sll, gb, isa, fl1, de, rpl, tsl, ppl, sp, bpl]).to_csv("Leagues.csv")
    #pd.concat([epl, sll, gb, isa, fl1]).to_csv("T5.csv")

    #ucl = summary("https://1xbet.whoscored.com/Regions/250/Tournaments/12/", 2023, "UEFA Champions League")
    #uel = summary("https://1xbet.whoscored.com/Regions/250/Tournaments/30/", 2013, "UEFA Europa League")
    #pd.concat([ucl, uel]).to_csv("Europe")
    #ucl.to_csv("UCL")
    
    #afcon = summary("https://1xbet.whoscored.com/Regions/247/Tournaments/104/", 2019, "AF Cup of Nations", True, 2)
    #cca = summary("https://1xbet.whoscored.com/Regions/247/Tournaments/94/", 2015, "CONMEBOL Copa America", True, 4)
    #uec = summary("https://1xbet.whoscored.com/Regions/247/Tournaments/124/", 2012, "UEFA European Championship", True, 4)
    fwc = summary("https://1xbet.whoscored.com/Regions/247/Tournaments/36/", 2023, "FIFA World Cup", True, 4)
    #pd.concat([afcon, cca, uec, fwc]).to_csv("International")
    fwc.to_csv("WC")

def complete_country(country):
    driver = webdriver.Edge('./msedgedriver')
    epl = nation(driver, "https://1xbet.whoscored.com/Regions/252/Tournaments/2/", 2010, "ENG Premier League", country)
    sll = nation(driver, "https://1xbet.whoscored.com/Regions/206/Tournaments/4/", 2010, "ESP La Liga", country)
    gb = nation(driver, "https://1xbet.whoscored.com/Regions/81/Tournaments/3/", 2010, "GER Bundesliga", country)
    isa = nation(driver, "https://1xbet.whoscored.com/Regions/108/Tournaments/5/", 2010, "ITA Serie A", country)
    fl1 = nation(driver, "https://1xbet.whoscored.com/Regions/74/Tournaments/22/", 2010, "FRA Ligue 1", country)
    de = nation(driver, "https://1xbet.whoscored.com/Regions/155/Tournaments/13/", 2014, "NED Eredivisie", country)
    rpl = nation(driver, "https://1xbet.whoscored.com/Regions/182/Tournaments/77/", 2014, "RUS Premier League", country)
    tsl = nation(driver, "https://1xbet.whoscored.com/Regions/225/Tournaments/17/", 2015, "TUR Süper Lig", country)
    ppl = nation(driver, "https://1xbet.whoscored.com/Regions/177/Tournaments/21/", 2017, "POR Primeira Liga", country)
    sp = nation(driver, "https://1xbet.whoscored.com/Regions/253/Tournaments/20/", 2021, "SCO Premiership", country)
    bpl = nation(driver, "https://1xbet.whoscored.com/Regions/22/Tournaments/18/", 2021, "BEL Pro League", country)

    eflc = nation(driver, "https://1xbet.whoscored.com/Regions/252/Tournaments/7/", 0, "ENG Championship", country)
    gb2 = nation(driver, "https://1xbet.whoscored.com/Regions/81/Tournaments/6/", 0, "GER 2. Bundesliga", country)

    mls = nation(driver, "https://1xbet.whoscored.com/Regions/233/Tournaments/85/", 0, "USA Major League Soccer", country)
    bsa = nation(driver, "https://1xbet.whoscored.com/Regions/31/Tournaments/95/", 0, "BRA Série A", country)
    apd = nation(driver, "https://1xbet.whoscored.com/Regions/11/Tournaments/68/", 0, "ARG Primera División", country)

    pd.concat([epl, sll, gb, isa, fl1, de, rpl, tsl, ppl, sp, bpl, eflc]).to_csv(country + ".csv")  
    driver.close()

def complete_teams():
    epl = teams("https://1xbet.whoscored.com/Regions/252/Tournaments/2/", 2010, "ENG Premier League")
    sll = teams("https://1xbet.whoscored.com/Regions/206/Tournaments/4/", 2010, "ESP La Liga")
    gb = teams("https://1xbet.whoscored.com/Regions/81/Tournaments/3/", 2010, "GER Bundesliga")
    isa = teams("https://1xbet.whoscored.com/Regions/108/Tournaments/5/", 2010, "ITA Serie A")
    fl1 = teams("https://1xbet.whoscored.com/Regions/74/Tournaments/22/", 2010, "FRA Ligue 1")
    de = teams("https://1xbet.whoscored.com/Regions/155/Tournaments/13/", 2014, "NED Eredivisie")
    rpl = teams("https://1xbet.whoscored.com/Regions/182/Tournaments/77/", 2014, "RUS Premier League")
    tsl = teams("https://1xbet.whoscored.com/Regions/225/Tournaments/17/", 2015, "TUR Süper Lig")
    ppl = teams("https://1xbet.whoscored.com/Regions/177/Tournaments/21/", 2017, "POR Primeira Liga")
    sp = teams("https://1xbet.whoscored.com/Regions/253/Tournaments/20/", 2021, "SCO Premiership")
    bpl = teams("https://1xbet.whoscored.com/Regions/22/Tournaments/18/", 2021, "BEL Pro League")

    ucl = teams("https://1xbet.whoscored.com/Regions/250/Tournaments/12/", 2010, "UEFA Champions League")
    uel = teams("https://1xbet.whoscored.com/Regions/250/Tournaments/30/", 2013, "UEFA Europa League")
    
    afcon = teams("https://1xbet.whoscored.com/Regions/247/Tournaments/104/", 2019, "AF Cup of Nations", True, 2)
    cca = teams("https://1xbet.whoscored.com/Regions/247/Tournaments/94/", 2015, "CONMEBOL Copa America", True, 4)
    uec = teams("https://1xbet.whoscored.com/Regions/247/Tournaments/124/", 2012, "UEFA European Championship", True, 4)
    fwc = teams("https://1xbet.whoscored.com/Regions/247/Tournaments/36/", 2014, "FIFA World Cup", True, 4)