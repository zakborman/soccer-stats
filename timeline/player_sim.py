import csv
from collections import defaultdict
from functools import lru_cache

def load_trophies(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

    header = data[0]
    clubs_data = data[1:]

    years = header[1:-1]

    trophies = {}
    club_nations = {}
    for row in clubs_data:
        club = row[0]
        nation = row[1]
        values = list(map(int, row[2:]))
        trophies[club] = dict(zip(years, values))
        club_nations[club] = nation  # <-- Track nations here

    return trophies, club_nations, years

def max_trophies(trophies, club_nations, years, start_season, min_seasons, excluded_nations=None, one_club_per_nation=False):
    if excluded_nations is None:
        excluded_nations = set()

    start_idx = years.index(start_season)
    total_seasons = len(years)

    @lru_cache(maxsize=None)
    def dfs(season_idx, used_nations_fset, used_clubs_fset):
        if season_idx >= total_seasons:
            return 0, []

        used_nations = set(used_nations_fset)
        used_clubs = set(used_clubs_fset)

        best_total = 0
        best_path = []

        for club in trophies:
            nation = club_nations[club]

            if nation in excluded_nations:
                continue

            if one_club_per_nation and nation in used_nations and club not in used_clubs:
                continue  # 👈 skip other clubs from used nations

            for stint_length in range(min_seasons, total_seasons - season_idx + 1):
                end_idx = season_idx + stint_length
                stint_years = years[season_idx:end_idx]

                club_trophies = sum(trophies[club][year] for year in stint_years)

                new_used_nations = used_nations.copy()
                new_used_clubs = used_clubs.copy()

                if one_club_per_nation and nation not in used_nations:
                    new_used_nations.add(nation)

                new_used_clubs.add(club)

                future_total, path = dfs(end_idx, frozenset(new_used_nations), frozenset(new_used_clubs))
                total = club_trophies + future_total

                if total > best_total:
                    best_total = total
                    best_path = [(club, stint_years)] + path

        return best_total, best_path


    return dfs(start_idx, frozenset(), frozenset())

if __name__ == "__main__":
    filename = "trophy_timeline.csv"
    start_season = "2004/05"
    min_seasons = 4
    excluded_nations = {"France"}
    one_club_per_nation = False

    trophies, club_nations, years = load_trophies(filename)
    total, path = max_trophies(
        trophies,
        club_nations,
        years,
        start_season,
        min_seasons,
        excluded_nations,
        one_club_per_nation,
    )

    print(f"\nMaximum possible trophies: {total}")
    for club, stint in path:
        print(f"{club}: {stint[0]} to {stint[-1]} ({len(stint)} seasons)")
