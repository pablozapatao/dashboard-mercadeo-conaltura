"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           CONALTURA - DASHBOARD COMERCIAL JUNTA INTERNACIONAL 2025           ║
║                    Alineación Ventas & Mercadeo                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import locale
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA Y BRANDING CONALTURA
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Conaltura | Dashboard Comercial 2025",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de Colores Conaltura (Manual de Marca)
COLORS = {
    'primary': '#125160',      # Verde Petróleo - Fondos/Headers
    'accent_orange': '#FF795A', # Naranja Vibrante - Acentos/KPIs
    'accent_lime': '#DBFF69',   # Verde Lima - Datos positivos
    'accent_green': '#A1D81A',  # Verde claro secundario
    'beige': '#F4F0E5',         # Beige claro - Fondos paneles
    'purple': '#B382FF',        # Púrpura secundario
    'white': '#FFFFFF',
    'dark_text': '#125160',
    'gray': '#445254'
}

# Paleta extendida para gráficos
CHART_COLORS = [
    '#125160', '#FF795A', '#DBFF69', '#A1D81A', '#B382FF',
    '#F4F0E5', '#1a6b7a', '#ff9580', '#e5ff8a', '#c4a3ff'
]

# ══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS PERSONALIZADOS - LOVABLE STYLE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
    /* ══════ FUENTES Y BASE ══════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', 'Funnel Sans', Arial, sans-serif !important;
    }}
    
    .main {{
        background-color: {COLORS['beige']};
    }}
    
    /* ══════ SIDEBAR ══════ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary']} 0%, #0d3d4a 100%);
        padding: 1rem;
    }}
    
    [data-testid="stSidebar"] * {{
        color: {COLORS['white']} !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {{
        color: {COLORS['accent_lime']} !important;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* ══════ TARJETAS KPI ══════ */
    .kpi-card {{
        background: {COLORS['white']};
        border-radius: 20px;
        padding: 1.5rem 2rem;
        box-shadow: 0 4px 20px rgba(18, 81, 96, 0.08);
        border: 1px solid rgba(18, 81, 96, 0.05);
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(18, 81, 96, 0.15);
    }}
    
    .kpi-label {{
        color: {COLORS['gray']};
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }}
    
    .kpi-value {{
        color: {COLORS['primary']};
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
    }}
    
    .kpi-value-orange {{
        color: {COLORS['accent_orange']};
    }}
    
    .kpi-subtitle {{
        color: {COLORS['accent_green']};
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }}
    
    /* ══════ SECCIONES ══════ */
    .section-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #1a6b7a 100%);
        color: {COLORS['white']};
        padding: 1rem 1.5rem;
        border-radius: 15px 15px 0 0;
        margin-top: 2rem;
        margin-bottom: 0;
    }}
    
    .section-header h2 {{
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
    }}
    
    .section-header p {{
        margin: 0.3rem 0 0 0;
        font-size: 0.85rem;
        opacity: 0.85;
    }}
    
    .section-content {{
        background: {COLORS['white']};
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 20px rgba(18, 81, 96, 0.08);
        margin-bottom: 1rem;
    }}
    
    /* ══════ HEADER PRINCIPAL ══════ */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #0d3d4a 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(18, 81, 96, 0.2);
    }}
    
    .main-header h1 {{
        color: {COLORS['white']};
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }}
    
    .main-header .subtitle {{
        color: {COLORS['accent_lime']};
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }}
    
    .logo-smile {{
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }}
    
    /* ══════ TABLA ESTILIZADA ══════ */
    .dataframe {{
        border-radius: 10px !important;
        overflow: hidden;
    }}
    
    .dataframe th {{
        background-color: {COLORS['primary']} !important;
        color: {COLORS['white']} !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }}
    
    .dataframe td {{
        font-size: 0.9rem;
    }}
    
    /* ══════ BADGES ══════ */
    .badge {{
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }}
    
    .badge-digital {{
        background: {COLORS['accent_lime']};
        color: {COLORS['primary']};
    }}
    
    .badge-tradicional {{
        background: {COLORS['accent_orange']};
        color: {COLORS['white']};
    }}
    
    /* ══════ FILE UPLOADER ══════ */
    [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1rem;
        border: 2px dashed {COLORS['accent_lime']};
    }}
    
    /* ══════ METRICS ══════ */
    [data-testid="stMetric"] {{
        background: {COLORS['white']};
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(18, 81, 96, 0.05);
    }}
    
    /* ══════ DIVIDER ══════ */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLORS['accent_lime']}, transparent);
        margin: 2rem 0;
    }}
    
    /* ══════ BOTONES ══════ */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['accent_orange']} 0%, #ff6040 100%);
        color: {COLORS['white']};
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(255, 121, 90, 0.4);
    }}
    
    /* ══════ HIDE STREAMLIT BRANDING ══════ */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ══════════════════════════════════════════════════════════════════════════════

