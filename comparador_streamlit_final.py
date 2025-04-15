
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

valor_final_a = precio_a * ((1 + valorizacion_a) ** anios)
valor_final_b = precio_b * ((1 + valorizacion_b) ** anios)

st.markdown("### Resultados Comparativos")
col3, col4 = st.columns(2)
with col3:
    st.markdown(f"**Depto A**\n- Dividendo: ${dividendo_a:,.0f}\n- Cashflow: ${cashflow_a:,.0f}\n- ROI: {roi_a:.2f}% anual\n- Valor Proyectado: ${valor_final_a:,.0f}")
with col4:
    st.markdown(f"**Depto B**\n- Dividendo: ${dividendo_b:,.0f}\n- Cashflow: ${cashflow_b:,.0f}\n- ROI: {roi_b:.2f}% anual\n- Valor Proyectado: ${valor_final_b:,.0f}")

# Gráfico comparativo
st.markdown("### Comparación Gráfica: ROI, Cashflow y Valor Proyectado")
fig, ax = plt.subplots(figsize=(8, 4))
categorias = ["ROI (%)", "Cashflow ($)", "Valor Proyectado ($)"]
valores_a = [roi_a, cashflow_a, valor_final_a]
valores_b = [roi_b, cashflow_b, valor_final_b]

x = range(len(categorias))
bar_width = 0.35
ax.bar([i - bar_width/2 for i in x], valores_a, width=bar_width, label="Depto A")
ax.bar([i + bar_width/2 for i in x], valores_b, width=bar_width, label="Depto B")
ax.set_xticks(x)
ax.set_xticklabels(categorias)
ax.set_ylabel("Valor")
ax.set_title("Comparación entre Departamentos")
ax.legend()
st.pyplot(fig)
