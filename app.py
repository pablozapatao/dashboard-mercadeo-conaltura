"""
CONALTURA - Dashboard Ejecutivo 2025 (High-End Version)
Estilo: Antigravity / Corporate
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# 1. CONFIGURACIÓN ESTRATÉGICA
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Conaltura | Visión 2025",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta Corporativa Estricta (Manual de Marca)
COLORS = {
    'primary': '#125160',    # Verde Petróleo (Base)
    'accent': '#FF795A',     # Naranja Coral (Acción/Alerta)
    'highlight': '#DBFF69',  # Verde Lima (Digital/Éxito)
    'neutral': '#F8FAFC',    # Gris Humo (Fondo)
    'text': '#1E293B',       # Texto Oscuro
    'white': '#FFFFFF',
    'sankey_node': '#125160',
    'sankey_link': 'rgba(18, 81, 96, 0.2)' # Transparencia elegante
}

# ══════════════════════════════════════════════════════════════════════════════
# 2. INYECCIÓN DE ESTILO "LOVABLE" (CSS AVANZADO)
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Reset Global */
    * {{ font-family: 'Poppins', sans-serif !important; }}
    .stApp {{ background-color: {COLORS['neutral']} !important; }}
    
    /* Tarjetas Flotantes (Antigravity Effect) */
    .metric-card {{
        background: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 20px -2px rgba(18, 81, 96, 0.08); /* Sombra difusa corporativa */
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(18, 81, 96, 0.15);
    }}
    
    .metric-title {{ font-size: 0.85rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
    .metric-value {{ font-size: 2.2rem; color: {COLORS['primary']}; font-weight: 700; margin: 8px 0; }}
    .metric-delta {{ 
        font-size: 0.8rem; 
        color: {COLORS['accent']}; 
        background-color: rgba(255, 121, 90, 0.1); 
        padding: 4px 10px; 
        border-radius: 20px; 
        font-weight: 600;
        display: inline-block;
    }}
    
    /* Encabezados */
    h1, h2, h3 {{ color: {COLORS['primary']} !important; }}
    
    /* Ajustes finos de Streamlit */
    .block-container {{ padding-top: 2rem !important; }}
    div[data-testid="stExpander"] {{ border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border-radius: 12px; }}
    
    /* Ocultar elementos de sistema */
    #MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3. LÓGICA DE NEGOCIO Y DATOS
# ══════════════════════════════════════════════════════════════════════════════

def format_cop(value):
    """Formato Moneda Colombiana Ejecutivo"""
    if value >= 1e9: return f"${value/1e9:.2f} B"
    if value >= 1e6: return f"${value/1e6:.1f} M"
    return f"${value:,.0f}"

def load_data(file):
    """Carga y limpieza inteligente de datos"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, sep=None, engine='python')
        else:
            df = pd.read_excel(file)
            
        # Normalización de nombres de columnas (Para que no falle si cambia una mayúscula)
        col_map = {}
        for col in df.columns:
            c = col.lower().strip()
            if 'proyecto' in c: col_map[col] = 'Proyecto'
            elif 'medio' in c: col_map[col] = 'Medio'
            elif 'agrupación' in c or 'agrupacion' in c: col_map[col] = 'Agrupacion'
            elif 'valor' in c or 'neto' in c: col_map[col] = 'Ventas'
            elif 'ciudad' in c: col_map[col] = 'Ciudad'
            elif 'fecha' in c: col_map[col] = 'Fecha'
            
        df = df.rename(columns=col_map)
        
        # Limpieza de tipos de datos
        if 'Ventas' in df.columns: 
            df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')
            
        return df
    except Exception as e:
        return None

# ══════════════════════════════════════════════════════════════════════════════
# 4. INTERFAZ DE USUARIO (UI)
# ══════════════════════════════════════════════════════════════════════════════

# --- HEADER VIP ---
col_logo, col_header = st.columns([1, 6])

with col_logo:
    # Busca el logo, si no está usa un placeholder elegante
    if Path("logo.png").exists():
        st.image("logo.png", width=110)
    else:
        st.markdown(f"<div style='font-size:3rem; text-align:center;'>🏢</div>", unsafe_allow_html=True)

with col_header:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h1 style="margin:0; font-size:2.5rem; letter-spacing:-1px;">Tablero Comercial <span style="color:{COLORS['highlight']}; background-color:{COLORS['primary']}; padding:0 10px; border-radius:8px;">2025</span></h1>
        <p style="margin:0; color:#64748B; font-size:1rem;">Gran Convención de Ventas • Análisis de Alineación Mercadeo & Ventas</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("🎛️ Configuración")
    uploaded_file = st.file_uploader("Cargar Datos (Excel/CSV)", type=['xlsx', 'csv'])
    st.caption("Asegúrese de cargar la sábana 'Mercadeo 2025'")

if uploaded_file is None:
    # Pantalla de espera elegante
    st.info("👋 **Bienvenido, Equipo Conaltura.** Por favor cargue el archivo de datos en el panel lateral para iniciar la visualización.")
    st.stop()

df = load_data(uploaded_file)
if df is None:
    st.error("⚠️ Error en el archivo. Verifique el formato.")
    st.stop()

# --- FILTROS GLOBALES ---
with st.container():
    c1, c2, c3 = st.columns(3)
    ciudad_sel = c1.multiselect("📍 Filtrar Ciudad", options=df['Ciudad'].unique(), default=df['Ciudad'].unique())
    
    # Lógica segura para proyectos
    proyectos_opt = df['Proyecto'].unique() if 'Proyecto' in df.columns else []
    proyecto_sel = c2.multiselect("🏗️ Filtrar Proyecto", options=proyectos_opt)
    
    agrupacion_opt = df['Agrupacion'].unique() if 'Agrupacion' in df.columns else []
    agrupacion_sel = c3.multiselect("📢 Filtrar Agrupación", options=agrupacion_opt)

