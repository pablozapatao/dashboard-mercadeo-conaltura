"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                    CONALTURA - DASHBOARD COMERCIAL 2025                              ║
║                    UI/UX Premium - Junta Internacional                               ║
║                                                                                      ║
║  INSTRUCCIONES:                                                                      ║
║  1. Coloca el archivo 'logo.png' en el mismo directorio que app.py                  ║
║  2. Ejecuta: streamlit run app.py                                                   ║
║  3. Carga tu archivo CSV/Excel con los datos de ventas                              ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL
# ══════════════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Conaltura | Gerencia Comercial",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES CONALTURA
# ══════════════════════════════════════════════════════════════════════════════════════

COLORS = {
    'primary': '#125160',       # Verde Petróleo - Títulos, textos principales
    'accent': '#FF795A',        # Naranja Vibrante - Destacados, Digital
    'lime': '#DBFF69',          # Verde Lima - Acentos positivos
    'neutral': '#D3D3D3',       # Gris suave - Neutros
    'bg_app': '#F9F9F9',        # Fondo de la app
    'bg_card': '#FFFFFF',       # Fondo de tarjetas
    'text_dark': '#125160',     # Texto oscuro
    'text_muted': '#6B7280',    # Texto secundario
    'success': '#10B981',       # Verde éxito
    'border': '#E5E7EB'         # Bordes
}

# Secuencia para gráficos
CHART_SEQUENCE = ['#FF795A', '#125160', '#DBFF69', '#B382FF', '#A1D81A', '#F97316']

