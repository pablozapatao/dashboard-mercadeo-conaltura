"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CONALTURA - ENTERPRISE DASHBOARD SYSTEM                   ║
║                    Gran Convención de Ventas 2025                            ║
║                    Versión: UI/UX High-Fidelity (Maximalist)                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# 1. SISTEMA DE CONFIGURACIÓN Y BRANDING
# ══════════════════════════════════════════════════════════════════════════════

# Configuración de la página (Debe ser la primera instrucción)
st.set_page_config(
    page_title="Conaltura | Intelligence Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------------------------
# PALETA DE COLORES CORPORATIVA (HARDCODED PARA CONSISTENCIA)
# ------------------------------------------------------------------------------
# Definimos los colores como constantes globales para usarlos en todo el código
COLORS = {
    'primary': '#125160',      # Verde Petróleo (Identidad Core)
    'primary_light': '#1A6B7F',# Variante clara para hovers
    'accent': '#FF795A',       # Naranja Coral (Call to Actions / Alertas)
    'highlight': '#DBFF69',    # Verde Lima (KPIs Positivos / Digital)
    'secondary': '#B382FF',    # Lila (Categorías secundarias)
    'neutral_bg': '#F8FAFC',   # Fondo General (Gris Humo)
    'card_bg': '#FFFFFF',      # Fondo Tarjetas
    'text_main': '#0F172A',    # Texto Principal (Casi negro)
    'text_muted': '#64748B',   # Texto Secundario (Gris)
    'border': '#E2E8F0',       # Bordes sutiles
    'success': '#10B981',      # Verde genérico éxito
    'warning': '#F59E0B',      # Amarillo alerta
    'danger': '#EF4444'        # Rojo peligro
}

# Mapas de colores específicos para consistencia en gráficos
GAMA_COLOR_MAP = {
    'VIS/Acceso': '#E8FFB0',
    'Media': '#DBFF69',
    'Alta': '#B382FF',
    'Premium': '#FF795A',
    'Sin Definir': '#94A3B8'
}

CANAL_COLOR_MAP = {
    'DIGITAL': '#DBFF69',          # Foco en innovación
    'RELACIONAMIENTO': '#125160',  # Foco corporativo
    'EXPERIENCIA': '#B382FF',
    'EVENTOS': '#FF795A',
    'TRADICIONAL': '#A8D861',
    'OTROS': '#CBD5E1'
}

# ------------------------------------------------------------------------------
# INYECCIÓN DE CSS AVANZADO (THE "ANTIGRAVITY" ENGINE)
# ------------------------------------------------------------------------------
# Aquí es donde ocurre la magia visual. Reescribimos el CSS de Streamlit.
st.markdown(f"""
<style>
    /* Importar Tipografía Premium */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Reset Global */
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
        color: {COLORS['text_main']};
    }}
    
    /* Fondo de la Aplicación */
    .stApp {{
        background-color: {COLORS['neutral_bg']};
        background-image: radial-gradient({COLORS['border']} 1px, transparent 1px);
        background-size: 20px 20px;
    }}
    
    /* Contenedor Principal Ajustado */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
        max_width: 1600px;
    }}
    
    /* ---------------------------------------------------------------------- */
    /* COMPONENTE: TARJETAS KPI (METRIC CARDS)                                */
    /* ---------------------------------------------------------------------- */
    .kpi-card {{
        background-color: {COLORS['card_bg']};
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid {COLORS['border']};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: {COLORS['primary']};
    }}
    
    /* Decoración lateral en las tarjetas */
    .kpi-accent {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 6px;
        background: linear-gradient(180deg, {COLORS['primary']}, {COLORS['highlight']});
    }}
    
    .kpi-title {{
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {COLORS['text_muted']};
        margin-bottom: 8px;
    }}
    
    .kpi-value {{
        font-size: 2.25rem;
        font-weight: 700;
        color: {COLORS['primary']};
        line-height: 1.1;
        margin-bottom: 8px;
    }}
    
    .kpi-meta {{
        font-size: 0.85rem;
        color: {COLORS['text_muted']};
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    .kpi-badge {{
        background-color: rgba(219, 255, 105, 0.3);
        color: #4D6600;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.75rem;
    }}

    /* ---------------------------------------------------------------------- */
    /* COMPONENTE: CONTENEDORES DE GRÁFICOS                                   */
    /* ---------------------------------------------------------------------- */
    .chart-container {{
        background-color: {COLORS['card_bg']};
        border-radius: 16px;
        padding: 20px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }}
    
    .section-header {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .section-header::before {{
        content: '';
        display: block;
        width: 6px;
        height: 24px;
        background-color: {COLORS['accent']};
        border-radius: 3px;
    }}

    /* ---------------------------------------------------------------------- */
    /* AJUSTES DE INTERFAZ DE STREAMLIT                                       */
    /* ---------------------------------------------------------------------- */
    
    /* Headers H1, H2, H3 */
    h1 {{ color: {COLORS['primary']}; font-weight: 800; letter-spacing: -1px; }}
    h2 {{ color: {COLORS['text_main']}; font-weight: 700; }}
    h3 {{ color: {COLORS['text_main']}; font-weight: 600; }}
    
    /* Botones */
    .stButton button {{
        background-color: {COLORS['primary']};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }}
    .stButton button:hover {{
        background-color: {COLORS['primary_light']};
        transform: scale(1.02);
    }}
    
    /* Tablas (Dataframes) */
    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {COLORS['border']};
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {COLORS['card_bg']};
        border-radius: 8px;
        font-weight: 600;
    }}
    
    /* Ocultar menú hamburguesa y footer para look "App Nativa" */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2. MOTOR DE PROCESAMIENTO DE DATOS (ETL)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_and_process_data(file_buffer):
    """
    Función robusta para cargar datos. Maneja CSV y Excel.
    Normaliza nombres de columnas para evitar errores de tipeo.
    """
    try:
        # Detectar tipo de archivo
        if file_buffer.name.endswith('.csv'):
            # Intentar leer CSV con diferentes encodings y separadores
            try:
                df = pd.read_csv(file_buffer, encoding='utf-8', sep=None, engine='python')
            except:
                file_buffer.seek(0)
                df = pd.read_csv(file_buffer, encoding='latin-1', sep=';')
        else:
            df = pd.read_excel(file_buffer)

        # Diccionario de normalización de columnas (Mapping)
        # Esto asegura que si el Excel dice "Venta Neta" o "Valor Neto", el código funcione.
        column_mapping = {}
        for col in df.columns:
            clean_col = col.lower().strip().replace(' ', '').replace('_', '')
            
            if 'proyecto' in clean_col: column_mapping[col] = 'MacroProyecto'
            elif 'medio' in clean_col: column_mapping[col] = 'MedioPublicitario'
            elif 'agrupacion' in clean_col or 'agrupación' in clean_col: column_mapping[col] = 'MacroCanal'
            elif 'valor' in clean_col and ('neto' in clean_col or 'venta' in clean_col): column_mapping[col] = 'ValorNeto'
            elif 'ciudad' in clean_col: column_mapping[col] = 'Ciudad'
            elif 'gama' in clean_col: column_mapping[col] = 'Gama'
            elif 'fecha' in clean_col: column_mapping[col] = 'Fecha'

        # Renombrar columnas
        df = df.rename(columns=column_mapping)
        
        # Limpieza de tipos de datos
        if 'ValorNeto' in df.columns:
            # Eliminar caracteres no numéricos si vienen como string
            if df['ValorNeto'].dtype == object:
                df['ValorNeto'] = df['ValorNeto'].astype(str).str.replace(r'[$,.]', '', regex=True)
            df['ValorNeto'] = pd.to_numeric(df['ValorNeto'], errors='coerce').fillna(0)
            
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.strftime('%Y-%m') # Formato Año-Mes para ordenamiento
            df['MesNombre'] = df['Fecha'].dt.strftime('%B') # Nombre del mes

        # Rellenar nulos en categóricas
        categoricals = ['MacroProyecto', 'MedioPublicitario', 'Ciudad', 'MacroCanal', 'Gama']
        for cat in categoricals:
            if cat in df.columns:
                df[cat] = df[cat].fillna('Sin Asignar').astype(str)

        return df

    except Exception as e:
        return None

# Funciones de Formato Visual
def format_currency_cop(value):
    """Formatea números grandes a formato legible COP (K, M, B)"""
    if value == 0: return "$0"
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    elif value >= 1e3:
        return f"${value/1e3:.0f}K"
    else:
        return f"${value:,.0f}"

# ══════════════════════════════════════════════════════════════════════════════
# 3. INTERFAZ: HEADER Y SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

# --- SIDEBAR (Panel de Control) ---
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 10px; background: {COLORS['primary']}; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0; text-align: center; font-size: 1.2rem;">PANEL DE CONTROL</h2>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📂 Cargar Sábana de Datos", type=['xlsx', 'csv'])
    
    st.markdown("---")
    st.info("ℹ️ **Nota:** El sistema espera columnas como 'MacroProyecto', 'Medio', 'Valor Neto', 'Ciudad'.")

# --- HEADER PRINCIPAL ---
col_logo, col_text, col_date = st.columns([1, 4, 2])

with col_logo:
    # Intentamos cargar el logo, si falla mostramos un icono elegante
    if Path('logo.png').exists():
        st.image('logo.png', width=120)
    else:
        st.markdown(f"""
        <div style="background: {COLORS['primary']}; width: 80px; height: 80px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 40px;">🏢</span>
        </div>
        """, unsafe_allow_html=True)

with col_text:
    st.markdown(f"""
    <div>
        <h1 style="margin-bottom: 0px; font-size: 2.5rem;">CONALTURA <span style="font-weight: 300; color: {COLORS['text_muted']};">| INTELLIGENCE</span></h1>
        <p style="font-size: 1.1rem; color: {COLORS['primary']}; font-weight: 500;">
            Gran Convención de Ventas 2025 &bull; Análisis Estratégico de Mercadeo
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_date:
    today = datetime.now().strftime("%d %B, %Y")
    st.markdown(f"""
    <div style="text-align: right; padding-top: 10px;">
        <div style="font-size: 0.9rem; color: {COLORS['text_muted']}; font-weight: 600;">FECHA REPORTE</div>
        <div style="font-size: 1.5rem; color: {COLORS['text_main']}; font-weight: 700;">{today}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# 4. LÓGICA DE CONTROL DE FLUJO (CHECKEO DE DATOS)
# ══════════════════════════════════════════════════════════════════════════════

if uploaded_file is None:
    # Pantalla de "Empty State" Bonita
    st.markdown(f"""
    <div style="text-align: center; padding: 4rem; background: white; border-radius: 20px; border: 2px dashed {COLORS['border']}; margin: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📂</div>
        <h3 style="color: {COLORS['primary']};">Esperando Datos</h3>
        <p style="color: {COLORS['text_muted']}; max-width: 600px; margin: 0 auto;">
            Para visualizar el dashboard ejecutivo, por favor cargue el archivo Excel o CSV 
            en el panel lateral izquierdo. El sistema procesará automáticamente la información.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop() # Detener ejecución aquí si no hay archivo

# Cargar datos
df = load_and_process_data(uploaded_file)

if df is None:
    st.error("❌ Error Crítico: No se pudo procesar el archivo. Verifique que no esté corrupto.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# 5. FILTROS GLOBALES (INTERACTIVOS)
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-header'>🔎 Filtros de Segmentación</div>", unsafe_allow_html=True)

with st.container():
    # Usamos un contenedor con estilo de tarjeta para los filtros
    st.markdown(f"<div style='background: white; padding: 20px; border-radius: 12px; border: 1px solid {COLORS['border']}; box-shadow: 0 2px 4px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    # Lógica segura para extraer opciones únicas
    opts_ciudad = ['Todas'] + sorted(list(df['Ciudad'].unique())) if 'Ciudad' in df.columns else []
    opts_proyecto = ['Todos'] + sorted(list(df['MacroProyecto'].unique())) if 'MacroProyecto' in df.columns else []
    opts_canal = ['Todos'] + sorted(list(df['MacroCanal'].unique())) if 'MacroCanal' in df.columns else []
    
    with f_col1:
        sel_ciudad = st.selectbox("📍 Ciudad", opts_ciudad)
    with f_col2:
        sel_proyecto = st.selectbox("🏗️ MacroProyecto", opts_proyecto)
    with f_col3:
        sel_canal = st.selectbox("📢 Canal / Agrupación", opts_canal)
    with f_col4:
        # Filtro de fecha simplificado (Año completo si no hay filtro)
        st.markdown(f"<div style='font-size: 0.85rem; color: {COLORS['text_muted']}; margin-bottom: 5px;'>📅 Período</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-weight: 600; color: {COLORS['primary']};'>Año Fiscal 2025</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# APLICACIÓN DE FILTROS AL DATAFRAME
df_filtered = df.copy()
if sel_ciudad != 'Todas':
    df_filtered = df_filtered[df_filtered['Ciudad'] == sel_ciudad]
if sel_proyecto != 'Todos':
    df_filtered = df_filtered[df_filtered['MacroProyecto'] == sel_proyecto]
if sel_canal != 'Todos':
    df_filtered = df_filtered[df_filtered['MacroCanal'] == sel_canal]

# Check si nos quedamos sin datos tras filtrar
if df_filtered.empty:
    st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6. SECCIÓN 1: HIGH-LEVEL KPIs (TARJETAS PERSONALIZADAS)
# ══════════════════════════════════════════════════════════════════════════════

# Cálculos de Negocio
kpi_ventas = df_filtered['ValorNeto'].sum()
kpi_unidades = len(df_filtered) # Asumiendo 1 fila = 1 unidad vendida
kpi_ticket = kpi_ventas / kpi_unidades if kpi_unidades > 0 else 0
# Ciudad Top
top_city_name = df_filtered.groupby('Ciudad')['ValorNeto'].sum().idxmax()
top_city_val = df_filtered.groupby('Ciudad')['ValorNeto'].sum().max()
top_city_share = (top_city_val / kpi_ventas * 100) if kpi_ventas > 0 else 0

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

# Función helper para renderizar HTML de tarjeta
def render_kpi_html(title, value, badge_text, icon):
    return f"""
    <div class="kpi-card">
        <div class="kpi-accent"></div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-meta">
            <span>{icon}</span>
            <span class="kpi-badge">{badge_text}</span>
        </div>
    </div>
    """

with col_kpi1:
    st.markdown(render_kpi_html(
        "Ingresos Totales (Neto)", 
        format_currency_cop(kpi_ventas), 
        "Obj: 100%", 
        "💰"
    ), unsafe_allow_html=True)

with col_kpi2:
    st.markdown(render_kpi_html(
        "Unidades Vendidas", 
        f"{kpi_unidades:,.0f}", 
        "Transacciones", 
        "🔑"
    ), unsafe_allow_html=True)

with col_kpi3:
    st.markdown(render_kpi_html(
        "Ticket Promedio", 
        format_currency_cop(kpi_ticket), 
        "Por Unidad", 
        "📈"
    ), unsafe_allow_html=True)

with col_kpi4:
    st.markdown(render_kpi_html(
        f"Líder: {top_city_name}", 
        f"{top_city_share:.1f}%", 
        "Del Total", 
        "🏆"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7. SECCIÓN 2: ALINEACIÓN MERCADEO-VENTAS (SANKEY DIAGRAM)
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-header'>🕸️ Flujo de Atribución: Mercadeo ➔ Ventas</div>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
    
    if 'MacroCanal' in df_filtered.columns and 'MedioPublicitario' in df_filtered.columns:
        # Preparación de datos compleja para Sankey
        # Nivel 1: MacroCanal -> MedioPublicitario
        df_l1 = df_filtered.groupby(['MacroCanal', 'MedioPublicitario'])['ValorNeto'].sum().reset_index()
        df_l1.columns = ['Source', 'Target', 'Value']
        
        # Nivel 2: MedioPublicitario -> MacroProyecto (Top 10 para no saturar)
        top_projects = df_filtered.groupby('MacroProyecto')['ValorNeto'].sum().nlargest(10).index
        df_l2 = df_filtered[df_filtered['MacroProyecto'].isin(top_projects)].groupby(['MedioPublicitario', 'MacroProyecto'])['ValorNeto'].sum().reset_index()
        df_l2.columns = ['Source', 'Target', 'Value']
        
        # Concatenar flujos
        links = pd.concat([df_l1, df_l2], axis=0)
        
        # Mapeo de nodos a índices
        all_nodes = list(pd.unique(links[['Source', 'Target']].values.ravel('K')))
        mapping = {k: v for v, k in enumerate(all_nodes)}
        
        links['Source'] = links['Source'].map(mapping)
        links['Target'] = links['Target'].map(mapping)
        
        # Colores personalizados para los nodos
        node_colors = []
        for node in all_nodes:
            if node in CANAL_COLOR_MAP:
                node_colors.append(CANAL_COLOR_MAP[node])
            else:
                node_colors.append(COLORS['primary']) # Default
        
        # Crear Figura Sankey
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=COLORS['primary'], # Forzar color primario o usar node_colors
                hovertemplate='Nodo: %{label}<br>Valor: $%{value:,.0f}<extra></extra>'
            ),
            link=dict(
                source=links['Source'],
                target=links['Target'],
                value=links['Value'],
                color='rgba(18, 81, 96, 0.2)' # Enlaces Teal transparentes
            )
        )])
        
        fig_sankey.update_layout(
            title_text="<b>Mapa de Conversión de Inversión</b><br><span style='font-size:12px; color:grey'>Flujo desde Agrupación hasta Proyecto final</span>",
            font=dict(size=12, family="Poppins"),
            height=600,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.info("No hay suficientes columnas categóricas para generar el diagrama de flujo.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 8. SECCIÓN 3: ANÁLISIS DETALLADO (GRÁFICOS COMPUESTOS)
# ══════════════════════════════════════════════════════════════════════════════

col_c1, col_c2 = st.columns([1, 1])

with col_c1:
    st.markdown("<div class='section-header'>📊 Top Ciudades (Volumen)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
    
    if 'Ciudad' in df_filtered.columns:
        df_city = df_filtered.groupby('Ciudad')['ValorNeto'].sum().reset_index().sort_values('ValorNeto', ascending=True)
        
        # Asignar colores según la ciudad definida en constantes
        city_colors = [CIUDAD_COLORS.get(c, COLORS['primary']) for c in df_city['Ciudad']]
        
        fig_bar = go.Figure(go.Bar(
            x=df_city['ValorNeto'],
            y=df_city['Ciudad'],
            orientation='h',
            text=df_city['ValorNeto'].apply(format_currency_cop),
            textposition='auto',
            marker_color=city_colors,
            marker_line_width=0,
            opacity=0.9
        ))
        
        fig_bar.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=12, weight='bold')),
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins")
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_c2:
    st.markdown("<div class='section-header'>🥧 Mix de Canales</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
    
    if 'MacroCanal' in df_filtered.columns:
        df_pie = df_filtered.groupby('MacroCanal')['ValorNeto'].sum().reset_index()
        
        # Colores seguros
        pie_colors = [CANAL_COLOR_MAP.get(x, COLORS['text_muted']) for x in df_pie['MacroCanal']]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=df_pie['MacroCanal'],
            values=df_pie['ValorNeto'],
            hole=.6,
            marker=dict(colors=pie_colors),
            textinfo='label+percent',
            textfont=dict(size=11),
            hoverinfo='label+value+percent'
        )])
        
        fig_pie.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins"),
            annotations=[dict(text='MIX %', x=0.5, y=0.5, font_size=20, showarrow=False, font_family='Poppins', font_color=COLORS['primary'])]
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 9. SECCIÓN 4: TABLA DETALLADA CON BARRAS DE PROGRESO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div class='section-header'>📋 Detalle Táctico por Proyecto</div>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
    
    if 'MacroProyecto' in df_filtered.columns:
        # Crear tabla resumen
        df_table = df_filtered.groupby('MacroProyecto').agg(
            Ciudad=('Ciudad', 'first'),
            Ventas=('ValorNeto', 'sum'),
            Unidades=('ValorNeto', 'count'),
            Ticket=('ValorNeto', 'mean')
        ).reset_index().sort_values('Ventas', ascending=False)
        
        # Configuración de columnas para st.dataframe (Streamlit Column Config)
        st.dataframe(
            df_table,
            column_config={
                "MacroProyecto": st.column_config.TextColumn(
                    "Nombre del Proyecto",
                    width="medium",
                    help="Nombre comercial del desarrollo"
                ),
                "Ciudad": st.column_config.TextColumn(
                    "Plaza",
                    width="small"
                ),
                "Ventas": st.column_config.ProgressColumn(
                    "Volumen de Ventas (COP)",
                    help="Ingresos netos totales",
                    format="$%d",
                    min_value=0,
                    max_value=int(df_table['Ventas'].max()),
                    width="large",
                ),
                "Unidades": st.column_config.NumberColumn(
                    "Unds",
                    help="Total unidades vendidas",
                    format="%d 🏠"
                ),
                "Ticket": st.column_config.NumberColumn(
                    "Ticket Promedio",
                    format="$%d",
                )
            },
            hide_index=True,
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 10. FOOTER CORPORATIVO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col_foot1, col_foot2, col_foot3 = st.columns([1, 2, 1])

with col_foot2:
    st.markdown(f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.8rem;">
        <p><strong>CONALTURA CONSTRUCCIÓN Y VIVIENDA S.A.S</strong></p>
        <p>Dashboard generado automáticamente • Datos confidenciales de uso interno</p>
        <p style="opacity: 0.5;">Powered by Python Streamlit Engine &bull; V.2025.1.0 (Antigravity)</p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FIN DEL CÓDIGO
# ══════════════════════════════════════════════════════════════════════════════
