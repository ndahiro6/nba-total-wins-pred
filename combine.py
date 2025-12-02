import pandas as pd
import glob
import os
import re

# Folder containing your files
folder = "Sportsref"

# Get all files
files = glob.glob(os.path.join(folder, "sportsref_*_*.xls"))

team_dfs = []
opp_dfs = []

for file in files:
    match = re.search(r"sportsref_(\d{4})_(team|opponent)", file)
    if not match:
        continue
    year, file_type = match.groups()

    # Try to read file as Excel or HTML
    try:
        df = pd.read_excel(file, engine="xlrd")
    except Exception:
        try:
            df = pd.read_html(file)[0]
        except Exception as e:
            print(f"⚠️ Could not read {file}: {e}")
            continue

    # Clean data
    df = df.iloc[:-1, :]  # drop last row (League Average)
    if "Team" in df.columns:
        df["Team"] = (
            df["Team"].astype(str)
            .str.replace(r"\*", "", regex=True)
            .str.strip()
        )

    df["SEASON"] = int(year)

    if file_type == "team":
        team_dfs.append(df)
    else:
        opp_dfs.append(df)

# Combine all team and opponent data
if not team_dfs or not opp_dfs:
    raise ValueError("❌ No valid team or opponent files were read — check file names and paths!")

teams_all = pd.concat(team_dfs, ignore_index=True)
opps_all = pd.concat(opp_dfs, ignore_index=True)

# Add _OPP suffix
opps_all = opps_all.add_suffix("_OPP")
opps_all.rename(columns={"Team_OPP": "Team", "SEASON_OPP": "SEASON"}, inplace=True)

# Merge
combined = pd.merge(teams_all, opps_all, on=["Team", "SEASON"], how="inner")

print(f"✅ Combined shape: {combined.shape}")
print(combined.head())

# Save
combined.to_csv("nba_team_opponent_combined_2010_2024.csv", index=False)
print(f"💾 Saved!")