def format_cop(value):
    """Formatea un valor numérico a Pesos Colombianos"""
    try:
        if pd.isna(value) or value == 0:
            return "$ 0"
        if value >= 1_000_000_000:
            return f"$ {value/1_000_000_000:,.1f} B"
        elif value >= 1_000_000:
            return f"$ {value/1_000_000:,.0f} M"
        elif value >= 1_000:
            return f"$ {value/1_000:,.0f} K"
        else:
            return f"$ {value:,.0f}"
    except:
        return "$ 0"

def format_cop_full(value):
    """Formatea un valor numérico a Pesos Colombianos completo"""
    try:
        if pd.isna(value):
            return "$ 0"
        return f"$ {value:,.0f}".replace(",", ".")
    except:
        return "$ 0"

def clean_column_names(df):
    """Normaliza y limpia los nombres de columnas"""
    column_mapping = {
        'macroproyecto': 'MacroProyecto',
        'macro_proyecto': 'MacroProyecto',
        'proyecto': 'MacroProyecto',
        'medio_publicitario': 'Medio Publicitario',
        'mediopublicitario': 'Medio Publicitario',
        'medio': 'Medio Publicitario',
        'canal': 'Medio Publicitario',
        'valor_neto': 'Valor Neto',
        'valorneto': 'Valor Neto',
        'valor': 'Valor Neto',
        'ingresos': 'Valor Neto',
        'ventas': 'Valor Neto',
        'ciudad': 'Ciudad',
        'ubicacion': 'Ciudad',
        'fecha': 'Fecha',
        'date': 'Fecha',
        'agrupacion': 'Agrupación',
        'agrupación': 'Agrupación',
        'categoria': 'Agrupación',
        'categoría': 'Agrupación',
        'tipo': 'Agrupación'
    }
    
    # Normalizar nombres de columnas
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    df = df.rename(columns=column_mapping)
    
    return df

