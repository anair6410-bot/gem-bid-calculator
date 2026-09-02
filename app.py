import streamlit as st
import pandas as pd
from io import BytesIO
import fitz # PyMuPDF
import docx
import re

st.set_page_config(page_title="GeM ATC Pro", page_icon="🇮🇳", layout="wide")

# --- PREMIUM CSS ---
st.markdown("""
<style>
.main-header {background: linear-gradient(90deg, #0f172a 0%, #1e40af 100%); padding: 22px; border-radius: 15px; color: white; text-align: center; margin-bottom:20px;}
div[data-testid="stSidebar"] {background-color: #f1f5f9;}
.metric {background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🇮🇳 GeM Bid - UNIVERSAL SMART ATC READER</h1><p>Upload Any ATC PDF → Auto Detects Components from your 22 List</p></div>', unsafe_allow_html=True)

# YOUR 22 COMPONENTS WITH KEYWORDS
COMPONENT_KEYWORDS = {
    "Processor CPU": ["processor", "cpu", "intel core", "i3", "i5", "i7", "ryzen", "14th gen", "14400", "7600"],
    "MB": ["motherboard", "baseboard", "chipset", "h610", "b760", "mainboard"],
    "Graphics CARD": ["graphics", "gpu", "uhd graphics", "radeon", "integrated graphics"],
    "OS": ["operating system", "windows", "win 11", "os", "windows 11 pro"],
    "RAM": ["ram", "system memory", "ddr4", "ddr5", "16 gb", "memory"],
    "SSD": ["ssd", "nvme", "storage type", "256 gb", "512 gb ssd", "solid state"],
    "SSD (SECONDARY)": ["secondary", "1 tb", "sata ssd", "hdd", "2nd storage"],
    "Cabinet LTR": ["cabinet", "chassis type", "tower", "sff", "form factor"],
    "SMPS WATT": ["smps", "power supply", "power"],
    "ADAPTER": ["adapter"],
    "DVD WRITER": ["dvd", "optical drive"],
    "MONITOR": ["monitor", "display", "21.5", "24 inch", "screen", "1920x1080", "ips"],
    "SPEAKER": ["speaker", "audio", "hd audio"],
    "WIRELESS + BLUETOOTH": ["wireless", "bluetooth", "wifi", "wireless + bluetooth"],
    "MS OFFICE": ["ms office", "microsoft office", "office 2021"],
    "CHASSIS SWITCH": ["chassis intrusion", "intrusion switch", "chassis switch"],
    "TPM 2.0": ["tpm", "trusted platform", "tpm 2.0"],
    "CAMERA": ["webcam", "camera", "hd webcam"],
    "ANTIVIRUS": ["antivirus"],
    "DP PORT": ["hdmi", "dp port", "display port", "hdmi port"],
    "SERIAL COM PORT+PARALLEL": ["serial port", "com port", "parallel", "rs232"],
    "Keyboard & Mouse": ["keyboard", "mouse", "kbd & mouse", "104 keys"]
}

PRESETS_HIGH = {"Processor CPU":14500, "MB":4250, "Graphics CARD":0, "OS":600, "RAM":17500, "SSD":3650, "SSD (SECONDARY)":11500, "Cabinet LTR":1850, "SMPS WATT":0, "ADAPTER":0, "DVD WRITER":0, "MONITOR":4450, "SPEAKER":0, "WIRELESS + BLUETOOTH":0, "MS OFFICE":0, "CHASSIS SWITCH":0, "TPM 2.0":700, "CAMERA":500, "ANTIVIRUS":0, "DP PORT":0, "SERIAL COM PORT+PARALLEL":0, "Keyboard & Mouse":350}

def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
    elif file.name.endswith(".docx"):
        d = docx.Document(file)
        text = "\n".join([p.text for p in d.paragraphs])
    else:
        text = file.read().decode("utf-8", errors="ignore")
    return text.lower()

def detect_components(atc_text):
    found = []
    for comp, kws in COMPONENT_KEYWORDS.items():
        for kw in kws:
            if kw in atc_text:
                found.append(comp)
                break
    return sorted(list(set(found)))

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7d/Government_e_Marketplace_Logo.png", width=140)
    st.subheader("📤 STEP 1: Upload ATC")
    atc_file = st.file_uploader("Upload BID ATC (PDF/DOCX)", type=["pdf","docx","txt"])

    st.divider()
    st.subheader("📋 STEP 2: Bid Details")
    dept = st.text_input("Department", "BANK OF INDIA")
    bid_no = st.text_input("Bid No", "GEM/2026/B/7936262")
    qty = st.number_input("Qty", 1, 1000, 65)
    margin = st.number_input("Your Margin", 4000)

    if atc_file:
        st.success(f"File: {atc_file.name}")

# --- MAIN LOGIC ---
if atc_file:
    atc_text = extract_text(atc_file)
    detected = detect_components(atc_text)
    if not detected:
        st.warning("No components matched. Your PDF might be scanned image. Showing all 22.")
        detected = list(COMPONENT_KEYWORDS.keys())
else:
    st.info("👆 Upload ATC PDF to auto-filter. Example: BOI ATC will show 16-18 components only.")
    detected = list(COMPONENT_KEYWORDS.keys())
    atc_text = ""

# Show result
if atc_file:
    col1, col2, col3 = st.columns(3)
    col1.metric("📄 ATC Detected", f"{len(detected)} Components")
    col2.metric("📦 Total 22 List", "22 Components")
    col3.metric("🤖 Filtered Out", f"{22-len(detected)} Hidden")

    with st.expander(f"👁️ View Detected Components List from {atc_file.name}"):
        st.write(", ".join(detected))

    with st.expander("📝 View ATC Extracted Text (First 8000 chars)"):
        st.text(atc_text[:8000])

st.subheader(f"💻 Costing - Showing ONLY {len(detected)} Components from ATC")

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
            if p>0:
                st.caption(f"₹{p:,}")

# TOTALS
sub = total + margin
gst = int(sub * 0.18)
grand = sub + gst
total_bid = grand * qty

st.divider()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Cost", f"₹{total:,}")
c2.metric("Grand Total / PC", f"₹{grand:,}", delta="18% GST")
c3.metric("Total Bid Value", f"₹{total_bid:,}")
c4.metric("Components Shown", f"{len(detected)} / 22")

df = pd.DataFrame(list(prices.items()), columns=["Component (Auto-Detected from ATC)", "Your Cost"])
df.loc[len(df)] = ["TOTAL COST", total]
df.loc[len(df)] = ["MARGIN", margin]
df.loc[len(df)] = ["GST 18%", gst]
df.loc[len(df)] = ["GRAND TOTAL", grand]
df.loc[len(df)] = ["TOTAL BID VALUE", total_bid]

st.dataframe(df, use_container_width=True, hide_index=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="ATC Costing")
    return output.getvalue()

st.download_button("📥 Download ATC-Based Excel (Only Detected Components)", to_excel(df), file_name=f"ATC_{dept}_{grand}.xlsx", type="primary", use_container_width=True)