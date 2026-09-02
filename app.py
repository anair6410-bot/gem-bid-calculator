import streamlit as st

st.set_page_config(page_title="GeM Bid Costing Calculator", page_icon="🇮🇳", layout="wide")
st.title("🇮🇳 GeM Bid Costing Calculator - Desktop Computers")
st.caption("As per your Dhanbad Sheet - BID 7936262")

# Sidebar
with st.sidebar:
    st.header("📋 Bid Details")
    bid_no = st.text_input("GEM BID NO", "GEM/2026/B/7936262")
    dept = st.text_input("Department", "DEPT OF FINANCIAL SERVICES")
    location = st.text_input("Location", "DHANBAD")
    qty = st.number_input("Quantity", 1, 1000, 65)

# Costing
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
    st.metric("SUB TOTAL (with Margin)", f"Rs. {sub_total}")
    st.metric("GST 18%", f"Rs. {gst}")
    st.success(f"### GRAND TOTAL / BID PRICE = Rs. {grand}")
    st.info(f"For {qty} Units = Rs. {grand*qty:,}")

    if grand == 76464:
        st.balloons()
        st.write("✅ Matched with your paper: 76464")