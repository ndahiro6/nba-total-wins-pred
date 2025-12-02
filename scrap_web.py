import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from nba_api.stats.static import teams
import numpy as np

def get_spotrac_salary_cap(year):
    url = f"https://www.spotrac.com/nba/cap/{year}/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    print(f"Fetching {year} data...")
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"⚠️ Skipping {year} (status code {resp.status_code})")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if table is None:
        print(f"⚠️ No table found for {year}")
        return None

    df = pd.read_html(str(table))[0]
    df["SEASON"] = f"{year}-{year+1}"
    return df

all_years = []
for year in range(2010, 2025):
    if year in (2019, 2020):  # skip pandemic years
        continue
    df = get_spotrac_salary_cap(year)
    if df is not None:
        all_years.append(df)
    sleep(2)

# Combine
final_df = pd.concat(all_years, ignore_index=True)

# Clean columns
final_df.columns = [c.strip().upper().replace(" ", "_") for c in final_df.columns]

# Rename key columns to match stats data conventions
rename_map = {
    "TEAM": "TEAM_ABBREVIATION",
    "SEASON": "SEASON_STRING",
    "TOTAL_CAP_ALLOCATIONS": "TOTAL_CAP_ALLOCATIONS",
    "CAP_SPACE_ALL": "CAP_SPACE_ALL",
    "ACTIVE": "ACTIVE",
    "ACTIVE_TOP_3": "ACTIVE_TOP_3",
    "DEAD_CAP": "DEAD_CAP"
}
final_df.rename(columns=rename_map, inplace=True)

# Convert salary columns to numeric
salary_cols = ["TOTAL_CAP_ALLOCATIONS", "CAP_SPACE_ALL", "ACTIVE", "ACTIVE_TOP_3", "DEAD_CAP"]

for col in salary_cols:
    final_df[col] = (
        final_df[col]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .replace("-", np.nan)
    )
    final_df[col] = pd.to_numeric(final_df[col], errors="coerce")

# Clean abbreviations & team names
final_df["TEAM_ABBREVIATION"] = (
    final_df["TEAM_ABBREVIATION"]
    .astype(str)
    .str.strip()
    .str.split()
    .str[0]
)

final_df = final_df.replace(["", " ", "-", "--", "None", "nan"], pd.NA)

# Fetch NBA team metadata
nba_teams = teams.get_teams()
teams_df = pd.DataFrame(nba_teams)[["id", "abbreviation", "full_name"]]
teams_df.columns = ["TEAM_ID", "TEAM_ABBREVIATION", "TEAM_NAME"]

# Merge and finalize
merged_df = final_df.merge(teams_df, on="TEAM_ABBREVIATION", how="left")

merged_df["SEASON_START"] = merged_df["SEASON_STRING"].str[:4].astype(int)
merged_df.drop(columns=["SEASON_STRING"], inplace=True)

# Save results
print("✅ Cleaned and merged dataset preview:")
print(merged_df.head())

merged_df.to_csv("nba_salary_cap_2010_2024.csv", index=False)
teams_df.to_csv("team_metadata.csv", index=False)
