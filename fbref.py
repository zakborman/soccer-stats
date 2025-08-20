import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def fbref():
    options = Options()
    service = Service(executable_path="msedgedriver.exe")

    out_df = pd.DataFrame(columns = ["Player", "Age", "Nation", "Club", "Position", "Min", "npG", "npxG", "Shots", "Assists", "xAG", "npxG + xAG", "SCA", "Pass Attempts", 
                                       "Pass %", "Prog Passes", "Prog Carries", "Take-Ons", "Touches (Att Pen)", "Prog Passes Rec",
                                       "Tackles", "Inter", "Blocks", "Clears", "Aerials", "OVR"])
    gk_df = pd.DataFrame(columns = ["Player", "Age", "Nation", "Club", "Min", "PSxG-GA", "GA", "Save %", "PSxG/SoT", "Save % (Pen)", "Clean Sheet %", "Touches", "Launch %",
                                     "Goal Kicks", "Length", "Crosses Stopped %", "Def. Actions", "Distance", "OVR"])
    leagues = [9, 12, 11, 20, 13]
    time.sleep(3)
    for id in leagues:
        driver = webdriver.Edge(service=service, options=options)
        driver.get("https://fbref.com/en/comps/" + str(id) + "/stats/")
        subdriver = webdriver.Edge(service=service, options=options)
        elements = driver.find_element(By.CSS_SELECTOR, "table#stats_standard").find_element(By.CSS_SELECTOR, "tbody").find_elements(By.CSS_SELECTOR,"tr")
        for element in elements:
            try:
                player = element.find_elements(By.CSS_SELECTOR, "td")[0].find_element(By.CSS_SELECTOR, "a").text
            except
                continue
            print(player)
            try:
                nation = element.find_elements(By.CSS_SELECTOR, "td")[1].find_element(By.CSS_SELECTOR, "a > span").text.split(" ")[1]
            except:
                nation = "-"
            try:
                age = int(element.find_elements(By.CSS_SELECTOR, "td")[4].text.split("-")[0])
            except:
                age = "-"
            club = element.find_elements(By.CSS_SELECTOR, "td")[3].find_element(By.CSS_SELECTOR, "a").text
            link = element.find_elements(By.CSS_SELECTOR, "td")[0].find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            subdriver.get(link)
            try:
                position = subdriver.find_element(By.CSS_SELECTOR, ".sr_preset").text.split("s. ")[1].split("s")[0]
                stats = subdriver.find_element(By.CSS_SELECTOR, ".stats_table").find_elements(By.CSS_SELECTOR, "tbody tr")
            except:
                continue
            level = subdriver.find_element(By.CSS_SELECTOR, "div.footer.no_hide_long").find_element(By.CSS_SELECTOR, "div").text
            # print(level)
            if(level.find("Big 5 Leagues") == -1): continue
            minutes = int(level.split("Based on ")[1].split(" minutes")[0])
            if(position == "Goalkeeper"):
                psxgga = int(stats[0].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                ga = int(stats[1].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                save = int(stats[2].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                psxgsot = int(stats[3].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                pen = int(stats[4].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                try:
                    clean = int(stats[5].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    touch = int(stats[7].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    launch = int(stats[8].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    kick = int(stats[9].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    length = int(stats[10].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                    cross = int(stats[12].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    action = int(stats[13].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    dist = int(stats[14].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                    ovr = sum([psxgga, ga, save, psxgsot, pen, clean, touch, launch, kick, length, cross, action, dist]) / 13
                except:
                    clean = pen
                    pen = "-"
                    touch = int(stats[6].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    launch = int(stats[7].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    kick = int(stats[8].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    length = int(stats[9].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                    cross = int(stats[11].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    action = int(stats[12].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                    dist = int(stats[13].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                    ovr = sum([psxgga, ga, save, psxgsot, clean, touch, launch, kick, length, cross, action, dist]) / 12

                gk_dict = {
                    "Player": player,
                    "Age": age,
                    "Nation": nation,
                    "Club": club,
                    "Min": minutes,
                    "PSxG-GA": psxgga,
                    "GA": ga,
                    "Save %": save,
                    "PSxG/SoT": psxgsot,
                    "Save % (Pen)": pen,
                    "Clean Sheet %": clean,
                    "Touches": touch,
                    "Launch %": launch,
                    "Goal Kicks": kick,
                    "Length": length,
                    "Crosses Stopped %": cross,
                    "Def. Actions": action,
                    "Distance": dist,
                    "OVR": ovr
                }

                gk_df.loc[len(gk_df)] = gk_dict
            else:
                npg = int(stats[0].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                npxg = int(stats[1].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                shots = int(stats[2].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                assist = int(stats[3].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                xag = int(stats[4].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                xswag = int(stats[5].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                sca = int(stats[6].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                passes = int(stats[8].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                passper = int(stats[9].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                progpass = int(stats[10].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                progcarry = int(stats[11].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                takeon = int(stats[12].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                touch = int(stats[13].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                rec = int(stats[14].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                tackle = int(stats[16].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                inter = int(stats[17].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                block = int(stats[18].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                clear = int(stats[19].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)
                aerial = int(stats[20].find_elements(By.CSS_SELECTOR, "td")[1].find_elements(By.CSS_SELECTOR, "div")[0].text)

                ovr = sum([npg, npxg, shots, assist, xag, xswag, sca, passes, passper, progpass, progcarry, takeon, touch, rec, tackle, inter, block, clear, aerial]) / 19
                
                out_dict = {
                    "Player": player,
                    "Age": age,
                    "Nation": nation,
                    "Club": club,
                    "Position": position,
                    "Min": minutes,
                    "npG": npg,
                    "npxG": npxg,
                    "Shots": shots,
                    "Assists": assist,
                    "xAG": xag,
                    "npxG + xAG": xswag,
                    "SCA": sca,
                    "Pass Attempts": passes,
                    "Pass %": passper,
                    "Prog Passes": progpass,
                    "Prog Carries": progcarry,
                    "Take-Ons": takeon,
                    "Touches (Att Pen)": touch,
                    "Prog Passes Rec": rec,
                    "Tackles": tackle,
                    "Inter": inter,
                    "Blocks": block,
                    "Clears": clear,
                    "Aerials": aerial,
                    "OVR": ovr,
                }
                
                out_df.loc[len(out_df)] = out_dict
        driver.close()
        subdriver.close()
        out_df.drop_duplicates(subset=["Player", "Age", "Nation", "Position"]).to_csv("fbref " + str(id) + " out.csv")
        gk_df.drop_duplicates(subset=["Player", "Age", "Nation"]).to_csv("fbref " + str(id) + " gk.csv")
    out_df.drop_duplicates(subset=["Player", "Age", "Nation", "Position"]).to_csv("fbref out.csv")
    gk_df.drop_duplicates(subset=["Player", "Age", "Nation"]).to_csv("fbref gk.csv")

fbref()