
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64

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

def semaforo(roi, cashflow):
    if roi >= 8 and cashflow > 0:
        return "🟢 Buena inversión"
    elif 5 <= roi < 8 or -50000 < cashflow <= 0:
        return "🟡 Regular, requiere análisis"
    else:
        return "🔴 Riesgosa o poco rentable"

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

eva_a = semaforo(roi_a, cashflow_a)
eva_b = semaforo(roi_b, cashflow_b)

st.markdown("### Resultados Comparativos")
col3, col4 = st.columns(2)
with col3:
    st.markdown(f"**Depto A**\n- Dividendo: ${dividendo_a:,.0f}\n- Cashflow: ${cashflow_a:,.0f}\n- ROI: {roi_a:.2f}% anual\n- Valor Proyectado: ${valor_final_a:,.0f}")
    st.markdown(f"**Evaluación:** {eva_a}")
with col4:
    st.markdown(f"**Depto B**\n- Dividendo: ${dividendo_b:,.0f}\n- Cashflow: ${cashflow_b:,.0f}\n- ROI: {roi_b:.2f}% anual\n- Valor Proyectado: ${valor_final_b:,.0f}")
    st.markdown(f"**Evaluación:** {eva_b}")

# Generar PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Reporte de Comparación Inmobiliaria", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Departamento A", ln=True)
    pdf.ln(2)
    pdf.multi_cell(200, 8, txt=(
        f"Precio: ${precio_a:,.0f}\n"
        f"Pie: ${pie_a:,.0f}\n"
        f"Arriendo: ${arriendo_a:,.0f}\n"
        f"ROI: {roi_a:.2f}%\n"
        f"Cashflow: ${cashflow_a:,.0f}\n"
        f"Valor Proyectado: ${valor_final_a:,.0f}\n"
        f"Evaluación: {eva_a}"
    ))

    pdf.ln(5)
    pdf.cell(200, 10, txt="Departamento B", ln=True)
    pdf.ln(2)
    pdf.multi_cell(200, 8, txt=(
        f"Precio: ${precio_b:,.0f}\n"
        f"Pie: ${pie_b:,.0f}\n"
        f"Arriendo: ${arriendo_b:,.0f}\n"
        f"ROI: {roi_b:.2f}%\n"
        f"Cashflow: ${cashflow_b:,.0f}\n"
        f"Valor Proyectado: ${valor_final_b:,.0f}\n"
        f"Evaluación: {eva_b}"
    ))

    return pdf.output(dest='S').encode('latin-1')

if st.button("📄 Descargar análisis en PDF"):
    pdf_bytes = generar_pdf()
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="analisis_inversion.pdf">Haz clic aquí para descargar tu PDF 📄</a>'
    st.markdown(href, unsafe_allow_html=True)

