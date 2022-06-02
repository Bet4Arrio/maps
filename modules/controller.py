from ctypes import util
import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from . import utils
import pathlib
import unidecode



class Controller:
    def __init__(self):
        self.classes = dict()
        self.sf = shp.Reader("shapes\GO_Microrregioes_2021\GO_Microrregioes_2021.shp")
        
    def open_xlsx(self, file_path):
        self.file_path:str = file_path
        if pathlib.Path(self.file_path).suffix in ['.csv', '.txt']:
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = pd.read_excel(self.file_path)
        self.format_loc()
    
    def open_shp(self, file_path=None):
        del self.sf
        if file_path:
            self.sf = shp.Reader(file_path)
        else:
            self.sf = shp.Reader("shapes\GO_Microrregioes_2021\GO_Microrregioes_2021.shp")

    def format_loc(self):
        self.df[["latitude","longitude"]] = self.df["Localização"].str.split(", ", n=1, expand=True)
        self.df[["latitude", "longitude"]] = self.df[["latitude", "longitude"]].apply(pd.to_numeric)
    
    def get_columns(self):
        rcols = self.__normalize_columns_name()

        

    def __normalize_columns_name(self):
        rcols = {}
        for c in self.df.columns:
            unaccented_string = unidecode.unidecode(c)
            new_name = unaccented_string.replace(" ","_")
            rcols[c] = new_name
        self.df.rename(rcols)

        return rcols
        
    def set_class(self):
        pass

    def set_heatcolumn(self, heat):
        self.heat = heat
        pass

    def new_plot(self, heatmap = False,  points = False):
        fig, ax = plt.subplots()
        ax.legend(loc="upper left")
        ax.axis('equal')
        utils.map(self.sf, ax, att='NM_MICRO')
        if heatmap:
            utils.heat_map(self.df, ax=ax,X='longitude', Y='latitude', Z=self.heat)
        if points:
            utils.points(self.df, X='longitude', Y='latitude', ax=ax, classes=self.classes)

        
        plt.show()
        return  fig

        # fig.savefig(F'{}.png', dpi=fig.dpi)
        # ax.add_artist(legend1) 
        # fig.set_size_inches(16, 10, forward=True)
        # ax.set_title(metodo)
        # fig.savefig(F'{metodo}.png', dpi=fig.dpi)