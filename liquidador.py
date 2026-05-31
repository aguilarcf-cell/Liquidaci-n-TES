from datetime import datetime
import math

def liquidar_bono(f_emision, f_vcto, f_nego, tasa_facial, tasa_nego, periodicidad):
    """
    Liquida un bono de largo plazo.
    periodicidad: 1 (Anual), 2 (Semestral), 4 (Trimestral), etc.
    Tasas en formato decimal (ej: 0.05 para 5%)
    """
    # Convertir strings a objetos datetime
    formato = "%Y-%m-%d"
    emision = datetime.strptime(f_emision, formato)
    vcto = datetime.strptime(f_vcto, formato)
    nego = datetime.strptime(f_nego, formato)
    
    if nego < emision or nego > vcto:
        raise ValueError("La fecha de negociación debe estar entre la emisión y el vencimiento.")
        
    # 1. Estimar los flujos de cupones desde la emisión
    # En un caso real se usan calendarios bancarios (ej: ACT/360 o 30/360). 
    # Usaremos aproximación exacta en días (ACT/ACT) para este ejemplo.
    
    dias_periodo = 365 / periodicidad
    tasa_cupon_periodo = tasa_facial / periodicidad
    tasa_nego_periodo = tasa_nego / periodicidad
    
    # Encontrar las fechas de los cupones
    fechas_cupones = []
    temp_fecha = vcto
    while temp_fecha > emision:
        fechas_cupones.insert(0, temp_fecha)
        # Retroceder un período (aproximación por meses)
        meses_a_restar = int(12 / periodicidad)
        nuevo_mes = temp_fecha.month - meses_a_restar
        nuevo_año = temp_fecha.year
        while nuevo_mes <= 0:
            nuevo_mes += 12
            nuevo_año -= 1
        try:
            temp_fecha = temp_fecha.replace(year=nuevo_año, month=nuevo_mes)
        except ValueError:
            # Manejo de fin de mes (ej: 31 de ahorros que cae en 30 o 28)
            temp_fecha = temp_fecha.replace(year=nuevo_año, month=nuevo_mes, day=28)

    # Identificar el cupón anterior y el siguiente a la fecha de negociación
    cupon_anterior = emision
    cupon_siguiente = fechas_cupones[0]
    
    for c in fechas_cupones:
        if c >= nego:
            cupon_siguiente = c
            break
        cupon_anterior = c
        
    # 2. Calcular Intereses Corridos (Accrued Interest)
    dias_desde_ultimo_cupon = (nego - cupon_anterior).days
    dias_totales_periodo = (cupon_siguiente - cupon_anterior).days
    
    # Si nego es igual a emision, intereses corridos es 0
    if dias_totales_periodo > 0:
        fraccion_periodo_transcurrido = dias_desde_ultimo_cupon / dias_totales_periodo
    else:
        fraccion_periodo_transcurrido = 0
        
    interes_corrido = 100 * tasa_cupon_periodo * fraccion_periodo_transcurrido
    
    # 3. Calcular el Precio Sucio (Valor Presente de los flujos remanentes)
    # Fracción de tiempo que falta para el próximo cupón
    t_proximo = (cupon_siguiente - nego).days / dias_totales_periodo
    
    precio_sucio = 0
    flujos_restantes = [c for c in fechas_cupones if c >= nego]
    
    for i, f in enumerate(flujos_restantes):
        # El exponente para el descuento
        n = t_proximo + i 
        
        # El último flujo incluye el Principal (100)
        es_ultimo = (i == len(flujos_restantes) - 1)
        flujo_caja = 100 * tasa_cupon_periodo
        if es_ultimo:
            flujo_caja += 100 # Pago del Nominal
            
        # Descuento a la tasa de negociación
        precio_sucio += flujo_caja / ((1 + tasa_nego_periodo) ** n)
        
    # 4. Calcular Precio Limpio
    precio_limpio = precio_sucio - interes_corrido
    
    return {
        "Precio Sucio (%)": round(precio_sucio, 4),
        "Precio Limpio (%)": round(precio_limpio, 4),
        "Intereses Corridos (%)": round(interes_corrido, 4),
        "Próximo Cupón": cupon_siguiente.strftime("%Y-%m-%d"),
        "Días Corridos": dias_desde_ultimo_cupon
    }

# --- EJEMPLO DE USO ---
resultado = liquidar_bono(
    f_emision="2024-01-01",
    f_vcto="2029-01-01",
    f_nego="2026-06-01",
    tasa_facial=0.06,  # 6% anual
    tasa_nego=0.05,    # 5% anual (El bono debería venderse con prima, > 100%)
    periodicidad=2     # Semestral
)

print("--- RESULTADO DE LA LIQUIDACIÓN ---")
for k, v in resultado.items():
    print(f"{k}: {v}")