def load_data(uploaded_file):
    """Carga y procesa el archivo de datos"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Formato de archivo no soportado. Use CSV o Excel.")
            return None
        
        # Limpiar nombres de columnas
        df = clean_column_names(df)
        
        # Verificar columnas requeridas
        required_cols = ['MacroProyecto', 'Medio Publicitario', 'Valor Neto', 'Ciudad', 'Fecha', 'Agrupación']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ Columnas faltantes detectadas: {', '.join(missing_cols)}. Intentando mapear...")
            # Intentar mapear con columnas existentes
            for col in df.columns:
                if col not in required_cols:
                    for req_col in missing_cols:
                        if req_col.lower() in col.lower():
                            df = df.rename(columns={col: req_col})
                            missing_cols.remove(req_col)
                            break
        
        # Convertir tipos de datos
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
            df['Año'] = df['Fecha'].dt.year
            df['Mes_Nombre'] = df['Fecha'].dt.strftime('%b %Y')
        
        if 'Valor Neto' in df.columns:
            df['Valor Neto'] = pd.to_numeric(df['Valor Neto'], errors='coerce').fillna(0)
        
        # Limpiar valores nulos en columnas categóricas
        for col in ['MacroProyecto', 'Medio Publicitario', 'Ciudad', 'Agrupación']:
            if col in df.columns:
                df[col] = df[col].fillna('Sin Definir').astype(str).str.strip()
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {str(e)}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Logo y título
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">
            <span style="color: #125160;">C</span><span style="color: #A1D81A;">O</span>
        </div>
        <div style="font-size: 2.5rem; color: #125160;">😊</div>
        <h2 style="color: #A1D81A; margin: 0.5rem 0; font-weight: 700;">CONALTURA</h2>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;">
            Dashboard Comercial 2025
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # File Uploader
    st.markdown("### 📁 Cargar Datos")
    uploaded_file = st.file_uploader(
        "Arrastra tu archivo CSV/Excel",
        type=['csv', 'xlsx', 'xls'],
        help="El archivo debe contener: MacroProyecto, Medio Publicitario, Valor Neto, Ciudad, Fecha, Agrupación"
    )
    
    st.markdown("---")
    
    # Filtros (se activarán cuando se cargue el archivo)
    st.markdown("### 🎯 Filtros Globales")
    
    # Placeholder para filtros
    filter_ciudad = None
    filter_proyecto = None
    filter_fecha = None
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None and not df.empty:
            # Filtro de Ciudad
            if 'Ciudad' in df.columns:
                ciudades = ['Todas'] + sorted(df['Ciudad'].unique().tolist())
                filter_ciudad = st.selectbox("🏙️ Ciudad", ciudades)
            
            # Filtro de MacroProyecto
            if 'MacroProyecto' in df.columns:
                proyectos = ['Todos'] + sorted(df['MacroProyecto'].unique().tolist())
                filter_proyecto = st.selectbox("🏗️ Proyecto", proyectos)
            
            # Filtro de Fecha
            if 'Fecha' in df.columns:
                min_date = df['Fecha'].min()
                max_date = df['Fecha'].max()
                if pd.notna(min_date) and pd.notna(max_date):
                    filter_fecha = st.date_input(
                        "📅 Rango de Fechas",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )
    else:
        st.info("👆 Carga un archivo para activar los filtros")
    
    st.markdown("---")
    
    # Créditos
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; font-size: 0.75rem; opacity: 0.7;">
        <p>Desarrollado para</p>
        <p><strong>Junta Internacional 2025</strong></p>
        <p style="margin-top: 1rem;">🏠 Construyendo un futuro sostenible</p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONTENIDO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

# Header Principal
st.markdown("""
<div class="main-header">
    <div class="logo-smile">😊</div>
    <h1>CONALTURA</h1>
    <p class="subtitle">Dashboard Comercial | Junta Internacional 2025</p>
