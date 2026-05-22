#  Clasificador de Residuos para Reciclaje
### Sistema Experto basado en reglas

---

##  Información del trabajo

| Campo | Detalle |
|---|---|
| **Materia** | Análisis de Datos II |
| **Trabajo** | Trabajo Práctico — Sistema Experto |
| **Universidad** | Universidad de la Ciudad de Buenos Aires |
| **Profesor** | Agustín Asuaje |
| **Cuatrimestre** | 1º Cuatrimestre 2026 |
| **Fecha de presentación** | 4 de junio de 2026 |

---

##  Grupo A

| Integrantes |
|---|
| Luciano Asís |
| Gustavo Barrajón |
| Fernando Galera |
| Gabriel García |
| Facundo Martinez |
| Andrea Moreno |

---

##  Objetivo

Construir un **Sistema Experto basado en reglas** capaz de clasificar residuos domésticos e indicar cómo descartarlos correctamente, contribuyendo a una gestión más responsable de los residuos en Argentina.

---

##  Descripción del sistema

El sistema recibe una descripción de un residuo (por texto o imagen) y devuelve:

- **Categoría** del residuo (reciclable, orgánico, especial, basura común)
- **Instrucciones** paso a paso para descartarlo correctamente
- **Errores comunes** a evitar con ese material
- **Impacto ambiental** si se recicla o descarta correctamente
- **Puntos Verdes más cercanos** según la ubicación del usuario (CABA)

---

##  Arquitectura

```
Entrada del usuario (texto o imagen)
            │
            ▼
    detectar_tipo()
    keywords.csv → ordenadas por longitud (más específicas primero)
            │
            ├── término ambiguo → pregunta al usuario
            │
            ▼
    Motor de inferencia (experta — KnowledgeEngine)
    Reglas generadas dinámicamente desde reglas.csv
    Forward Chaining
            │
            ▼
    Clasificacion(categoria, instrucciones, impacto...)
            │
            ▼
        Resultado
```

### Componentes

| Componente | Tecnología | Descripción |
|---|---|---|
| Motor de inferencia | `experta` | KnowledgeEngine con Forward Chaining |
| Reglas | `reglas.csv` | Una regla por tipo de residuo |
| Keywords | `keywords.csv` | Detección por palabras clave ordenadas por longitud |
| Ambigüedad | `ambiguos.csv` | Términos que requieren aclaración del usuario |
| Clasificación por imagen | Gemini 2.5 Flash | Identifica el material desde una foto |
| Puntos Verdes | `puntos-verdes.csv` Dataset GCBA | Centros de reciclaje más cercanos |
| Interfaz | Streamlit | UI web opcional |

---

##  Estructura del repositorio

```
📁 clasificador-residuos/
│
├── Clasificador_residuos.ipynb   ← Notebook principal (entregable)
├── app.py                        ← Interfaz Streamlit (opcional)
├── requirements.txt              ← Dependencias para Streamlit Cloud
├── README.md
│
└── 📁 data/
    ├── keywords.csv              ← Keywords por tipo de residuo
    ├── reglas.csv                ← Reglas de clasificación completas
    ├── ambiguos.csv              ← Términos con aclaración requerida
    └── puntos-verdes.csv         ← Centros de reciclaje
```

---

##  Base de conocimiento

| Categoría | Tipos de residuos cubiertos |
|---|---|
| ♻️ Reciclables | Plástico PET, Bolsas/Film, Vidrio, Papel, Cartón, Tetrabrik, Latas |
| 🌱 Orgánicos | Restos de comida, frutas, verduras, yerba, café |
| ⚠️ Especiales | Pilas/Baterías, Medicamentos, Aceite de cocina, Electrónicos (RAEE) |
| 🚫 Basura común | Papel higiénico, Pañales, Telgopor, Papel no reciclable |
| 🖥️ RAEE | Celulares, computadoras, electrodomésticos |
| ❓ Desconocido | Manejo por defecto con orientación general |

La base de conocimiento es **extensible sin modificar el código**: agregar un material nuevo implica solo agregar filas en los CSV.

---

##  Cómo usar

### Notebook (entregable principal)

1. Abrir `Clasificador_residuos_GrupoA.ipynb` en Google Colab
2. Ejecutar todas las celdas en orden
3. Subir los tres CSV a Google Drive y ajustar la ruta `DRIVE_PATH`
4. Usar la interfaz interactiva al final del notebook

### App Streamlit (local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

### App Streamlit (online)

[Ver la app desplegada](https://clasificador-residuos-grupo-a.streamlit.app/) 

---

##  API Key de Gemini (clasificación por imagen)

La clasificación por imagen usa **Google Gemini 2.5 Flash**, cuya API es gratuita:

1. Ir a [aistudio.google.com](https://aistudio.google.com)
2. Iniciar sesión con cuenta de Google
3. Click en **Get API Key** → **Create API Key**
4. Ingresarla en el panel lateral de la app Streamlit

---

##  Dependencias principales

| Librería | Uso |
|---|---|
| `experta==1.9.4` | Motor de inferencia (KnowledgeEngine) |
| `pandas` | Carga y procesamiento de CSV |
| `google-generativeai` | Clasificación por imagen con Gemini |
| `streamlit` | Interfaz web opcional |
| `matplotlib` | Visualización del árbol de decisión |

---

##  Datos abiertos utilizados

- **Puntos Verdes CABA**: [Portal de Datos Abiertos del Gobierno de la Ciudad de Buenos Aires](https://data.buenosaires.gob.ar/dataset/puntos-verdes)

---

> ⚠️ *Este sistema es orientativo y educativo. Para dudas específicas sobre el descarte de residuos, consultá en tu municipio o Punto Verde más cercano.*
