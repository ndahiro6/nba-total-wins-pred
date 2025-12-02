# Predicting NBA Teams' Total Wins 

This project builds a predictive modeling pipeline to estimate NBA teams’ total wins using historical performance, roster composition, and salary-cap structure data from 2010–2024. I combined multiple data sources including team statistics from Basketball Reference, salary and cap information from Spotrac, and additional player metrics through the NBA API—to create a unified, analysis-ready dataset.

After extensive exploration of correlations and multicollinearity, I engineered key features such as cap space ratio, dead cap ratio, top-3 salary ratio, point differential, defensive rebound differential, and previous season wins. I evaluated several modeling techniques (Ridge, Lasso, PCA-based regression, and Bayesian regression), with Ridge and Lasso achieving the strongest performance (RMSE ≈ 7.8).

The project includes data scraping, cleaning, feature engineering, model training, evaluation, and forward prediction for the 2024 season. It demonstrates how roster construction, financial structure, and team-level performance metrics interact to shape expected outcomes across an NBA season.