</div>
""", unsafe_allow_html=True)

# Verificar si hay datos cargados
if uploaded_file is None:
    # Estado inicial - sin datos
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 20px; box-shadow: 0 4px 20px rgba(18,81,96,0.08);">
        <div style="font-size: 5rem; margin-bottom: 1rem;">📊</div>
        <h2 style="color: #125160; margin-bottom: 1rem;">¡Bienvenido al Dashboard Comercial!</h2>
        <p style="color: #445254; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
            Para comenzar, carga tu archivo de datos desde el panel lateral izquierdo.
            El archivo debe contener las siguientes columnas:
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;">
            <span style="background: #DBFF69; color: #125160; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">MacroProyecto</span>
            <span style="background: #FF795A; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">Medio Publicitario</span>
            <span style="background: #125160; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">Valor Neto</span>
            <span style="background: #B382FF; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">Ciudad</span>
            <span style="background: #A1D81A; color: #125160; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">Fecha</span>
            <span style="background: #F4F0E5; color: #125160; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; border: 2px solid #125160;">Agrupación</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Si hay datos cargados, procesar
df = load_data(uploaded_file)

if df is None or df.empty:
    st.error("❌ El archivo está vacío o no se pudo procesar correctamente.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# APLICAR FILTROS
# ══════════════════════════════════════════════════════════════════════════════

df_filtered = df.copy()

if filter_ciudad and filter_ciudad != 'Todas':
    df_filtered = df_filtered[df_filtered['Ciudad'] == filter_ciudad]

if filter_proyecto and filter_proyecto != 'Todos':
    df_filtered = df_filtered[df_filtered['MacroProyecto'] == filter_proyecto]

if filter_fecha and len(filter_fecha) == 2:
    df_filtered = df_filtered[
        (df_filtered['Fecha'] >= pd.Timestamp(filter_fecha[0])) & 
        (df_filtered['Fecha'] <= pd.Timestamp(filter_fecha[1]))
    ]

if df_filtered.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados. Ajusta los filtros.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1: EL PUM - RESUMEN EJECUTIVO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <h2>🚀 EL PUM - Resumen Ejecutivo</h2>
    <p>Vista 360° de los resultados comerciales 2025</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# KPI 1: Ventas Totales
total_ventas = df_filtered['Valor Neto'].sum()
with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Ventas Totales 2025</div>
        <div class="kpi-value">{format_cop(total_ventas)}</div>
        <div class="kpi-subtitle">Valor Neto Consolidado</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 2: Top Ciudad
top_ciudad_data = df_filtered.groupby('Ciudad')['Valor Neto'].sum().sort_values(ascending=False)
if not top_ciudad_data.empty:
    top_ciudad = top_ciudad_data.index[0]
    top_ciudad_valor = top_ciudad_data.iloc[0]
    top_ciudad_pct = (top_ciudad_valor / total_ventas * 100) if total_ventas > 0 else 0
else:
    top_ciudad = "N/A"
    top_ciudad_pct = 0

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🏙️ Top Ciudad en Ventas</div>
        <div class="kpi-value kpi-value-orange">{top_ciudad}</div>
        <div class="kpi-subtitle">{top_ciudad_pct:.1f}% del total</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 3: Canal #1
top_canal_data = df_filtered.groupby('Medio Publicitario')['Valor Neto'].sum().sort_values(ascending=False)
if not top_canal_data.empty:
    top_canal = top_canal_data.index[0]
    top_canal_valor = top_canal_data.iloc[0]
    top_canal_pct = (top_canal_valor / total_ventas * 100) if total_ventas > 0 else 0
else:
    top_canal = "N/A"
    top_canal_pct = 0

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📣 Canal #1 en Aportes</div>
        <div class="kpi-value">{top_canal}</div>
        <div class="kpi-subtitle">{format_cop(top_canal_valor)} ({top_canal_pct:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Métricas adicionales en fila
st.markdown("<br>", unsafe_allow_html=True)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    n_proyectos = df_filtered['MacroProyecto'].nunique()
    st.metric("🏗️ Proyectos Activos", n_proyectos)

with col_m2:
    n_canales = df_filtered['Medio Publicitario'].nunique()
    st.metric("📢 Canales de Venta", n_canales)

with col_m3:
    n_ciudades = df_filtered['Ciudad'].nunique()
    st.metric("🗺️ Ciudades", n_ciudades)

with col_m4:
    ticket_promedio = total_ventas / len(df_filtered) if len(df_filtered) > 0 else 0
    st.metric("🎫 Ticket Promedio", format_cop(ticket_promedio))

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2: ALINEACIÓN MERCADEO - VENTAS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div class="section-header">
    <h2>🎯 Alineación Mercadeo - Ventas</h2>
    <p>¿De dónde vino cada peso invertido? Análisis de atribución por canal</p>
</div>
<div class="section-content">
""", unsafe_allow_html=True)

col_sun, col_trend = st.columns([1.2, 1])

