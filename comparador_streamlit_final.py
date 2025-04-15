
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="DON'T PATO - Inversión Inmobiliaria", layout="wide")

# ---- LOGO Y SLOGAN ----
st.image("perfil_pato.png", width=200)
st.markdown("<h2 style='text-align: center;'>Simula. Compara. Invierte con inteligencia.</h2>", unsafe_allow_html=True)

# ---- PARÁMETROS GENERALES ----
with st.sidebar:
    st.header("📋 Parámetros Generales")
    tasa = st.number_input("Tasa de interés anual (%)", value=4.5) / 100
    anios = st.number_input("Años del crédito", value=20, step=1)

def calcular_dividendo(monto, tasa_anual, anios):
    tasa_mensual = tasa_anual / 12
    cuotas = anios * 12
    return (monto * tasa_mensual * (1 + tasa_mensual) ** cuotas) / ((1 + tasa_mensual) ** cuotas - 1)

def semaforo_simple(roi, cashflow):
    if roi >= 8 and cashflow > 0:
        return "Buena inversión"
    elif 5 <= roi < 8 or -50000 < cashflow <= 0:
        return "Regular, requiere análisis"
    else:
        return "Riesgosa o poco rentable"

# ---- FORMULARIO ----
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏢 Departamento A")
    precio_a = st.number_input("Precio A ($)", value=100000000)
    pie_a = st.number_input("Pie A ($)", value=20000000)
    arriendo_a = st.number_input("Arriendo A ($)", value=450000)
    valorizacion_a = st.number_input("Valorización anual A (%)", value=3.0) / 100

with col2:
    st.subheader("🏢 Departamento B")
    precio_b = st.number_input("Precio B ($)", value=90000000)
    pie_b = st.number_input("Pie B ($)", value=18000000)
    arriendo_b = st.number_input("Arriendo B ($)", value=430000)
    valorizacion_b = st.number_input("Valorización anual B (%)", value=5.0) / 100

# ---- CÁLCULOS ----
dividendo_a = calcular_dividendo(precio_a - pie_a, tasa, anios)
dividendo_b = calcular_dividendo(precio_b - pie_b, tasa, anios)

cashflow_a = arriendo_a - dividendo_a
cashflow_b = arriendo_b - dividendo_b

roi_a = (cashflow_a * 12) / pie_a * 100
roi_b = (cashflow_b * 12) / pie_b * 100

valor_venta_a = precio_a * ((1 + valorizacion_a) ** anios)
valor_venta_b = precio_b * ((1 + valorizacion_b) ** anios)

utilidad_a = valor_venta_a - precio_a + (cashflow_a * 12 * anios)
utilidad_b = valor_venta_b - precio_b + (cashflow_b * 12 * anios)

eva_a = semaforo_simple(roi_a, cashflow_a)
eva_b = semaforo_simple(roi_b, cashflow_b)

# ---- MOSTRAR RESULTADOS ----
st.markdown("### 📊 Resultados Comparativos")
col3, col4 = st.columns(2)
with col3:
    st.write(f"**Depto A**")
    st.write(f"Dividendo: ${dividendo_a:,.0f}")
    st.write(f"Cashflow: ${cashflow_a:,.0f}")
    st.write(f"ROI: {roi_a:.2f}% anual")
    st.write(f"Valor proyectado venta: ${valor_venta_a:,.0f}")
    st.write(f"Utilidad total: ${utilidad_a:,.0f}")
    st.write(f"Evaluación: {eva_a}")
with col4:
    st.write(f"**Depto B**")
    st.write(f"Dividendo: ${dividendo_b:,.0f}")
    st.write(f"Cashflow: ${cashflow_b:,.0f}")
    st.write(f"ROI: {roi_b:.2f}% anual")
    st.write(f"Valor proyectado venta: ${valor_venta_b:,.0f}")
    st.write(f"Utilidad total: ${utilidad_b:,.0f}")
    st.write(f"Evaluación: {eva_b}")


