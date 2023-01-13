import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import shutil

messagebox.showinfo("", "Seleccione una carpeta de origen")
folder_selected_1 = filedialog.askdirectory()
if (not folder_selected_1 or folder_selected_1==""):
    messagebox.showerror("", "Es estrictamente necesaria la selección de un directorio de origen")
    exit()
dirInicio = f'{folder_selected_1}'
contenido = os.listdir(dirInicio)

messagebox.showinfo("", "Seleccione una carpeta de vertido")
folder_selected = filedialog.askdirectory()
if (not folder_selected or folder_selected==""):
    messagebox.showerror("", "Es estrictamente necesaria la selección de un directorio de vertido")
    exit()
dirFinal = f'{folder_selected}'

x = 0
for folder in contenido:
    if (not os.path.isfile(os.path.join(dirInicio, folder))):
        newPath = f"{dirInicio}/{folder}"
        newContenido = os.listdir(newPath)
        for file in newContenido:
            if os.path.isfile(os.path.join(newPath, file)):
                if os.path.exists(dirFinal+"/"+file):
                    messagebox.showerror("", "Elemento duplicado")
                new_name = os.path.join(dirFinal, file)
                shutil.move(newPath +"/"+ file, new_name)
                x += 1
messagebox.showinfo("", f"{x} elementos procesados")