with col_sun:
    st.markdown("#### 📊 Árbol de Atribución de Ventas")
    st.caption("Jerarquía: Agrupación → Medio Publicitario → Proyecto")
    
    # Preparar datos para Sunburst
    sunburst_data = df_filtered.groupby(['Agrupación', 'Medio Publicitario', 'MacroProyecto'])['Valor Neto'].sum().reset_index()
    
    if not sunburst_data.empty:
        fig_sunburst = px.sunburst(
            sunburst_data,
            path=['Agrupación', 'Medio Publicitario', 'MacroProyecto'],
            values='Valor Neto',
            color='Agrupación',
            color_discrete_map={
                'Ventas Digitales': COLORS['accent_lime'],
                'Digital': COLORS['accent_lime'],
                'Tradicional': COLORS['accent_orange'],
                'Ventas Tradicionales': COLORS['accent_orange'],
                'Referidos': COLORS['purple'],
                'Otros': COLORS['primary']
            },
            hover_data={'Valor Neto': ':,.0f'}
        )
        
        fig_sunburst.update_traces(
            textinfo='label+percent parent',
            hovertemplate='<b>%{label}</b><br>Valor: $%{value:,.0f}<br>%{percentParent:.1%} del padre<extra></extra>'
        )
        
        fig_sunburst.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            height=450,
            font=dict(family="Inter, sans-serif")
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("No hay datos suficientes para el gráfico Sunburst")

with col_trend:
    st.markdown("#### 📈 Tendencia Mensual por Estrategia")
    st.caption("Comparativa: Digital vs Tradicional")
    
    if 'Mes' in df_filtered.columns:
        trend_data = df_filtered.groupby(['Mes', 'Agrupación'])['Valor Neto'].sum().reset_index()
        
        if not trend_data.empty:
            fig_trend = px.line(
                trend_data,
                x='Mes',
                y='Valor Neto',
                color='Agrupación',
                markers=True,
                color_discrete_sequence=[COLORS['accent_lime'], COLORS['accent_orange'], COLORS['purple'], COLORS['primary']]
            )
            
            fig_trend.update_traces(
                line=dict(width=3),
                marker=dict(size=10)
            )
            
            fig_trend.update_layout(
                xaxis_title="",
                yaxis_title="Valor Neto (COP)",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=50, l=10, r=10, b=10),
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif")
            )
            
            fig_trend.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(18,81,96,0.1)')
            fig_trend.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(18,81,96,0.1)')
            
            st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No hay datos de fecha para mostrar tendencias")

st.markdown("</div>", unsafe_allow_html=True)

# Gráfico de barras de canales
st.markdown("<br>", unsafe_allow_html=True)
col_bar1, col_bar2 = st.columns(2)

with col_bar1:
    st.markdown("#### 📣 Rendimiento por Canal")
    canal_data = df_filtered.groupby('Medio Publicitario')['Valor Neto'].sum().sort_values(ascending=True).tail(10)
    
    fig_canal = go.Figure(go.Bar(
        x=canal_data.values,
        y=canal_data.index,
        orientation='h',
        marker=dict(
            color=canal_data.values,
            colorscale=[[0, COLORS['primary']], [0.5, COLORS['accent_orange']], [1, COLORS['accent_lime']]],
            line=dict(width=0)
        ),
        text=[format_cop(v) for v in canal_data.values],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Ventas: $%{x:,.0f}<extra></extra>'
    ))
    
    fig_canal.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Valor Neto (COP)",
        yaxis_title="",
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig_canal, use_container_width=True)

