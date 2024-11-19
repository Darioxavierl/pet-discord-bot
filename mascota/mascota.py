import random
import json
import os

class Mascota:
    def __init__(self):
        self.archivo_config = "config\config.json"

        try:
            self.load_config()
        except:
            self.archivo_datos = ""
            self.archivo_gifs = ""

        try:
            self.load_atributtes()
        except:
            self.nombre = ""
            self.hambre = 50
            self.sed = 50
            self.higiene = 50
            self.felicidad = 50

    def load_config(self):
        # Intenta cargar las configuraciones por defecto
        print("Recargando configuraciones...")
        try:
            if os.path.exists(self.archivo_config):
                with open(self.archivo_config, "r") as f:
                    config = json.load(f)
                    self.archivo_datos = config["rutas"]["mascota_datos"]
                    self.archivo_gifs = config["rutas"]["gifs_datos"]
                    self.nivel_critico = config["limites"]["nivel_critico"]
                    self.min_reduccion = config["limites"]["min_reduccion"]
                    self.max_reduccion = config["limites"]["max_reduccion"]
                    self.min_adicion = config["limites"]["min_adicion"]
                    self.max_adicion = config["limites"]["max_adicion"]
                    self.rol_alerta = config["roles"]["rol_alerta"]
                    self.pet_channel_id = config["channels"]["pet_id"]
        except Exception as e:
            print("Error al cargar configuracion...")

    def load_atributtes(self):    
        # Intentar cargar los datos desde el archivo
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, "r") as f:
                    datos = json.load(f)
                    self.nombre = datos["datos"]["nombre"]
                    self.hambre = datos["estadisticas"]["hambre"]
                    self.sed = datos["estadisticas"]["sed"]
                    self.higiene = datos["estadisticas"]["higiene"]
                    self.felicidad = datos["estadisticas"]["felicidad"]
            print(f"Datos cargados")
        except Exception as e:
            print(f"No se cargo los datos del json {e}")

    def get_random_gif(self, diccionario):
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_gifs, "r") as f:
                datos = json.load(f)
                try:
                    gifs = datos[diccionario]
                    gif = random.choice(list(gifs.keys()))
                    url = gifs[gif]
                except:
                    gifs = datos["error"]
                    gif = random.choice(list(gifs.keys()))
                    url = gifs[gif]
            return url

            
        
                
        

    def guardar_atributos(self):
        # Crear un diccionario de todos los atributos relevantes
        datos = {
            "datos": {
                "nombre": self.nombre
            },
            "estadisticas": {
                "hambre": self.hambre,
                "sed": self.sed,
                "higiene": self.higiene,
                "felicidad": self.felicidad
            }
        }

        # Guardar el diccionario en el archivo JSON
        with open(self.archivo_datos, "w") as f:
            json.dump(datos, f, indent=4)
        print("Datos actualizados...")

        
    def alimentar(self):
        if self.hambre < 100:
            disminucion = random.randint(self.min_adicion, self.max_adicion)
            self.hambre = min(self.hambre + disminucion, 100)
            self.guardar_atributos()
            
            url = self.get_random_gif("alimentar")
            return [url,f"```Alimento: {self.hambre}```"]
        else:
            url = self.get_random_gif("lleno")
            return [url, f"```{self.nombre} ya está lleno.\n```"]

    def dar_agua(self):
        if self.sed < 100:
            disminucion = random.randint(self.min_adicion, self.max_adicion)
            self.sed = min(self.sed + disminucion, 100)
            self.guardar_atributos()
            url = self.get_random_gif("beber")
            return [url,f"```Sed: {self.sed}```"]
        else:
            url = self.get_random_gif("lleno")
            return [url,f"```{self.nombre} ya no tiene sed.```"]

    def banar(self):
        if self.higiene < 100:
            self.higiene = 100
            self.guardar_atributos()
            url = self.get_random_gif("bano")
            return [url,f"```Higiene: {self.higiene}```"]
        else:

            url = self.get_random_gif("limpio")
            return [url,f"```{self.nombre} ya está limpio.```"]

    def jugar(self):
        if self.felicidad < 100:
            self.felicidad = min(self.felicidad + 10, 100)
            self.hambre = max(self.hambre - 5 , 0)  # Jugar disminuye un poco el hambre
            self.sed = max(self.hambre - 5 , 0)     # Jugar también disminuye un poco la sed
            self.higiene = max(self.higiene - 10, 0)
            self.guardar_atributos()
            url = self.get_random_gif("jugar")
            return [url,f"```Felicidad: {self.felicidad}```"]
        else:
            url = self.get_random_gif("divertido")
            return [url,f"```{self.nombre} ya está muy feliz.```"]