# Aplicar filtros
df_f = df.copy()
if ciudad_sel: df_f = df_f[df_f['Ciudad'].isin(ciudad_sel)]
if proyecto_sel: df_f = df_f[df_f['Proyecto'].isin(proyecto_sel)]
if agrupacion_sel: df_f = df_f[df_f['Agrupacion'].isin(agrupacion_sel)]

# --- SECCIÓN 1: BIG NUMBERS (TARJETAS PERSONALIZADAS) ---
st.markdown("### 🚀 Resultados Ejecutivos")

total_ventas = df_f['Ventas'].sum()
total_tx = len(df_f)
ticket_promedio = total_ventas / total_tx if total_tx > 0 else 0
top_plaza = df_f.groupby('Ciudad')['Ventas'].sum().idxmax() if not df_f.empty else "N/A"

col1, col2, col3, col4 = st.columns(4)

metrics_data = [
    ("Ventas Totales", format_cop(total_ventas), "Ingresos Netos"),
    ("Unidades Vendidas", f"{total_tx:,}", "Transacciones"),
    ("Ticket Promedio", format_cop(ticket_promedio), "Por Unidad"),
    ("Plaza Líder", top_plaza, "Mayor Volumen")
]

for col, (label, value, sub) in zip([col1, col2, col3, col4], metrics_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SECCIÓN 2: EL FLUJO DE ATRIBUCIÓN (SANKEY DIAGRAM) ---
# Esta es la pieza clave para Mercadeo vs Ventas
st.markdown("### 🕸️ Alineación Estratégica: El Viaje del Cliente")
st.caption("Visualización del flujo: **Estrategia (Agrupación)** ➔ **Canal (Medio)** ➔ **Conversión (Proyecto)**")

if 'Agrupacion' in df_f.columns and 'Medio' in df_f.columns:
    # Preparar datos para Sankey (Lógica compleja simplificada)
    # Paso 1: Agrupacion -> Medio
    df_l1 = df_f.groupby(['Agrupacion', 'Medio'])['Ventas'].sum().reset_index()
    df_l1.columns = ['Source', 'Target', 'Value']
    
    # Paso 2: Medio -> Proyecto (Filtramos Top 8 Proyectos para legibilidad)
    top_proyectos = df_f.groupby('Proyecto')['Ventas'].sum().nlargest(8).index
    df_l2 = df_f[df_f['Proyecto'].isin(top_proyectos)].groupby(['Medio', 'Proyecto'])['Ventas'].sum().reset_index()
    df_l2.columns = ['Source', 'Target', 'Value']
    
    links = pd.concat([df_l1, df_l2], axis=0)
    
    # Crear índices únicos para los nodos
    all_nodes = list(pd.unique(links[['Source', 'Target']].values.ravel('K')))
    mapping = {k: v for v, k in enumerate(all_nodes)}
    links['Source'] = links['Source'].map(mapping)
    links['Target'] = links['Target'].map(mapping)
    
    # Diagrama
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20, thickness=20, line=dict(color="white", width=0.5),
            label=all_nodes, 
            color=COLORS['primary'] # Todos los nodos en Verde Corporativo
        ),
        link=dict(
            source=links['Source'], target=links['Target'], value=links['Value'],
            color=COLORS['sankey_link'] # Enlaces con transparencia elegante
        )
    )])
    
    fig_sankey.update_layout(
        height=550, 
        font=dict(family="Poppins", size=12),
        margin=dict(l=10, r=10, t=30, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_sankey, use_container_width=True)

# --- SECCIÓN 3: DETALLE OPERATIVO (TABLA INTELIGENTE) ---
c1, c2 = st.columns([2, 1], gap="large")

with c1:
    st.markdown("### 🏆 Top Proyectos (Ranking & Eficiencia)")
    if 'Proyecto' in df_f.columns:
        # Preparamos data para la tabla
        df_table = df_f.groupby('Proyecto').agg(
            Ciudad=('Ciudad', 'first'),
            Ventas=('Ventas', 'sum'),
            Unidades=('Ventas', 'count')
        ).sort_values('Ventas', ascending=False).reset_index().head(10)
        
        # Tabla interactiva con Barras de Progreso (Look VIP)
        st.dataframe(
            df_table,
            column_config={
                "Proyecto": st.column_config.TextColumn("Desarrollo", width="medium"),
                "Ciudad": st.column_config.TextColumn("Plaza", width="small"),
                "Ventas": st.column_config.ProgressColumn(
                    "Volumen de Ventas (COP)",
                    format="$%d",
                    min_value=0,
                    max_value=df_table['Ventas'].max(),
                    width="large"
                ),
                "Unidades": st.column_config.NumberColumn("Unds", format="%d")
            },
            hide_index=True,
            use_container_width=True
        )

with c2:
    st.markdown("### 🌍 Distribución Geográfica")
    if 'Ciudad' in df_f.columns:
        df_geo = df_f.groupby('Ciudad')['Ventas'].sum().reset_index()
        
        fig_geo = px.bar(
            df_geo.sort_values('Ventas', ascending=True), 
            x='Ventas', y='Ciudad', 
            orientation='h',
            text_auto='.2s',
            color_discrete_sequence=[COLORS['primary']]
        )
        
        fig_geo.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        # Pintar la barra más grande de color Naranja (Accent)
        st.plotly_chart(fig_geo, use_container_width=True)

# Footer discreto
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#94A3B8; font-size:0.8rem;'>Conaltura Intelligence • Powered by Python & Streamlit</div>", unsafe_allow_html=True)
