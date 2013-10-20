# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Use [urllib](http://docs.python.org/2/library/urllib.html) to open arbitrary resources by URL and pass that data to the [read_csv](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.parsers.read_csv.html) function of pandas. Then print out the first few rows of data using pandas [Indexing and Selecting Data](http://pandas.pydata.org/pandas-docs/dev/indexing.html).

# <codecell>

import urllib
from pandas import read_csv


url = 'http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M1.txt'
data = read_csv(urllib.urlopen(url))

data[0:10]

# <markdowncell>

# **UH OH!** Note that our data is a bit *dirty* and contains a notice that this data feed has been deprecated:

# <codecell>

print data[0:1]['Src'].values[0]

# <markdowncell>

# We can filter out the dirty data using [dropna](http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.dropna.html) to drop any rows that contain **NaN**.

# <codecell>

clean_data = data.dropna(axis=0, how='any')
clean_data[0:3]

# <markdowncell>

# In the code above note that I saved the results of `data.dropna()` into a different variable `clean_data` rather than over-writing the old variable `data`. **Why?** Why not just re-use old variable names? And if we did re-use old variable names what extra danger do we have to keep in mind while using the IPython Notebook?

# <markdowncell>

# Now let's just focus on earthquakes in Alaska (my home state! :)

# <codecell>

state = clean_data[clean_data.Src == 'ak']
state[0:10]

# <codecell>

from mpl_toolkits.basemap import Basemap

def bbox(q):
    #calculate quake bounding box
    Latmin = min(q.Lat)
    Latmax = max(q.Lat)
    Latmid = average(q.Lat)
    Lonmin = min(q.Lon)
    Lonmax = max(q.Lon)
    Lonmid = average(q.Lon)
    # create appropriate boundary, reject weird outliers
    if Lonmid+4*sqrt(var(q.Lon))< Lonmax or Lonmid-4*sqrt(var(q.Lon))> Lonmin:
        Height = 2*sqrt(var(q.Lon))
    elif 1>0:
        Height = max((Lonmax-Lonmid+1),(Lonmid-Lonmin+1))
    if Latmid+4*sqrt(var(q.Lat))< Latmax or Latmid-4*sqrt(var(q.Lat))> Latmin:
        Width =2*sqrt(var(q.Lat))
        b = [Latmid-Width,Latmid+Width, Lonmid-Height, Lonmid+Height]
    elif 1>0:
        Width = max((Latmax-Latmid+1),(Latmid-Latmin+1))
        b = [Latmid-Width,Latmid+Width, Lonmid-Height, Lonmid+Height]
    return b
def plot_quakes(quakes):
    boundary = bbox(quakes)
    m = Basemap(llcrnrlon=boundary[2],llcrnrlat=boundary[0],
                urcrnrlon=boundary[3],urcrnrlat=boundary[1],
                resolution='l',area_thresh=1000.,projection='merc')
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral',lake_color='blue',zorder=0)
    m.drawmapboundary(fill_color='aqua')
    x, y = m(quakes.Lon, quakes.Lat)
    MagLab = 30*quakes.Magnitude
    Dep = quakes.Depth
    m.scatter(x, y, s=MagLab, c=Dep, marker="o")
    c = plt.colorbar(orientation='horizontal')
    c.set_label("Depth")
    
    plt.show()

plot_quakes(state)
