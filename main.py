import numpy as np
import pandas as pd
from bokeh.io import show, output_file
from bokeh.models import HoverTool
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure, save
import geopandas as gpd
import copy

def rgbtohex(r,g,b):
    x=[]
    array=list(zip(r,g,b))
    for (r,g,b) in array:
        x.append('#%02x%02x%02x' % (r, g, b))
    x=np.array(x)
    return x

def percent_to_color(pct):
    max1=max(pct)
    min1=min(pct)
    denom=max1-min1
    x=[]
    for item in pct:
        x.append((item-min1)/denom)
    r=[]
    g=[]
    b=[]
    for val in x:
        r.append(255)
        g.append(((2000**-val))*220)
        b.append(((2000**-val))*152+80)
    return np.floor(r).astype('int'),np.floor(g).astype('int'),np.floor(b).astype('int')

def state_data(party,party_dict):
    states=[]
    percent=[]
    for state in party_dict[party][0]:
        states.append(state)
        percent.append(party_dict[party][0][state][1])
    return states,percent

def save_csv_of_party(party,party_dict):
    states,percent=state_data(party,party_dict)
    test=pd.DataFrame()
    test['State']=states
    test['Percent']=percent
    return test

def initial_run():
    df=pd.read_csv('India general election results 2014 - Complete List.csv')
    statename=[]
    for index,row in df.iterrows():
        statename.append(str(row['State']))
        statename=list(set(statename))
        votes=[]
        j=0
    for index,row in df.iterrows():
        votes.append(0)
        count=[x for x in row['Votes'].split(',')]
        l=len(count)
        for i in range(l):
            votes[j]+=int(count[i])*(1000**(l-i-1))
        j+=1
    df['Votes']=votes

    state_dict={}
    for state in statename:
        state_dict[state]=0

    state_count = copy.deepcopy(state_dict)
    for index,row in df.iterrows():
        state_count[row['State']]+=row['Votes']

    partyname=[]
    for item in df['Party']:
        partyname.append(str(item))
    partyname=list(set(partyname))

    party_dict={}
    state_for_party={}
    for state in statename:
        state_for_party[state]=[0,0]
    for party in partyname:
        party_dict[party]=[copy.deepcopy(state_for_party),0]

    for index,row in df.iterrows():
        party_dict[row['Party']][0][row['State']][0]+=row['Votes']
        party_dict[row['Party']][1]+=row['Votes']
    for party in party_dict:
        for state in party_dict[party][0]:
            party_dict[party][0][state][1]=(party_dict[party][0][state][0]*100.0)/state_count[state]

    grid = gpd.read_file('gadm36_IND_1.shp')
    tel=grid['geometry'][31]
    ap=grid['geometry'][1]
    ap=ap.union(tel)
    grid=grid.drop([31])
    grid['geometry'][1]=ap

    return party_dict,grid

def print_map(party, party_dict, grid):
    test=save_csv_of_party(party,party_dict)
    test=test.sort_values('State')
    test=test.reset_index(drop=True)
    delhi=pd.DataFrame({"State": 'NCT of Delhi', "Percent": test.iloc[9]['Percent']}, index=[24])
    test=test.drop([9]).reset_index(drop=True)
    test = pd.concat([test.iloc[:24], delhi, test.iloc[24:]]).reset_index(drop=True)
    grid['Percent']=test['Percent'].values
    grid['State']=test['State'].values
    r,g,b=percent_to_color(test['Percent'].values)
    percent=rgbtohex(r,g,b)
    grid['percent']=percent
    source = GeoJSONDataSource(geojson=grid.to_json())
    p = figure(plot_width=600, plot_height=600,output_backend="webgl")
    p.patches('xs', 'ys', source=source, fill_color='percent',line_color='black',line_width=0.1)
    p.add_tools(HoverTool(tooltips=[
        ('State', "@State"),
        ('Percent', '@Percent')], ))
    output_file("templates/map.html", title="Votes Percentage")
    save(p)