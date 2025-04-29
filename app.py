import streamlit as st

def solar_design(peak_load_kw, offpeak_load_kw, sun_hours, usage_type, battery_voltage=48):
    peak_hours = 4 if usage_type == "Domestic" else 6
    offpeak_hours = 20 if usage_type == "Domestic" else 18

    total_daily_load = (peak_load_kw * peak_hours) + (offpeak_load_kw * offpeak_hours)
    required_kw = total_daily_load / sun_hours
    panel_count = int((required_kw * 1000) / 400)  # 400W panels assumed
    inverter_size_kw = peak_load_kw * 1.5

    battery_backup_kwh = offpeak_load_kw * offpeak_hours
    battery_capacity_ah = (battery_backup_kwh * 1000) / battery_voltage
    battery_count = int(battery_capacity_ah / 200)  # 200Ah batteries assumed

    # Costing
    panel_cost = panel_count * 150
    inverter_cost = inverter_size_kw * 300
    battery_cost = battery_count * 250
    structure_cost = panel_count * 50
    misc_cost = 0.15 * (panel_cost + inverter_cost + battery_cost + structure_cost)
    total_cost = panel_cost + inverter_cost + battery_cost + structure_cost + misc_cost

    return {
        "required_kw": required_kw,
        "panel_count": panel_count,
        "inverter_size_kw": inverter_size_kw,
        "battery_count": battery_count,
        "total_cost": total_cost,
        "daily_energy_kwh": total_daily_load
    }

def calculate_roi(total_cost, daily_savings, lifespan_years=25):
    annual_savings = daily_savings * 365
    payback_years = total_cost / annual_savings if annual_savings else float('inf')
    total_roi = (annual_savings * lifespan_years) - total_cost
    return {
        "annual_savings": annual_savings,
        "payback_years": payback_years,
        "total_roi": total_roi
    }

st.set_page_config(page_title="Solar Estimator with ROI", page_icon="🌞")

st.title("🌞 Solar System Estimator + ROI (Domestic & Industrial)")

usage_type = st.radio("Select Usage Type:", ["Domestic", "Industrial"])
st.markdown("### 🔌 Load Inputs")
peak_load_kw = st.number_input("Peak Hour Load (kW)", min_value=0.1, value=2.0)
offpeak_load_kw = st.number_input("Off-Peak Hour Load (kW)", min_value=0.1, value=1.0)
sun_hours = st.slider("Average Sunlight Hours", 3.0, 8.0, 5.0, step=0.5)

st.markdown("### ⚡ Electricity Tariff")
tariff = st.number_input("Your Electricity Tariff ($/kWh)", min_value=0.01, value=0.15, step=0.01)

if st.button("Estimate System & ROI"):
    result = solar_design(peak_load_kw, offpeak_load_kw, sun_hours, usage_type)
    daily_savings = result["daily_energy_kwh"] * tariff
    roi_result = calculate_roi(result["total_cost"], daily_savings)

    st.subheader("🔋 System Design")
    st.write(f"Required Solar Capacity: **{result['required_kw']:.2f} kW**")
    st.write(f"Number of Solar Panels (400W): **{result['panel_count']}**")
    st.write(f"Inverter Size: **{result['inverter_size_kw']:.2f} kW**")
    st.write(f"Batteries (200Ah): **{result['battery_count']}**")

    st.subheader("💰 Cost Estimate")
    st.write(f"Estimated System Cost: **${result['total_cost']:,.2f}**")

    st.subheader("📈 ROI Calculation")
    st.write(f"Estimated Daily Energy Generation: **{result['daily_energy_kwh']:.2f} kWh**")
    st.write(f"Daily Savings: **${daily_savings:.2f}**")
    st.write(f"Annual Savings: **${roi_result['annual_savings']:,.2f}**")
    st.write(f"💸 Payback Period: **{roi_result['payback_years']:.1f} years**")
    st.write(f"📊 25-Year ROI: **${roi_result['total_roi']:,.2f}**")
