"""
CONALTURA - Dashboard Ejecutivo 2025
Gran Convención de Ventas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Conaltura | Dashboard Ejecutivo",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# COLORES
# ══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'teal': '#125160',
    'lime': '#DBFF69',
    'coral': '#FF795A',
    'lilac': '#B382FF',
    'bg': '#F8FAFC',
    'card': '#FFFFFF',
    'text': '#1E293B',
    'muted': '#64748B',
    'border': '#E2E8F0',
}

CANAL_COLORS = {
    'DIGITAL': '#DBFF69',
    'RELACIONAMIENTO': '#125160',
    'EXPERIENCIA': '#B382FF',
    'EVENTOS': '#FF795A',
    'TRADICIONAL': '#A8D861',
    'OTROS': '#94A3B8',
}

GAMA_COLORS = {
    'VIS/Acceso': '#E8FFB0',
    'Media': '#DBFF69',
    'Alta': '#B382FF',
    'Premium': '#FF795A',
}

CIUDAD_COLORS = {
    'Medellín': '#125160',
    'Barranquilla': '#FF795A',
    'Bogotá': '#B382FF',
    'Cali': '#DBFF69',
    'Cartagena': '#E8FFB0',
}

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif !important; }
    
    .stApp { background-color: #F8FAFC !important; }
    
    .main .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1500px;
    }
    
    /* Ocultar elementos Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Cards */
    div[data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
    
    div[data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 0.8rem !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1E293B !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES
# ══════════════════════════════════════════════════════════════════════════════

def format_cop(value):
    """Formato completo COP"""
    if pd.isna(value) or value == 0:
        return "$0"
    return f"${value:,.0f}".replace(",", ".")

def format_short(value):
    """Formato corto"""
    if pd.isna(value) or value == 0:
        return "$0"
    if value >= 1e12:
        return f"${value/1e12:.2f}T"
    if value >= 1e9:
        return f"${value/1e9:.1f}B"
    if value >= 1e6:
        return f"${value/1e6:.0f}M"
    return f"${value/1e3:.0f}K"

def load_logo():
    """Cargar logo"""
    for path in ['logo.png', './logo.png']:
        if Path(path).exists():
            return path
    return None

def clean_df(df):
    """Limpiar y normalizar DataFrame"""
    # Normalizar nombres de columnas
    col_map = {}
    for col in df.columns:
        col_lower = col.lower().strip().replace(' ', '_')
        if 'proyecto' in col_lower:
            col_map[col] = 'MacroProyecto'
        elif 'medio' in col_lower and 'publicitario' in col_lower:
            col_map[col] = 'MedioPublicitario'
        elif 'macro' in col_lower and 'canal' in col_lower:
            col_map[col] = 'MacroCanal'
        elif 'canal' in col_lower or 'agrupacion' in col_lower or 'agrupación' in col_lower:
            col_map[col] = 'MacroCanal'
        elif 'valor' in col_lower or 'neto' in col_lower or 'venta' in col_lower:
            col_map[col] = 'ValorNeto'
        elif 'ciudad' in col_lower:
            col_map[col] = 'Ciudad'
        elif 'gama' in col_lower or 'segmento' in col_lower:
            col_map[col] = 'Gama'
        elif 'fecha' in col_lower:
            col_map[col] = 'Fecha'
    
    df = df.rename(columns=col_map)
    
    # Procesar columnas
    if 'ValorNeto' in df.columns:
        df['ValorNeto'] = pd.to_numeric(df['ValorNeto'], errors='coerce').fillna(0)
    
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df['Mes'] = df['Fecha'].dt.month
    
    # Limpiar strings
    for col in ['MacroProyecto', 'MedioPublicitario', 'Ciudad', 'MacroCanal', 'Gama']:
        if col in df.columns:
            df[col] = df[col].fillna('Sin Definir').astype(str).str.strip()
    
    return df

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📊 Panel de Control")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "📁 Cargar archivo de datos",
        type=['csv', 'xlsx', 'xls'],
        help="Sube tu archivo CSV o Excel"
    )
    
    # Variables para filtros
    filter_ciudad = 'Todas'
    filter_canal = 'Todos'
    filter_gama = 'Todas'

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════

col_logo, col_title = st.columns([1, 4])

with col_logo:
    logo_path = load_logo()
    if logo_path:
        st.image(logo_path, width=120)

with col_title:
    st.markdown(f"""
    <h1 style="margin:0; color:{COLORS['text']}; font-size:1.8rem;">
        con<span style="background:{COLORS['teal']}; color:{COLORS['lime']}; padding:0 4px; border-radius:4px;">altura</span>
    </h1>
    <p style="margin:0; color:{COLORS['muted']}; font-size:0.9rem;">
        Gran Convención de Ventas 2025 • Dashboard Ejecutivo
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SIN DATOS - PANTALLA DE BIENVENIDA
# ══════════════════════════════════════════════════════════════════════════════

