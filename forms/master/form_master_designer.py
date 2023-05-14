import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from db.BD import BaseDatos

class MasterPanelDesigner:
    def __init__(self, id_usuario):
        self.conexion()
        self.id_usuario = id_usuario
        self.ventana = tk.Tk()
        self.ventana.title('BookExtent')
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        logo = utl.leer_imagen("./imagenes/BE_sinfondo.png", (40, 40))

        # Panel superior 
        frame_top = tk.Frame(self.ventana, height=50, bd=0, relief=tk.SOLID, bg='gray')
        frame_top.pack(side="top", fill=tk.BOTH)

        frame_top_left = tk.Frame(frame_top, bd=0, relief=tk.SOLID, bg='gray')
        frame_top_left.pack(side="left", fill=tk.BOTH, expand=tk.NO)
        lLogo = tk.Label(frame_top_left, image=logo, bg='gray')
        lLogo.grid(row=0, column=0, sticky='w', padx=10)

        self.nombre = self.obtenerNombre(id_usuario=self.id_usuario)
        self.lUsuario = tk.Label(frame_top_left, text=self.nombre, font=('Times', 14), fg="black", bg="gray")
        self.lUsuario.grid(row=0, column=1, sticky='e')
 
        frame_top_left.grid_columnconfigure(0, minsize=50)
        frame_top_left.grid_columnconfigure(1,minsize=150)

        # Panel izquierdo menu
        frame_menu = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='black')
        frame_menu.pack(side="left", expand=tk.NO,fill=tk.BOTH)
        
        bLibros = tk.Button(frame_menu, text="Libros", font=('Times', 15, BOLD), fg="#fff", bd=0, bg="black", anchor="w", padx=20, command=self.verLibros)
        bLibros.grid(row=0, column=0, pady=10, sticky='nsew')
        bLibros.bind("<Return>", (lambda event: self.verLibros()))  # Si le das al enter tambien llama a la funcion

        bFavoritos = tk.Button(frame_menu, text="Favoritos", font=('Times', 15, BOLD), fg="#fff", bd=0, bg="black", anchor="w", padx=20, command=lambda: self.verFavoritos(id_usuario=self.id_usuario))
        bFavoritos.grid(row=1, column=0, pady=10, sticky='nsew')
        bFavoritos.bind("<Return>", (lambda event: self.verFavoritos(id_usuario=self.id_usuario)))  # Si le das al enter tambien llama a la funcion

        bSiguiendo = tk.Button(frame_menu, text="Siguiendo", font=('Times', 15, BOLD), fg="#fff", bd=0, bg="black", anchor="w", padx=20, command=lambda: self.verSiguiendo(id_usuario=self.id_usuario))
        bSiguiendo.grid(row=2, column=0, pady=10, sticky='nsew')
        bSiguiendo.bind("<Return>", (lambda event: self.verSiguiendo(id_usuario=self.id_usuario)))  # Si le das al enter tambien llama a la funcion

        bPendientes = tk.Button(frame_menu, text="Pendientes", font=('Times', 15, BOLD), fg="#fff", bd=0, bg="black", anchor="w", padx=20, command=lambda: self.verPendientes(id_usuario=self.id_usuario))
        bPendientes.grid(row=3, column=0, pady=10, sticky='nsew')
        bPendientes.bind("<Return>", (lambda event: self.verPendientes(id_usuario=self.id_usuario)))  # Si le das al enter tambien llama a la funcion

        bFinalizados = tk.Button(frame_menu, text="Finalizados", font=('Times', 15, BOLD), fg="#fff", bd=0, bg="black", anchor="w", padx=20, command=lambda: self.verLeido(id_usuario=self.id_usuario))
        bFinalizados.grid(row=4, column=0, pady=10, sticky='nsew')
        bFinalizados.bind("<Return>", (lambda event: self.verLeido(id_usuario=self.id_usuario)))  # Si le das al enter tambien llama a la funcion

        frame_menu.grid_columnconfigure(0, minsize=220)
        
        # Panel derecha
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES,fill=tk.BOTH)

        self.lista = ttk.Treeview(frame_form, columns=(1,2,3), show="headings", height="8")
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview.Heading", background="#7ed957", relief="flat", foreground="white")
        self.lista.heading(1, text="ID")
        self.lista.heading(2, text="Titulo")
        self.lista.heading(3, text="Autor")
        self.lista.column(2, anchor=CENTER)
        self.lista.pack(fill=tk.X, padx=20, pady=5)
        
        self.ventana.mainloop()
        self.desconexion()

    
    def verLibros(self):
        pass

    def verFavoritos(self, id_usuario):
        pass

    def verSiguiendo(self, id_usuario):
        pass

    def verPendientes(self, id_usuario):
        pass

    def verLeido(self, id_usuario):
        pass

    def obtenerNombre(self, id_usuario):
        pass

    def conexion(self):
        self.bd = BaseDatos(usuario="x6520114", password="x6520114", dsn="oracle0.ugr.es:1521/practbd.oracle0.ugr.es")
        BaseDatos.conexion(self=self.bd)

    def desconexion(self):
        BaseDatos.desconexion(self=self.bd)