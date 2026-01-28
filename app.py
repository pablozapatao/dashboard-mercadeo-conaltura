"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                    CONALTURA - DASHBOARD EJECUTIVO 2025                              ║
║                    Gran Convención de Ventas                                         ║
║                                                                                      ║
║  Principios BI aplicados:                                                           ║
║  • KPIs claros con contexto                                                         ║
║  • Participación % sobre el total                                                   ║
║  • Leyendas visibles y completas                                                    ║
║  • Análisis por canal, ciudad, proyecto y gama                                      ║
║  • Insights ejecutivos automáticos                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Conaltura | Dashboard Ejecutivo",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES - SISTEMA DE DISEÑO CONALTURA
# ══════════════════════════════════════════════════════════════════════════════════════

COLORS = {
    'teal': '#125160',
    'lime': '#DBFF69',
    'coral': '#FF795A',
    'lilac': '#B382FF',
    'lime_light': '#E8FFB0',
    'gray': '#94A3B8',
    'bg': '#F8FAFC',
    'card': '#FFFFFF',
    'text': '#1E293B',
    'text_muted': '#64748B',
    'border': '#E2E8F0',
    'success': '#10B981',
}

# Colores por MacroCanal
CANAL_COLORS = {
    'DIGITAL': '#DBFF69',
    'RELACIONAMIENTO': '#125160',
    'EXPERIENCIA': '#B382FF',
    'EVENTOS': '#FF795A',
    'TRADICIONAL': '#A8D861',
    'OTROS': '#94A3B8',
    'SIN DEFINIR': '#CBD5E1',
}

# Colores por Gama
GAMA_COLORS = {
    'VIS/Acceso': '#E8FFB0',
    'Media': '#DBFF69',
    'Alta': '#B382FF',
    'Premium': '#FF795A',
}

# Colores por Ciudad
CIUDAD_COLORS = {
    'Medellín': '#125160',
    'Barranquilla': '#FF795A',
    'Bogotá': '#B382FF',
    'Cali': '#DBFF69',
    'Cartagena': '#E8FFB0',
    'Sabaneta': '#A8D861',
    'Pereira': '#94A3B8',
}

