import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import shutil

class APP():
    def __init__(self):
        self.windows = {}
        self.fields = {}
        self.origin = ""
        self.final = ""
        self.startWindow("Inicio", 500, 150)
        self.newField(self.windows["Inicio"], "Directorio de origen", 10, 10)
        self.newField(self.windows["Inicio"], "Directorio de vertido", 10, 75)
        self.newButton(self.windows["Inicio"], "Mover", 12, 7, 400, 16)
        self.fields["Directorio de origen_Entry"].bind("<1>", self.selectOrigin)
        self.fields["Directorio de vertido_Entry"].bind("<1>", self.selectFinal)
        self.windows["Inicio"].mainloop()

    def startWindow(self, title, w, h, padx=100, pady=100):
        self.windows[title] = Tk()
        self.windows[title].resizable(0 , 0)
        self.windows[title].configure(bg="#fff")
        self.windows[title].geometry(f"{w}x{h}+{padx}+{pady}")
        self.windows[title].title(title)

    def newField(self, window, title, xplace=None, yplace=None):
        self.fields[f"{title}_Label"] = Label(window, text=title, font=('Arial', 12), bg="#fff", fg="#000")
        self.fields[f"{title}_Entry"] = Entry(window, text=title, font=('Arial', 12), bd=0, bg="#eee", fg="#000", borderwidth=4, relief=FLAT, width=40)
        self.fields[f"{title}_Label"].place(x=xplace, y=yplace)
        self.fields[f"{title}_Entry"].place(x=xplace, y=yplace+25)
        self.fields[f"{title}_Entry"].config(state= "disabled")

    def newButton(self, window, title, w, h, xplace=None, yplace=None):
        self.fields[f"{title}_Button"] = Button(window, text=title, command=self.move, bd=0, bg="#eee", fg="#000", height=h, width=w)
        self.fields[f"{title}_Button"].place(x=xplace, y=yplace)


    def selectOrigin(self, event=None):
        folder_selected_1 = filedialog.askdirectory()
        if (folder_selected_1 and folder_selected_1!=""):
            self.origin= f'{folder_selected_1}'
            self.fields["Directorio de origen_Entry"].configure(state="normal")
            self.fields["Directorio de origen_Entry"].delete(0, END)
            self.fields["Directorio de origen_Entry"].insert(0, self.origin)
            self.fields["Directorio de origen_Entry"].config(state= "disabled")
            self.contenido = os.listdir(self.origin)

    def selectFinal(self, event=None):
        folder_selected = filedialog.askdirectory()
        if (folder_selected and folder_selected!=""):
            self.final = f'{folder_selected}'
            self.fields["Directorio de vertido_Entry"].configure(state="normal")
            self.fields["Directorio de vertido_Entry"].delete(0, END)
            self.fields["Directorio de vertido_Entry"].insert(0, self.final)
            self.fields["Directorio de vertido_Entry"].config(state= "disabled")

    def move(self, event=None):
        if (self.origin == "" or self.final ==""):
            return messagebox.showerror("", "¡Cubre todos los campos antes de continuar!")
        if (not os.path.exists(self.origin)):
            return messagebox.showerror("", "No se puede encontrar el directorio de origen")
        if (not os.path.exists(self.final)):
            return messagebox.showerror("", "No se puede encontrar el directorio de vertido")
        x = 0
        self.startWindow("Moviendo", 250, 75, 125, 125)
        self.windows["Moviendo"].attributes("-topmost", True)
        number = Label(self.windows["Moviendo"], text="0 archivos movidos", font=('Arial', 12), bg="#fff", fg="#000")
        number.place(x=25, y=25)
        movidos:list[object] = []
        for folder in self.contenido:
            if (not os.path.isfile(os.path.join(self.origin, folder))):
                newPath = f"{self.origin}/{folder}"
                newContenido = os.listdir(newPath)
                for file in newContenido:
                    original_file_name = ".".join(file.split(".")[:-1])
                    new_file_name = ".".join(file.split(".")[:-1])
                    file_extension = file.split(".")[-1]
                    if os.path.isfile(os.path.join(newPath, original_file_name+"."+file_extension)):
                        if os.path.exists(self.final+"/"+new_file_name+"."+file_extension):
                            if (messagebox.askyesno("Elemento duplicado", f"Ya existe un archivo {new_file_name}.{file_extension} en la carpeta de vertido.\n¿Desea cambiarle el nombre?\nDe lo contrario este archivo no será trasladado.")):
                                i = 1
                                while True:
                                    temp_name= f"{new_file_name} ({i})"
                                    i+= 1
                                    if not os.path.exists(self.final+"/"+temp_name+"."+file_extension):
                                        new_file_name = temp_name
                                        break
                            else:
                                continue
                        new_name = os.path.join(self.final, new_file_name+"."+file_extension)
                        shutil.move(newPath +"/"+ file, new_name)
                        movidos.append({"origen": newPath+"/"+ file, "destino": self.final+"/"+new_file_name+"."+file_extension})
                        x += 1
                        number.config(text = f"{len(movidos)} archivos movidos")
        messagebox.showinfo("", "Los archivos han sido movidos satisfactoriamente")
        self.windows["Moviendo"].destroy()
APP()