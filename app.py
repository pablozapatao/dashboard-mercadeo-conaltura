"""
CONALTURA - DASHBOARD EJECUTIVO 2025
Gran Convención de Ventas
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Conaltura | Dashboard Ejecutivo 2025",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# COLORES
# ══════════════════════════════════════════════════════════════════════════════

TEAL = '#125160'
LIME = '#DBFF69'
CORAL = '#FF795A'
LILAC = '#B382FF'
CYAN = '#00D4AA'
GOLD = '#FFB800'

AGRUPACION_COLORS = {
    'Ventas Digitales': '#00D4AA',
    'Ventas Tradicionales': '#125160',
    'Ventas Referidos': '#B382FF',
    'Ventas Ferias': '#FF795A',
    'Ventas Recompra': '#FFB800',
    'Ventas Colaboradores': '#4A90D9',
    'Ventas Aliados': '#FF6B9D',
    'Ventas Canjes': '#DBFF69',
    'Ventas Empresas': '#8B5CF6',
    'Eventos Internacionales': '#EC4899',
}

CIUDAD_COLORS = {
    'Medellín': '#125160',
    'Barranquilla': '#FF795A',
    'Bogotá': '#B382FF',
    'Cali': '#00D4AA',
    'Cartagena': '#FFB800',
}

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: #F8FAFC !important; }
    .main .block-container { padding: 1rem 2rem !important; max-width: 1600px; }
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    div[data-testid="stMetric"] {
        background: white;
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 20px rgba(18, 81, 96, 0.08);
    }
    div[data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #125160 !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: white; padding: 8px; border-radius: 12px; }
    .stTabs [aria-selected="true"] { background: #125160 !important; color: #DBFF69 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES
# ══════════════════════════════════════════════════════════════════════════════

def format_cop(value):
    if pd.isna(value) or value == 0:
        return "$0"
    return f"${value:,.0f}".replace(",", ".")

def format_short(value):
    if pd.isna(value) or value == 0:
        return "$0"
    abs_val = abs(value)
    if abs_val >= 1_000_000_000_000:
        return f"${value/1_000_000_000_000:.2f}B"
    elif abs_val >= 1_000_000_000:
        return f"${value/1_000_000_000:.1f}MM"
    elif abs_val >= 1_000_000:
        return f"${value/1_000_000:.0f}M"
    elif abs_val >= 1_000:
        return f"${value/1_000:.0f}K"
    return f"${value:.0f}"

def format_num(value):
    if pd.isna(value) or value == 0:
        return "0"
    return f"{int(value):,}".replace(",", ".")

def get_color(name, color_dict):
    return color_dict.get(name, '#64748B')

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            sep = ';' if ';' in content[:1000] else ','
            df = pd.read_csv(uploaded_file, sep=sep)
        else:
            df = pd.read_excel(uploaded_file)
        
        df.columns = df.columns.str.strip()
        
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.month
        
        if 'Valor Neto' in df.columns:
            df['Valor Neto'] = pd.to_numeric(df['Valor Neto'], errors='coerce').fillna(0)
        
        for col in ['MacroProyecto', 'Medio Publicitario', 'Ciudad', 'Agrupación']:
            if col in df.columns:
                df[col] = df[col].fillna('Sin Definir').astype(str).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0 1.5rem 0; border-bottom:2px solid rgba(219,255,105,0.3); margin-bottom:1.5rem;">
        <div style="font-size:1.4rem; font-weight:800; color:{TEAL};">
            con<span style="background:{TEAL}; color:{LIME}; padding:2px 6px; border-radius:4px;">altura</span>
        </div>
        <div style="font-size:0.7rem; color:#64748B; margin-top:4px;">Dashboard Ejecutivo 2025</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 CARGAR DATOS", type=['csv', 'xlsx', 'xls'])
    
    filter_ciudad = 'Todas'
    filter_agrupacion = 'Todas'

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem;">
        <h1 style="margin:0; font-size:2rem; font-weight:800; color:{TEAL};">Dashboard Ejecutivo</h1>
        <span style="background:{CORAL}; color:white; padding:6px 14px; border-radius:20px; font-size:0.75rem; font-weight:700;">
            🎯 Gran Convención 2025
        </span>
    </div>
    <p style="margin:0; color:#64748B; font-size:0.9rem;">Análisis integral de ventas por agrupación, ciudad y proyecto</p>
    """, unsafe_allow_html=True)

