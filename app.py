import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="GeM Bid Pro", page_icon="🇮🇳", layout="wide")

# --- PREMIUM CSS ---
st.markdown("""
<style>
   .main-header {background: linear-gradient(90deg, #0f172a 0%, #1e40af 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;}
   .metric-card {background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #1e40af; text-align: center;}
   .comp-card {background: #f8fafc; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 10px;}
   .stNumberInput {background: white;}
    div[data-testid="stSidebar"] {background-color: #f1f5f9;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🇮🇳 GeM Bid Pro - Premium Costing Tool</h1><p>Only 22 Components | Auto Pricing by Category</p></div>', unsafe_allow_html=True)

COMPONENTS_22 = [
    "Processor CPU", "MB", "Graphics CARD", "OS", "RAM", "SSD",
    "SSD (SECONDARY)", "Cabinet LTR", "SMPS WATT", "ADAPTER",
    "DVD WRITER", "MONITOR", "SPEAKER", "WIRELESS + BLUETOOTH",
    "MS OFFICE", "CHASSIS SWITCH", "TPM 2.0", "CAMERA",
    "ANTIVIRUS", "DP PORT", "SERIAL COM PORT+PARALLEL", "Keyboard & Mouse"
]

PRESETS = {
    "Entry and Mid Level": {"Processor CPU": 10500, "MB": 3800, "Graphics CARD": 0, "OS": 600, "RAM": 4500, "SSD": 2500, "SSD (SECONDARY)": 0, "Cabinet LTR": 1500, "SMPS WATT": 0, "ADAPTER": 0, "DVD WRITER": 0, "MONITOR": 3800, "SPEAKER": 0, "WIRELESS + BLUETOOTH": 0, "MS OFFICE": 0, "CHASSIS SWITCH": 0, "TPM 2.0": 700, "CAMERA": 0, "ANTIVIRUS": 0, "DP PORT": 0, "SERIAL COM PORT+PARALLEL": 0, "Keyboard & Mouse": 350},
    "High End Desktop": {"Processor CPU": 14500, "MB": 4250, "Graphics CARD": 0, "OS": 600, "RAM": 17500, "SSD": 3650, "SSD (SECONDARY)": 11500, "Cabinet LTR": 1850, "SMPS WATT": 0, "ADAPTER": 0, "DVD WRITER": 0, "MONITOR": 4450, "SPEAKER": 0, "WIRELESS + BLUETOOTH": 0, "MS OFFICE": 0, "CHASSIS SWITCH": 0, "TPM 2.0": 700, "CAMERA": 0, "ANTIVIRUS": 0, "DP PORT": 0, "SERIAL COM PORT+PARALLEL": 0, "Keyboard & Mouse": 350},
    "All in One": {"Processor CPU": 16500, "MB": 5000, "Graphics CARD": 0, "OS": 600, "RAM": 8500, "SSD": 4500, "SSD (SECONDARY)": 0, "Cabinet LTR": 0, "SMPS WATT": 0, "ADAPTER": 0, "DVD WRITER": 0, "MONITOR": 0, "SPEAKER": 0, "WIRELESS + BLUETOOTH": 500, "MS OFFICE": 0, "CHASSIS SWITCH": 0, "TPM 2.0": 700, "CAMERA": 500, "ANTIVIRUS": 0, "DP PORT": 0, "SERIAL COM PORT+PARALLEL": 0, "Keyboard & Mouse": 350}
}

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7d/Government_e_Marketplace_Logo.png", width=150)
    st.subheader("📋 Bid Info")
    bid_no = st.text_input("GEM BID NO", "GEM/2026/B/7936262")
    dept = st.selectbox("🏛️ Department", ["DEPT OF FINANCIAL SERVICES","SBI","PNB","ARMY","NAVY","OTHER"])
    category = st.selectbox("🖥️ Item Category", list(PRESETS.keys()), index=1)
    focus_comp = st.selectbox("🔧 Focus Component (22 List)", COMPONENTS_22)
    qty = st.number_input("Quantity", 1, 1000, 65)
    margin = st.number_input("Company Margin", 4000)

preset = PRESETS[category]
prices = {}
total_cost = 0

tab1, tab2 = st.tabs(["💻 Components Costing (22 Only)", "📊 Summary & Export"])

with tab1:
    st.markdown(f"#### Category: **{category}** | Focus: **{focus_comp}**")
    cols = st.columns(4)
    for i, comp in enumerate(COMPONENTS_22):
        with cols[i % 4]:
            with st.container(border=True):
                icon = "⭐" if comp == focus_comp else "🔹"
                st.markdown(f"**{icon} {comp}**")
                default = preset.get(comp, 0)
                price = st.number_input(f"Price {comp}", value=default, label_visibility="collapsed", key=f"p_{comp}")
                prices[comp] = price
                total_cost += price
                if price > 0:
                    st.caption(f"₹{price:,}")

with tab2:
    sub_total = total_cost + margin
    gst = int(sub_total * 0.18)
    grand = sub_total + gst
    total_bid = grand * qty

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cost", f"₹{total_cost:,}")
    c2.metric("Sub Total", f"₹{sub_total:,}")
    c3.metric("Grand Total", f"₹{grand:,}", delta="18% GST")
    c4.metric("Total Bid Value", f"₹{total_bid:,}")

    st.divider()
    colA, colB = st.columns([2,1])
    with colA:
        df = pd.DataFrame(list(prices.items()), columns=["Component", "Price"])
        df = df[df["Price"] > 0]
        st.dataframe(df, use_container_width=True, hide_index=True)
    with colB:
        st.markdown("##### 📄 Bid Summary")
        st.code(f"BID: {bid_no}\nDept: {dept}\nCategory: {category}\nQty: {qty}\nGrand: {grand}\nTotal: {total_bid:,}")
        def to_excel(df_full):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_full.to_excel(writer, index=False)
            return output.getvalue()

        df_export = pd.DataFrame({"Item": list(prices.keys())+["Margin","GST","Grand Total"], "Value": list(prices.values())+[margin,gst,grand]})
        st.download_button("📥 Download Premium Excel", to_excel(df_export), file_name=f"GeM_Premium_{category}_{grand}.xlsx", type="primary", use_container_width=True)