if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center; padding:3rem; background:white; border-radius:16px; border:1px solid #E2E8F0; max-width:500px; margin:2rem auto;">
        <div style="font-size:3rem; margin-bottom:1rem;">📊</div>
        <h2 style="color:#1E293B; margin-bottom:0.5rem;">Dashboard Ejecutivo</h2>
        <p style="color:#64748B;">Carga tu archivo de datos desde el panel lateral para comenzar el análisis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Ver estructura de datos requerida"):
        st.markdown("""
        | Columna | Descripción | Ejemplo |
        |---------|-------------|---------|
        | MacroProyecto | Nombre del proyecto | VENTAS AMARA |
        | MedioPublicitario | Canal específico | INSTAGRAM |
        | MacroCanal | Agrupación | DIGITAL, RELACIONAMIENTO |
        | ValorNeto | Monto en COP | 235389706 |
        | Ciudad | Ubicación | Medellín |
        | Gama | Segmento | VIS/Acceso, Media, Alta, Premium |
        | Fecha | Fecha de venta | 2025-01-15 |
        """)
    
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# CARGAR DATOS
# ══════════════════════════════════════════════════════════════════════════════

try:
    if uploaded_file.name.endswith('.csv'):
        content = uploaded_file.read().decode('utf-8')
        uploaded_file.seek(0)
        sep = ';' if ';' in content[:1000] else ','
        df = pd.read_csv(uploaded_file, sep=sep)
    else:
        df = pd.read_excel(uploaded_file)
    
    df = clean_df(df)
    
except Exception as e:
    st.error(f"❌ Error al cargar el archivo: {str(e)}")
    st.stop()

if df.empty:
    st.error("❌ El archivo está vacío")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# FILTROS EN SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎯 Filtros")
    
    if 'Ciudad' in df.columns:
        ciudades = ['Todas'] + sorted(df['Ciudad'].unique().tolist())
        filter_ciudad = st.selectbox("Ciudad", ciudades)
    
    if 'MacroCanal' in df.columns:
        canales = ['Todos'] + sorted(df['MacroCanal'].unique().tolist())
        filter_canal = st.selectbox("Canal", canales)
    
    if 'Gama' in df.columns:
        gamas = ['Todas'] + sorted(df['Gama'].unique().tolist())
        filter_gama = st.selectbox("Gama", gamas)
    
    st.markdown("---")
    st.markdown(f"📊 **{len(df):,}** registros cargados")

# Aplicar filtros
df_f = df.copy()
if filter_ciudad != 'Todas' and 'Ciudad' in df_f.columns:
    df_f = df_f[df_f['Ciudad'] == filter_ciudad]
if filter_canal != 'Todos' and 'MacroCanal' in df_f.columns:
    df_f = df_f[df_f['MacroCanal'] == filter_canal]
if filter_gama != 'Todas' and 'Gama' in df_f.columns:
    df_f = df_f[df_f['Gama'] == filter_gama]

if df_f.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════════════════════

total_ventas = df_f['ValorNeto'].sum()
unidades = len(df_f)
ticket = total_ventas / unidades if unidades > 0 else 0
proyectos = df_f['MacroProyecto'].nunique() if 'MacroProyecto' in df_f.columns else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("💰 Venta Total", format_short(total_ventas), format_cop(total_ventas))

with kpi2:
    st.metric("🏠 Unidades", f"{unidades:,}", "Inmuebles vendidos")

with kpi3:
    st.metric("📈 Ticket Promedio", format_short(ticket), format_cop(ticket))