with col2:
    if Path('logo.png').exists():
        st.image('logo.png', width=140)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIN DATOS
# ══════════════════════════════════════════════════════════════════════════════

if uploaded_file is None:
    st.markdown(f"""
    <div style="text-align:center; padding:4rem 2rem; background:white; border-radius:20px; border:1px solid #E2E8F0; max-width:550px; margin:3rem auto;">
        <div style="font-size:4rem; margin-bottom:1.5rem;">📊</div>
        <h2 style="color:{TEAL}; margin-bottom:0.5rem; font-weight:800;">Bienvenido</h2>
        <p style="color:#64748B; font-size:1rem; margin-bottom:2rem;">Carga la Sabana de Datos de Mercadeo para visualizar el análisis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# CARGAR DATOS
# ══════════════════════════════════════════════════════════════════════════════

df = load_data(uploaded_file)

if df is None or df.empty:
    st.error("No se pudieron cargar los datos")
    st.stop()

required_cols = ['MacroProyecto', 'Valor Neto', 'Ciudad', 'Agrupación']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Faltan columnas: {missing}")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# FILTROS
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("---")
    ciudades = ['Todas'] + sorted(df['Ciudad'].unique().tolist())
    filter_ciudad = st.selectbox("🏙️ Ciudad", ciudades)
    
    agrupaciones = ['Todas'] + sorted(df['Agrupación'].unique().tolist())
    filter_agrupacion = st.selectbox("📢 Agrupación", agrupaciones)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background:{TEAL}; padding:1rem; border-radius:12px; text-align:center;">
        <p style="color:{LIME}; font-size:0.7rem; font-weight:700; margin:0;">REGISTROS</p>
        <p style="color:white; font-size:1.5rem; font-weight:800; margin:0;">{format_num(len(df))}</p>
    </div>
    """, unsafe_allow_html=True)

df_f = df.copy()
if filter_ciudad != 'Todas':
    df_f = df_f[df_f['Ciudad'] == filter_ciudad]
if filter_agrupacion != 'Todas':
    df_f = df_f[df_f['Agrupación'] == filter_agrupacion]

if df_f.empty:
    st.warning("No hay datos para los filtros seleccionados")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════════════════════

total_ventas = df_f['Valor Neto'].sum()
total_unidades = len(df_f)
ticket = total_ventas / total_unidades if total_unidades > 0 else 0
n_proyectos = df_f['MacroProyecto'].nunique()
n_agrupaciones = df_f['Agrupación'].nunique()
n_ciudades = df_f['Ciudad'].nunique()

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("💰 VENTA TOTAL", format_short(total_ventas), format_cop(total_ventas))
with k2:
    st.metric("🏠 UNIDADES", format_num(total_unidades), "Inmuebles")
with k3:
    st.metric("📈 TICKET", format_short(ticket), "Promedio")
with k4:
    st.metric("🏗️ PROYECTOS", n_proyectos, "Activos")
with k5:
    st.metric("📢 AGRUPACIONES", n_agrupaciones, "Canales")
