"""
♻️ Clasificador de Residuos para Reciclaje
Sistema Experto — Análisis de Datos II
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import os
import base64
import re

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="♻️ Clasificador de Residuos",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fondo general */
.stApp {
    background-color: #0f1a0f;
    color: #e8f5e9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1a2e1a;
    border-right: 1px solid #2e4a2e;
}

/* Título principal */
.titulo-principal {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #69f0ae;
    letter-spacing: -1px;
    margin-bottom: 0;
    line-height: 1.1;
}
.subtitulo {
    font-size: 1rem;
    color: #81c784;
    margin-top: 4px;
    font-weight: 300;
}

/* Cards de resultado */
.card-resultado {
    background: linear-gradient(135deg, #1b2e1b 0%, #162816 100%);
    border: 1px solid #2e4a2e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.card-categoria {
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.card-sub {
    color: #81c784;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.card-contenedor {
    background: #0d1f0d;
    border-left: 3px solid #69f0ae;
    padding: 0.6rem 1rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}
.urgencia-alta {
    background: #3e1a1a;
    border: 1px solid #ef5350;
    color: #ef9a9a;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    display: inline-block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.urgencia-media {
    background: #3e2e1a;
    border: 1px solid #ffa726;
    color: #ffcc80;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    display: inline-block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.urgencia-baja {
    background: #1a2e1a;
    border: 1px solid #66bb6a;
    color: #a5d6a7;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    display: inline-block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.paso {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 0.5rem;
    align-items: flex-start;
    font-size: 0.9rem;
}
.paso-num {
    background: #69f0ae;
    color: #0f1a0f;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.75rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.error-item {
    color: #ef9a9a;
    font-size: 0.88rem;
    margin-bottom: 0.3rem;
}
.impacto-box {
    background: #0d2218;
    border: 1px solid #2e7d32;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #a5d6a7;
    font-size: 0.88rem;
    margin-top: 1rem;
    font-style: italic;
}
.seccion-titulo {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4caf50;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}
.punto-verde-card {
    background: #1b2e1b;
    border: 1px solid #2e4a2e;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.8rem;
}
.punto-verde-nombre {
    font-weight: 600;
    color: #69f0ae;
    font-size: 0.95rem;
}
.punto-verde-dir {
    color: #81c784;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}
.punto-verde-dist {
    color: #4caf50;
    font-size: 0.82rem;
    margin-top: 0.3rem;
    font-family: 'Space Mono', monospace;
}
.disclaimer {
    background: #1a1a0d;
    border: 1px solid #827717;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #fff176;
    font-size: 0.82rem;
    margin-top: 1.5rem;
}
/* Input */
.stTextInput input {
    background: #1b2e1b !important;
    border: 1px solid #2e4a2e !important;
    color: #e8f5e9 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus {
    border-color: #69f0ae !important;
    box-shadow: 0 0 0 2px rgba(105,240,174,0.15) !important;
}
/* Botones */
.stButton button {
    background: #69f0ae !important;
    color: #0f1a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: #40c4a0 !important;
    transform: translateY(-1px) !important;
}
/* File uploader */
.stFileUploader {
    background: #1b2e1b !important;
    border: 1px dashed #2e4a2e !important;
    border-radius: 8px !important;
}
/* Radio */
.stRadio label {
    color: #e8f5e9 !important;
}
/* Selectbox */
.stSelectbox div {
    background: #1b2e1b !important;
    border-color: #2e4a2e !important;
    color: #e8f5e9 !important;
}
/* Number input */
.stNumberInput input {
    background: #1b2e1b !important;
    border-color: #2e4a2e !important;
    color: #e8f5e9 !important;
}
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #1a2e1a;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #81c784 !important;
    border-radius: 6px !important;
}
.stTabs [aria-selected="true"] {
    background: #69f0ae !important;
    color: #0f1a0f !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

@st.cache_data
def cargar_sistema():
    """Carga los tres CSV y construye los diccionarios del sistema."""
    # Keywords
    df_kw = pd.read_csv(os.path.join(DATA_PATH, "keywords.csv"), encoding="utf-8")
    keywords_dict = {}
    for _, row in df_kw.iterrows():
        keywords_dict.setdefault(row["tipo"], []).append(str(row["keyword"]).strip())

    # Reglas
    df_reg = pd.read_csv(os.path.join(DATA_PATH, "reglas.csv"), encoding="utf-8")
    reglas_dict = {}
    for _, row in df_reg.iterrows():
        reglas_dict[row["tipo"]] = {
            "categoria"      : row["categoria"],
            "subcategoria"   : row["subcategoria"],
            "contenedor"     : row["contenedor"],
            "instrucciones"  : [i.strip() for i in str(row["instrucciones"]).split(";") if i.strip()],
            "errores_comunes": [e.strip() for e in str(row["errores_comunes"]).split(";") if e.strip()],
            "impacto"        : row["impacto"],
            "urgencia"       : row["urgencia"],
        }

    # Ambiguos
    df_amb = pd.read_csv(os.path.join(DATA_PATH, "ambiguos.csv"), encoding="utf-8")
    ambiguos_dict = {}
    for _, row in df_amb.iterrows():
        t = row["termino"]
        if t not in ambiguos_dict:
            ambiguos_dict[t] = {"pregunta": row["pregunta"], "opciones": {}}
        ambiguos_dict[t]["opciones"][str(row["opcion_num"])] = (
            row["tipo"], row["descripcion"]
        )

    return keywords_dict, reglas_dict, ambiguos_dict


@st.cache_data
def cargar_puntos_verdes():
    """Carga los Puntos Verdes desde el CSV local en data/puntos_verdes.csv."""
    ruta = os.path.join(DATA_PATH, "puntos_verdes.csv")
    try:
        df = pd.read_csv(ruta, encoding="utf-8")

        if "geometry" in df.columns:
            geom = df["geometry"].astype(str).str.extract(r"POINT\s*\(\s*([-0-9\.]+)\s+([-0-9\.]+)\s*\)")
            if geom.shape[1] == 2:
                df["long"] = geom[0].astype(float)
                df["lat"] = geom[1].astype(float)

        return df
    except Exception:
        # Fallback con datos de ejemplo
        return pd.DataFrame({
            "nombre": ["Punto Verde Palermo", "Punto Verde Recoleta", "Punto Verde Caballito", "Punto Verde Almagro", "Punto Verde San Telmo"],
            "direccion": ["Av. Santa Fe 3200", "Av. Las Heras 1900", "Av. Rivadavia 5000", "Av. Corrientes 3800", "Defensa 400"],
            "lat": [-34.5876, -34.5795, -34.6188, -34.6078, -34.6218],
            "long": [-58.4193, -58.3942, -58.4380, -58.4120, -58.3712],
        })


KEYWORDS_DICT, REGLAS_DICT, AMBIGUOS_DICT = cargar_sistema()
DF_PUNTOS_VERDES = cargar_puntos_verdes()


# ══════════════════════════════════════════════════════════════════════════════
# MOTOR DE DETECCIÓN
# ══════════════════════════════════════════════════════════════════════════════

def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    for src, dst in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),
                     ("à","a"),("è","e"),("ì","i"),("ò","o"),("ù","u"),
                     ("ñ","n"),("ä","a"),("ë","e"),("ï","i"),("ö","o"),("ü","u")]:
        texto = texto.replace(src, dst)
    return texto


def detectar_tipo(texto_usuario: str) -> str:
    texto = normalizar(texto_usuario)
    todas = []
    for tipo, kws in KEYWORDS_DICT.items():
        for kw in kws:
            todas.append((len(kw), tipo, kw))
    todas.sort(reverse=True)

    for _, tipo, kw in todas:
        if normalizar(kw) in texto:
            return tipo

    for termino in AMBIGUOS_DICT:
        if normalizar(termino) in texto:
            return f"ambiguo:{termino}"

    return "desconocido"


def obtener_regla(tipo: str) -> dict:
    return REGLAS_DICT.get(tipo, REGLAS_DICT.get("desconocido", {}))


# ══════════════════════════════════════════════════════════════════════════════
# PUNTOS VERDES
# ══════════════════════════════════════════════════════════════════════════════

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def puntos_cercanos(lat, lon, n=3):
    df = DF_PUNTOS_VERDES.copy()
    col_lat = next((c for c in df.columns if "lat" in c.lower()), None)
    col_lon = next((c for c in df.columns if "lon" in c.lower() or "lng" in c.lower() or "long" in c.lower()), None)
    col_nom = next((c for c in df.columns if "nombre" in c.lower() or "name" in c.lower()), df.columns[0])
    col_dir = next((c for c in df.columns if "direcc" in c.lower() or "address" in c.lower()), None)

    if not col_lat or not col_lon:
        return []

    df = df.dropna(subset=[col_lat, col_lon]).copy()
    df["dist"] = df.apply(lambda r: haversine(lat, lon, r[col_lat], r[col_lon]), axis=1)
    cerca = df.nsmallest(n, "dist")

    resultado = []
    for _, row in cerca.iterrows():
        resultado.append({
            "nombre"   : row[col_nom],
            "direccion": row[col_dir] if col_dir else "—",
            "dist_km"  : round(row["dist"], 2),
            "lat"      : row[col_lat],
            "lon"      : row[col_lon],
        })
    return resultado


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTES DE UI
# ══════════════════════════════════════════════════════════════════════════════

def color_urgencia(urgencia: str) -> str:
    u = urgencia.lower()
    if "alta" in u or "🔴" in u:
        return "urgencia-alta"
    if "media" in u:
        return "urgencia-media"
    return "urgencia-baja"


def mostrar_resultado(regla: dict, tipo: str):
    """Renderiza la card de resultado."""
    pasos = regla.get("instrucciones", [])
    errores = regla.get("errores_comunes", [])
    clase_urg = color_urgencia(regla.get("urgencia", ""))

    pasos_html = "".join(
        f'<div class="paso"><div class="paso-num">{i+1}</div><div>{p}</div></div>'
        for i, p in enumerate(pasos)
    )
    errores_html = "".join(f'<div class="error-item">{e}</div>' for e in errores)

    html = f"""
    <style>
    body {{
        margin: 0;
        padding: 0;
        background: transparent;
        color: #e8f5e9;
        font-family: 'DM Sans', sans-serif;
    }}
    .card-resultado {{
        background: linear-gradient(135deg, #1b2e1b 0%, #162816 100%);
        border: 1px solid #2e4a2e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        width: 100%;
    }}
    .card-categoria {{
        font-family: 'Space Mono', monospace;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }}
    .card-sub {{
        color: #81c784;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }}
    .card-contenedor {{
        background: #0d1f0d;
        border-left: 3px solid #69f0ae;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }}
    .urgencia-alta {{
        background: #3e1a1a;
        border: 1px solid #ef5350;
        color: #ef9a9a;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}
    .urgencia-media {{
        background: #3e2e1a;
        border: 1px solid #ffa726;
        color: #ffcc80;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}
    .urgencia-baja {{
        background: #1a2e1a;
        border: 1px solid #66bb6a;
        color: #a5d6a7;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}
    .paso {{
        display: flex;
        gap: 0.8rem;
        margin-bottom: 0.5rem;
        align-items: flex-start;
        font-size: 0.95rem;
    }}
    .paso-num {{
        background: #69f0ae;
        color: #0f1a0f;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.75rem;
        flex-shrink: 0;
        margin-top: 2px;
    }}
    .error-item {{
        color: #ef9a9a;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }}
    .impacto-box {{
        background: #0d2218;
        border: 1px solid #2e7d32;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #a5d6a7;
        font-size: 0.95rem;
        margin-top: 1rem;
        font-style: italic;
    }}
    .seccion-titulo {{
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #4caf50;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }}
    .disclaimer {{
        background: #1a1a0d;
        border: 1px solid #827717;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        color: #fff176;
        font-size: 0.88rem;
        margin-top: 1.5rem;
    }}
    </style>

    <div class="card-resultado">
        <div class="card-categoria">{regla.get('categoria', '—')}</div>
        <div class="card-sub">{regla.get('subcategoria', '—')} · tipo: <code>{tipo}</code></div>
        <div class="card-contenedor">🗑️ {regla.get('contenedor', '—')}</div>
        <span class="{ clase_urg }">⚡ Urgencia: {regla.get('urgencia', '—')}</span>

        <div class="seccion-titulo">📋 Instrucciones</div>
        {pasos_html}

        <div class="seccion-titulo">⚠️ Errores comunes</div>
        {errores_html}

        <div class="impacto-box">🌍 {regla.get('impacto', '—')}</div>
    </div>

    <div class="disclaimer">
    ⚠️ Este sistema es orientativo y educativo. Para dudas específicas consultá en tu municipio o Punto Verde más cercano.
    </div>
    """

    height = 240 + 40 * max(len(pasos), len(errores))
    components.html(html, height=min(height, 820), scrolling=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <div style="font-family:'Space Mono',monospace; font-size:1.1rem; color:#69f0ae; font-weight:700;">
            ♻️ Clasificador
        </div>
        <div style="font-size:0.8rem; color:#81c784; margin-top:4px;">
            Sistema Experto · Análisis de Datos II
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📊 Base de conocimiento**")
    st.metric("Tipos de residuos", len(REGLAS_DICT))
    st.metric("Keywords activas", sum(len(v) for v in KEYWORDS_DICT.values()))
    st.metric("Términos ambiguos", len(AMBIGUOS_DICT))

    st.markdown("---")
    st.markdown("**🔧 Configuración**")

    gemini_key = st.text_input(
        "API Key de Gemini",
        type="password",
        placeholder="Para clasificación por imagen",
        help="Obtené tu key gratis en aistudio.google.com"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:#4caf50; line-height:1.6;">
        <b>Motores:</b><br>
        • experta (KnowledgeEngine)<br>
        • Forward Chaining<br>
        • Gemini Vision (imágenes)<br><br>
        <b>Datos:</b><br>
        • keywords.csv<br>
        • reglas.csv<br>
        • ambiguos.csv<br>
        • puntos_verdes.csv (local)
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONTENIDO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="padding: 1.5rem 0 1rem 0;">
    <div class="titulo-principal">Clasificador de<br>Residuos ♻️</div>
    <div class="subtitulo">Sistema Experto basado en reglas · Análisis de Datos II</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Por texto", "📷 Por imagen", "📍 Puntos Verdes"])


# ── TAB 1: Clasificación por texto ────────────────────────────────────────────
with tab1:
    st.markdown("#### Describí el residuo que tenés")

    col1, col2 = st.columns([3, 1])
    with col1:
        texto_input = st.text_input(
            label="residuo",
            placeholder="ej: botella de plástico, pila gastada, cáscara de naranja...",
            label_visibility="collapsed"
        )
    with col2:
        clasificar_btn = st.button("Clasificar →", use_container_width=True)

    if clasificar_btn and texto_input.strip():
        tipo = detectar_tipo(texto_input)

        # Manejo de ambigüedad
        if tipo.startswith("ambiguo:"):
            termino = tipo.split(":")[1]
            info = AMBIGUOS_DICT[termino]

            st.warning(f"🤔 **\"{termino}\"** puede ser de distintos materiales.")
            st.markdown(f"**{info['pregunta']}**")

            opciones_labels = [desc for _, desc in info["opciones"].values()]
            opciones_tipos  = [t for t, _ in info["opciones"].values()]

            eleccion = st.radio(
                "Seleccioná una opción:",
                options=range(len(opciones_labels)),
                format_func=lambda i: opciones_labels[i],
                label_visibility="collapsed"
            )

            if st.button("Confirmar →"):
                tipo = opciones_tipos[eleccion]
                regla = obtener_regla(tipo)
                mostrar_resultado(regla, tipo)

        else:
            regla = obtener_regla(tipo)
            mostrar_resultado(regla, tipo)

    elif clasificar_btn:
        st.info("Escribí qué residuo tenés para clasificarlo.")

    # Ejemplos rápidos
    st.markdown("---")
    st.markdown("**⚡ Ejemplos rápidos**")
    ejemplos = [
        "botella de gaseosa", "pila gastada", "aceite de cocina usado",
        "caja de pizza", "árbol de navidad de plástico", "cáscara de naranja",
        "celular roto", "espejo roto", "papel higiénico"
    ]
    cols = st.columns(3)
    for i, ej in enumerate(ejemplos):
        if cols[i % 3].button(ej, key=f"ej_{i}", use_container_width=True):
            tipo = detectar_tipo(ej)
            if not tipo.startswith("ambiguo:"):
                regla = obtener_regla(tipo)
                st.markdown(f"**Consulta:** *{ej}*")
                mostrar_resultado(regla, tipo)


# ── TAB 2: Clasificación por imagen ──────────────────────────────────────────
with tab2:
    st.markdown("#### Subí una foto del residuo")
    st.markdown("La IA identifica el material y el sistema experto lo clasifica.")

    if not gemini_key:
        st.warning("⚠️ Ingresá tu API Key de Gemini en el panel izquierdo para usar esta función. Podés obtenerla gratis en [aistudio.google.com](https://aistudio.google.com).")
    else:
        imagen = st.file_uploader(
            "Subir imagen",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )

        if imagen:
            col_img, col_res = st.columns([1, 1])
            with col_img:
                st.image(imagen, caption="Imagen subida", use_container_width=True)

            with col_res:
                with st.spinner("🤖 Analizando con Gemini..."):
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=gemini_key)
                        modelo = genai.GenerativeModel("gemini-2.5-flash")

                        image_bytes = imagen.read()
                        ext = imagen.name.split(".")[-1].lower()
                        mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
                                "png":"image/png","webp":"image/webp"}.get(ext,"image/jpeg")

                        prompt = (
                            "Sos un asistente de clasificación de residuos para reciclaje en Argentina. "
                            "Analizá esta imagen y describí en UNA oración corta qué tipo de residuo es. "
                            "Sé específico con el material y el objeto. "
                            "Respondé SOLO con la descripción, sin explicaciones adicionales."
                        )

                        respuesta = modelo.generate_content([
                            prompt,
                            {"mime_type": mime, "data": image_bytes}
                        ])

                        descripcion = respuesta.text.strip()
                        st.success(f"🤖 Gemini identificó: **{descripcion}**")

                        tipo = detectar_tipo(descripcion)
                        if tipo.startswith("ambiguo:"):
                            st.info(f"Material ambiguo detectado: **{descripcion}**. Usá la pestaña de texto para aclarar.")
                        else:
                            regla = obtener_regla(tipo)
                            mostrar_resultado(regla, tipo)

                    except ImportError:
                        st.error("Instalá google-generativeai: `pip install google-generativeai`")
                    except Exception as e:
                        st.error(f"Error al consultar Gemini: {e}")


# ── TAB 3: Puntos Verdes ──────────────────────────────────────────────────────
with tab3:
    st.markdown("#### Puntos Verdes más cercanos")
    st.markdown("Ingresá tu ubicación para encontrar los centros de reciclaje más cercanos.")

    col_lat, col_lon, col_n = st.columns([2, 2, 1])

    # Valores por defecto: Plaza de Mayo, CABA
    with col_lat:
        lat = st.number_input("Latitud", value=-34.6083, format="%.4f", step=0.0001)
    with col_lon:
        lon = st.number_input("Longitud", value=-58.3712, format="%.4f", step=0.0001)
    with col_n:
        n_puntos = st.number_input("Cantidad", min_value=1, max_value=10, value=3)

    st.caption("💡 Podés obtener tus coordenadas haciendo clic derecho en Google Maps → \"¿Qué hay aquí?\"")

    if st.button("🔍 Buscar Puntos Verdes", use_container_width=True):
        with st.spinner("Buscando..."):
            puntos = puntos_cercanos(lat, lon, n=n_puntos)

        if puntos:
            st.markdown(f"**{len(puntos)} Puntos Verdes más cercanos:**")

            for p in puntos:
                st.markdown(f"""
                <div class="punto-verde-card">
                    <div class="punto-verde-nombre">📌 {p['nombre']}</div>
                    <div class="punto-verde-dir">📍 {p['direccion']}</div>
                    <div class="punto-verde-dist">🚶 {p['dist_km']} km de distancia</div>
                </div>
                """, unsafe_allow_html=True)

            # Mapa con los puntos
            mapa_data = pd.DataFrame({
                "lat": [p["lat"] for p in puntos] + [lat],
                "lon": [p["lon"] for p in puntos] + [lon],
            })
            st.map(mapa_data, zoom=13)

        else:
            st.error("No se pudieron obtener los Puntos Verdes. Verificá tu conexión.")

    st.markdown("---")
    st.caption("Datos: cargados desde el archivo local data/puntos_verdes.csv")
