import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="DON'T PATO - Inversión Inmobiliaria", layout="wide")

st.image("perfil_pato.png", width=200)
st.markdown("<h2 style='text-align: center;'>Simula. Compara. Invierte con inteligencia.</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 Parámetros Generales")
    tasa = st.number_input("Tasa de interés anual (%)", value=4.5) / 100
    anios = st.number_input("Años del crédito", value=20)

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

dividendo_a = calcular_dividendo(precio_a - pie_a, tasa, anios)
dividendo_b = calcular_dividendo(precio_b - pie_b, tasa, anios)

cashflow_a = arriendo_a - dividendo_a
cashflow_b = arriendo_b - dividendo_b

roi_a = (cashflow_a * 12) / pie_a * 100
roi_b = (cashflow_b * 12) / pie_b * 100

valor_final_a = precio_a * ((1 + valorizacion_a) ** anios)
valor_final_b = precio_b * ((1 + valorizacion_b) ** anios)

utilidad_a = (valor_final_a - precio_a) + (cashflow_a * 12 * anios)
utilidad_b = (valor_final_b - precio_b) + (cashflow_b * 12 * anios)

eva_a = semaforo_simple(roi_a, cashflow_a)
eva_b = semaforo_simple(roi_b, cashflow_b)

st.markdown("### 📊 Resultados Comparativos")
col3, col4 = st.columns(2)
with col3:
    st.markdown(f"**Depto A**\n- Dividendo: ${dividendo_a:,.0f}\n- Cashflow: ${cashflow_a:,.0f}\n- ROI: {roi_a:.2f}% anual\n- Valor Venta: ${valor_final_a:,.0f}\n- Utilidad: ${utilidad_a:,.0f}\n- Evaluación: {eva_a}")
with col4:
    st.markdown(f"**Depto B**\n- Dividendo: ${dividendo_b:,.0f}\n- Cashflow: ${cashflow_b:,.0f}\n- ROI: {roi_b:.2f}% anual\n- Valor Venta: ${valor_final_b:,.0f}\n- Utilidad: ${utilidad_b:,.0f}\n- Evaluación: {eva_b}")

# Gráficos compactos
def mostrar_bar(titulo, etiquetas, valores, colores, ylabel):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(etiquetas, valores, color=colores)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    st.pyplot(fig)

mostrar_bar("ROI (%)", ["Depto A", "Depto B"], [roi_a, roi_b], ["blue", "orange"], "ROI")
mostrar_bar("Cashflow mensual", ["Depto A", "Depto B"], [cashflow_a, cashflow_b], ["green", "red"], "$")
mostrar_bar("Utilidad total estimada", ["Depto A", "Depto B"], [utilidad_a, utilidad_b], ["purple", "brown"], "$")

# PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Comparación Inmobiliaria", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, "Departamento A", ln=True)
    pdf.multi_cell(200, 8, f"Precio: ${precio_a:,.0f}\nPie: ${pie_a:,.0f}\nArriendo: ${arriendo_a:,.0f}\nROI: {roi_a:.2f}%\nCashflow: ${cashflow_a:,.0f}\nValor Venta: ${valor_final_a:,.0f}\nUtilidad: ${utilidad_a:,.0f}\nEvaluación: {eva_a}")
    pdf.ln(5)
    pdf.cell(200, 10, "Departamento B", ln=True)
    pdf.multi_cell(200, 8, f"Precio: ${precio_b:,.0f}\nPie: ${pie_b:,.0f}\nArriendo: ${arriendo_b:,.0f}\nROI: {roi_b:.2f}%\nCashflow: ${cashflow_b:,.0f}\nValor Venta: ${valor_final_b:,.0f}\nUtilidad: ${utilidad_b:,.0f}\nEvaluación: {eva_b}")
    return pdf.output(dest="S").encode("latin-1")

if st.button("📄 Descargar análisis en PDF"):
    pdf_bytes = generar_pdf()
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="analisis_inversion.pdf">Haz clic aquí para descargar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# Excel
df = pd.DataFrame({
    "Depto": ["A", "B"],
    "Precio": [precio_a, precio_b],
    "Pie": [pie_a, pie_b],
    "Arriendo": [arriendo_a, arriendo_b],
    "Dividendo": [dividendo_a, dividendo_b],
    "Cashflow": [cashflow_a, cashflow_b],
    "ROI": [roi_a, roi_b],
    "Valor Venta": [valor_final_a, valor_final_b],
    "Utilidad": [utilidad_a, utilidad_b],
    "Evaluación": [eva_a, eva_b]
})

excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False)

st.download_button(
    label="📊 Descargar Excel",
    data=excel_buffer.getvalue(),
    file_name="comparacion_inversion.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Historial
if "historial" not in st.session_state:
    st.session_state.historial = []

sim_actual = {
    "ROI A": round(roi_a, 2),
    "ROI B": round(roi_b, 2),
    "Cashflow A": round(cashflow_a),
    "Cashflow B": round(cashflow_b),
    "Utilidad A": round(utilidad_a),
    "Utilidad B": round(utilidad_b),
    "Eval A": eva_a,
    "Eval B": eva_b
}

if sim_actual not in st.session_state.historial:
    st.session_state.historial.insert(0, sim_actual)

st.markdown("### 🧾 Historial de simulaciones")
for i, h in enumerate(st.session_state.historial[:5]):
    st.markdown(f"- ROI A: {h['ROI A']}% | ROI B: {h['ROI B']}% | Cashflow A: ${h['Cashflow A']} | Cashflow B: ${h['Cashflow B']} | Utilidad A: ${h['Utilidad A']} | Utilidad B: ${h['Utilidad B']} | A: {h['Eval A']} | B: {h['Eval B']}")
