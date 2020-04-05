from math import pi
import csv
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from collections import Counter
from bokeh.embed import components





#-----BOKEH PLOTS-----#


def gamesPieChart(players, numOfGames, finishedRaces): # creates a pie chart that compares the most playing players' amount of games to the total amount of games
    output_file("pie.html")

    g = Counter(numOfGames)
    mostGames = g.most_common(3)

    x = dict()
    
    for mg in mostGames:
        finishedRaces -= mg[1]
        x[mg[0]] = mg[1]

    rest = finishedRaces
    
    x['rest'] = rest

    

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'player'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]

    p = figure(plot_height=350, title="Anteile der Top 3 an Gesamtzahl der Spiele", toolbar_location=None,
               tools="hover", tooltips="@player: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    script, div = components(p)

    return [script, div]




def barChartChosenAndAverage(categoryList, dictionary, player, myTitle): # bar chart that compares the average value of a specific dict to the dict's value of a chosen player
    output_file("bar_sorted.html")

    valueList = []

    for key in categoryList:
        valueList.append(dictionary[key])


    average = sum(valueList)/len(valueList)

    x_Axis = ['Durchschnitt', str(player)]
    y_Axis = [average, dictionary[player]]

    p = figure(x_range=x_Axis, plot_height=250, title=myTitle,
               toolbar_location=None)

    p.vbar(x=x_Axis, top=y_Axis, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    script, div = components(p)
    return [script,div]






def xSortedDictBarChart(keys, dictionary, myTitle): # creates a bar chart that holds keys of a dictionary as the x-axis and their corresponding values as the y-values
    output_file('chart.html')

    keys.sort()
    x_Axis = [] 
    y_Axis = []

    for k in keys:
        x_Axis.append(str(k))
        y_Axis.append(dictionary[k])

    p = figure(x_range=x_Axis, plot_height=250, title=myTitle,
               toolbar_location=None)

    p.vbar(x=x_Axis, top=y_Axis, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    script, div = components(p)

    return [script,div]

