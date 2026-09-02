import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="GeM Bid Costing", page_icon="🇮🇳", layout="wide")
st.title("🇮🇳 GeM Bid Costing Calculator - Desktop Computers")
st.caption("BID 7936262 Logic - Grand Total 76,464")

# Sidebar - Bid Details
with st.sidebar:
    st.header("📋 Bid Details")
    bid_no = st.text_input("GEM BID NO", "GEM/2026/B/7936262")
    dept = st.text_input("Department", "DEPT OF FINANCIAL SERVICES")
    
    # LOCATION DROPDOWN
    location = st.selectbox(
        "📍 Select Location",
        ["DHANBAD", "RANCHI", "JAMSHEDPUR", "BOKARO", "DEOGHAR", "HAZARIBAGH", "KOLKATA", "PATNA", "DELHI", "MUMBAI", "OTHER"],
        index=0
    )
    if location == "OTHER":
        location = st.text_input("Enter Custom Location", "DHANBAD")
    
    qty = st.number_input("Quantity", 1, 1000, 65)

# Main Costing
col1, col2 = st.columns(2)
with col1:
    st.subheader("Component Costing")
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
    other = st.number_input("Other (Non-HDD+Late)", 550)

with col2:
    total_cost = cpu+mb+os_cost+ram+ssd1+ssd2+cabinet+monitor+tpm+kbd+warranty+freight+other
    margin = st.number_input("Company Margin", 4000)
    sub_total = total_cost + margin
    gst = int(sub_total * 0.18)
    grand = sub_total + gst
    
    st.divider()
    st.metric("TOTAL COST", f"Rs. {total_cost}")
    st.metric("SUB TOTAL", f"Rs. {sub_total}")
    st.metric("GST 18%", f"Rs. {gst}")
    st.success(f"### GRAND TOTAL = Rs. {grand}")
    st.info(f"For {qty} Units at {location} = Rs. {grand*qty:,}")
    
    if grand == 76464:
        st.write("✅ Matched with your paper: 76464")

# Excel Save Section
st.divider()
st.subheader(f"📊 Data Preview - {location}")

data = {
    "Particulars": ["GEM BID NO", "Department", "Location", "Quantity", "TOTAL COST", "Company Margin", "Sub Total", "GST 18%", "GRAND TOTAL (BID PRICE)", "Total Bid Value"],
    "Value": [bid_no, dept, location, qty, total_cost, margin, sub_total, gst, grand, grand*qty]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Costing')
    return output.getvalue()

st.download_button(
    label="📥 Download Excel File",
    data=to_excel(df),
    file_name=f"{location}_{grand}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)