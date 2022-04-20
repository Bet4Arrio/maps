import pandas as pd


df = pd.read_excel("COLETAS - AGRIVALLE 2.xlsx")
df = df.replace(r'\n',' ', regex=True)
df[["latitude","longitude"]] = df["Localização"].str.split(", ", n=1, expand=True)

print(df.head())

df.to_excel("data.xlsx")