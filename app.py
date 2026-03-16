import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import re

# =========================
# 1. HELPERS
# =========================
def clean_text(text):
    """Menyingkirkan emoji dan aksara khas untuk kestabilan PDF"""
    if not text: return ""
    # Gantikan aksara khas dengan teks kosong
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

# =========================
# 2. PDF ENGINE (MULTI-PAGE ENABLED)
# =========================
class StrategicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "OFFICIAL STRATEGIC REPORT - CLASSIFIED", 0, 0, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | Researcher: {RESEARCHER_NAME}", 0, 0, 'C')

def create_comprehensive_pdf(researcher, scenario, risk, oil, gold, fx, debt, df_risk, logs):
    # Inisialisasi PDF (A4)
    pdf = StrategicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ---------------------------------------------------------
    # TITLE SECTION
    # ---------------------------------------------------------
    pdf.set_font("Helvetica", 'B', 18)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 15, "NATIONAL STRATEGIC ANALYSIS REPORT", ln=True, align='C')
    
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.cell(0, 5, f"Lead Analyst: {clean_text(researcher)}", ln=True, align='C')
    pdf.ln(10)

    # ---------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY
    # ---------------------------------------------------------
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, " 1. EXECUTIVE SUMMARY", ln=True, fill=True)
    pdf.ln(2)
    
    pdf.set_font("Helvetica", '', 11)
    summary_data = [
        ("Simulation Scenario", scenario),
        ("Global Risk Posture", risk),
        ("Projected Brent Oil", f"USD {oil:,.2f}"),
        ("USD/MYR Rate", f"RM {fx:,.4f}"),
        ("National Debt Impact", f"RM {debt/1e12:.4f} Trillion")
    ]
    
    for label, val in summary_data:
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(50, 8, f"{label}:", 0)
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(0, 8, clean_text(val), 0, ln=True)
    pdf.ln(5)

    # ---------------------------------------------------------
    # SECTION 2: STATE-LEVEL RISK INVENTORY (FULL TABLE)
    # ---------------------------------------------------------
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, " 2. STATE-LEVEL STRATEGIC RISK MAPPING", ln=True, fill=True)
    pdf.ln(2)
    
    # Table Widths (Total must be around 190 for A4)
    col_width = [45, 80, 30, 35] 
    
    # Header Table
    pdf.set_font("Helvetica", 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(col_width[0], 8, "Location", 1, 0, 'C', fill=True)
    pdf.cell(col_width[1], 8, "Strategic Domain", 1, 0, 'C', fill=True)
    pdf.cell(col_width[2], 8, "Priority", 1, 0, 'C', fill=True)
    pdf.cell(col_width[3], 8, "Stress Score", 1, 1, 'C', fill=True)
    
    # Table Content
    pdf.set_font("Helvetica", '', 8)
    for _, row in df_risk.iterrows():
        pdf.cell(col_width[0], 7, clean_text(row['Location']), 1)
        pdf.cell(col_width[1], 7, clean_text(row['Domain']), 1)
        pdf.cell(col_width[2], 7, clean_text(row['Priority']), 1, 0, 'C')
        pdf.cell(col_width[3], 7, str(round(row['Stress'], 2)), 1, 1, 'C')
    pdf.ln(10)

    # ---------------------------------------------------------
    # SECTION 3: INTELLIGENCE LOGS (FLOWS TO NEXT PAGE)
    # ---------------------------------------------------------
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, " 3. CHRONOLOGICAL COMMAND LOGS", ln=True, fill=True)
    pdf.ln(2)
    
    pdf.set_font("Helvetica", '', 9)
    # Masukkan semua log, jika log banyak, FPDF akan automatik tambah muka surat
    for log in logs:
        # Gunakan multi_cell supaya teks yang panjang automatik turun baris
        pdf.multi_cell(0, 6, f"- {clean_text(log)}", border='B')
    
    # Final Output
    return pdf.output()

# --- Bahagian kod yang lain kekal sama ---
# Pastikan dipanggil menggunakan:
# report_data = create_comprehensive_pdf(...)
# st.download_button(data=report_data, ...)
