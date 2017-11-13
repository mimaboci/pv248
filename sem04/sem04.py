import json
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet, ranges
from math import pi

file = open('election.json')
data = json.load(file)

names = []
shares = []
colors = []

below_One_sum = 0
for i in data:
    if(i.get('share') < 1):
        below_One_sum += i.get('share') #sum
        continue
    if 'short' in i:
		names.append(i.get('short'))
	else:
        names.append(i.get('name'))
	shares.append(i.get('share'))
	if 'color' in i:
		colors.append(i.get('color'))
	else:
        colorList.append("#000000")

names.append("below one")
shares.append(below_One_sum)
colors.append("#000000")

source = ColumnDataSource(dict(x=names,y=shares, color=colors))

plot = figure( title = "volby 2017",
			x_axis_label = "strany",
			y_axis_label = "hlasy" )

plot.vbar(source=source, x='x', top='y', bottom=0, width=0.7, color='color')

labels = LabelSet(x='x', y='y', text='y', level='glyph',
        x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')
plot.add_layout(labels)

show(plot)
