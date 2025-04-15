
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparador Inmobiliario", layout="wide")
st.title("🏠 Comparador de Inversión Inmobiliaria")

with st.sidebar:
    st.header("Parámetros Generales")
    tasa = st.number_input("Tasa de interés anual (%)", value=4.5) / 100
    anios = st.number_input("Años del crédito", value=20, step=1)

def calcular_dividendo(monto, tasa_anual, anios):
    tasa_mensual = tasa_anual / 12
    cuotas = anios * 12
    return (monto * tasa_mensual * (1 + tasa_mensual) ** cuotas) / ((1 + tasa_mensual) ** cuotas - 1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Departamento A")
    precio_a = st.number_input("Precio A ($)", value=100000000)
    pie_a = st.number_input("Pie A ($)", value=20000000)
    arriendo_a = st.number_input("Arriendo estimado A ($)", value=450000)
    valorizacion_a = st.number_input("Valorización anual A (%)", value=3.0) / 100

with col2:
    st.subheader("Departamento B")
    precio_b = st.number_input("Precio B ($)", value=90000000)
    pie_b = st.number_input("Pie B ($)", value=18000000)
    arriendo_b = st.number_input("Arriendo estimado B ($)", value=430000)
    valorizacion_b = st.number_input("Valorización anual B (%)", value=5.0) / 100

# Cálculos
dividendo_a = calcular_dividendo(precio_a - pie_a, tasa, anios)
dividendo_b = calcular_dividendo(precio_b - pie_b, tasa, anios)
cashflow_a = arriendo_a - dividendo_a
cashflow_b = arriendo_b - dividendo_b
roi_a = (cashflow_a * 12) / pie_a * 100
roi_b = (cashflow_b * 12) / pie_b * 100

st.markdown("### Resultados Comparativos")
col3, col4 = st.columns(2)
with col3:
    st.markdown(f"**Depto A**\n- Dividendo: ${dividendo_a:,.0f}\n- Cashflow: ${cashflow_a:,.0f}\n- ROI: {roi_a:.2f}% anual")
with col4:
    st.markdown(f"**Depto B**\n- Dividendo: ${dividendo_b:,.0f}\n- Cashflow: ${cashflow_b:,.0f}\n- ROI: {roi_b:.2f}% anual")

# Valorización
valores_a = [precio_a]
valores_b = [precio_b]
for _ in range(anios):
    valores_a.append(valores_a[-1] * (1 + valorizacion_a))
    valores_b.append(valores_b[-1] * (1 + valorizacion_b))

st.markdown("### Proyección de Valorización")
fig, ax = plt.subplots()
ax.plot(range(anios + 1), valores_a, label="Depto A", linewidth=2)
ax.plot(range(anios + 1), valores_b, label="Depto B", linestyle="--", linewidth=2)
ax.set_xlabel("Años")
ax.set_ylabel("Valor en $")
ax.legend()
ax.grid(True)
st.pyplot(fig)