# ══════════════════════════════════════════════════════════════════════════════════════
# CSS PROFESIONAL
# ══════════════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{ font-family: 'Poppins', sans-serif !important; }}
    
    .stApp {{ background-color: {COLORS['bg']} !important; }}
    
    .main .block-container {{
        padding: 1.5rem 2rem !important;
        max-width: 1600px;
    }}
    
    /* Header */
    .header-main {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 1.5rem 0;
        border-bottom: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
    }}
    
    .header-brand {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .header-title {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORS['text']};
        margin: 0;
    }}
    
    .header-title span {{
        color: {COLORS['lime']};
        background: {COLORS['teal']};
        padding: 0 0.3rem;
        border-radius: 4px;
    }}
    
    .header-subtitle {{
        font-size: 0.85rem;
        color: {COLORS['text_muted']};
        margin: 0;
    }}
    
    /* KPI Cards */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .kpi-card {{
        background: {COLORS['card']};
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid {COLORS['border']};
        position: relative;
        overflow: hidden;
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        filter: blur(40px);
        opacity: 0.3;
    }}
    
    .kpi-card.lime::before {{ background: {COLORS['lime']}; }}
    .kpi-card.lilac::before {{ background: {COLORS['lilac']}; }}
    .kpi-card.coral::before {{ background: {COLORS['coral']}; }}
    .kpi-card.teal::before {{ background: {COLORS['teal']}; }}
    
    .kpi-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }}
    
    .kpi-icon {{
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }}
    
    .kpi-icon.lime {{ background: rgba(219, 255, 105, 0.2); }}
    .kpi-icon.lilac {{ background: rgba(179, 130, 255, 0.2); }}
    .kpi-icon.coral {{ background: rgba(255, 121, 90, 0.2); }}
    .kpi-icon.teal {{ background: rgba(18, 81, 96, 0.15); }}
    
    .kpi-label {{
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {COLORS['text_muted']};
    }}
    
    .kpi-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {COLORS['text']};
        line-height: 1.2;
    }}
    
    .kpi-detail {{
        font-size: 0.75rem;
        color: {COLORS['text_muted']};
        margin-top: 0.25rem;
    }}
    
    /* Section */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    .section-icon {{
        font-size: 1.1rem;
    }}
    
    .section-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {COLORS['text']};
        margin: 0;
    }}
    
    /* Chart Card */
    .chart-card {{
        background: {COLORS['card']};
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid {COLORS['border']};
        height: 100%;
    }}
    
    .chart-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {COLORS['text']};
        margin-bottom: 0.25rem;
    }}
    
    .chart-subtitle {{
        font-size: 0.75rem;
        color: {COLORS['text_muted']};
        margin-bottom: 1rem;
    }}
    
    /* Legend inline */
    .legend-inline {{
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }}
    
    .legend-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
    }}
    
    .legend-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }}
    
    .legend-label {{
        color: {COLORS['text_muted']};
        flex: 1;
    }}
    
    .legend-value {{
        font-weight: 700;
        color: {COLORS['text']};
    }}
    
    /* Proyecto ranking */
    .proyecto-item {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.6rem 0.75rem;
        border-radius: 10px;
        transition: background 0.2s;
    }}
    
    .proyecto-item:hover {{
        background: {COLORS['bg']};
    }}
    
    .proyecto-rank {{
        width: 28px;
        height: 28px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        color: white;
        flex-shrink: 0;
    }}
    
    .proyecto-rank.top {{ background: {COLORS['coral']}; }}
    .proyecto-rank.normal {{ background: {COLORS['teal']}; }}
    
    .proyecto-info {{
        flex: 1;
        min-width: 0;
    }}
    
    .proyecto-name {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {COLORS['text']};
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    
    .proyecto-meta {{
        font-size: 0.7rem;
        color: {COLORS['text_muted']};
    }}
    
    .proyecto-values {{
        text-align: right;
        flex-shrink: 0;
    }}
    
    .proyecto-ventas {{
        font-size: 0.85rem;
        font-weight: 700;
        color: {COLORS['lime']};
        background: {COLORS['teal']};
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
    }}
    
    .proyecto-ticket {{
        font-size: 0.7rem;
        color: {COLORS['text_muted']};
        margin-top: 0.2rem;
    }}
    
    /* Insights */
    .insights-container {{
        background: rgba(18, 81, 96, 0.05);
        border: 1px solid rgba(18, 81, 96, 0.2);
        border-radius: 16px;
        padding: 1.25rem;
    }}
    
    .insight-card {{
        background: {COLORS['card']};
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid {COLORS['border']};
    }}
    
    .insight-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.7rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .insight-badge-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }}
    
    .insight-text {{
        font-size: 0.8rem;
        color: {COLORS['text_muted']};
        line-height: 1.5;
    }}
    
    .insight-text strong {{
        color: {COLORS['text']};
    }}
    
    /* Welcome */
    .welcome-box {{
        background: {COLORS['card']};
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        max-width: 500px;
        margin: 2rem auto;
        border: 1px solid {COLORS['border']};
    }}
    
    .welcome-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
    .welcome-title {{ font-size: 1.5rem; font-weight: 700; color: {COLORS['text']}; margin-bottom: 0.5rem; }}
    .welcome-text {{ color: {COLORS['text_muted']}; margin-bottom: 1.5rem; }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 1.5rem 0;
        border-top: 1px solid {COLORS['border']};
        margin-top: 2rem;
    }}
    
    .footer-text {{
        font-size: 0.75rem;
        color: {COLORS['text_muted']};
    }}
    
    /* Ocultar elementos Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Filtros */
    .stSelectbox > div > div {{
        background: {COLORS['card']} !important;
        border-radius: 10px !important;
    }}
    
    @media (max-width: 1200px) {{
        .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    
    @media (max-width: 768px) {{
        .kpi-grid {{ grid-template-columns: 1fr; }}
        .kpi-value {{ font-size: 1.5rem; }}
    }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# FUNCIONES UTILIDAD
# ══════════════════════════════════════════════════════════════════════════════════════

def format_cop(value):
    """Formato completo COP"""
    try:
        if pd.isna(value) or value == 0:
            return "$0"
        return f"${value:,.0f}".replace(",", ".")
    except:
        return "$0"

def format_cop_short(value):
    """Formato corto para KPIs"""
    try:
        if pd.isna(value) or value == 0:
            return "$0"
        if value >= 1_000_000_000_000:
            return f"${value/1_000_000_000_000:.2f}T"
        if value >= 1_000_000_000:
            return f"${value/1_000_000_000:.1f}B"
        if value >= 1_000_000:
            return f"${value/1_000_000:.0f}M"
        return f"${value/1_000:.0f}K"
    except:
        return "$0"

def get_logo_base64():
    """Cargar logo"""
    for path in ['logo.png', './logo.png']:
        if Path(path).exists():
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

def clean_columns(df):
    """Normaliza columnas"""
    mapping = {
        'macroproyecto': 'MacroProyecto',
        'macro_proyecto': 'MacroProyecto',
        'proyecto': 'MacroProyecto',
        'medio_publicitario': 'MedioPublicitario',
        'mediopublicitario': 'MedioPublicitario',
        'medio': 'MedioPublicitario',
        'canal': 'MedioPublicitario',
        'valor_neto': 'ValorNeto',
        'valorneto': 'ValorNeto',
        'valor': 'ValorNeto',
        'ventas': 'ValorNeto',
        'ciudad': 'Ciudad',
        'fecha': 'Fecha',
        'mes': 'Mes',
        'macrocanal': 'MacroCanal',
        'macro_canal': 'MacroCanal',
        'agrupacion': 'MacroCanal',
        'agrupación': 'MacroCanal',
        'gama': 'Gama',
        'segmento': 'Gama',
    }
    
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    df = df.rename(columns=mapping)
    return df

def load_data(uploaded_file):
    """Carga datos"""
    try:
        if uploaded_file.name.endswith('.csv'):
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            sep = ';' if ';' in content[:1000] else ','
            df = pd.read_csv(uploaded_file, sep=sep)
        else:
            df = pd.read_excel(uploaded_file)
        
        df = clean_columns(df)
        
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.month
        
        if 'ValorNeto' in df.columns:
            df['ValorNeto'] = pd.to_numeric(df['ValorNeto'], errors='coerce').fillna(0)
        
        for col in ['MacroProyecto', 'MedioPublicitario', 'Ciudad', 'MacroCanal', 'Gama']:
            if col in df.columns:
                df[col] = df[col].fillna('Sin Definir').astype(str).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# ══════════════════════════════════════════════════════════════════════════════════════
# COMPONENTES
# ══════════════════════════════════════════════════════════════════════════════════════

def render_header():
    """Header con logo"""
    logo_b64 = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:50px;">' if logo_b64 else ''
    
    st.markdown(f"""
    <div class="header-main">
        <div class="header-brand">
            {logo_html}
            <div>
                <h1 class="header-title">con<span>altura</span></h1>
                <p class="header-subtitle">Gran Convención de Ventas 2025 • Dashboard Ejecutivo</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(df):
    """KPIs principales"""
    total_ventas = df['ValorNeto'].sum()
    unidades = len(df)
    ticket = total_ventas / unidades if unidades > 0 else 0
    proyectos = df['MacroProyecto'].nunique() if 'MacroProyecto' in df.columns else 0
    
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card lime">
            <div class="kpi-header">
                <div class="kpi-icon lime">💰</div>
                <span class="kpi-label">Venta Total</span>
            </div>
            <div class="kpi-value">{format_cop_short(total_ventas)}</div>
            <div class="kpi-detail">{format_cop(total_ventas)}</div>
        </div>
        <div class="kpi-card lilac">
            <div class="kpi-header">
                <div class="kpi-icon lilac">🏠</div>
                <span class="kpi-label">Unidades</span>
            </div>
            <div class="kpi-value">{unidades:,}</div>
            <div class="kpi-detail">Inmuebles vendidos</div>
        </div>
        <div class="kpi-card coral">
            <div class="kpi-header">
                <div class="kpi-icon coral">📈</div>
                <span class="kpi-label">Ticket Promedio</span>
            </div>
            <div class="kpi-value">{format_cop_short(ticket)}</div>
            <div class="kpi-detail">{format_cop(ticket)}</div>
        </div>
        <div class="kpi-card teal">
            <div class="kpi-header">
                <div class="kpi-icon teal">🏗️</div>
                <span class="kpi-label">Proyectos</span>
            </div>
            <div class="kpi-value">{proyectos}</div>
            <div class="kpi-detail">Proyectos activos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_welcome():
    """Pantalla bienvenida"""
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-icon">📊</div>
        <h2 class="welcome-title">Dashboard Ejecutivo</h2>
        <p class="welcome-text">Carga tu archivo de datos para visualizar el análisis de ventas por canal, ciudad y proyecto.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Estructura de datos"):
        st.markdown("""
        | Columna | Descripción |
        |---------|-------------|
        | MacroProyecto | Nombre del proyecto |
        | MedioPublicitario | Canal específico |
        | MacroCanal | Agrupación (DIGITAL, RELACIONAMIENTO, etc.) |
        | ValorNeto | Monto en COP |
        | Ciudad | Ubicación |
        | Gama | Segmento (VIS/Acceso, Media, Alta, Premium) |
        | Fecha | Fecha de la venta |
        """)

# ══════════════════════════════════════════════════════════════════════════════════════
# GRÁFICOS BI
# ══════════════════════════════════════════════════════════════════════════════════════

def chart_ranking_ciudades(df):
    """Ranking de ciudades - barras horizontales"""
    data = df.groupby('Ciudad')['ValorNeto'].sum().sort_values(ascending=True).tail(6)
    
    colors = [CIUDAD_COLORS.get(c, COLORS['gray']) for c in data.index]
    
    fig = go.Figure(go.Bar(
        y=data.index,
        x=data.values,
        orientation='h',
        marker=dict(color=colors, cornerradius=6),
        text=[format_cop_short(v) for v in data.values],
        textposition='outside',
        textfont=dict(size=11, color=COLORS['text'], family='Poppins'),
        hovertemplate='<b>%{y}</b><br>Ventas: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=60, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color=COLORS['text'], family='Poppins')),
        font=dict(family='Poppins')
    )
    
    return fig

def chart_evolucion_mensual(df):
    """Evolución mensual - área"""
    if 'Mes' not in df.columns:
        return None
    
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    monthly = df.groupby('Mes')['ValorNeto'].sum().reindex(range(1, 13), fill_value=0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=meses,
        y=monthly.values,
        mode='lines',
        fill='tozeroy',
        line=dict(color=COLORS['lime'], width=3),
        fillcolor='rgba(219, 255, 105, 0.3)',
        hovertemplate='<b>%{x}</b><br>Ventas: %{customdata}<extra></extra>',
        customdata=[format_cop_short(v) for v in monthly.values]
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color=COLORS['text_muted'], family='Poppins')),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', tickformat='$.2s', 
                   tickfont=dict(size=10, color=COLORS['text_muted'], family='Poppins')),
        font=dict(family='Poppins')
    )
    
    return fig

def chart_participacion_canal(df):
    """Participación por canal - donut"""
    if 'MacroCanal' not in df.columns:
        return None, []
    
    data = df.groupby('MacroCanal')['ValorNeto'].sum().sort_values(ascending=False)
    total = data.sum()
    
    colors = [CANAL_COLORS.get(c, COLORS['gray']) for c in data.index]
    
    fig = go.Figure(go.Pie(
        labels=data.index,
        values=data.values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family='Poppins')
    )
    
    # Datos para leyenda
    legend_data = []
    for canal, valor in data.items():
        pct = (valor / total * 100) if total > 0 else 0
        legend_data.append({
            'canal': canal,
            'valor': valor,
            'pct': pct,
            'color': CANAL_COLORS.get(canal, COLORS['gray'])
        })
    
    return fig, legend_data

def chart_ticket_por_canal(df):
    """Ticket promedio por canal"""
    if 'MacroCanal' not in df.columns:
        return None
    
    data = df.groupby('MacroCanal').agg({'ValorNeto': ['sum', 'count']}).reset_index()
    data.columns = ['MacroCanal', 'Total', 'Count']
    data['Ticket'] = data['Total'] / data['Count']
    data = data.sort_values('Ticket', ascending=False)
    
    colors = [CANAL_COLORS.get(c, COLORS['gray']) for c in data['MacroCanal']]
    
    fig = go.Figure(go.Bar(
        x=data['MacroCanal'],
        y=data['Ticket'],
        marker=dict(color=colors, cornerradius=6),
        text=[format_cop_short(v) for v in data['Ticket']],
        textposition='outside',
        textfont=dict(size=9, color=COLORS['text'], family='Poppins'),
        hovertemplate='<b>%{x}</b><br>Ticket: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        height=220,
        margin=dict(l=0, r=0, t=20, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color=COLORS['text_muted'], family='Poppins'), tickangle=-20),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', showticklabels=False),
        font=dict(family='Poppins'),
        bargap=0.3
    )
    
    return fig

def chart_distribucion_gama(df):
    """Distribución por gama - donut"""
    if 'Gama' not in df.columns:
        return None, []
    
    data = df.groupby('Gama')['ValorNeto'].sum().sort_values(ascending=False)
    total = data.sum()
    
    colors = [GAMA_COLORS.get(g, COLORS['gray']) for g in data.index]
    
    fig = go.Figure(go.Pie(
        labels=data.index,
        values=data.values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family='Poppins')
    )
    
    legend_data = []
    for gama, valor in data.items():
        pct = (valor / total * 100) if total > 0 else 0
        legend_data.append({
            'gama': gama,
            'valor': valor,
            'pct': pct,
            'color': GAMA_COLORS.get(gama, COLORS['gray'])
        })
    
    return fig, legend_data

def chart_matriz_canal_gama(df):
    """Matriz Canal × Gama - barras apiladas"""
    if 'MacroCanal' not in df.columns or 'Gama' not in df.columns:
        return None
    
    pivot = df.pivot_table(index='MacroCanal', columns='Gama', values='ValorNeto', aggfunc='sum', fill_value=0)
    
    # Ordenar canales por total
    totals = pivot.sum(axis=1).sort_values(ascending=False)
    pivot = pivot.loc[totals.index]
    
    gama_order = ['VIS/Acceso', 'Media', 'Alta', 'Premium']
    gamas_present = [g for g in gama_order if g in pivot.columns]
    
    fig = go.Figure()
    
    for gama in gamas_present:
        if gama in pivot.columns:
            fig.add_trace(go.Bar(
                name=gama,
                x=pivot.index,
                y=pivot[gama],
                marker_color=GAMA_COLORS.get(gama, COLORS['gray']),
                hovertemplate=f'<b>%{{x}}</b><br>{gama}: %{{y:,.0f}}<extra></extra>'
            ))
    
    fig.update_layout(
        barmode='stack',
        height=300,
        margin=dict(l=0, r=0, t=10, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color=COLORS['text_muted'], family='Poppins'), tickangle=-20),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', tickformat='$.2s',
                   tickfont=dict(size=10, color=COLORS['text_muted'], family='Poppins')),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=10, family='Poppins')
        ),
        font=dict(family='Poppins'),
        bargap=0.2
    )
    
    return fig

def render_legend(data, key_field, show_value=True):
    """Renderiza leyenda al lado del gráfico"""
    html = '<div class="legend-inline">'
    for item in data[:6]:
        label = item.get(key_field, '')
        pct = item.get('pct', 0)
        color = item.get('color', COLORS['gray'])
        html += f'''
        <div class="legend-item">
            <div class="legend-dot" style="background:{color}"></div>
            <span class="legend-label">{label}</span>
            <span class="legend-value">{pct:.1f}%</span>
        </div>
        '''
    html += '</div>'
    return html

def render_top_proyectos(df, n=10):
    """Top proyectos con ranking"""
    if 'MacroProyecto' not in df.columns:
        return ""
    
    data = df.groupby('MacroProyecto').agg({
        'ValorNeto': 'sum',
        'Ciudad': 'first'
    }).reset_index()
    data['Count'] = df.groupby('MacroProyecto').size().values
    data['Ticket'] = data['ValorNeto'] / data['Count']
    data = data.sort_values('ValorNeto', ascending=False).head(n)
    
    html = ''
    for i, row in data.iterrows():
        rank = data.index.get_loc(i) + 1
        nombre = row['MacroProyecto'].replace('VENTAS ', '').strip()
        ciudad = row['Ciudad']
        unidades = row['Count']
        ventas = format_cop_short(row['ValorNeto'])
        ticket = format_cop_short(row['Ticket'])
        rank_class = 'top' if rank <= 3 else 'normal'
        
        html += f'''
        <div class="proyecto-item">
            <div class="proyecto-rank {rank_class}">{rank}</div>
            <div class="proyecto-info">
                <div class="proyecto-name">{nombre}</div>
                <div class="proyecto-meta">{ciudad} • {unidades} uds</div>
            </div>
            <div class="proyecto-values">
                <div class="proyecto-ventas">{ventas}</div>
                <div class="proyecto-ticket">Ticket: {ticket}</div>
            </div>
        </div>
        '''
    
    return html

def render_insights(df):
    """Insights automáticos"""
    insights = []
    
    # Canal estrella (mayor ticket)
    if 'MacroCanal' in df.columns:
        canal_data = df.groupby('MacroCanal').agg({'ValorNeto': ['sum', 'count']})
        canal_data.columns = ['Total', 'Count']
        canal_data['Ticket'] = canal_data['Total'] / canal_data['Count']
        top_canal = canal_data['Ticket'].idxmax()
        top_ticket = canal_data.loc[top_canal, 'Ticket']
        
        insights.append({
            'badge': 'Canal Estrella',
            'color': COLORS['lime'],
            'text': f'<strong>{top_canal}</strong> genera el ticket promedio más alto con <strong>{format_cop_short(top_ticket)}</strong>'
        })
        
        # Canal oportunidad (menor ticket)
        low_canal = canal_data['Ticket'].idxmin()
        insights.append({
            'badge': 'Oportunidad',
            'color': COLORS['coral'],
            'text': f'<strong>{low_canal}</strong> tiene el ticket más bajo. Oportunidad de mejorar conversión.'
        })
    
    # Ciudad líder
    if 'Ciudad' in df.columns:
        ciudad_data = df.groupby('Ciudad')['ValorNeto'].sum()
        top_ciudad = ciudad_data.idxmax()
        n_proy = df[df['Ciudad'] == top_ciudad]['MacroProyecto'].nunique()
        
        insights.append({
            'badge': 'Mercado Líder',
            'color': COLORS['lilac'],
            'text': f'<strong>{top_ciudad}</strong> concentra el mayor volumen con <strong>{n_proy}</strong> proyectos activos.'
        })
    
    return insights

# ══════════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0; border-bottom:1px solid {COLORS['border']}; margin-bottom:1rem;">
        <span style="font-size:1.2rem; font-weight:700; color:{COLORS['text']};">⚙️ Filtros</span>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 Cargar datos", type=['csv', 'xlsx', 'xls'])
    
    filter_ciudad = None
    filter_canal = None
    filter_gama = None
    filter_mes = None
    
    if uploaded_file:
        df_temp = load_data(uploaded_file)
        if df_temp is not None:
            st.markdown("---")
            
            if 'Ciudad' in df_temp.columns:
                ciudades = ['Todas'] + sorted(df_temp['Ciudad'].unique().tolist())
                filter_ciudad = st.selectbox("🏙️ Ciudad", ciudades)
            
            if 'MacroCanal' in df_temp.columns:
                canales = ['Todos'] + sorted(df_temp['MacroCanal'].unique().tolist())
                filter_canal = st.selectbox("📢 Canal", canales)
            
            if 'Gama' in df_temp.columns:
                gamas = ['Todas'] + sorted(df_temp['Gama'].unique().tolist())
                filter_gama = st.selectbox("🎯 Gama", gamas)
            
            meses_opt = ['Todos', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            filter_mes = st.selectbox("📅 Mes", meses_opt)

# ══════════════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════════════

render_header()

if uploaded_file is None:
    render_welcome()
    st.stop()

df = load_data(uploaded_file)

if df is None or df.empty:
    st.error("❌ No se pudieron cargar los datos")
    st.stop()

# Aplicar filtros
df_filtered = df.copy()

if filter_ciudad and filter_ciudad != 'Todas':
    df_filtered = df_filtered[df_filtered['Ciudad'] == filter_ciudad]

if filter_canal and filter_canal != 'Todos':
    df_filtered = df_filtered[df_filtered['MacroCanal'] == filter_canal]

if filter_gama and filter_gama != 'Todas':
    df_filtered = df_filtered[df_filtered['Gama'] == filter_gama]

if filter_mes and filter_mes != 'Todos':
    meses_map = {'Ene':1,'Feb':2,'Mar':3,'Abr':4,'May':5,'Jun':6,'Jul':7,'Ago':8,'Sep':9,'Oct':10,'Nov':11,'Dic':12}
    if 'Mes' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Mes'] == meses_map.get(filter_mes)]

if df_filtered.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# KPIs
# ═══════════════════════════════════════════════════════════════════════════════

render_kpis(df_filtered)

# ═══════════════════════════════════════════════════════════════════════════════
# PANORAMA GENERAL
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <span class="section-icon">🎯</span>
    <h2 class="section-title">Panorama General</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">🏆 Ranking de Ciudades</div>
        <div class="chart-subtitle">Ventas totales por ubicación</div>
    """, unsafe_allow_html=True)
    
    fig = chart_ranking_ciudades(df_filtered)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">📈 Evolución Mensual</div>
        <div class="chart-subtitle">Comportamiento de ventas en el año</div>
    """, unsafe_allow_html=True)
    
    fig = chart_evolucion_mensual(df_filtered)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Se requiere columna 'Fecha'")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INTELIGENCIA DE CANALES
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-header" style="margin-top: 1.5rem;">
    <span class="section-icon">📢</span>
    <h2 class="section-title">Inteligencia de Canales</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Participación por Canal</div>
        <div class="chart-subtitle">% sobre venta total</div>
    """, unsafe_allow_html=True)
    
    fig_canal, legend_canal = chart_participacion_canal(df_filtered)
    if fig_canal:
        subcol1, subcol2 = st.columns([1.2, 1])
        with subcol1:
            st.plotly_chart(fig_canal, use_container_width=True, config={'displayModeBar': False})
        with subcol2:
            st.markdown(render_legend(legend_canal, 'canal'), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Ticket Promedio por Canal</div>
        <div class="chart-subtitle">¿Cuál canal trae clientes de mayor valor?</div>
    """, unsafe_allow_html=True)
    
    fig = chart_ticket_por_canal(df_filtered)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Distribución por Gama</div>
        <div class="chart-subtitle">Segmentación del mercado</div>
    """, unsafe_allow_html=True)
    
    fig_gama, legend_gama = chart_distribucion_gama(df_filtered)
    if fig_gama:
        subcol1, subcol2 = st.columns([1.2, 1])
        with subcol1:
            st.plotly_chart(fig_gama, use_container_width=True, config={'displayModeBar': False})
        with subcol2:
            st.markdown(render_legend(legend_gama, 'gama'), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MATRIZ Y TOP PROYECTOS
# ═══════════════════════════════════════════════════════════════════════════════

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card" style="margin-top: 1rem;">
        <div class="chart-title">📊 Matriz Canal × Gama</div>
        <div class="chart-subtitle">Cruce estratégico de canales y segmentos</div>
    """, unsafe_allow_html=True)
    
    fig = chart_matriz_canal_gama(df_filtered)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-card" style="margin-top: 1rem;">
        <div class="chart-title">🏗️ Top 10 Proyectos</div>
        <div class="chart-subtitle">Ranking por volumen de ventas</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div style="max-height:320px; overflow-y:auto;">{render_top_proyectos(df_filtered)}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="insights-container" style="margin-top: 1.5rem;">
    <div class="section-header">
        <span class="section-icon">✨</span>
        <h2 class="section-title">Insights Clave</h2>
    </div>
""", unsafe_allow_html=True)

insights = render_insights(df_filtered)
cols = st.columns(len(insights))

for i, insight in enumerate(insights):
    with cols[i]:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-badge">
                <div class="insight-badge-dot" style="background:{insight['color']}"></div>
                <span style="color:{insight['color']}">{insight['badge']}</span>
            </div>
            <p class="insight-text">{insight['text']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="footer">
    <p class="footer-text">
        Dashboard Ejecutivo • Gran Convención de Ventas CONALTURA 2025<br>
        <span style="opacity:0.7">Total registros: {len(df_filtered):,} de {len(df):,} | Filtros activos: {sum([1 for f in [filter_ciudad, filter_canal, filter_gama, filter_mes] if f and f not in ['Todas', 'Todos']])}</span>
    </p>
</div>
""", unsafe_allow_html=True)
