import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing_extensions import Self
from modules.controller import Controller
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.classes  = []
        self.controller = Controller()
        self.master = master
        self.master.geometry("960x640+300+300")
        self.master.title("MAPS")
        self.pack()
        self.create_widgets()

    def ask_db(self):
        path  = filedialog.askopenfilename(filetypes=[("excel files","*.xlsx")])
        self.df_path["text"] =  path

        self.controller.open_xlsx(path)

    def ask_shape(self):
        path  = filedialog.askopenfilename(filetypes=[("shape files", "*.shp")])
        self.shp_path["text"] =  path
        self.controller.open_shp(path)
        
    def create_file_widgets(self):
        self.file_container = tk.Frame(self.master)
        self.file_container.pack()
        self.df_b = tk.Button(self.file_container, command=self.ask_db)
        self.df_b["text"] = "Importar Base de dados"
        self.df_b.grid(row=0) 
        self.df_path = tk.Label(self.file_container)
        self.df_path.grid(row=1) 

        self.shp_b = tk.Button(self.file_container, command=self.ask_shape)
        self.shp_b["text"] = "Importar Shapefile (fundo do mapa)"
        self.shp_b.grid(row=0, column=1) 
        self.shp_path = tk.Label(self.file_container)
        self.shp_path.grid(row=1, column=1) 
        

    def create_info_widgets(self):
          #https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html?=&t=acesso-ao-produto
        pass 
    
    def create_calor_wigets(self):
        self.pontos_cotainers = tk.Frame(self.map_container)
        self.pontos_cotainers.grid(row=0)
        self.calor = tk.IntVar()
        tk.Checkbutton(self.pontos_cotainers, text="Mapa de calor", variable=self.calor).grid(row=0) 

    def create_pontos_wigets(self):
        
        self.pontos_cotainers = tk.Frame(self.map_container)
        self.pontos_cotainers.grid(row=1)   
        self.Pontos = tk.IntVar()
        tk.Checkbutton(self.pontos_cotainers, text="Mapa de pontos", variable=self.Pontos).grid(row=0, column=0) 
        self.class_container = tk.Frame(self.pontos_cotainers)
        self.class_container.grid(row=0, column = 1)
        self.new_class = tk.Button(self.pontos_cotainers, command=self.new_class)
        self.new_class["text"] = "Nova classe"
        self.new_class.grid(row=1, column=0)


    def create_map_widgets(self):
        self.map_container = tk.Frame(self.master)
        self.map_container.pack()
        self.create_pontos_wigets()
        self.create_calor_wigets()

        start = tk.Button(self.map_container, command=self.gen_map)
        start["text"] = "Gerar"
        start.grid(row=2)

    def save_fig(self, fig, nome = "defualt"):
        fig.set_size_inches(16, 10, forward=True)
        fig.savefig(f'{nome}.png', dpi=fig.dpi)

    def gen_map(self):
        fig = self.controller.new_plot(self.calor.get(), self.Pontos.get())
        
        start = tk.Button(self.map_container, command= lambda : self.save_fig(fig))
        start["text"] = "salvar imagem"
        start.grid(row=2, column=2)
        self.canvas = FigureCanvasTkAgg(fig, master=self.map_container)
        self.canvas.get_tk_widget().grid(row=3)
        self.canvas.draw()

    def create_column_widgets(self):
        pass 
    

    def new_class(self):
        r = len(self.classes)
        nome = tk.Entry(self.class_container)
        nome.insert(tk.END, 'None')
        nome.grid(row=r, column=0)
        expressao =  tk.Entry(self.class_container)
        expressao.insert(tk.END, 'True')
        expressao.grid(row=r, column=1)
        cor =  tk.Entry(self.class_container)
        cor.insert(tk.END, '#FF00FF')
        cor.grid(row=r, column=2)

        self.classes.append((nome, expressao, cor))

    def create_widgets(self):
        self.create_file_widgets()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_info_widgets()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_column_widgets()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_map_widgets()
        
      

        self.quit = tk.Button(self, text="Sair", fg="red",
                            command=self.master.destroy)
        self.quit.pack(side="bottom")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()