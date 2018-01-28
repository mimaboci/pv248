import json
from bokeh.plotting import ColumnDataSource, figure, show
from bokeh.models import LabelSet, ranges
from cmath import pi

file = open('election.json')
data = json.load(file)
    
names = []
shares = []
colors = []        
below_One_sum = 0

for i in data:
    if(i.get('share') < 1):
        below_One_sum += i.get('share') 
        continue
    shares.append(i.get('share'))
    if 'short' in i:
        names.append("{} {}%".format(i.get('short'), i.get('share')))
    else:
        names.append(i.get('name'))
    if 'color' in i:
        colors.append(i.get('color'))
    else:
        colors.append("#000000")

names.append("below one {:.2f}%".format(below_One_sum))
shares.append("{:.2f}".format(below_One_sum))
colors.append("#000000")
x = range(0, len(shares))
    
#barplot

def barplot():

    source = ColumnDataSource(dict(x=x,y=shares, names = names, color=colors))

    plot = figure( title = "volby 2017",
                    x_axis_label = "strany",
                    y_axis_label = "hlasy" )

    plot.vbar(source=source, x='x', top='y', bottom=0, width=0.7, color='color', legend='names')

    labels = LabelSet(x='x', y='y', text='y', level='glyph',
            x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')
    plot.add_layout(labels)

    show(plot)

#piechart

def piechart():

    shares2 = [0] + shares
    percents = []
    achieved = 0
    for s in shares2:
        achieved += (float(s) / 100)
        percents.append(achieved)

    source = ColumnDataSource(data={
        'start':[p*2*pi for p in percents[:-1]],
        'end':[p*2*pi for p in percents[1:]],
        'color':colors,
        'label': names,
        'value': percents[:-1]
    })

    plot = figure(x_range=(-1,1), y_range=(-1,1))
    plot.wedge(x=0, y=0, radius=1,
            start_angle='start',
            end_angle='end',
            color='color',
            legend='label',
            source=source)

    show(plot)
