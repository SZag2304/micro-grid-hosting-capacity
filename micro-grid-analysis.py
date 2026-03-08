
import pandapower as pp

net = pp.create_empty_network()
vn_kv = 0.24 # Voltage level in kV

# External Grid
bus_hv = pp.create_bus(net, vn_kv=11.0, name="HV Grid") # Assuming 11 kV for primary side
pp.create_ext_grid(net, bus=bus_hv, vm_pu=1.0)

# Grid Bus
bus_lv_main = pp.create_bus(net, vn_kv=vn_kv, name="Transformer LV Bus")

# Creating the 25KVA Transformer
pp.create_transformer_from_parameters(
    net, 
    hv_bus=bus_hv, 
    lv_bus=bus_lv_main,
    sn_mva=0.033,       # 25 kVA rating
    vn_hv_kv=11.0,      # Primary side voltage
    vn_lv_kv=vn_kv,     # Secondary side voltage
    vkr_percent=1.5,    # Estimated resistive losses
    vk_percent=4.0,     # Estimated short-circuit voltage
    pfe_kw=0.05,         # Iron losses
    i0_percent=0.1,     # Open-loop current
    name="25KVA xfmr"
)

# Create the loop for busses for the houses
house_buses = []

for i in range(1, 7):  # Create 6 houses
    bus_idx = pp.create_bus(net, vn_kv=vn_kv, name=f"House {i} Bus")

    house_buses.append(bus_idx)

    # Connect each house bus to the main grid bus with a line
    pp.create_line_from_parameters(
        net, 
        from_bus=bus_lv_main,
        to_bus=bus_idx,
        length_km=0.04,      # Assuming 40 meters between the transformer and each house
        r_ohm_per_km=1.32,   # Resistance per km for 16 mm² conductor
        x_ohm_per_km=0.08,   # Reactance per km for 16 mm² conductor
        c_nf_per_km=0.0,     # Capacitance per km for 16 mm² conductor is negligible
        max_i_ka=0.15,       # Maximum current for the line 150 Amps limit
        name=f"Line to House {i}"
    )

# Create Solar generation
pp.create_sgen(net, bus=house_buses[0], p_mw=0.0075, name=f"Solar Gen House for House 1")
pp.create_sgen(net, bus=house_buses[1], p_mw=0.010, name=f"Solar Gen House for House 2")
pp.create_sgen(net, bus=house_buses[2], p_mw=0.0115, name=f"Solar Gen House for House 3 (new)")

# Run Power Flow Analysis
# Execute the Newton-Raphson Power Flow
pp.runpp(net)

# Check the Transformer Loading
print("--- TRANSFORMER STATUS ---")
print(net.res_trafo[['loading_percent']])

# Check the House Voltages
print("\n--- HOUSE VOLTAGES (pu) ---")
print(net.res_bus[['vm_pu']])