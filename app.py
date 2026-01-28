"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CONALTURA - ENTERPRISE DASHBOARD SYSTEM                   ║
║                    Gran Convención de Ventas 2025                            ║
║                    Versión: UI/UX High-Fidelity (Brand & Data Fix)           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# 1. SISTEMA DE CONFIGURACIÓN Y BRANDING (MANUAL DE MARCA ESTRICTO)
# ══════════════════════════════════════════════════════════════════════════════

# Configuración de página: Sidebar expandido por defecto para que el usuario vea los controles
st.set_page_config(
    page_title="Conaltura | Intelligence Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# ------------------------------------------------------------------------------
# PALETA DE COLORES CORPORATIVA (CONSTANTES GLOBALES)
# ------------------------------------------------------------------------------
# Extraída del Manual de Marca Conaltura
COLORS = {
    'primary': '#125160',      # Verde Petróleo (Identidad Core)
    'primary_dark': '#0E3F4B', # Verde más oscuro para contrastes
    'accent': '#FF795A',       # Naranja Coral (Call to Actions / Alertas)
    'highlight': '#DBFF69',    # Verde Lima (KPIs Positivos / Digital)
    'secondary': '#B382FF',    # Lila (Categorías secundarias)
    'bg_app': '#F8FAFC',       # Fondo General (Gris Humo muy suave)
    'bg_card': '#FFFFFF',      # Fondo Tarjetas (Blanco Puro)
    'text_main': '#0F172A',    # Texto Principal
    'text_muted': '#64748B',   # Texto Secundario
    'border': '#E2E8F0',       # Bordes sutiles
}

# Mapas de color para consistencia visual en gráficos
# Se usarán estos mapas para forzar la identidad visual en Plotly
GAMA_COLOR_MAP = {
    'VIS/Acceso': '#E8FFB0',   # Verde pálido
    'Media': '#DBFF69',        # Verde Lima (Marca)
    'Alta': '#125160',         # Verde Petróleo (Marca)
    'Premium': '#FF795A',      # Coral (Marca)
    'Sin Definir': '#94A3B8'
}

CANAL_COLOR_MAP = {
    'DIGITAL': '#DBFF69',          # Lima (Innovación)
    'RELACIONAMIENTO': '#125160',  # Petróleo (Seriedad)
    'EXPERIENCIA': '#B382FF',      # Lila
    'EVENTOS': '#FF795A',          # Coral
    'TRADICIONAL': '#A8D861',      # Verde secundario
    'OTROS': '#CBD5E1'
}

# Secuencia de colores por defecto para gráficos donde no hay mapa específico
BRAND_PALETTE = [COLORS['primary'], COLORS['accent'], COLORS['highlight'], COLORS['secondary'], '#10B981', '#F59E0B']

# ------------------------------------------------------------------------------
# INYECCIÓN DE CSS AVANZADO (ESTILO CORPORATIVO)
# ------------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* Tipografía Global */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
        color: {COLORS['text_main']};
    }}
    
    /* Fondo Aplicación */
    .stApp {{
        background-color: {COLORS['bg_app']};
    }}
    
    /* Ajustes del contenedor principal */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1600px;
    }}
    
    /* ESTILO DE TARJETAS KPI (HIGH-END) */
    .kpi-card {{
        background-color: {COLORS['bg_card']};
        border-radius: 12px;
        padding: 24px;
        border-left: 5px solid {COLORS['primary']};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-left: 5px solid {COLORS['highlight']};
    }}
    .kpi-title {{
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {COLORS['text_muted']};
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin-bottom: 5px;
    }}
    .kpi-badge {{
        display: inline-block;
        padding: 2px 10px;
        background-color: rgba(18, 81, 96, 0.1); /* Primary con transparencia */
        color: {COLORS['primary']};
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}

    /* HEADERS Y TÍTULOS */
    h1 {{ color: {COLORS['primary']}; font-weight: 700; }}
    h2 {{ color: {COLORS['primary_dark']}; font-weight: 600; font-size: 1.5rem; }}
    h3 {{ color: {COLORS['text_main']}; font-weight: 600; font-size: 1.2rem; }}
    
    /* SEPARADORES DE SECCIÓN */
    .section-divider {{
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid {COLORS['border']};
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .section-icon {{
        background: {COLORS['accent']};
        color: white;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        font-size: 1.2rem;
    }}
    .section-title {{
        font-size: 1.4rem;
        color: {COLORS['primary']};
        font-weight: 700;
    }}
    
    /* BOTONES */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
    }}
    .stButton > button:hover {{
        background-color: {COLORS['accent']};
        color: white;
    }}

    /* ESTILO PARA EL MENSAJE DE CARGA (UPLOAD BOX) */
    .upload-box {{
        border: 2px dashed {COLORS['primary']};
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
    }}

    /* OCULTAR ELEMENTOS NO DESEADOS DE STREAMLIT */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2. MOTOR DE DATOS (ROBUSTO Y DIAGNÓSTICO)
# ══════════════════════════════════════════════════════════════════════════════

def format_currency_cop(value):
    """Formatea moneda a pesos colombianos legibles"""
    if value == 0: return "$0"
    if value >= 1e9: return f"${value/1e9:.2f} MM" # Billones colombianos (Miles de Millones)
    if value >= 1e6: return f"${value/1e6:.1f} M"
    return f"${value:,.0f}"

@st.cache_data(show_spinner=False)
def load_data(file):
    """
    Carga el archivo intentando corregir errores comunes de Excel/CSV
    """
    try:
        # 1. Lectura inteligente
        if file.name.endswith('.csv'):
            try:
                df = pd.read_csv(file, encoding='utf-8', sep=None, engine='python')
            except:
                file.seek(0)
                df = pd.read_csv(file, encoding='latin-1', sep=';')
        else:
            df = pd.read_excel(file)
            
        # 2. Normalización de columnas (Mapping agresivo)
        # Esto soluciona que 'Agrupación' tenga tilde o no, mayúsculas, etc.
        cols_renamed = {}
        for col in df.columns:
            c = col.lower().strip().replace(' ', '').replace('_', '').replace('ó', 'o').replace('neta', 'neto')
            
            if 'macroproyecto' in c or 'proyecto' in c: cols_renamed[col] = 'MacroProyecto'
            elif 'medio' in c: cols_renamed[col] = 'Medio'
            elif 'agrupacion' in c or 'categoria' in c: cols_renamed[col] = 'Agrupacion'
            elif 'valor' in c and 'neto' in c: cols_renamed[col] = 'ValorNeto'
            elif 'ciudad' in c: cols_renamed[col] = 'Ciudad'
            elif 'gama' in c: cols_renamed[col] = 'Gama'
            elif 'fecha' in c: cols_renamed[col] = 'Fecha'
            
        df = df.rename(columns=cols_renamed)
        
        # 3. Limpieza de tipos
        if 'ValorNeto' in df.columns:
            if df['ValorNeto'].dtype == object:
                df['ValorNeto'] = df['ValorNeto'].astype(str).str.replace(r'[$,.]', '', regex=True)
            df['ValorNeto'] = pd.to_numeric(df['ValorNeto'], errors='coerce').fillna(0)
            
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')
            
        # 4. Rellenar vacíos visuales
        cols_text = ['MacroProyecto', 'Medio', 'Ciudad', 'Agrupacion', 'Gama']
        for c in cols_text:
            if c in df.columns:
                df[c] = df[c].fillna('Sin Asignar').astype(str).str.title()
                
        return df
        
    except Exception as e:
        return None

# ══════════════════════════════════════════════════════════════════════════════
# 3. INTERFAZ: GESTIÓN DE ESTADO Y CARGA
# ══════════════════════════════════════════════════════════════════════════════

# --- LOGO Y TÍTULO ---
col_head1, col_head2 = st.columns([1, 6])
with col_head1:
    # Intentar cargar logo si existe, si no, placeholder verde
    if Path("logo.png").exists():
        st.image("logo.png", width=100)
    else:
        st.markdown(f"""
        <div style="background:{COLORS['primary']}; width:80px; height:80px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; font-size:40px;">🏢</div>
        """, unsafe_allow_html=True)

with col_head2:
    st.markdown(f"""
    <div style="padding-top:10px;">
        <h1 style="margin:0; font-size:2.2rem; letter-spacing:-1px;">TABLERO COMERCIAL <span style="color:{COLORS['highlight']}; background:{COLORS['primary']}; padding:0 8px; border-radius:6px;">2025</span></h1>
        <p style="margin:0; color:{COLORS['text_muted']};">Gran Convención Conaltura • Análisis de Impacto y Eficiencia</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- LÓGICA DE CARGA (CENTRAL + SIDEBAR) ---
# Primero revisamos si ya hay un archivo en session_state o cargado
uploaded_file = st.sidebar.file_uploader("📂 Panel de Carga (Sidebar)", type=['xlsx', 'csv'])

# Si NO hay archivo cargado en el sidebar, mostramos el cargador CENTRAL GIGANTE
if uploaded_file is None:
    st.markdown(f"""
    <div class="upload-box">
        <h2 style="color:{COLORS['primary']}">👋 Bienvenido al Centro de Inteligencia</h2>
        <p style="font-size:1.1rem; color:{COLORS['text_muted']}">Para generar el reporte, necesitamos la sábana de datos.</p>
        <p><em>Por favor utilice el cargador en la barra lateral izquierda (Sidebar)</em></p>
        <div style="font-size:3rem; margin-top:20px;">👈</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detenemos la ejecución aquí para que no de errores de variables vacías
    st.stop()

# Si llegamos aquí, hay archivo. Lo procesamos.
df = load_data(uploaded_file)

if df is None:
    st.error("❌ Error de Lectura: El archivo no tiene el formato esperado. Asegúrate de que sea un Excel o CSV válido.")
    st.stop()

# Validación rápida de columnas críticas
required_cols = ['MacroProyecto', 'ValorNeto', 'Ciudad']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.warning(f"⚠️ Alerta de Calidad de Datos: No encontré las columnas exactas: {missing}. Verifique su archivo.")
    # No detenemos, intentamos seguir

# ══════════════════════════════════════════════════════════════════════════════
# 4. FILTROS (SIDEBAR)
# ══════════════════════════════════════════════════════════════════════════════

st.sidebar.markdown("---")
st.sidebar.header("🔍 Segmentación")

# Filtros Dinámicos
city_opts = ['Todas'] + sorted(list(df['Ciudad'].unique())) if 'Ciudad' in df.columns else []
sel_city = st.sidebar.selectbox("Ciudad", city_opts)

proj_opts = ['Todos'] + sorted(list(df['MacroProyecto'].unique())) if 'MacroProyecto' in df.columns else []
sel_proj = st.sidebar.selectbox("Proyecto", proj_opts)

agrup_opts = ['Todas'] + sorted(list(df['Agrupacion'].unique())) if 'Agrupacion' in df.columns else []
sel_agrup = st.sidebar.selectbox("Agrupación / Canal", agrup_opts)

# Aplicar Filtros
df_f = df.copy()
if sel_city != 'Todas': df_f = df_f[df_f['Ciudad'] == sel_city]
if sel_proj != 'Todos': df_f = df_f[df_f['MacroProyecto'] == sel_proj]
if sel_agrup != 'Todas': df_f = df_f[df_f['Agrupacion'] == sel_agrup]

# Feedback visual de filtrado
st.sidebar.success(f"✅ Visualizando {len(df_f):,} registros")

# ══════════════════════════════════════════════════════════════════════════════
# 5. KPI CARDS (DISEÑO VIP)
# ══════════════════════════════════════════════════════════════════════════════

# Cálculos
total_sales = df_f['ValorNeto'].sum() if 'ValorNeto' in df_f.columns else 0
tx_count = len(df_f)
avg_ticket = total_sales / tx_count if tx_count > 0 else 0
top_city = df_f.groupby('Ciudad')['ValorNeto'].sum().idxmax() if 'Ciudad' in df_f.columns and not df_f.empty else "N/A"

col1, col2, col3, col4 = st.columns(4)

def render_kpi(title, val, badge, col):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-badge">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

render_kpi("VENTAS TOTALES (NETO)", format_currency_cop(total_sales), "Ingreso Real", col1)
render_kpi("UNIDADES VENDIDAS", f"{tx_count:,.0f}", "Transacciones", col2)
render_kpi("TICKET PROMEDIO", format_currency_cop(avg_ticket), "Eficiencia", col3)
render_kpi("PLAZA LÍDER", top_city, "Mayor Volumen", col4)

# ══════════════════════════════════════════════════════════════════════════════
# 6. STORYTELLING VISUAL (GRÁFICOS CON MARCA)
# ══════════════════════════════════════════════════════════════════════════════

# --- SECCIÓN A: SANKEY (FLUJO DE DINERO) ---
st.markdown("""
<div class="section-divider">
    <div class="section-icon">🕸️</div>
    <div class="section-title">Alineación Estratégica: Mercadeo a Ventas</div>
</div>
""", unsafe_allow_html=True)

if 'Agrupacion' in df_f.columns and 'Medio' in df_f.columns:
    with st.container():
        # Lógica de Sankey
        # 1. Agrupar Data Nivel 1 (Agrupación -> Medio)
        sankey_data_1 = df_f.groupby(['Agrupacion', 'Medio'])['ValorNeto'].sum().reset_index()
        sankey_data_1.columns = ['Source', 'Target', 'Value']
        
        # 2. Agrupar Data Nivel 2 (Medio -> Proyecto Top 10)
        top_projects = df_f.groupby('MacroProyecto')['ValorNeto'].sum().nlargest(10).index
        sankey_data_2 = df_f[df_f['MacroProyecto'].isin(top_projects)].groupby(['Medio', 'MacroProyecto'])['ValorNeto'].sum().reset_index()
        sankey_data_2.columns = ['Source', 'Target', 'Value']
        
        links = pd.concat([sankey_data_1, sankey_data_2], axis=0)
        
        # Mapeo Nodos
        all_labels = list(pd.unique(links[['Source', 'Target']].values.ravel('K')))
        mapping = {k: v for v, k in enumerate(all_labels)}
        links['Source'] = links['Source'].map(mapping)
        links['Target'] = links['Target'].map(mapping)
        
        # Colores Nodos (Forzando Paleta Conaltura)
        node_colors = [COLORS['primary'] for _ in all_labels]
        
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20, thickness=15, line=dict(color="white", width=0.5),
                label=all_labels, color=node_colors
            ),
            link=dict(
                source=links['Source'], target=links['Target'], value=links['Value'],
                color='rgba(18, 81, 96, 0.2)' # Enlaces Verde Petróleo Transparente
            )
        )])
        
        fig_sankey.update_layout(
            height=500, margin=dict(l=0,r=0,t=20,b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins")
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

# --- SECCIÓN B: ANÁLISIS TÁCTICO ---
c_left, c_right = st.columns([1, 1])

with c_left:
    st.markdown("""
    <div class="section-divider">
        <div class="section-icon">🏆</div>
        <div class="section-title">Ranking Ciudades</div>
    </div>
    """, unsafe_allow_html=True)
    
    if 'Ciudad' in df_f.columns:
        city_data = df_f.groupby('Ciudad')['ValorNeto'].sum().sort_values(ascending=True)
        
        fig_bar = px.bar(
            city_data, orientation='h', 
            text_auto='.2s',
            color_discrete_sequence=[COLORS['primary']] # Verde Conaltura
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins"),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(title=None)
        )
        # Pintar la barra más alta de Naranja (Accent)
        fig_bar.update_traces(marker_color=COLORS['primary'], marker_line_width=0)
        st.plotly_chart(fig_bar, use_container_width=True)

with c_right:
    st.markdown("""
    <div class="section-divider">
        <div class="section-icon">📢</div>
        <div class="section-title">Mix de Canales</div>
    </div>
    """, unsafe_allow_html=True)
    
    if 'Agrupacion' in df_f.columns:
        pie_data = df_f.groupby('Agrupacion')['ValorNeto'].sum().reset_index()
        
        # Mapeo de colores estricto
        pie_data['Color'] = pie_data['Agrupacion'].map(CANAL_COLOR_MAP).fillna(COLORS['secondary'])
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=pie_data['Agrupacion'], 
            values=pie_data['ValorNeto'],
            hole=.6,
            marker=dict(colors=pie_data['Color']), # Usar colores mapeados
            textinfo='percent+label',
            showlegend=False
        )])
        
        fig_pie.update_layout(
            height=350, margin=dict(l=20,r=20,t=20,b=20),
            font=dict(family="Poppins")
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7. TABLA DE DETALLE (ENTERPRISE GRID)
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-divider">
    <div class="section-icon">📋</div>
    <div class="section-title">Detalle de Ejecución por Proyecto</div>
</div>
""", unsafe_allow_html=True)

if 'MacroProyecto' in df_f.columns:
    # Agrupación para la tabla
    table_data = df_f.groupby('MacroProyecto').agg(
        Ciudad=('Ciudad', 'first'),
        Ventas=('ValorNeto', 'sum'),
        Unidades=('ValorNeto', 'count'), # Asumiendo conteo de registros
        Ticket=('ValorNeto', 'mean')
    ).reset_index().sort_values('Ventas', ascending=False)
    
    st.dataframe(
        table_data,
        column_config={
            "MacroProyecto": st.column_config.TextColumn("Proyecto", width="medium"),
            "Ciudad": st.column_config.TextColumn("Plaza", width="small"),
            "Ventas": st.column_config.ProgressColumn(
                "Volumen Total",
                format="$%d",
                min_value=0,
                max_value=int(table_data['Ventas'].max()),
                width="large"
            ),
            "Unidades": st.column_config.NumberColumn("Unds", format="%d"),
            "Ticket": st.column_config.NumberColumn("Ticket Prom.", format="$%d")
        },
        hide_index=True,
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# 8. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
col_f1, col_f2 = st.columns([1, 1])
with col_f1:
    st.caption("© 2025 CONALTURA - Construcción y Vivienda | Reporte Confidencial")
with col_f2:
    st.caption(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
