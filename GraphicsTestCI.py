import os
import smtplib
from email.message import EmailMessage
import matplotlib

matplotlib.use('Agg')  # Evita la interfaz gráfica

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

# 1. Cargar datos
file_path = 'TopPeliculas.csv'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"No se encontró el archivo '{file_path}'")

df = pd.read_csv(file_path)
df_clean = df.dropna(subset=['título', 'rating', 'metascore', 'recaudación(M)']).copy()

# Lista para almacenar las rutas de las imágenes generadas temporalmente
archivos_adjuntos = []

# --- GRÁFICO 1 ---
fig1, ax1 = plt.subplots(figsize=(8, 6))
top_generos = df_clean['género'].value_counts().head(10).reset_index(name='cantidad')
sns.barplot(data=top_generos, x='cantidad', y='género', hue='género', ax=ax1, palette='viridis')
ax1.set_title('Top 10 Géneros más Frecuentes')
plt.tight_layout()
path1 = 'grafico_generos.png'
plt.savefig(path1, dpi=300)
plt.close(fig1)
archivos_adjuntos.append(path1)

# --- GRÁFICO 2 ---
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.histplot(df_clean['rating'], bins=15, kde=True, ax=ax2, color='skyblue')
ax2.set_title('Distribución de Ratings IMDb')
plt.tight_layout()
path2 = 'grafico_ratings.png'
plt.savefig(path2, dpi=300)
plt.close(fig2)
archivos_adjuntos.append(path2)


# --- FUNCIÓN PARA ENVIAR CORREO CON MÚLTIPLES ADJUNTOS ---
def enviar_correo(archivos):
    # Leer variables de entorno (credenciales seguras)
    email_emisor = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    email_receptor = os.environ.get('MAIL_TO', email_emisor)  # Si no se define destino, se manda a sí mismo

    msg = EmailMessage()
    msg['Subject'] = 'Reporte de Gráficos de Películas'
    msg['From'] = email_emisor
    msg['To'] = email_receptor
    msg.set_content('Hola, adjunto encontrarás los gráficos generados durante la ejecución de las pruebas CI.')

    # Adjuntar cada archivo guardado en la lista
    for ruta_archivo in archivos:
        with open(ruta_archivo, 'rb') as f:
            contenido_file = f.read()
            nombre_file = os.path.basename(ruta_archivo)
            msg.add_attachment(contenido_file, maintype='image', subtype='png', filename=nombre_file)

    # Conexión al servidor SMTP (Ejemplo: Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_emisor, password)
        smtp.send_message(msg)

    print("Correo enviado exitosamente con todos los gráficos adjuntos.")

    # Limpieza: Borrar los archivos temporales de la memoria del contenedor
    for ruta_archivo in archivos:
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)


# Ejecutar el envío al final
enviar_correo(archivos_adjuntos)