# ══════════════════════════════════════════════════════════════════════════════════════
# CSS PREMIUM - INYECCIÓN DE ESTILOS PERSONALIZADOS
# ══════════════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<style>
    /* ══════════════════════════════════════════════════════════════════════════════
       IMPORTACIÓN DE FUENTE POPPINS
    ══════════════════════════════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* ══════════════════════════════════════════════════════════════════════════════
       RESET Y BASE
    ══════════════════════════════════════════════════════════════════════════════ */
    *, *::before, *::after {{
        font-family: 'Poppins', sans-serif !important;
    }}
    
    /* Fondo principal de la app */
    .stApp {{
        background-color: {COLORS['bg_app']} !important;
    }}
    
    .main .block-container {{
        padding: 2rem 3rem !important;
        max-width: 1400px;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       SIDEBAR - ELEGANTE Y FUNCIONAL
    ══════════════════════════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary']} 0%, #0a3540 100%) !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {{
        color: white !important;
    }}
    
    /* Labels de selectores en sidebar - MUY IMPORTANTE: legibles */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stFileUploader label {{
        color: {COLORS['lime']} !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    
    /* Selectores dentro del sidebar - fondo blanco, texto oscuro */
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {{
        background-color: white !important;
        border-radius: 10px !important;
        border: none !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox > div > div > div,
    [data-testid="stSidebar"] [data-baseweb="select"] span {{
        color: {COLORS['text_dark']} !important;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       TARJETAS KPI - DISEÑO PREMIUM
    ══════════════════════════════════════════════════════════════════════════════ */
    .kpi-card {{
        background: {COLORS['bg_card']};
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }}
    
    .kpi-icon {{
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }}
    
    .kpi-icon-orange {{ background: rgba(255, 121, 90, 0.15); }}
    .kpi-icon-green {{ background: rgba(18, 81, 96, 0.15); }}
    .kpi-icon-lime {{ background: rgba(219, 255, 105, 0.3); }}
    
    .kpi-label {{
        color: {COLORS['text_muted']};
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }}
    
    .kpi-value {{
        color: {COLORS['text_dark']};
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.3rem;
    }}
    
    .kpi-change {{
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }}
    
    .kpi-change-positive {{ color: {COLORS['success']}; }}
    .kpi-change-accent {{ color: {COLORS['accent']}; }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       SECCIONES Y CONTENEDORES
    ══════════════════════════════════════════════════════════════════════════════ */
    .section-container {{
        background: {COLORS['bg_card']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
    }}
    
    .section-title {{
        color: {COLORS['text_dark']};
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid {COLORS['border']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .section-title-icon {{
        font-size: 1.2rem;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       HEADER
    ══════════════════════════════════════════════════════════════════════════════ */
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 2rem 0;
        border-bottom: 1px solid {COLORS['border']};
        margin-bottom: 2rem;
    }}
    
    .header-left {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .header-logo {{
        height: 50px;
    }}
    
    .header-title {{
        color: {COLORS['text_dark']};
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .header-subtitle {{
        color: {COLORS['text_muted']};
        font-size: 0.9rem;
        margin: 0;
    }}
    
    .header-badge {{
        background: linear-gradient(135deg, {COLORS['accent']} 0%, #e5684a 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       WELCOME SCREEN
    ══════════════════════════════════════════════════════════════════════════════ */
    .welcome-container {{
        text-align: center;
        padding: 4rem 2rem;
        background: {COLORS['bg_card']};
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: 3rem auto;
    }}
    
    .welcome-icon {{
        font-size: 4rem;
        margin-bottom: 1.5rem;
    }}
    
    .welcome-title {{
        color: {COLORS['text_dark']};
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }}
    
    .welcome-text {{
        color: {COLORS['text_muted']};
        font-size: 1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }}
    
    .welcome-steps {{
        text-align: left;
        background: {COLORS['bg_app']};
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
    }}
    
    .welcome-step {{
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 0;
        color: {COLORS['text_dark']};
        font-size: 0.95rem;
    }}
    
    .step-number {{
        background: {COLORS['accent']};
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.85rem;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       DATAFRAME STYLING
    ══════════════════════════════════════════════════════════════════════════════ */
    .stDataFrame {{
        border-radius: 12px !important;
        overflow: hidden !important;
    }}
    
    [data-testid="stDataFrame"] > div {{
        border-radius: 12px !important;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       OCULTAR ELEMENTOS DE STREAMLIT
    ══════════════════════════════════════════════════════════════════════════════ */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Ocultar el decorador de streamlit */
    .stDeployButton {{display: none;}}
    
    /* ══════════════════════════════════════════════════════════════════════════════
       RESPONSIVE
    ══════════════════════════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {{
        .kpi-value {{
            font-size: 1.5rem;
        }}
        .main .block-container {{
            padding: 1rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ══════════════════════════════════════════════════════════════════════════════════════

def format_cop(value):
    """Formatea números como moneda COP sin decimales"""
    try:
        if pd.isna(value) or value == 0:
            return "$ 0"
        # Formato con puntos como separador de miles (estilo colombiano)
        return f"$ {value:,.0f}".replace(",", ".")
    except:
        return "$ 0"

def format_cop_short(value):
    """Formato corto para KPIs grandes"""
    try:
        if pd.isna(value) or value == 0:
            return "$ 0"
        if value >= 1_000_000_000:
            return f"$ {value/1_000_000_000:,.1f}B".replace(",", ".")
        elif value >= 1_000_000:
            return f"$ {value/1_000_000:,.0f}M".replace(",", ".")
        elif value >= 1_000:
            return f"$ {value/1_000:,.0f}K".replace(",", ".")
        else:
            return f"$ {value:,.0f}".replace(",", ".")
    except:
        return "$ 0"

def get_logo_base64():
    """Intenta cargar el logo y convertirlo a base64"""
    logo_paths = ['logo.png', './logo.png', 'assets/logo.png']
    for path in logo_paths:
        if Path(path).exists():
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

def clean_columns(df):
    """Normaliza nombres de columnas"""
    mapping = {
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
        'fecha': 'Fecha',
        'agrupacion': 'Agrupación',
        'agrupación': 'Agrupación',
        'categoria': 'Agrupación',
        'tipo': 'Agrupación'
    }
    
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    df = df.rename(columns=mapping)
    return df

def load_data(uploaded_file):
    """Carga y procesa el archivo"""
    try:
        if uploaded_file.name.endswith('.csv'):
            # Intentar detectar separador
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            separator = ';' if ';' in content[:1000] else ','
            df = pd.read_csv(uploaded_file, sep=separator, encoding='utf-8')
        else:
            df = pd.read_excel(uploaded_file)
        
        df = clean_columns(df)
        
        # Procesar fecha
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
        
        # Procesar valor
        if 'Valor Neto' in df.columns:
            df['Valor Neto'] = pd.to_numeric(df['Valor Neto'], errors='coerce').fillna(0)
        
        # Limpiar categóricas
        for col in ['MacroProyecto', 'Medio Publicitario', 'Ciudad', 'Agrupación']:
            if col in df.columns:
                df[col] = df[col].fillna('Sin Definir').astype(str).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error al cargar: {str(e)}")
        return None

# ══════════════════════════════════════════════════════════════════════════════════════
# COMPONENTES UI
# ══════════════════════════════════════════════════════════════════════════════════════

def render_header():
    """Renderiza el header con logo"""
    logo_b64 = get_logo_base64()
    
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="header-logo" alt="Conaltura">'
    else:
        logo_html = f'<span style="font-size: 2rem; color: {COLORS["primary"]}; font-weight: 800;">CONALTURA</span>'
    
    st.markdown(f"""
    <div class="header-container">
        <div class="header-left">
            {logo_html}
            <div>
                <h1 class="header-title">Dashboard Comercial</h1>
                <p class="header-subtitle">Gerencia Comercial | Análisis de Ventas 2025</p>
            </div>
        </div>
        <div class="header-badge">
            📊 Junta Internacional 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(icon, label, value, change_text="", change_type="positive", icon_color="orange"):
    """Renderiza una tarjeta KPI estilizada"""
    change_class = f"kpi-change-{change_type}"
    icon_class = f"kpi-icon-{icon_color}"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon {icon_class}">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-change {change_class}">{change_text}</div>
    </div>
    """

def render_welcome_screen():
    """Pantalla de bienvenida cuando no hay datos"""
    logo_b64 = get_logo_base64()
    
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 60px; margin-bottom: 1rem;" alt="Conaltura">'
    else:
        logo_html = f'<div style="font-size: 2.5rem; color: {COLORS["primary"]}; font-weight: 800; margin-bottom: 1rem;">CONALTURA</div>'
    
    st.markdown(f"""
    <div class="welcome-container">
        {logo_html}
        <div class="welcome-icon">📊</div>
        <h2 class="welcome-title">Bienvenido al Dashboard Comercial</h2>
        <p class="welcome-text">
            Visualiza el desempeño de ventas por ciudad, canal y proyecto.
            Carga tu archivo de datos para comenzar el análisis.
        </p>
        <div class="welcome-steps">
            <div class="welcome-step">
                <span class="step-number">1</span>
                <span>Abre el panel lateral izquierdo (☰)</span>
            </div>
            <div class="welcome-step">
                <span class="step-number">2</span>
                <span>Carga tu archivo CSV o Excel</span>
            </div>
            <div class="welcome-step">
                <span class="step-number">3</span>
                <span>Explora los insights automáticamente</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Columnas requeridas
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Estructura de datos requerida"):
        st.markdown("""
        | Columna | Descripción | Ejemplo |
        |---------|-------------|---------|
        | `MacroProyecto` | Nombre del proyecto | Amara, Bora |
        | `Medio Publicitario` | Canal de venta | Instagram, Vallas |
        | `Valor Neto` | Monto en COP | 450000000 |
        | `Ciudad` | Ubicación | Medellín, Bogotá |
        | `Fecha` | Fecha transacción | 2025-01-15 |
        | `Agrupación` | Categoría canal | Ventas Digitales, Tradicional |
        """)

# ══════════════════════════════════════════════════════════════════════════════════════
# GRÁFICOS MINIMALISTAS
# ══════════════════════════════════════════════════════════════════════════════════════

def create_horizontal_bar_chart(df, top_n=5):
    """Top ciudades - Barras horizontales limpias"""
    city_data = df.groupby('Ciudad')['Valor Neto'].sum().sort_values(ascending=True).tail(top_n)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=city_data.index,
        x=city_data.values,
        orientation='h',
        marker=dict(
            color=city_data.values,
            colorscale=[[0, COLORS['primary']], [1, COLORS['accent']]],
            cornerradius=6
        ),
        text=[format_cop_short(v) for v in city_data.values],
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_dark'], family='Poppins'),
        hovertemplate='<b>%{y}</b><br>Ventas: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=80, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color=COLORS['text_dark'], family='Poppins')
        ),
        font=dict(family='Poppins')
    )
    
    return fig

def create_donut_chart(df):
    """Donut chart con % del mayor en el centro"""
    agrup_data = df.groupby('Agrupación')['Valor Neto'].sum()
    total = agrup_data.sum()
    max_pct = (agrup_data.max() / total * 100) if total > 0 else 0
    max_label = agrup_data.idxmax() if len(agrup_data) > 0 else ""
    
    # Mapear colores
    colors_map = {
        'Ventas Digitales': COLORS['accent'],
        'Digital': COLORS['accent'],
        'Tradicional': COLORS['primary'],
        'Ventas Tradicionales': COLORS['primary'],
        'Referidos': COLORS['lime'],
    }
    
    colors = [colors_map.get(label, COLORS['neutral']) for label in agrup_data.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=agrup_data.index,
        values=agrup_data.values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color='white', width=3)),
        textinfo='percent',
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_dark'], family='Poppins'),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} COP<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11, family='Poppins')
        ),
        annotations=[
            dict(
                text=f'<b>{max_pct:.0f}%</b><br><span style="font-size:10px">{max_label[:12]}</span>',
                x=0.5, y=0.5,
                font=dict(size=24, color=COLORS['text_dark'], family='Poppins'),
                showarrow=False
            )
        ],
        font=dict(family='Poppins')
    )
    
    return fig

def create_heatmap(df):
    """Heatmap de eficiencia: Ciudad vs Medio Publicitario"""
    # Crear matriz
    pivot = df.pivot_table(
        index='Ciudad',
        columns='Medio Publicitario',
        values='Valor Neto',
        aggfunc='sum',
        fill_value=0
    )
    
    # Limitar a top ciudades y medios
    top_cities = df.groupby('Ciudad')['Valor Neto'].sum().nlargest(6).index
    top_medios = df.groupby('Medio Publicitario')['Valor Neto'].sum().nlargest(8).index
    
    pivot = pivot.loc[pivot.index.isin(top_cities), pivot.columns.isin(top_medios)]
    
    if pivot.empty:
        return None
    
    # Crear texto formateado
    text_matrix = [[format_cop_short(val) for val in row] for row in pivot.values]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        text=text_matrix,
        texttemplate="%{text}",
        textfont=dict(size=10, color='white', family='Poppins'),
        colorscale=[
            [0, '#E5E7EB'],
            [0.25, COLORS['primary']],
            [0.5, '#1a7a8a'],
            [0.75, COLORS['accent']],
            [1, '#ff5030']
        ],
        showscale=False,
        hovertemplate='<b>%{y}</b> × <b>%{x}</b><br>Ventas: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            side='top',
            tickfont=dict(size=10, color=COLORS['text_dark'], family='Poppins'),
            tickangle=-45
        ),
        yaxis=dict(
            tickfont=dict(size=11, color=COLORS['text_dark'], family='Poppins'),
            autorange='reversed'
        ),
        font=dict(family='Poppins')
    )
    
    return fig

def create_trend_chart(df):
    """Gráfico de tendencia mensual"""
    if 'Mes' not in df.columns:
        return None
    
    trend = df.groupby(['Mes', 'Agrupación'])['Valor Neto'].sum().reset_index()
    
    if trend.empty:
        return None
    
    color_map = {
        'Ventas Digitales': COLORS['accent'],
        'Digital': COLORS['accent'],
        'Tradicional': COLORS['primary'],
        'Ventas Tradicionales': COLORS['primary'],
        'Referidos': COLORS['lime'],
    }
    
    fig = px.area(
        trend,
        x='Mes',
        y='Valor Neto',
        color='Agrupación',
        color_discrete_map=color_map
    )
    
    fig.update_traces(
        line=dict(width=2),
        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>$%{y:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            title='',
            tickfont=dict(size=10, family='Poppins')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            title='',
            tickfont=dict(size=10, family='Poppins')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10, family='Poppins')
        ),
        font=dict(family='Poppins')
    )
    
    return fig

# ══════════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Logo en sidebar
    logo_b64 = get_logo_base64()
    if logo_b64:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">
            <img src="data:image/png;base64,{logo_b64}" style="height: 45px;" alt="Conaltura">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">
            <span style="color: white; font-size: 1.5rem; font-weight: 700;">CONALTURA</span>
        </div>
        """, unsafe_allow_html=True)
    
    # File uploader
    st.markdown('<p style="color: #DBFF69; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.5rem;">📁 CARGAR DATOS</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=['csv', 'xlsx', 'xls'],
        help="Archivo CSV o Excel con datos de ventas"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filtros
    filter_ciudad = None
    filter_agrupacion = None
    
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None and not df.empty:
            st.markdown('<p style="color: #DBFF69; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.5rem;">🎯 FILTROS</p>', unsafe_allow_html=True)
            
            if 'Ciudad' in df.columns:
                ciudades = ['Todas'] + sorted(df['Ciudad'].unique().tolist())
                filter_ciudad = st.selectbox("Ciudad", ciudades)
            
            if 'Agrupación' in df.columns:
                agrupaciones = ['Todas'] + sorted(df['Agrupación'].unique().tolist())
                filter_agrupacion = st.selectbox("Canal", agrupaciones)
    
    # Footer sidebar
    st.markdown("""
    <div style="position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;">
        <p style="color: rgba(255,255,255,0.5); font-size: 0.7rem; margin: 0;">
            Dashboard Gerencia Comercial<br>
            © Conaltura 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# CONTENIDO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════════════

# Header
render_header()

# Verificar datos
if uploaded_file is None:
    render_welcome_screen()
    st.stop()

df = load_data(uploaded_file)

if df is None or df.empty:
    st.error("❌ No se pudieron cargar los datos. Verifica el formato del archivo.")
    st.stop()

# Aplicar filtros
df_filtered = df.copy()

if filter_ciudad and filter_ciudad != 'Todas':
    df_filtered = df_filtered[df_filtered['Ciudad'] == filter_ciudad]

if filter_agrupacion and filter_agrupacion != 'Todas':
    df_filtered = df_filtered[df_filtered['Agrupación'] == filter_agrupacion]

if df_filtered.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════════════
# KPIs ROW
# ══════════════════════════════════════════════════════════════════════════════════════

total_ventas = df_filtered['Valor Neto'].sum()
meta_ficticia = total_ventas * 1.1  # Meta 10% arriba para simular
cumplimiento = (total_ventas / meta_ficticia * 100) if meta_ficticia > 0 else 0
ticket_promedio = total_ventas / len(df_filtered) if len(df_filtered) > 0 else 0
n_operaciones = len(df_filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(render_kpi_card(
        "💰", "Ventas Totales",
        format_cop_short(total_ventas),
        f"📈 {n_operaciones} operaciones",
        "positive", "orange"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(render_kpi_card(
        "🎯", "Cumplimiento Meta",
        f"{cumplimiento:.1f}%",
        "vs meta proyectada",
        "accent", "green"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(render_kpi_card(
        "🎫", "Ticket Promedio",
        format_cop_short(ticket_promedio),
        "por operación",
        "positive", "lime"
    ), unsafe_allow_html=True)

with col4:
    top_city = df_filtered.groupby('Ciudad')['Valor Neto'].sum().idxmax() if 'Ciudad' in df_filtered.columns else "N/A"
    st.markdown(render_kpi_card(
        "🏆", "Ciudad Líder",
        top_city,
        "mayor volumen",
        "accent", "orange"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# NIVEL 1: VISIÓN MACRO
# ══════════════════════════════════════════════════════════════════════════════════════

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            <span class="section-title-icon">🏙️</span>
            Top 5 Ciudades por Ventas
        </div>
    """, unsafe_allow_html=True)
    
    fig_bars = create_horizontal_bar_chart(df_filtered)
    st.plotly_chart(fig_bars, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            <span class="section-title-icon">📊</span>
            Share por Tipo de Canal
        </div>
    """, unsafe_allow_html=True)
    
    fig_donut = create_donut_chart(df_filtered)
    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# NIVEL 2: DETALLE TÁCTICO
# ══════════════════════════════════════════════════════════════════════════════════════

col_heat, col_trend = st.columns([1.3, 1])

with col_heat:
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            <span class="section-title-icon">🔥</span>
            Mapa de Eficiencia: Ciudad × Canal
        </div>
        <p style="color: #6B7280; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;">
            ¿Qué funciona en cada ciudad? Intensidad = volumen de ventas
        </p>
    """, unsafe_allow_html=True)
    
    fig_heat = create_heatmap(df_filtered)
    if fig_heat:
        st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Datos insuficientes para el heatmap")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_trend:
    st.markdown("""
    <div class="section-container">
        <div class="section-title">
            <span class="section-title-icon">📈</span>
            Tendencia Mensual
        </div>
    """, unsafe_allow_html=True)
    
    fig_trend = create_trend_chart(df_filtered)
    if fig_trend:
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Se requiere columna 'Fecha' para tendencias")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# TABLA DE DETALLE
# ══════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-container">
    <div class="section-title">
        <span class="section-title-icon">📋</span>
        Detalle de Operaciones | Top 15 por Valor
    </div>
""", unsafe_allow_html=True)

# Preparar tabla
table_df = df_filtered.nlargest(15, 'Valor Neto')[['MacroProyecto', 'Ciudad', 'Medio Publicitario', 'Agrupación', 'Valor Neto']].copy()
table_df['Valor Neto'] = table_df['Valor Neto'].apply(format_cop)
table_df.columns = ['Proyecto', 'Ciudad', 'Canal', 'Tipo', 'Valor Venta']

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    height=400
)

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 1px solid {COLORS['border']};">
    <p style="color: {COLORS['text_muted']}; font-size: 0.85rem; margin: 0;">
        Dashboard Gerencia Comercial | Conaltura © 2025 | Junta Internacional
    </p>
</div>
""", unsafe_allow_html=True)
