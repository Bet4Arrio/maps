import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
# import geopandas as gpd
a = "Micrbiologia e nematologica final.xlsx"
df = pd.read_excel(a, "completo")
df = df.replace(r'\n',' ', regex=True)
print(df.info(verbose=True))
df[["latitude","longitude"]] = df["Localização"].str.split(", ", n=1, expand=True)
df[["latitude", "longitude"]] = df[["latitude", "longitude"]].apply(pd.to_numeric)
col = df.columns
# raise("erro")

METODO = 1 # 0 ou 1
METODOS_NAME = ("Fator triplo", "Macrophomina", "Meloidogyne", "Pratylenchus raiz", "Helicotylenchus", "Cisto solo")
for num,metodo in enumerate(METODOS_NAME):
    fig, ax = plt.subplots()
    #FS, FO, R, M,"Meloidogyne", "Praty_raiz", "Helicotylenchus, Cisto_solo"
    classe_cor = {"Muito alto": "#fe0000", "Alto":"#ee7d31", "Moderado":"#fdd965", "Baixo":"#00ff00", "Zero":"#0030ee", "":"#fff"}
    classe_intervalo = {"Muito alto": [{"criterio":"(FS>3000 or FO>3000) and R>=50"},
                {"criterio":"M>80"},
                {"criterio": "False"},
                {"criterio": "Praty_raiz>1000"}, 
                {"criterio": "Helicotylenchus>500"}, 
                {"criterio": "Cisto_solo>20"}],
    "Alto":[{"criterio": "(FS>3000 or FO>3000) and R<=50"},
                {"criterio":"40<M<80"},
                {"criterio": "Meloidogyne>=10"},
                {"criterio": "1000>=Praty_raiz>500"}, 
                {"criterio": "500>=Helicotylenchus>200"}, 
                {"criterio": "20>=Cisto_solo>5"}], 
    "Moderado":[{"criterio": "(1500<FS<=3000 or 1500<FO<3000) and R<=50"},
                {"criterio": "20<M<40"},
                {"criterio": "False"},
                {"criterio": "500>=Praty_raiz>200"}, 
                {"criterio": "Helicotylenchus<=200"}, 
                {"criterio": "5>=Cisto_solo>=1"}], 
    "Baixo":[{"criterio":"(FS<1500 or FO<=1500) and R<=50"},
                {"criterio": "M<20"},
                {"criterio": "False"},
                {"criterio": "Praty_raiz>=200"}, 
                {"criterio": "False"}, 
                {"criterio": "False"}],
    "Zero":[{"criterio":"False"},
                {"criterio": "False"},
                {"criterio": "Meloidogyne<20"},
                {"criterio": "Praty_raiz>=200"}, 
                {"criterio": "Helicotylenchus<1"}, 
                {"criterio": "Cisto_solo<1"}]}

    def classifica(FO, FS, R, M, Meloidogyne, Praty_raiz, Helicotylenchus, Cisto_solo):
        for cl in classe_intervalo.keys():
            if eval(classe_intervalo[cl][num]["criterio"]):
                return cl
        print(metodo)
        print(FO, FS, R, M, Meloidogyne, Praty_raiz, Helicotylenchus, Cisto_solo)
        return ""

    df["classe"] = df.apply(lambda x: classifica(x["FO"], x["FS"], x["R"], x["M"], x[col[12]], x['Praty_raiz'], x['Helicotylenchus'], x['Cisto_solo']), axis=1)
    sf = shp.Reader("shapes/GO_Microrregioes_2021/GO_Microrregioes_2021.shp")
    fields = sf.fields[1:] 
    field_names = [field[0] for field in fields] 
    # plt.figure()
    plot_lines = []
    micro = []
    for shape in sf.shapeRecords():
        atr = dict(zip(field_names, shape.record)) 
        # if atr["UF"] == "52" or atr["UF"] == "Goiás":
        if True:
            x = list(reversed([i[0] for i in shape.shape.points[:]]))
            y = list(reversed([i[1] for i in shape.shape.points[:]]))
            map, = ax.plot(x,y, linestyle='solid', alpha=0.4, zorder=-1)
            plot_lines.append(map)
            micro.append(atr['NM_MICRO'])


    grouped = df.groupby('classe')
    for key, group in grouped:
        # print(key)
        # ax.scatter
        group.plot(ax=ax, kind='scatter', x='longitude', y='latitude', label=key, color=classe_cor[key], s=30)

    legend1 = ax.legend(plot_lines, micro, loc=1)

    ax.legend(loc="upper left")
    ax.axis('equal')
    ax.add_artist(legend1) 
    fig.set_size_inches(16, 10, forward=True)
    ax.set_title(metodo)
    fig.savefig(F'{metodo}.png', dpi=fig.dpi)
    # plt.show()