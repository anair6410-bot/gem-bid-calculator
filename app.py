import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="GeM Bid", page_icon="🇮🇳", layout="wide")
st.title("🇮🇳 GeM Bid - Costing Calculator")

with st.sidebar:
    st.header("📋 Bid Details")
    bid_no = st.text_input("GEM BID NO", "GEM/2026/B/7936262")

    dept = st.selectbox(
        "🏛️ Department",
        ["DEPT OF FINANCIAL SERVICES","MINISTRY OF FINANCE","MINISTRY OF DEFENCE","MINISTRY OF HOME AFFAIRS","MINISTRY OF EDUCATION","MINISTRY OF RAILWAYS","STATE BANK OF INDIA (SBI)","PUNJAB NATIONAL BANK (PNB)","BANK OF BARODA","CANARA BANK","RBI","LIC","INDIAN ARMY","INDIAN NAVY","INDIAN AIR FORCE","CRPF","BSF","DRDO","OTHER"],
    )
    if dept == "OTHER":
        dept = st.text_input("Enter Department", "DEPT OF FINANCIAL SERVICES")

    location = st.selectbox(
        "📍 Location",
        ["DHANBAD","RANCHI","JAMSHEDPUR","BOKARO","KOLKATA","PATNA","DELHI","MUMBAI","OTHER"],
        index=0
    )
    if location == "OTHER":
        location = st.text_input("Enter Location", "DHANBAD")

    # --- NEW ITEM CATEGORY DROPDOWN BELOW LOCATION ---
    category = st.selectbox(
        "🖥️ Item Category",
        [
            "Entry Level Desktop Computer",
            "Mid Level Desktop Computer", 
            "High End Desktop Computer",
            "All in One Desktop Computer",
            "Workstation",
            "Thin Client"
        ],
        index=2  # Default High End
    )
    
    qty = st.number_input("Quantity", 1, 1000, 65)

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Component Costing - {category}")
    cpu = st.number_input("CPU i5 14400", 14500)
    mb = st.number_input("MB H610", 4250)
    os_cost = st.number_input("OS WIN 11 PRO", 600)
    ram = st.number_input("RAM 16GB DDR5", 17500)
    ssd1 = st.number_input("SSD 256GB NVME", 3650)
    ssd2 = st.number_input("SSD 1TB SATA", 11500)
    cabinet = st.number_input("Cabinet", 1850)
    monitor = st.number_input("Monitor 21.5 IPS", 4450)
    tpm = st.number_input("TPM 2.0", 700)
    kbd = st.number_input("KBD+Mouse", 350)
    warranty = st.number_input("Warranty 3Y", 600)
    freight = st.number_input("Freight", 300)
    other = st.number_input("Other", 550)

with col2:
    total_cost = cpu+mb+os_cost+ram+ssd1+ssd2+cabinet+monitor+tpm+kbd+warranty+freight+other
    margin = st.number_input("Company Margin", 4000)
    sub_total = total_cost + margin
    gst = int(sub_total * 0.18)
    grand = sub_total + gst
    st.divider()
    st.metric("TOTAL COST", f"Rs. {total_cost}")
    st.metric("GST 18%", f"Rs. {gst}")
    st.success(f"GRAND TOTAL = Rs. {grand}")
    st.info(f"{category} | {dept} | {location} | Total = Rs. {grand*qty:,}")

# Excel
st.divider()
data = {"Particulars": ["BID NO","Department","Location","Item Category","Qty","TOTAL COST","Margin","Sub Total","GST","GRAND TOTAL","Total Value"], "Value": [bid_no,dept,location,category,qty,total_cost,margin,sub_total,gst,grand,grand*qty]}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button("📥 Download Excel", to_excel(df), file_name=f"GeM_Bid_{category[:4]}_{location}_{grand}.xlsx", use_container_width=True)