with k6:
    st.metric("🌎 CIUDADES", n_ciudades, "Operación")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📊 PANORAMA", "📢 AGRUPACIONES", "🏗️ PROYECTOS"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: PANORAMA
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**🏆 Ranking de Ciudades**")
        
        city_data = df_f.groupby('Ciudad').agg({'Valor Neto': 'sum'}).reset_index()
        city_data['Unidades'] = df_f.groupby('Ciudad').size().values
        city_data = city_data.sort_values('Valor Neto', ascending=True)
        
        colors_ventas = [get_color(c, CIUDAD_COLORS) for c in city_data['Ciudad']]
        colors_uds = ['rgba(18,81,96,0.5)' for _ in city_data['Ciudad']]
        
        fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                           subplot_titles=('Ventas ($)', 'Unidades (#)'),
                           horizontal_spacing=0.02)
        
        fig.add_trace(go.Bar(
            y=city_data['Ciudad'].tolist(),
            x=city_data['Valor Neto'].tolist(),
            orientation='h',
            marker_color=colors_ventas,
            text=[format_short(v) for v in city_data['Valor Neto']],
            textposition='outside',
            showlegend=False
        ), row=1, col=1)
        
        fig.add_trace(go.Bar(
            y=city_data['Ciudad'].tolist(),
            x=city_data['Unidades'].tolist(),
            orientation='h',
            marker_color=colors_uds,
            text=[str(int(u)) for u in city_data['Unidades']],
            textposition='outside',
            showlegend=False
        ), row=1, col=2)
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=50, t=30, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_xaxes(showgrid=False, showticklabels=False)
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"**📈 Evolución Mensual**")
        
        if 'Mes' in df_f.columns:
            meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            monthly_ventas = df_f.groupby('Mes')['Valor Neto'].sum().reindex(range(1, 13), fill_value=0)
            monthly_uds = df_f.groupby('Mes').size().reindex(range(1, 13), fill_value=0)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=monthly_ventas.tolist(),
                mode='lines+markers',
                fill='tozeroy',
                name='Ventas ($)',
                line=dict(color=CORAL, width=3),
                fillcolor='rgba(255, 121, 90, 0.2)',
                marker=dict(size=8, color=CORAL)
            ), secondary_y=False)
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=monthly_uds.tolist(),
                mode='lines+markers',
                name='Unidades (#)',
                line=dict(color=TEAL, width=3, dash='dot'),
                marker=dict(size=8, color=TEAL, symbol='square')
            ), secondary_y=True)
            
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=10, b=10),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)', tickformat='$.2s', secondary_y=False)
            fig.update_yaxes(showgrid=False, secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Se requiere columna 'Fecha'")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: AGRUPACIONES
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown(f"**📢 Distribución por Agrupación**")
    
    agrup_data = df_f.groupby('Agrupación').agg({'Valor Neto': 'sum'}).reset_index()
    agrup_data['Unidades'] = df_f.groupby('Agrupación').size().values
    agrup_data['Ticket'] = agrup_data['Valor Neto'] / agrup_data['Unidades']
    agrup_data['PctVentas'] = (agrup_data['Valor Neto'] / agrup_data['Valor Neto'].sum() * 100).round(1)
    agrup_data['PctUds'] = (agrup_data['Unidades'] / agrup_data['Unidades'].sum() * 100).round(1)
    agrup_data = agrup_data.sort_values('Valor Neto', ascending=False)
    
    colors = [get_color(a, AGRUPACION_COLORS) for a in agrup_data['Agrupación']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(go.Pie(
            labels=agrup_data['Agrupación'].tolist(),
            values=agrup_data['Valor Neto'].tolist(),
            hole=0.55,
            marker=dict(colors=colors),
            textinfo='percent+label',
            textposition='outside',
            textfont=dict(size=10)
        ))
        fig.add_annotation(
            text=f"<b>VENTAS</b><br>{format_short(agrup_data['Valor Neto'].sum())}", 
            x=0.5, y=0.5, font=dict(size=14, color=TEAL), showarrow=False
        )
        fig.update_layout(
            title='Participación en Ventas ($)',
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure(go.Pie(
            labels=agrup_data['Agrupación'].tolist(),
            values=agrup_data['Unidades'].tolist(),
            hole=0.55,
            marker=dict(colors=colors),
            textinfo='percent+label',
            textposition='outside',
            textfont=dict(size=10)
        ))
        fig.add_annotation(
            text=f"<b>UNIDADES</b><br>{format_num(agrup_data['Unidades'].sum())}", 
            x=0.5, y=0.5, font=dict(size=14, color=TEAL), showarrow=False
        )
        fig.update_layout(
            title='Participación en Unidades (#)',
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detalle
    st.markdown(f"**📋 Detalle por Agrupación**")
    
    for _, row in agrup_data.iterrows():
        color = get_color(row['Agrupación'], AGRUPACION_COLORS)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; padding:12px 16px; margin-bottom:8px; background:white; border-radius:12px; border-left:4px solid {color};">
            <div style="flex:1;"><div style="font-weight:700; color:#1E293B;">{row['Agrupación']}</div></div>
            <div style="text-align:center; padding:0 1rem; border-left:1px solid #E2E8F0;">
                <div style="font-size:0.7rem; color:#64748B;">VENTAS</div>
                <div style="font-weight:700; color:{TEAL};">{format_short(row['Valor Neto'])}</div>
                <div style="font-size:0.7rem; color:{CORAL};">{row['PctVentas']}%</div>
            </div>
            <div style="text-align:center; padding:0 1rem; border-left:1px solid #E2E8F0;">
                <div style="font-size:0.7rem; color:#64748B;">UNIDADES</div>
                <div style="font-weight:700; color:{TEAL};">{int(row['Unidades'])}</div>
                <div style="font-size:0.7rem; color:{CORAL};">{row['PctUds']}%</div>
            </div>
            <div style="text-align:center; padding:0 1rem; border-left:1px solid #E2E8F0;">
                <div style="font-size:0.7rem; color:#64748B;">TICKET</div>
                <div style="font-weight:700; color:{CORAL};">{format_short(row['Ticket'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ticket por agrupación
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**💵 Ticket Promedio por Agrupación**")
    
    agrup_sorted = agrup_data.sort_values('Ticket', ascending=True)
    colors_sorted = [get_color(a, AGRUPACION_COLORS) for a in agrup_sorted['Agrupación']]
    
    fig = go.Figure(go.Bar(
        y=agrup_sorted['Agrupación'].tolist(),
        x=agrup_sorted['Ticket'].tolist(),
        orientation='h',
        marker_color=colors_sorted,
        text=[f"{format_short(v)} ({int(u)} uds)" for v, u in zip(agrup_sorted['Ticket'], agrup_sorted['Unidades'])],
        textposition='outside'
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=150, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', tickformat='$.2s'),
        yaxis=dict(showgrid=False),
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: PROYECTOS
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    proy_data = df_f.groupby('MacroProyecto').agg({'Valor Neto': 'sum', 'Ciudad': 'first'}).reset_index()
    proy_data['Unidades'] = df_f.groupby('MacroProyecto').size().values
    proy_data['Ticket'] = proy_data['Valor Neto'] / proy_data['Unidades']
    proy_data = proy_data.sort_values('Valor Neto', ascending=False)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown(f"**🏆 Top 15 Proyectos por Ventas**")
        
        top15 = proy_data.head(15).sort_values('Valor Neto', ascending=True)
        
        fig = go.Figure(go.Bar(
            y=[p.strip() for p in top15['MacroProyecto']],
            x=top15['Valor Neto'].tolist(),
            orientation='h',
            marker_color=CORAL,
            text=[f"{format_short(v)} • {int(u)} uds" for v, u in zip(top15['Valor Neto'], top15['Unidades'])],
            textposition='outside'
        ))
        
        fig.update_layout(
            height=500,
            margin=dict(l=0, r=120, t=10, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"**📋 Detalle Top 10**")
        
        for i, (_, row) in enumerate(proy_data.head(10).iterrows()):
            rank = i + 1
            bg = CORAL if rank <= 3 else TEAL
            
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:10px; margin-bottom:8px; background:white; border-radius:10px; border:1px solid #E2E8F0;">
                <div style="width:30px; height:30px; background:{bg}; color:white; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:800;">{rank}</div>
                <div style="flex:1;">
                    <div style="font-weight:700; font-size:0.85rem; color:#1E293B;">{row['MacroProyecto'].strip()}</div>
                    <div style="font-size:0.7rem; color:#64748B;">📍 {row['Ciudad']} • 🏠 {int(row['Unidades'])} uds</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:800; color:{LIME}; background:{TEAL}; padding:4px 10px; border-radius:6px;">{format_short(row['Valor Neto'])}</div>
                    <div style="font-size:0.65rem; color:#64748B; margin-top:2px;">Ticket: {format_short(row['Ticket'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Unidades por proyecto
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**🏠 Top 15 por Unidades Vendidas**")
    
    proy_uds = proy_data.sort_values('Unidades', ascending=False).head(15)
    
    fig = go.Figure(go.Bar(
        x=[p.strip() for p in proy_uds['MacroProyecto']],
        y=proy_uds['Unidades'].tolist(),
        marker_color=TEAL,
        text=[str(int(u)) for u in proy_uds['Unidades']],
        textposition='outside'
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=20, b=80),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickangle=-35),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Unidades'),
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"**✨ Insights Ejecutivos**")

agrup_stats = df_f.groupby('Agrupación').agg({'Valor Neto': ['sum', 'count']})
agrup_stats.columns = ['Total', 'Count']
agrup_stats['Ticket'] = agrup_stats['Total'] / agrup_stats['Count']

i1, i2, i3, i4 = st.columns(4)

with i1:
    top_ticket_agrup = agrup_stats['Ticket'].idxmax()
    top_ticket_val = agrup_stats.loc[top_ticket_agrup, 'Ticket']
    st.markdown(f"""
    <div style="background:white; padding:1rem; border-radius:12px; border-left:4px solid {CYAN};">
        <div style="font-size:0.7rem; font-weight:700; color:{CYAN};">🌟 MAYOR TICKET</div>
        <p style="font-size:0.85rem; color:#64748B; margin:0.5rem 0 0 0;">
            <strong>{top_ticket_agrup}</strong>: <strong style="color:{CORAL};">{format_short(top_ticket_val)}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with i2:
    top_vol_agrup = agrup_stats['Count'].idxmax()
    top_vol_count = int(agrup_stats.loc[top_vol_agrup, 'Count'])
    st.markdown(f"""
    <div style="background:white; padding:1rem; border-radius:12px; border-left:4px solid {LIME};">
        <div style="font-size:0.7rem; font-weight:700; color:{TEAL};">📊 MAYOR VOLUMEN</div>
        <p style="font-size:0.85rem; color:#64748B; margin:0.5rem 0 0 0;">
            <strong>{top_vol_agrup}</strong>: <strong style="color:{CORAL};">{top_vol_count}</strong> uds
        </p>
    </div>
    """, unsafe_allow_html=True)

with i3:
    top_city = df_f.groupby('Ciudad')['Valor Neto'].sum().idxmax()
    city_pct = (df_f[df_f['Ciudad'] == top_city]['Valor Neto'].sum() / total_ventas * 100)
    st.markdown(f"""
    <div style="background:white; padding:1rem; border-radius:12px; border-left:4px solid {LILAC};">
        <div style="font-size:0.7rem; font-weight:700; color:{LILAC};">🌎 MERCADO LÍDER</div>
        <p style="font-size:0.85rem; color:#64748B; margin:0.5rem 0 0 0;">
            <strong>{top_city}</strong>: <strong style="color:{CORAL};">{city_pct:.1f}%</strong> ventas
        </p>
    </div>
    """, unsafe_allow_html=True)

with i4:
    top_proy = df_f.groupby('MacroProyecto')['Valor Neto'].sum().idxmax().strip()
    top_proy_val = df_f.groupby('MacroProyecto')['Valor Neto'].sum().max()
    st.markdown(f"""
    <div style="background:white; padding:1rem; border-radius:12px; border-left:4px solid {CORAL};">
        <div style="font-size:0.7rem; font-weight:700; color:{CORAL};">🏆 PROYECTO TOP</div>
        <p style="font-size:0.85rem; color:#64748B; margin:0.5rem 0 0 0;">
            <strong>{top_proy}</strong>: <strong style="color:{CORAL};">{format_short(top_proy_val)}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:1rem 0;">
    <p style="color:{TEAL}; font-weight:600;">Dashboard Ejecutivo • Gran Convención CONALTURA 2025</p>
    <p style="color:#64748B; font-size:0.8rem;">{format_num(len(df_f))} de {format_num(len(df))} registros</p>
</div>
""", unsafe_allow_html=True)