with kpi4:
    st.metric("🏗️ Proyectos", proyectos, "Proyectos activos")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FILA 1: CIUDADES + EVOLUCIÓN
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("### 🎯 Panorama General")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🏆 Ranking de Ciudades**")
    
    if 'Ciudad' in df_f.columns:
        city_data = df_f.groupby('Ciudad')['ValorNeto'].sum().sort_values(ascending=True).tail(6)
        colors = [CIUDAD_COLORS.get(c, '#94A3B8') for c in city_data.index]
        
        fig = go.Figure(go.Bar(
            y=city_data.index,
            x=city_data.values,
            orientation='h',
            marker_color=colors,
            text=[format_short(v) for v in city_data.values],
            textposition='outside',
            textfont=dict(size=11)
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=60, t=10, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            font=dict(family='Poppins')
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**📈 Evolución Mensual**")
    
    if 'Mes' in df_f.columns:
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        monthly = df_f.groupby('Mes')['ValorNeto'].sum().reindex(range(1, 13), fill_value=0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=meses,
            y=monthly.values,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color=COLORS['lime'], width=3),
            fillcolor='rgba(219, 255, 105, 0.3)',
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', tickformat='$.2s'),
            font=dict(family='Poppins')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Se requiere columna 'Fecha' para mostrar evolución")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 2: CANALES
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("### 📢 Inteligencia de Canales")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Participación por Canal**")
    
    if 'MacroCanal' in df_f.columns:
        canal_data = df_f.groupby('MacroCanal')['ValorNeto'].sum().sort_values(ascending=False)
        total = canal_data.sum()
        
        colors = [CANAL_COLORS.get(c, '#94A3B8') for c in canal_data.index]
        
        fig = go.Figure(go.Pie(
            labels=canal_data.index,
            values=canal_data.values,
            hole=0.6,
            marker=dict(colors=colors),
            textinfo='percent',
            textposition='outside',
            textfont=dict(size=11)
        ))
        
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='left',
                x=1.05,
                font=dict(size=10)
            ),
            font=dict(family='Poppins')
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Ticket Promedio por Canal**")
    
    if 'MacroCanal' in df_f.columns:
        ticket_data = df_f.groupby('MacroCanal').agg({'ValorNeto': ['sum', 'count']})
        ticket_data.columns = ['Total', 'Count']
        ticket_data['Ticket'] = ticket_data['Total'] / ticket_data['Count']
        ticket_data = ticket_data.sort_values('Ticket', ascending=False)
        
        colors = [CANAL_COLORS.get(c, '#94A3B8') for c in ticket_data.index]
        
        fig = go.Figure(go.Bar(
            x=ticket_data.index,
            y=ticket_data['Ticket'],
            marker_color=colors,
            text=[format_short(v) for v in ticket_data['Ticket']],
            textposition='outside',
            textfont=dict(size=9)
        ))
        
        fig.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickangle=-20, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', showticklabels=False),
            font=dict(family='Poppins'),
            bargap=0.3
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("**Distribución por Gama**")
    
    if 'Gama' in df_f.columns:
        gama_data = df_f.groupby('Gama')['ValorNeto'].sum().sort_values(ascending=False)
        
        colors = [GAMA_COLORS.get(g, '#94A3B8') for g in gama_data.index]
        
        fig = go.Figure(go.Pie(
            labels=gama_data.index,
            values=gama_data.values,
            hole=0.6,
            marker=dict(colors=colors),
            textinfo='percent',
            textposition='outside',
            textfont=dict(size=11)
        ))
        
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='left',
                x=1.05,
                font=dict(size=10)
            ),
            font=dict(family='Poppins')
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# FILA 3: MATRIZ + TOP PROYECTOS
# ══════════════════════════════════════════════════════════════════════════════

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Matriz Canal × Gama**")
    
    if 'MacroCanal' in df_f.columns and 'Gama' in df_f.columns:
        pivot = df_f.pivot_table(
            index='MacroCanal',
            columns='Gama',
            values='ValorNeto',
            aggfunc='sum',
            fill_value=0
        )
        
        # Ordenar por total
        pivot['_total'] = pivot.sum(axis=1)
        pivot = pivot.sort_values('_total', ascending=False).drop('_total', axis=1)
        
        gama_order = ['VIS/Acceso', 'Media', 'Alta', 'Premium']
        gamas_present = [g for g in gama_order if g in pivot.columns]
        
        fig = go.Figure()
        
        for gama in gamas_present:
            fig.add_trace(go.Bar(
                name=gama,
                x=pivot.index,
                y=pivot[gama],
                marker_color=GAMA_COLORS.get(gama, '#94A3B8')
            ))
        
        fig.update_layout(
            barmode='stack',
            height=320,
            margin=dict(l=0, r=0, t=10, b=50),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickangle=-20, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', tickformat='$.2s'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            font=dict(family='Poppins'),
            bargap=0.2
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**🏗️ Top 10 Proyectos**")
    
    if 'MacroProyecto' in df_f.columns:
        proy_data = df_f.groupby('MacroProyecto').agg({
            'ValorNeto': 'sum',
            'Ciudad': 'first'
        }).reset_index()
        proy_data['Unidades'] = df_f.groupby('MacroProyecto').size().values
        proy_data['Ticket'] = proy_data['ValorNeto'] / proy_data['Unidades']
        proy_data = proy_data.sort_values('ValorNeto', ascending=False).head(10)
        
        # Mostrar como tabla estilizada
        for i, row in proy_data.iterrows():
            rank = proy_data.index.get_loc(i) + 1
            nombre = row['MacroProyecto'].replace('VENTAS ', '')
            ciudad = row['Ciudad']
            uds = row['Unidades']
            ventas = format_short(row['ValorNeto'])
            ticket = format_short(row['Ticket'])
            
            bg_color = COLORS['coral'] if rank <= 3 else COLORS['teal']
            
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:8px; margin-bottom:6px; background:white; border-radius:8px; border:1px solid #E2E8F0;">
                <div style="width:28px; height:28px; background:{bg_color}; color:white; border-radius:6px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.8rem;">{rank}</div>
                <div style="flex:1;">
                    <div style="font-weight:600; font-size:0.85rem; color:#1E293B;">{nombre}</div>
                    <div style="font-size:0.7rem; color:#64748B;">{ciudad} • {uds} uds</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:700; font-size:0.85rem; color:{COLORS['lime']}; background:{COLORS['teal']}; padding:2px 8px; border-radius:4px;">{ventas}</div>
                    <div style="font-size:0.7rem; color:#64748B;">Ticket: {ticket}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("### ✨ Insights Clave")

ins1, ins2, ins3 = st.columns(3)

with ins1:
    if 'MacroCanal' in df_f.columns:
        canal_ticket = df_f.groupby('MacroCanal').agg({'ValorNeto': ['sum', 'count']})
        canal_ticket.columns = ['Total', 'Count']
        canal_ticket['Ticket'] = canal_ticket['Total'] / canal_ticket['Count']
        top_canal = canal_ticket['Ticket'].idxmax()
        top_val = canal_ticket.loc[top_canal, 'Ticket']
        
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                <div style="width:10px; height:10px; background:{COLORS['lime']}; border-radius:50%;"></div>
                <span style="font-size:0.75rem; font-weight:700; color:{COLORS['lime']};">CANAL ESTRELLA</span>
            </div>
            <p style="font-size:0.85rem; color:#64748B; margin:0;">
                <strong style="color:#1E293B;">{top_canal}</strong> genera el ticket promedio más alto con <strong style="color:#1E293B;">{format_short(top_val)}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

with ins2:
    if 'MacroCanal' in df_f.columns:
        low_canal = canal_ticket['Ticket'].idxmin()
        
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                <div style="width:10px; height:10px; background:{COLORS['coral']}; border-radius:50%;"></div>
                <span style="font-size:0.75rem; font-weight:700; color:{COLORS['coral']};">OPORTUNIDAD</span>
            </div>
            <p style="font-size:0.85rem; color:#64748B; margin:0;">
                <strong style="color:#1E293B;">{low_canal}</strong> tiene el ticket más bajo. Oportunidad de mejorar conversión.
            </p>
        </div>
        """, unsafe_allow_html=True)

with ins3:
    if 'Ciudad' in df_f.columns:
        top_ciudad = df_f.groupby('Ciudad')['ValorNeto'].sum().idxmax()
        n_proy = df_f[df_f['Ciudad'] == top_ciudad]['MacroProyecto'].nunique()
        
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                <div style="width:10px; height:10px; background:{COLORS['lilac']}; border-radius:50%;"></div>
                <span style="font-size:0.75rem; font-weight:700; color:{COLORS['lilac']};">MERCADO LÍDER</span>
            </div>
            <p style="font-size:0.85rem; color:#64748B; margin:0;">
                <strong style="color:#1E293B;">{top_ciudad}</strong> concentra el mayor volumen con <strong style="color:#1E293B;">{n_proy}</strong> proyectos activos.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:1rem 0;">
    <p style="font-size:0.8rem; color:#64748B; margin:0;">
        Dashboard Ejecutivo • Gran Convención de Ventas CONALTURA 2025<br>
        <span style="opacity:0.7;">Registros: {len(df_f):,} de {len(df):,}</span>
    </p>
</div>
""", unsafe_allow_html=True)
