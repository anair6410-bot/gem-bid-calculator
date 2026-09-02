import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="GeM Bid", page_icon="🇮🇳", layout="wide")
st.title("🇮🇳 GeM Bid - 22 Components Costing")

# YOUR 22 COMPONENTS ONLY
COMPONENTS_22 = [
    "Processor CPU", "MB", "Graphics CARD", "OS", "RAM", "SSD",
    "SSD (SECONDARY)", "Cabinet LTR", "SMPS WATT", "ADAPTER",
    "DVD WRITER", "MONITOR", "SPEAKER", "WIRELESS + BLUETOOTH",
    "MS OFFICE", "CHASSIS SWITCH", "TPM 2.0", "CAMERA",
    "ANTIVIRUS", "DP PORT", "SERIAL COM PORT+PARALLEL", "Keyboard & Mouse"
]

# AUTO PRICING BY YOUR SHEET LOGIC
PRESETS = {
    "Entry and Mid Level Desktop Computers": {
        "Processor CPU": 10500, "MB": 3800, "Graphics CARD": 0, "OS": 600, "RAM": 4500, "SSD": 2500,
        "SSD (SECONDARY)": 0, "Cabinet LTR": 1500, "SMPS WATT": 0, "ADAPTER": 0, "DVD WRITER": 0,
        "MONITOR": 3800, "SPEAKER": 0, "WIRELESS + BLUETOOTH": 0, "MS OFFICE": 0, "CHASSIS SWITCH": 0,
        "TPM 2.0": 700, "CAMERA": 0, "ANTIVIRUS": 0, "DP PORT": 0, "SERIAL COM PORT+PARALLEL": 0, "Keyboard & Mouse": 350
    },
    "High End Desktop Computer": {
        "Processor CPU": 14500, "MB": 4250, "Graphics CARD": 0, "OS": 600, "RAM": 17500, "SSD": 3650,
        "SSD (SECONDARY)": 11500, "Cabinet LTR": 1850, "SMPS WATT": 0, "ADAPTER": 0, "DVD WRITER": 0,
        "MONITOR": 4450, "SPEAKER": 0, "WIRELESS + BLUETOOTH": 0, "MS OFFICE": 0, "CHASSIS SWITCH": 0,
        "TPM 2.0": 700, "CAMERA": 0, "ANTIVIRUS": 0, "DP PORT": 0, "SERIAL COM PORT+PARALLEL": 0, "Keyboard & Mouse": 350
    },
    "All in One Desktop Computer": {
        "Processor CPU": 16500, "MB": 5000, "Graphics CARD": 0, "OS": 600, "RAM": 8500, "SSD": 4500,
        "SSD (SECONDARY)": 0, "Cabinet LTR": 0, "SMPS WATT": 0, "ADAPTER": 0, "DVD WRITER": 0,
        "MONITOR": 0, "SPEAKER": 0, "WIRELESS + BLUETOOTH": 500, "MS OFFICE": 0, "CHASSIS SWITCH": 0,
        "TPM 2.0": 700, "CAMERA": 500, "ANTIVIRUS": 0, "DP PORT": 0, "SERIAL COM PORT+PARALLEL": 0, "Keyboard & Mouse": 350
    }
}

with st.sidebar:
    st.header("📋 Bid Details")
    bid_no = st.text_input("GEM BID NO", "GEM/2026/B/7936262")
    dept = st.selectbox("🏛️ Department", ["DEPT OF FINANCIAL SERVICES","MINISTRY OF FINANCE","MINISTRY OF DEFENCE","SBI","PNB","INDIAN ARMY","INDIAN NAVY","OTHER"])
    location = st.selectbox("📍 Location", ["DHANBAD","RANCHI","JAMSHEDPUR","KOLKATA","DELHI","MUMBAI","OTHER"])

    # ITEM CATEGORY DROPDOWN
    category = st.selectbox("🖥️ Item Category", list(PRESETS.keys()), index=1)

    # COMPONENT DROPDOWN - ONLY 22
    selected_comp = st.selectbox("🔧 Select Component to Edit (22 List)", COMPONENTS_22)

    qty = st.number_input("Quantity", 1, 1000, 65)

st.info(f"Category: **{category}** | Editing: **{selected_comp}** | Showing all 22 components below with auto-price")

# Get preset for category
preset = PRESETS[category]
total_cost = 0
prices = {}

col1, col2, col3 = st.columns(3)
for i, comp in enumerate(COMPONENTS_22):
    with [col1, col2, col3][i % 3]:
        # Auto price from category
        default_price = preset.get(comp, 0)
        # Highlight selected component
        if comp == selected_comp:
            price = st.number_input(f"👉 {comp}", value=default_price, key=comp, help="Selected Component")
        else:
            price = st.number_input(f"{comp}", value=default_price, key=comp)
        prices[comp] = price
        total_cost += price

with st.sidebar:
    st.divider()
    margin = st.number_input("Company Margin", 4000)
    sub_total = total_cost + margin
    gst = int(sub_total * 0.18)
    grand = sub_total + gst
    st.success(f"GRAND TOTAL: Rs. {grand}")
    st.write(f"Total Bid: Rs. {grand*qty:,}")

# Summary
st.divider()
st.subheader(f"Costing Summary - {category}")
df = pd.DataFrame(list(prices.items()), columns=["Component (22 Only)", "Price"])
df.loc[len(df)] = ["TOTAL COST", total_cost]
df.loc[len(df)] = ["Company Margin", margin]
df.loc[len(df)] = ["GST 18%", gst]
df.loc[len(df)] = ["GRAND TOTAL", grand]
st.dataframe(df, use_container_width=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button("📥 Download Excel - 22 Components", to_excel(df), file_name=f"GeM_Bid_{category[:4]}_{grand}.xlsx", use_container_width=True)