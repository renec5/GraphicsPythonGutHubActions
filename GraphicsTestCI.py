import os
import matplotlib
# Configurar Matplotlib para ejecutarse sin interfaz gráfica (Headless)
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuración del estilo gráfico
sns.set_theme(style="whitegrid")

# 1. Carga y limpieza inicial de datos (usando ruta relativa)
file_path = 'TopPeliculas.csv'

if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"El archivo '{file_path}' no se encuentra en la raíz del proyecto."
    )

df = pd.read_csv(file_path)
df_clean = df.dropna(
    subset=['título', 'rating', 'metascore', 'recaudación(M)']
).copy()

# Crear una ventana con 4 paneles de gráficos
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gráfico 1: Top 10 géneros con más películas
top_generos = (
    df_clean['género'].value_counts().head(10).reset_index(name='cantidad')
)
sns.barplot(
    data=top_generos,
    x='cantidad',
    y='género',
    hue='género',
    ax=axes[0, 0],
    palette='viridis',
)
axes[0, 0].set_title('Top 10 Géneros más Frecuentes')
axes[0, 0].set_xlabel('Cantidad de Películas')

# Gráfico 2: Distribución de Ratings IMDb
sns.histplot(
    df_clean['rating'], bins=15, kde=True, ax=axes[0, 1], color='skyblue'
)
axes[0, 1].set_title('Distribución de Ratings IMDb')
axes[0, 1].set_xlabel('Rating IMDb')

# Gráfico 3: Correlación entre Metascore y Rating IMDb
sns.scatterplot(
    data=df_clean,
    x='metascore',
    y='rating',
    alpha=0.6,
    ax=axes[1, 0],
    color='purple',
)
axes[1, 0].set_title('Relación entre Metascore y Rating IMDb')
axes[1, 0].set_xlabel('Metascore')
axes[1, 0].set_ylabel('Rating IMDb')

# Gráfico 4: Top 10 directores por recaudación total acumulada
df_unique = df_clean.drop_duplicates(subset=['título'])
top_directores = (
    df_unique.groupby('director')['recaudación(M)']
    .sum()
    .nlargest(10)
    .reset_index()
)
sns.barplot(
    data=top_directores,
    x='recaudación(M)',
    y='director',
    hue='director',
    ax=axes[1, 1],
    palette='magma',
)
axes[1, 1].set_title('Top 10 Directores por Recaudación Total ($M)')
axes[1, 1].set_xlabel('Recaudación Total ($ Millones)')

# Crear el directorio .screenshots si no existe
os.makedirs('.screenshots', exist_ok=True)

# Ajustar distribución y guardar
plt.tight_layout()
output_path = '.screenshots/analisis_peliculas_sin_warnings.png'
plt.savefig(output_path, dpi=300)
plt.close(fig)

print(f"Gráfico guardado exitosamente en: {output_path}")