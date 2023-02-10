import pandas as pd
import numpy as np
import scipy.stats as stats
import lxml
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

nhl_df = nhl_df[nhl_df["year"] == 2018][["team", "W", "L"]]
for item in nhl_df["team"]:
    if item[-1] == "*":
        nhl_df["team"].replace(item, item[:-1], inplace = True)
for item in nhl_df["team"]:        
    nhl_df["team"].replace(item, item.split()[-1], inplace = True)
nhl_df = nhl_df[nhl_df["team"] != "Division"]

cities = cities[["Metropolitan area", "Population (2016 est.)[8]", "NHL"]]
cities.columns = ["City", "Population", "team"]

for item in cities["team"]:
    for i in range(len(item)):
        if item[i] == "[":
            cities["team"].replace(item, item[:i], inplace = True)

dct = {"Maple Leafs" : "Leafs", "Red Wings": "Wings", "Blue Jackets" : "Jackets", "Golden Knights" : "Knights"}
cities["team"].replace(dct, inplace = True)
cities["team"] = [team.split() for team in cities["team"]]

new_cities = pd.DataFrame()
for index, row in cities.iterrows():
    for team in row["team"]:
        if len(team) > 1:
            temp_row = row
            temp_row["team"] = team
            new_cities = new_cities.append(temp_row)
new_cities = new_cities.set_index("team")

merger = pd.merge(nhl_df, new_cities, how="inner", left_on = "team", right_on = "team")
merger["W"] = merger["W"].astype(int)
merger["L"] = merger["L"].astype(int)
merger["ratio"] = merger["W"]/(merger["L"]+merger["W"])
ratio = merger.groupby(["City", "Population"])["ratio"].mean()
populations = merger.groupby(["City"])["Population"].first()
def nhl_correlation(): 
    # YOUR CODE HERE
    
    population_by_region = [] # pass in metropolitan area population from cities
    win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    population_by_region = populations.values.astype(int)
    win_loss_by_region = ratio.values
    #raise NotImplementedError()

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
print(nhl_correlation())
