# Predicting NBA Teams' Total Wins 

This project builds a predictive modeling pipeline to estimate NBA teams’ total wins using historical performance, roster composition, and salary-cap structure data from 2010–2024. I combined multiple data sources including team statistics from Basketball Reference, salary and cap information from Spotrac, and additional player metrics through the NBA API to create a unified, analysis-ready dataset.

After extensive exploration of correlations and multicollinearity, I engineered key features such as cap space ratio, dead cap ratio, top-3 salary ratio, point differential, defensive rebound differential, and previous season wins. I evaluated several modeling techniques (Ridge, Lasso, PCA-based regression, and Bayesian regression), with Ridge and Lasso achieving the strongest performance (RMSE ≈ 7.8).

The project includes data scraping, cleaning, feature engineering, model training, evaluation, and forward prediction for the 2024 season. It demonstrates how roster construction, financial structure, and team-level performance metrics interact to shape expected outcomes across an NBA season.
Sportsref/
Folder containing raw scraped data from Basketball Reference (team stats, opponent stats, advanced metrics, etc.).

- **script.ipynb**
Jupyter Notebook containing exploratory data analysis (EDA), feature engineering, regression model training, and evaluation.

- **combine.py**
Script that merges all cleaned datasets (salary cap, injuries, opponent stats, metadata) into a single flat modeling dataframe.

- **final.csv**
Final combined dataset used for modeling (Ridge/Lasso/PCA/Bayesian regression).

- **nba_salary_cap_2010_2024.csv**
Salary cap and team payroll data scraped from Spotrac for seasons 2010–2024.

- **nba_team_injuries_2010_2024.csv**
Dataset of team injury counts and metrics scraped from injury reports across seasons.

- **nba_team_opponent_combined_2010_2024.csv**
Combined team + opponent performance metrics (per-game, Four Factors, shooting splits, etc.) scraped from Basketball Reference.

- **scrap_web.py**
Web-scraper that collects team and opponent performance stats for all seasons from Basketball Reference.

- **scrap_web_injury.py**
Web-scraper that collects injury-related data for all teams across seasons.

- **team_metadata.csv**
Additional metadata for each NBA team (e.g., team IDs, abbreviations, conference, etc.) used to ensure consistent joins across datasets.