import streamlit as st
import pandas as pd
from io import BytesIO
import re

# SAFE PDF IMPORT - works on Streamlit Cloud
try:
    import fitz
except:
    import pymupdf as fitz

try:
    import docx
except:
    docx = None

try:
    import PyPDF2
except:
    PyPDF2 = None

st.set_page_config(page_title="GeM ATC Pro", page_icon="🇮🇳", layout="wide")

st.markdown("""
<style>
.main-header {background: linear-gradient(90deg, #0f172a 0%, #1e40af 100%); padding: 22px; border-radius: 15px; color: white; text-align: center; margin-bottom:20px;}
div[data-testid="stSidebar"] {background-color: #f1f5f9;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🇮🇳 GeM Bid - UNIVERSAL SMART ATC READER</h1><p>Upload Any ATC PDF → Auto Detects Components</p></div>', unsafe_allow_html=True)

COMPONENT_KEYWORDS = {
    "Processor CPU": ["processor", "cpu", "intel core", "i3", "i5", "i7", "ryzen", "14400", "7600"],
    "MB": ["motherboard", "baseboard", "chipset", "h610", "b760"],
    "Graphics CARD": ["graphics", "gpu", "uhd graphics", "radeon"],
    "OS": ["operating system", "windows", "win 11", "os"],
    "RAM": ["ram", "system memory", "ddr4", "ddr5", "16 gb", "memory"],
    "SSD": ["ssd", "nvme", "256 gb", "512 gb ssd"],
    "SSD (SECONDARY)": ["secondary", "1 tb", "sata ssd", "hdd"],
    "Cabinet LTR": ["cabinet", "chassis type", "tower", "sff"],
    "SMPS WATT": ["smps", "power supply"],
    "ADAPTER": ["adapter"],
    "DVD WRITER": ["dvd", "optical drive"],
    "MONITOR": ["monitor", "display", "21.5", "24 inch", "1920x1080"],
    "SPEAKER": ["speaker", "audio"],
    "WIRELESS + BLUETOOTH": ["wireless", "bluetooth", "wifi"],
    "MS OFFICE": ["ms office", "microsoft office"],
    "CHASSIS SWITCH": ["chassis intrusion", "intrusion switch"],
    "TPM 2.0": ["tpm", "trusted platform"],
    "CAMERA": ["webcam", "camera"],
    "ANTIVIRUS": ["antivirus"],
    "DP PORT": ["hdmi", "dp port", "display port"],
    "SERIAL COM PORT+PARALLEL": ["serial port", "com port", "parallel"],
    "Keyboard & Mouse": ["keyboard", "mouse", "104 keys"]
}

PRESETS_HIGH = {"Processor CPU":14500, "MB":4250, "Graphics CARD":0, "OS":600, "RAM":17500, "SSD":3650, "SSD (SECONDARY)":11500, "Cabinet LTR":1850, "SMPS WATT":0, "ADAPTER":0, "DVD WRITER":0, "MONITOR":4450, "SPEAKER":0, "WIRELESS + BLUETOOTH":0, "MS OFFICE":0, "CHASSIS SWITCH":0, "TPM 2.0":700, "CAMERA":500, "ANTIVIRUS":0, "DP PORT":0, "SERIAL COM PORT+PARALLEL":0, "Keyboard & Mouse":350}

def extract_text(file):
    text = ""
    try:
        # Try fitz first
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        return text.lower()
    except Exception as e:
        try:
            file.seek(0)
            if PyPDF2:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text.lower()
        except:
            pass
    return text.lower() if text else ""

def detect_components(atc_text):
    found = []
    for comp, kws in COMPONENT_KEYWORDS.items():
        for kw in kws:
            if kw in atc_text:
                found.append(comp)
                break
    return sorted(list(set(found)))

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7d/Government_e_Marketplace_Logo.png", width=140)
    st.subheader("📤 Upload ATC")
    atc_file = st.file_uploader("Upload BID ATC (PDF)", type=["pdf"])
    dept = st.text_input("Department", "BANK OF INDIA")
    qty = st.number_input("Qty", 1, 1000, 65)
    margin = st.number_input("Margin", 4000)

if atc_file:
    atc_text = extract_text(atc_file)
    detected = detect_components(atc_text)
    if not detected:
        st.warning("PDF is scanned image - cannot read text. Showing all 22.")
        detected = list(COMPONENT_KEYWORDS.keys())
else:
    st.info("👆 Upload ATC PDF. Example BOI ATC shows 16-18 components only.")
    detected = list(COMPONENT_KEYWORDS.keys())
    atc_text = ""

st.subheader(f"💻 Costing - {len(detected)} Components (from ATC)")

prices = {}
total = 0
cols = st.columns(4)
for i, comp in enumerate(detected):
    with cols[i % 4]:
        with st.container(border=True):
            st.markdown(f"**🔹 {comp}**")
            p = st.number_input(f"{comp}", value=PRESETS_HIGH.get(comp, 500), key=comp, label_visibility="collapsed")
            prices[comp] = p
            total += p

sub = total + margin
gst = int(sub * 0.18)
grand = sub + gst
total_bid = grand * qty

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Cost", f"₹{total:,}")
c2.metric("Grand / PC", f"₹{grand:,}")
c3.metric("Total Bid", f"₹{total_bid:,}")
c4.metric("Shown", f"{len(detected)}/22")

df = pd.DataFrame(list(prices.items()), columns=["Component (ATC)", "Cost"])
st.dataframe(df, use_container_width=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button("📥 Download Excel", to_excel(df), file_name=f"ATC_{dept}_{grand}.xlsx", type="primary", use_container_width=True)