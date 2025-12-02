import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import numpy as np

def get_spotrac_injuries(year):
    url = f"https://www.spotrac.com/nba/injured/_/year/{year}/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
    }

    print(f"🩺 Fetching injury data for {year}...")
    with requests.Session() as s:
        s.max_redirects = 5
        try:
            resp = s.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"⚠️ Skipping {year}: {e}")
            return None

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"⚠️ No injury table found for {year}")
        return None

    df = pd.read_html(str(table))[0]
    df["SEASON"] = year
    return df


# --- Loop over smaller set for test ---
all_years = []
for year in range(2010, 2025):
    if year in (2019, 2020):
        continue
    df = get_spotrac_injuries(year)
    if df is not None:
        all_years.append(df)
    sleep(1.0)

if not all_years:
    raise SystemExit("❌ No data fetched; Spotrac likely blocking automation.")



final_df = pd.concat(all_years, ignore_index=True)


final_df.columns = [c.strip().upper().replace(" ", "_") for c in final_df.columns]

salary_cols = ["TOTAL_CAP_ALLOCATIONS", "CAP_SPACE_ALL", "ACTIVE", "ACTIVE_TOP_3", "DEAD_CAP"]


col = 'CASH_SEASON_CUMULATIVE'

final_df[col] = (
        final_df[col]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .replace("-", np.nan)
    )
final_df[col] = pd.to_numeric(final_df[col], errors="coerce")


final_df.to_csv("nba_team_injuries_2010_2024.csv", index=False)
print("✅ Saved raw injury data for 2015–2024.")
