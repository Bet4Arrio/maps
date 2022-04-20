import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import interp2d


def get_extent(df, X, Y):
    return [df[X].min(),df[X].max(),df[Y].min(),df[Y].max()]

def heat_map(df, ax, X, Y, Z, extent=None):
    extent = extent if extent else get_extent(df, X, Y)
    if len(extent) < 4:
        raise("extente error")

    f = interp2d(df[X],df[Y],df[Z], kind='linear')
    x_coords = np.arange(extent[0],extent[1]+1)
    z_coords = np.arange(extent[2],extent[3]+1)
    c_i = f(x_coords,z_coords)
    fig = ax.imshow(c_i,
            extent= extent,
            origin="lower", interpolation='bicubic')
    fig.axes.set_autoscale_on(False)
    ax.scatter(df[X],df[Y])
    ax.colorbar()
    return fig

def map(sf, ax, att, restrition = []):
    fields = sf.fields[1:] 
    field_names = [field[0] for field in fields] 
    s = sf.shape(1)
    x = list([i[0] for i in s.shape.points[:]])
    y = list([i[1] for i in s.shape.points[:]])
    x_min, x_max= min(x), max(x) 
    y_min, y_max= min(y), max(y) 
    del x, y 
    plot_lines = []
    micro = []
    for shape in sf.shapeRecords():
        atr = dict(zip(field_names, shape.record)) 
        if not restrition or atr[att] in restrition:
            x = list(reversed([i[0] for i in shape.shape.points[:]]))
            y = list(reversed([i[1] for i in shape.shape.points[:]]))

            temp_x_min,temp_x_max = min(x), max(x) 
            temp_y_min,temp_y_max = min(y), max(y)

            x_min = temp_x_min if x_min > temp_x_min else x_min
            x_max = temp_x_max if x_max < temp_x_max else x_max
            y_min = temp_y_min if y_min > temp_y_min else y_min
            y_max = temp_y_max if y_max < temp_y_max else y_max

            map, = ax.plot(x,y, linestyle='solid', alpha=0.4, zorder=-1)
            plot_lines.append(map)
            micro.append(atr[att])
    
    legend1 = ax.legend(plot_lines, micro, loc=1)
    ax.add_artist(legend1)
    extent = [x_min,x_max,y_min,y_max]
    return extent, plot_lines, micro

def classifica(classes, **data):
    for cl in classes.keys():
        if eval(classes[cl]["criterio"]):
            return cl

def points(df, X, Y, ax, classes = None):
    """
    classes model:
        "Classe_name": "cor":"hexa", "criterio":"eval"
    """

    df["classe"] = df.apply(lambda x: classifica(classes, **x), axis=1)
    
    grouped = df.groupby('classe')
    for key, group in grouped:
        print(key)
        group.plot(ax=ax, kind='scatter', x=X, y=Y, label=key, color=classes[key]['cor'], s=50)
    return df