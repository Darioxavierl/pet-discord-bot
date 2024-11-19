# Usa una imagen base oficial de Python
FROM python:3.7.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo .env al contenedor
COPY .env /app/.env

# Comando para ejecutar el bot
CMD ["python", "main.py"]