with col_bar2:
    st.markdown("#### 🏗️ Top Proyectos por Ventas")
    proyecto_data = df_filtered.groupby('MacroProyecto')['Valor Neto'].sum().sort_values(ascending=True).tail(10)
    
    fig_proyecto = go.Figure(go.Bar(
        x=proyecto_data.values,
        y=proyecto_data.index,
        orientation='h',
        marker=dict(
            color=proyecto_data.values,
            colorscale=[[0, COLORS['accent_orange']], [0.5, COLORS['accent_lime']], [1, COLORS['primary']]],
            line=dict(width=0)
        ),
        text=[format_cop(v) for v in proyecto_data.values],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Ventas: $%{x:,.0f}<extra></extra>'
    ))
    
    fig_proyecto.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Valor Neto (COP)",
        yaxis_title="",
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig_proyecto, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3: GEOGRAFÍA Y EFICIENCIA
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div class="section-header">
    <h2>🗺️ Geografía y Eficiencia Comercial</h2>
    <p>Distribución territorial de ventas y análisis de desempeño</p>
</div>
<div class="section-content">
""", unsafe_allow_html=True)

col_geo, col_table = st.columns([1, 1])

with col_geo:
    st.markdown("#### 🌎 Distribución por Ciudad")
    
    ciudad_data = df_filtered.groupby('Ciudad')['Valor Neto'].sum().reset_index()
    ciudad_data = ciudad_data.sort_values('Valor Neto', ascending=False)
    
    # Coordenadas aproximadas de ciudades colombianas
    city_coords = {
        'Medellín': (6.2442, -75.5812),
        'Medellin': (6.2442, -75.5812),
        'Bogotá': (4.7110, -74.0721),
        'Bogota': (4.7110, -74.0721),
        'Cali': (3.4516, -76.5320),
        'Barranquilla': (10.9685, -74.7813),
        'Cartagena': (10.3910, -75.4794),
        'Bucaramanga': (7.1254, -73.1198),
        'Pereira': (4.8087, -75.6906),
        'Santa Marta': (11.2404, -74.1990),
        'Ibagué': (4.4389, -75.2322),
        'Ibague': (4.4389, -75.2322),
        'Manizales': (5.0689, -75.5174),
        'Villavicencio': (4.1420, -73.6266),
        'Armenia': (4.5339, -75.6811),
        'Neiva': (2.9273, -75.2819),
        'Popayán': (2.4419, -76.6063),
        'Popoyan': (2.4419, -76.6063),
        'Valledupar': (10.4631, -73.2532),
        'Montería': (8.7575, -75.8856),
        'Monteria': (8.7575, -75.8856),
        'Sincelejo': (9.3047, -75.3978),
        'Tunja': (5.5353, -73.3678),
        'Rionegro': (6.1553, -75.3743),
        'Envigado': (6.1696, -75.5891),
        'Sabaneta': (6.1517, -75.6165),
        'Bello': (6.3383, -75.5586),
        'Itagüí': (6.1843, -75.5994),
        'Itagui': (6.1843, -75.5994)
    }
    
    # Añadir coordenadas
    ciudad_data['lat'] = ciudad_data['Ciudad'].map(lambda x: city_coords.get(x, (4.5709, -74.2973))[0])
    ciudad_data['lon'] = ciudad_data['Ciudad'].map(lambda x: city_coords.get(x, (4.5709, -74.2973))[1])
    
    # Crear mapa o gráfico de barras según disponibilidad de coordenadas
    fig_geo = go.Figure()
    
    # Gráfico de barras como alternativa robusta
    fig_geo = px.bar(
        ciudad_data.head(10),
        x='Ciudad',
        y='Valor Neto',
        color='Valor Neto',
        color_continuous_scale=[[0, COLORS['primary']], [0.5, COLORS['accent_orange']], [1, COLORS['accent_lime']]],
        text=[format_cop(v) for v in ciudad_data.head(10)['Valor Neto']],
    )
    
    fig_geo.update_traces(
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
    )
    
    fig_geo.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title="Valor Neto (COP)",
        showlegend=False,
        font=dict(family="Inter, sans-serif"),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig_geo, use_container_width=True)

with col_table:
    st.markdown("#### 🏆 Top 10 Proyectos - Detalle")
    
    top_proyectos = df_filtered.groupby(['MacroProyecto', 'Ciudad']).agg({
        'Valor Neto': 'sum',
        'Medio Publicitario': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
    }).reset_index()
    
    top_proyectos = top_proyectos.sort_values('Valor Neto', ascending=False).head(10)
    top_proyectos['Valor Neto Formatted'] = top_proyectos['Valor Neto'].apply(format_cop_full)
    top_proyectos['Ranking'] = range(1, len(top_proyectos) + 1)
    
    # Mostrar tabla
    display_df = top_proyectos[['Ranking', 'MacroProyecto', 'Ciudad', 'Valor Neto Formatted', 'Medio Publicitario']].copy()
    display_df.columns = ['#', 'Proyecto', 'Ciudad', 'Ventas Netas', 'Canal Principal']
    
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "#": st.column_config.NumberColumn(width="small"),
            "Proyecto": st.column_config.TextColumn(width="medium"),
            "Ciudad": st.column_config.TextColumn(width="small"),
            "Ventas Netas": st.column_config.TextColumn(width="medium"),
            "Canal Principal": st.column_config.TextColumn(width="medium")
        }
    )

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4: ANÁLISIS ADICIONAL
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div class="section-header">
    <h2>📊 Análisis Complementario</h2>
    <p>Insights adicionales para la toma de decisiones estratégicas</p>
</div>
<div class="section-content">
""", unsafe_allow_html=True)

