import oracledb
import io
import numpy as np
import cv2

class BaseDatos:
    def __init__(self, usuario, password, dsn):
        self.usuario = usuario
        self.password = password
        self.dsn = dsn
        self.connection = None
        self.cursor = None
    
    def conexion(self):
        try:
            self.connection = oracledb.connect(user=self.usuario, password=self.password, dsn=self.dsn)
            self.cursor = self.connection.cursor()
            print("Se ha conectado a la Base de Datos")
        except Exception as e:
            print("Error al conectarse con la Base de Datos")
    
    def desconexion(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                self.connection.close()
            print("Se ha desconectado de la Base de Datos")
        except Exception as e:
            print("Error al desconectarse de la Base de Datos")

    def mostrar_tabla(self, tabla):
        self.cursor.execute("SELECT * FROM " + tabla)
        resultado = self.cursor.fetchall()

        for row in resultado:
            print(row)

    def obtenerUsuario(self, username):
        user = None
        self.cursor.execute("SELECT * FROM USUARIO WHERE NOMBRE_USUARIO='" + username +"'")
        user = self.cursor.fetchall()
        return user

    def insertarUsuario(self, username, password):
        self.cursor.execute("INSERT INTO USUARIO (NOMBRE_USUARIO, PASSWORD_USUARIO) VALUES ('"+username+"','"+password+"')")
        self.connection.commit()

    def obtenerUsername(self, id_usuario):
        query = "SELECT nombre_usuario FROM usuario WHERE id= :id"
        self.cursor.execute(query, {"id": id_usuario})
        username = self.cursor.fetchone()
        return username

    def existeLibro(self, id_libro):
        existe : bool = False
        libro = self.obtenerLibro(id_libro=id_libro)
        if(libro):
            existe = True
        return existe

    def obtenerLibro(self, id_libro):
        libro = None
        self.cursor.execute("SELECT * FROM LIBRO WHERE ID='" + id_libro +"'")
        libro = self.cursor.fetchall()
        return libro

    def obtenerDescripcion(self, id_libro):
        texto = ""
        self.cursor.execute("SELECT DBMS_LOB.SUBSTR(descripcion, 2000) FROM LIBRO WHERE id='" + id_libro +"'")
        texto = self.cursor.fetchall()
        return texto

    def cargarImagen(self, ruta, id_libro):
        with open(ruta, "rb") as f:
            imagen = f.read()

        ##self.cursor.execute("INSERT INTO tabla_imagen (id_img, imagen) VALUES (1, :blobImagen)", blobImagen=imagen)
        self.cursor.execute("UPDATE libro SET imagen=:blobImagen WHERE id=:id", blobImagen=imagen, id=id_libro)

        self.connection.commit()
    
    def descargarImagen(self, id_libro):
        query = "SELECT imagen FROM libro WHERE id= :id"
        
        self.cursor.execute(query, {"id": id_libro})
        
        #Resultados de la consulta
        result = self.cursor.fetchone()
        if result is not None and result[0] is not None:
            imagen = result[0].read()

            #Decodificamos la imagen
            imagen_np = np.frombuffer(imagen, dtype=np.uint8)
            img = cv2.imdecode(imagen_np, cv2.IMREAD_UNCHANGED)
        else:
            img = cv2.imread('./imagenes/BE_sinfondo.png')
        return img
        """
        cv2.imshow("Imagen", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
    
    def obtenerLibros(self):
        query = "SELECT libro.id, libro.titulo, libro.autor FROM libro"
        self.cursor.execute(query)
        libros = self.cursor.fetchall()
        return libros

    def obtenerLibrosFavoritos(self, id_usuario):
        query = "SELECT libro.id, libro.titulo, libro.autor FROM libro INNER JOIN biblioteca_usuario ON libro.ID = biblioteca_usuario.id_libro INNER JOIN seccion ON biblioteca_usuario.id_seccion = seccion.ID WHERE biblioteca_usuario.id_usuario = :id AND seccion.NOMBRE_SECCION = 'Favoritos' ORDER BY libro.id"
        self.cursor.execute(query, {"id": id_usuario})
        libros = self.cursor.fetchall()
        return libros
    
    def obtenerLibrosSiguiendo(self, id_usuario):
        query = "SELECT libro.id, libro.titulo, libro.autor FROM libro INNER JOIN biblioteca_usuario ON libro.ID = biblioteca_usuario.id_libro INNER JOIN seccion ON biblioteca_usuario.id_seccion = seccion.ID WHERE biblioteca_usuario.id_usuario = :id AND seccion.NOMBRE_SECCION = 'Siguiendo' ORDER BY libro.id"
        self.cursor.execute(query, {"id": id_usuario})
        libros = self.cursor.fetchall()
        return libros
    
    def obtenerLibrosLeido(self, id_usuario):
        query = "SELECT libro.id, libro.titulo, libro.autor FROM libro INNER JOIN biblioteca_usuario ON libro.ID = biblioteca_usuario.id_libro INNER JOIN seccion ON biblioteca_usuario.id_seccion = seccion.ID WHERE biblioteca_usuario.id_usuario = :id AND seccion.NOMBRE_SECCION = 'Leido' ORDER BY libro.id"
        self.cursor.execute(query, {"id": id_usuario})
        libros = self.cursor.fetchall()
        return libros
    
    def obtenerLibrosPendiente(self, id_usuario):
        query = "SELECT libro.id, libro.titulo, libro.autor FROM libro INNER JOIN biblioteca_usuario ON libro.ID = biblioteca_usuario.id_libro INNER JOIN seccion ON biblioteca_usuario.id_seccion = seccion.ID WHERE biblioteca_usuario.id_usuario = :id AND seccion.NOMBRE_SECCION = 'Pendiente' ORDER BY libro.id"
        self.cursor.execute(query, {"id": id_usuario})
        libros = self.cursor.fetchall()
        return libros




"""
BaseDatos = BaseDatos(usuario="x6520114", password="x6520114", dsn="oracle0.ugr.es:1521/practbd.oracle0.ugr.es")
BaseDatos.conexion()
#BaseDatos.insertarUsuario(username='paco', password='12345')

#libro = BaseDatos.obtenerLibro(id_libro='12')
#libros = BaseDatos.obtenerLibrosFavoritos(id_usuario='5')
libros = BaseDatos.obtenerLibros()
for i in libros:
    print(i)
#if(libro):
#   print(BaseDatos.obtenerDescripcion(id_libro='12')) 


#BaseDatos.cargarImagen(ruta="LaSangreDeLosElfos.jpeg", id_libro="3")
#BaseDatos.mostrar_tabla(tabla="libros")
#BaseDatos.descargarImagen(id_libro="1")

BaseDatos.desconexion()"""