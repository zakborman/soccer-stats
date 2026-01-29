import time
import re
import pandas as pd
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def lgrank(first=1960, last=2025):
    driver = webdriver.Firefox(service=Service('/usr/bin/geckodriver'), options=Options())

    # country -> { season: fraction_of_season_points }
    country_pct = defaultdict(dict)

    for season in range(first, last+1):
        method = 1
        if season >= 1999:
            method = 2
        if season >= 2004:
            method = 3
        if season >= 2009:
            method = 4
        if season >= 2018:
            method = 5

        url = f"https://kassiesa.net/uefa/data/method{method}/crank{season}.html"
        driver.get(url)
        time.sleep(2)

        # Wait for the table to load
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.t1"))
            )
        except:
            continue

        season_total = 0.0
        season_points_map = {}
        visible_rows = driver.find_elements(By.CSS_SELECTOR, "table.t1 tbody tr.countryline")

        for element in visible_rows:
            country = element.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
            points_text = element.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text.strip()

            # Normalize and parse numeric value
            points_text_clean = points_text.replace(',', '')
            points = float(points_text_clean)
            season_total += points
            season_points_map[country] = points

        if season_total == 0:
            continue

        # compute fraction (points / season_total) for each country
        for country, pts in season_points_map.items():
            country_pct[country][season] = pts / season_total

    driver.close()

    # Build DataFrame: rows = countries, columns = seasons
    # country_pct is { country: { season: fraction } }
    df_out = pd.DataFrame(country_pct).fillna(0).T
    # Order columns (seasons) ascending
    try:
        ordered_cols = sorted(df_out.columns)
        df_out = df_out.reindex(columns=ordered_cols)
    except Exception:
        pass

    # Convert fractions to percentages and export CSV.
    df_out = df_out * 100

    # ensure first column header is "Country" in the CSV
    df_out.index.name = 'Country'
    df_out.to_csv('season_country_percentages.csv', float_format='%.6f', index_label='Country')

    return df_out


if __name__ == '__main__':
    lgrank()