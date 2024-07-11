# Utiliza una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y del proyecto al contenedor
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que la aplicación usará
EXPOSE 8080

# Define la variable de entorno para la configuración de Flask
ENV FLASK_APP=main.py

# Comando para ejecutar la aplicación
CMD ["flask", "run"]