# Treemap alternativo
col_tree, col_donut = st.columns([1.5, 1])

with col_tree:
    st.markdown("#### 🌳 Treemap de Contribución por Segmento")
    
    treemap_data = df_filtered.groupby(['Agrupación', 'Medio Publicitario'])['Valor Neto'].sum().reset_index()
    
    if not treemap_data.empty and len(treemap_data) > 1:
        fig_treemap = px.treemap(
            treemap_data,
            path=['Agrupación', 'Medio Publicitario'],
            values='Valor Neto',
            color='Valor Neto',
            color_continuous_scale=[[0, COLORS['primary']], [0.5, COLORS['accent_orange']], [1, COLORS['accent_lime']]]
        )
        
        fig_treemap.update_traces(
            textinfo='label+value+percent root',
            hovertemplate='<b>%{label}</b><br>Valor: $%{value:,.0f}<br>%{percentRoot:.1%} del total<extra></extra>'
        )
        
        fig_treemap.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            height=400,
            font=dict(family="Inter, sans-serif"),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    else:
        st.info("Se requieren más datos para mostrar el Treemap")

with col_donut:
    st.markdown("#### 🍩 Distribución por Agrupación")
    
    agrupacion_data = df_filtered.groupby('Agrupación')['Valor Neto'].sum().reset_index()
    
    if not agrupacion_data.empty:
        fig_donut = go.Figure(data=[go.Pie(
            labels=agrupacion_data['Agrupación'],
            values=agrupacion_data['Valor Neto'],
            hole=0.6,
            marker=dict(colors=[COLORS['accent_lime'], COLORS['accent_orange'], COLORS['purple'], COLORS['primary']]),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Valor: $%{value:,.0f}<br>%{percent}<extra></extra>'
        )])
        
        fig_donut.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            font=dict(family="Inter, sans-serif"),
            annotations=[dict(
                text=f'<b>{format_cop(total_ventas)}</b>',
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False,
                font=dict(color=COLORS['primary'])
            )]
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {COLORS['primary']} 0%, #0d3d4a 100%); border-radius: 20px; margin-top: 2rem;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">
        <span style="color: {COLORS['white']};">C</span><span style="color: {COLORS['accent_lime']};">O</span>
        <span style="font-size: 1.5rem;">😊</span>
    </div>
    <h3 style="color: {COLORS['white']}; margin: 0;">CONALTURA</h3>
    <p style="color: {COLORS['accent_lime']}; margin: 0.5rem 0;">Construir un futuro sostenible donde las personas, los negocios y la naturaleza prosperan juntos.</p>
    <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 1rem;">Dashboard Comercial | Junta Internacional 2025</p>
</div>
""", unsafe_allow_html=True)
