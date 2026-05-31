import streamlit as st
from datetime import datetime

def liquidar_bono(f_emision, f_vcto, f_nego, tasa_facial, tasa_nego, periodicidad=1):
    """
    Liquidador estándar para TES Colombianos (Periodicidad Anual, Base ACT/365)
    """
    if f_nego < f_emision or f_nego > f_vcto:
        st.error("Error: La fecha de negociación debe estar entre la emisión y el vencimiento.")
        return None
        
    tasa_cupon_periodo = tasa_facial / periodicidad
    tasa_nego_periodo = tasa_nego / periodicidad
    
    # Generar fechas de cupones retrocediendo desde el vencimiento
    fechas_cupones = []
    temp_fecha = f_vcto
    while temp_fecha > f_emision:
        fechas_cupones.insert(0, temp_fecha)
        try:
            temp_fecha = temp_fecha.replace(year=temp_fecha.year - 1)
        except ValueError:
            temp_fecha = temp_fecha.replace(year=temp_fecha.year - 1, day=28)

    # Identificar cupones clave alrededor de la negociación
    cupon_anterior = f_emision
    cupon_siguiente = fechas_cupones[0]
    
    for c in fechas_cupones:
        if c >= f_nego:
            cupon_siguiente = c
            break
        cupon_anterior = c
        
    # Cálculo de días (Base ACT/365)
    dias_desde_ultimo_cupon = (f_nego - cupon_anterior).days
    dias_totales_periodo = (cupon_siguiente - cupon_anterior).days
    
    fraccion_periodo_transcurrido = dias_desde_ultimo_cupon / dias_totales_periodo if dias_totales_periodo > 0 else 0
    interes_corrido = 100 * tasa_cupon_periodo * fraccion_periodo_transcurrido
    
    # Valor presente de los flujos remanentes (Precio Sucio)
    t_proximo = (cupon_siguiente - f_nego).days / dias_totales_periodo
    precio_sucio = 0
    flujos_restantes = [c for c in fechas_cupones if c >= f_nego]
    
    for i, f in enumerate(flujos_restantes):
        n = t_proximo + i 
        es_ultimo = (i == len(flujos_restantes) - 1)
        flujo_caja = 100 * tasa_cupon_periodo
        if es_ultimo:
            flujo_caja += 100 
            
        precio_sucio += flujo_caja / ((1 + tasa_nego_periodo) ** n)
        
    precio_limpio = precio_sucio - interes_corrido
    
    return {
        "Precio Sucio": precio_sucio,
        "Precio Limpio": precio_limpio,
        "Intereses Corridos": interes_corrido,
        "Dias Corridos": dias_desde_ultimo_cupon,
        "Proximo Cupon": cupon_siguiente
    }

# --- INTERFAZ GRÁFICA DE STREAMLIT ---
st.set_page_config(page_title="Liquidador de TES", page_icon="📈", layout="centered")

st.title("📈 Liquidador de Bonos de Largo Plazo (TES)")
st.markdown("Introduce los parámetros del título para calcular el precio limpio y sucio.")

st.sidebar.header("Parámetros del Bono")

# Inputs de fechas
f_emision = st.sidebar.date_input("Fecha de Emisión", datetime(2024, 1, 1))
f_vcto = st.sidebar.date_input("Fecha de Vencimiento", datetime(2034, 1, 1))
f_nego = st.sidebar.date_input("Fecha de Negociación", datetime.now().date())

# Inputs de Tasas
tasa_facial_pct = st.sidebar.number_input("Tasa Facial / Cupón Anual (%)", min_value=0.0, max_value=30.0, value=7.5, step=0.05)
tasa_nego_pct = st.sidebar.number_input("Tasa de Negociación / YTM (%)", min_value=0.0, max_value=30.0, value=9.2, step=0.05)

if st.sidebar.button("Calcular Liquidación"):
    res = liquidar_bono(
        f_emision, f_vcto, f_nego, 
        tasa_facial_pct / 100, tasa_nego_pct / 100
    )
    
    if res:
        st.subheader("Resultados de la Valoración")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Precio Limpio (Clean Price)", value=f"{res['Precio Limpio']:.4f}%")
            st.metric(label="Intereses Corridos", value=f"{res['Intereses Corridos']:.4f}%")
        with col2:
            st.metric(label="Precio Sucio (Dirty Price)", value=f"{res['Precio Sucio']:.4f}%")
            st.metric(label="Días Corridos del Cupón", value=f"{res['Dias Corridos']} días")
            
        st.info(f"📅 El próximo pago de cupón es el: **{res['Proximo Cupon'].strftime('%Y-%m-%d')}**")
