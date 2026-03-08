import streamlit as st
import pandapower as pp
import pandas as pd

# --- 1. WEB PAGE HEADER ---
st.title("⚡ Micro-Grid Hosting Capacity Analyzer")
st.write("Adjust transformer capacity, neighborhood size, and solar installations to evaluate grid safety.")

# --- 2. SIDEBAR INPUTS ---
st.sidebar.header("1. Grid Parameters")
xfmr_kva = st.sidebar.number_input("Transformer Capacity (kVA)", min_value=10.0, max_value=100.0, value=25.0, step=1.0)
num_houses = st.sidebar.slider("Number of Houses", min_value=1, max_value=25, value=1, step=1)

st.sidebar.header("2. Solar Installations (kW)")
st.sidebar.write("Enter the max inverter export for each house:")

# Dynamically generate input boxes based on the slider!
solar_inputs = []
for i in range(1, num_houses + 1):
    kw = st.sidebar.number_input(f"House {i} Solar (kW)", min_value=0.0, max_value=9999.0, value=0.0, step=0.5)
    solar_inputs.append(kw)

# --- 3. THE ENGINEERING ENGINE ---
def run_simulation(xfmr_kVA, houses, solar_kW_list):
    net = pp.create_empty_network()
    vn_kv = 0.24
    
    # Grid & Transformer
    bus_hv = pp.create_bus(net, vn_kv=11.0, name="HV Grid")
    pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0)
    bus_lv_main = pp.create_bus(net, vn_kv=vn_kv, name="Transformer LV")
    
    # Notice we divide by 1000 to convert kVA to MVA!
    pp.create_transformer_from_parameters(
        net, hv_bus=bus_hv, lv_bus=bus_lv_main, 
        sn_mva=xfmr_kVA / 1000.0, 
        vn_hv_kv=11.0, vn_lv_kv=vn_kv,
        vkr_percent=1.5, vk_percent=4.0, pfe_kw=0.05, i0_percent=0.1,
        name=f"{xfmr_kVA}kVA Trafo"
    )
    
    # Build Houses & Solar
    for i in range(houses):
        b_idx = pp.create_bus(net, vn_kv=vn_kv, name=f"House {i+1}")
        
        pp.create_line_from_parameters(
            net, from_bus=bus_lv_main, to_bus=b_idx, 
            length_km=0.04, r_ohm_per_km=1.32, x_ohm_per_km=0.08,
            c_nf_per_km=0, max_i_ka=0.15, name=f"Line {i+1}"
        )
        
        # Only add a solar generator if the user typed a number > 0
        if solar_kW_list[i] > 0:
            pp.create_sgen(net, bus=b_idx, p_mw=solar_kW_list[i] / 1000.0, name=f"Solar {i+1}")
            
    pp.runpp(net)
    return net

# --- 4. RUNNING THE ANALYSIS & DISPLAYING RESULTS ---
if st.button("🚀 Run Grid Analysis"):
    with st.spinner("Calculating power flow..."):
        net = run_simulation(xfmr_kva, num_houses, solar_inputs)
        
        # Extract Results
        loading = net.res_trafo['loading_percent'].values[0]
        max_v = net.res_bus['vm_pu'].max()
        
        st.subheader("📊 Simulation Results")
        
        # Streamlit metrics look like professional dashboard widgets
        col1, col2 = st.columns(2)
        col1.metric("Transformer Loading", f"{loading:.2f}%")
        col2.metric("Max System Voltage", f"{max_v:.3f} pu")
        
        # The Engineering Logic Gate
        if loading > 100 or max_v > 1.05:
            st.error("🚨 SYSTEM FAIL: Violations Detected! Transformer overload or overvoltage.")
        else:
            st.success("✅ SYSTEM PASS: Grid is operating within safe limits.")
            
        st.write("---")
        st.write("**Detailed Bus Voltages:**")
        # Display the pandas dataframe right on the web page
        st.dataframe(net.res_bus[['vm_pu', 'p_mw', 'q_mvar']])


# --- 5. VISUALIZING THE VOLTAGE PROFILE (Upgraded with Plotly!) ---
        st.write("---")
        st.subheader("📈 House Voltage Profile (Interactive)")

        # Prepare the DataFrame as before
        bus_voltages = pd.DataFrame({
            'Bus Name': net.bus['name'],
            'Voltage (pu)': net.res_bus['vm_pu']
        })
        house_voltages = bus_voltages[bus_voltages['Bus Name'].str.contains("House")].copy()

        # Switch to Plotly Express for a professional, interactive chart
        import plotly.express as px

        fig = px.bar(
            house_voltages, 
            x='Bus Name', 
            y='Voltage (pu)', 
            title='Voltage Rise Along the Street',
            color='Voltage (pu)', # Color bars dynamically based on voltage!
            color_continuous_scale='Reds', # Higher voltage = Redder bar
            range_color=[1.0, 1.05] # Scale color from nominal to limit
        )

        # --- THE CRITICAL FIX: ZOOOMING IN THE Y-AXIS ---
        # We manually set the axis to magnify the difference from nominal.
        # Starting at 0.99 (just under nominal) and stopping at 1.06 (over the limit).
        fig.update_yaxes(range=[0.99, 1.06])

        # Add reference lines for engineering context
        # 1. Nominal Voltage (1.0 pu)
        fig.add_hline(y=1.0, line_dash="dash", line_color="green", annotation_text="Nominal (1.0 pu)")
        # 2. Upper Limit (1.05 pu)
        fig.add_hline(y=1.05, line_dash="dash", line_color="red", annotation_text="Upper Limit (1.05 pu)")

        # Display the interactive Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        st.caption("This chart has been zoomed in on the Y-axis to clearly show the Voltage Rise at each house. High solar injection causes the voltage to stack up at the end of the line.")

# To run the script "streamlit run app.py"  streamlit run yourscript.py
