import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="Conaltura Dashboard", page_icon="🏢", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-title { font-size: 14px; color: #888; margin-bottom: 5px; }
    .metric-value { font-size: 24px; font-weight: bold; color: #125160; }
    </style>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES ROBUSTAS DE CARGA
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data_robust(file):
    """Intenta cargar el archivo de todas las formas posibles."""
    df = None
    errores = []

    # 1. Intentar como CSV (UTF-8)
    if file.name.endswith('.csv'):
        try:
            file.seek(0)
            df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8')
        except Exception as e:
            errores.append(f"Fallo UTF-8: {e}")
            
            # 2. Intentar como CSV (Latin-1 - Común en Excel Español)
            try:
                file.seek(0)
                df = pd.read_csv(file, sep=';', encoding='latin-1') # Prueba punto y coma
                if len(df.columns) < 2: # Si falló el separador ; intenta coma
                    file.seek(0)
                    df = pd.read_csv(file, sep=',', encoding='latin-1')
            except Exception as e2:
                errores.append(f"Fallo Latin-1: {e2}")
    
    # 3. Intentar como Excel
    else:
        try:
            df = pd.read_excel(file)
        except Exception as e3:
            errores.append(f"Fallo Excel: {e3}")

    if df is None:
        return None, errores

    # Normalización de columnas (Convierte todo a mayúsculas para comparar fácil)
    # Buscamos patrones en los nombres de las columnas
    rename_map = {}
    for col in df.columns:
        c_clean = col.upper().strip().replace("Ó", "O").replace("Í", "I")
        
        if "PROYECTO" in c_clean: rename_map[col] = "PROYECTO"
        elif "MEDIO" in c_clean: rename_map[col] = "MEDIO"
        elif "AGRUPACION" in c_clean or "CATEGORIA" in c_clean: rename_map[col] = "AGRUPACION"
        elif "VALOR" in c_clean or "NETO" in c_clean or "VENTA" in c_clean: rename_map[col] = "VENTAS"
        elif "CIUDAD" in c_clean: rename_map[col] = "CIUDAD"
        elif "FECHA" in c_clean: rename_map[col] = "FECHA"

    df = df.rename(columns=rename_map)
    
    # Limpieza de datos
    if 'VENTAS' in df.columns:
        # Quitar símbolos de moneda si vienen como texto
        if df['VENTAS'].dtype == object:
             df['VENTAS'] = df['VENTAS'].astype(str).str.replace(r'[$,.]', '', regex=True)
        df['VENTAS'] = pd.to_numeric(df['VENTAS'], errors='coerce').fillna(0)
        
    if 'FECHA' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')

    return df, []

# ══════════════════════════════════════════════════════════════════════════════
# INTERFAZ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

st.title("🚧 Tablero de Diagnóstico y Control")
st.markdown("Sube tu archivo para detectar errores y visualizar los datos.")

uploaded_file = st.sidebar.file_uploader("Cargar Datos (CSV o Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    df, errores = load_data_robust(uploaded_file)
    
    if df is None:
        st.error("❌ No se pudo leer el archivo. Errores técnicos:")
        for e in errores:
            st.code(e)
        st.stop()
    
    # VERIFICACIÓN DE COLUMNAS (DIAGNÓSTICO)
    columnas_necesarias = ['PROYECTO', 'MEDIO', 'AGRUPACION', 'VENTAS', 'CIUDAD']
    columnas_presentes = df.columns.tolist()
    faltantes = [c for c in columnas_necesarias if c not in columnas_presentes]
    
    if faltantes:
        st.warning(f"⚠️ **Atención:** No encontré estas columnas clave: {faltantes}")
        st.info(f"Las columnas que SÍ encontré son: {columnas_presentes}")
        st.markdown("---")
    else:
        st.success("✅ Estructura de archivo correcta. Generando gráficos...")

    # --- FILTROS ---
    st.sidebar.header("Filtros")
    
    # Filtro Ciudad
    ciudades = ['Todas'] + list(df['CIUDAD'].unique()) if 'CIUDAD' in df.columns else []
    ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades)
    
    df_f = df.copy()
    if ciudad_sel != 'Todas':
        df_f = df_f[df_f['CIUDAD'] == ciudad_sel]

    # --- KPIs ---
    st.subheader("Resultados Generales")
    c1, c2, c3 = st.columns(3)
    
    if 'VENTAS' in df_f.columns:
        total = df_f['VENTAS'].sum()
        conteo = len(df_f)
        promedio = total / conteo if conteo > 0 else 0
        
        c1.markdown(f'<div class="metric-card"><div class="metric-title">Ventas Totales</div><div class="metric-value">${total:,.0f}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="metric-title">Transacciones</div><div class="metric-value">{conteo}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="metric-title">Ticket Promedio</div><div class="metric-value">${promedio:,.0f}</div></div>', unsafe_allow_html=True)

    # --- GRÁFICO SANKEY (ATRIBUCIÓN) ---
    st.markdown("---")
    st.subheader("🕸️ Flujo de Atribución (Sankey)")
    
    if 'AGRUPACION' in df_f.columns and 'MEDIO' in df_f.columns and 'VENTAS' in df_f.columns:
        try:
            # Agrupar datos
            sankey_data = df_f.groupby(['AGRUPACION', 'MEDIO'])['VENTAS'].sum().reset_index()
            # Limitar a top 15 medios para que no explote el gráfico
            sankey_data = sankey_data.sort_values('VENTAS', ascending=False).head(20)
            
            # Crear Nodos e Índices
            all_labels = list(pd.unique(sankey_data[['AGRUPACION', 'MEDIO']].values.ravel('K')))
            lab_map = {label: i for i, label in enumerate(all_labels)}
            
            # Crear enlaces
            source = sankey_data['AGRUPACION'].map(lab_map).tolist()
            target = sankey_data['MEDIO'].map(lab_map).tolist()
            value = sankey_data['VENTAS'].tolist()
            
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15, thickness=20,
                    line=dict(color="black", width=0.5),
                    label=all_labels,
                    color="#125160"
                ),
                link=dict(
                    source=source, target=target, value=value,
                    color='rgba(18, 81, 96, 0.2)'
                )
            )])
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error generando el Sankey: {e}")
    else:
        st.info("Faltan columnas (Agrupación, Medio, Ventas) para generar el gráfico de flujo.")

    # --- TABLA DE DATOS ---
    st.markdown("---")
    st.subheader("🔍 Explorador de Datos")
    st.dataframe(df_f.head(100), use_container_width=True)

else:
    st.info("👈 Esperando archivo en el panel lateral...")
