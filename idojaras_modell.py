import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Layout beállítása középre
st.set_page_config(page_title="Választási Kalkulátor", layout="centered")

# Egyedi stílus a kompakt megjelenéshez és mobil nézethez
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    
    /* A metrika doboz alapjai */
    [data-testid="stMetric"] {
        border: 1px solid #e6e9ef !important;
        padding: 8px !important;
        border-radius: 5px !important;
        background-color: #fafafa !important;
        text-align: center !important;
        min-height: 80px !important;
        display: block !important;
    }

    /* A felirat (label) kényszerítése */
    [data-testid="stMetricLabel"] > div {
        font-size: 0.75rem !important;
        color: #555555 !important;
        overflow: visible !important;
        text-overflow: unset !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }

    /* A számérték (value) kényszerítése */
    [data-testid="stMetricValue"] > div {
        font-size: 1.2rem !important;
        color: #31333F !important;
        font-weight: 700 !important;
    }

    /* Oszlopok közötti rés mobilon */
    [data-testid="column"] {
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.header("🗳️ Az időjárás hatása a választási részvételre")

# --- BEÁLLÍTÁSOK ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        max_part = st.number_input("Várt részvételi arány (%)", 0.0, 100.0, 70.0, step=0.1, format="%.1f")
    with col2:
        rain = st.number_input("Várható napi csapadékösszeg (mm)", 0, 100, 0)
    
    temp = st.select_slider("Várható napi átlaghőmérséklet (°C)", 
                            options=np.arange(-15.0, 35.5, 0.5).tolist(), value=10.0)

# --- MATEMATIKAI SZÁMÍTÁSOK ---
peak_temp = 4.9943
def calc_temp_p(t):
    # A tanulmány 6. modellje alapján: 0.002625*T - 0.0002628*T^2
    raw = (-0.0002628 * (t**2)) + (0.002625 * t)
    peak_raw = (-0.0002628 * (peak_temp**2)) + (0.002625 * peak_temp)
    return (raw - peak_raw) * 100

def calc_rain_p(r):
    # A tanulmány alapján: -0.0009251 * mm
    return (-0.0009251 * r) * 100

c_temp_p = calc_temp_p(temp)
c_rain_p = calc_rain_p(rain)
total_res = max_part + c_temp_p + c_rain_p

# --- EREDMÉNYEK ---
st.markdown("---")
m1, m2, m3 = st.columns(3)
m1.metric("Hőmérséklet hatása", f"{c_temp_p:+.2f} %")
m2.metric("Csapadék hatása", f"{c_rain_p:+.2f} %")
m3.metric("Várható részvétel", f"{total_res:.1f} %")

if temp < -3.4 or temp > 16.7 or rain > 11.9:
    st.warning("⚠️ **Figyelem:** A beállított értékek kívül esnek a tanulmányban vizsgált eredeti tartományon (-3,4°C – 16,7°C és max. 11,9 mm). Az ezen kívüli becslések statisztikailag bizonytalanabbak.")

# --- GRAFIKONOK ---
st.write("---")
g1, g2 = st.columns(2)

def style_plot(ax, title, xlabel):
    ax.set_title(title, fontsize=10, pad=8)
    ax.tick_params(labelsize=8)
    ax.grid(True, alpha=0.15)
    ax.set_xlabel(xlabel, fontsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)

with g1:
    t_axis = np.linspace(-15, 35, 100)
    y_temp = [calc_temp_p(t) for t in t_axis]
    fig1, ax1 = plt.subplots(figsize=(4, 2.5))
    ax1.plot(t_axis, y_temp, color='#1f77b4', lw=2)
    ax1.axvline(peak_temp, color='green', linestyle='--', linewidth=1, alpha=0.7)
    ax1.scatter([temp], [c_temp_p], color='red', s=60, zorder=5)
    style_plot(ax1, "Hőmérséklet hatás", "°C")
    st.pyplot(fig1)

with g2:
    r_axis = np.linspace(0, 50, 100)
    y_rain = [calc_rain_p(r) for r in r_axis]
    fig2, ax2 = plt.subplots(figsize=(4, 2.5))
    ax2.plot(r_axis, y_rain, color='#ff7f0e', lw=2)
    ax2.scatter([rain], [c_rain_p], color='red', s=60, zorder=5)
    style_plot(ax2, "Csapadék hatás", "mm")
    st.pyplot(fig2)

# --- ÖSSZEFOGLALÓ ---
st.write("### Összefoglaló a tanulmány* alapján")
st.write("""
A 2014 és 2022 közötti magyarországi választási adatokat elemző kutatás alapján:

* **Hőmérséklet:** Az összefüggés **negatív négyzetes**. Létezik egy optimális hőmérséklet (kb. **5°C**), ahol a legmagasabb a választási kedv. Ennél hidegebb időben a diszkomfort, melegebb időben pedig az alternatív szabadidős programok csökkentik a részvételt.
* **Csapadék:** A kapcsolat **lineárisan negatív**. Minden milliméternyi csapadék növeli a szavazás kényelmetlenségét, ami arányosan csökkenti a részvételt.
""")

# --- MATEMATIKAI HÁTTÉR ---
st.write("### A modell matematikai háttere")

st.write("**1. Hőmérsékleti hatás (négyzetes összefüggés):**")
st.latex(r"f(T) = 0,002625 \cdot T - 0,0002628 \cdot T^2")

st.write("**2. Csapadék hatása (lineáris összefüggés):**")
st.latex(r"\Delta Részvétel = -0,0009251 \cdot Csapadék_{mm}")

st.info("""
A fenti egyenletek a tanulmány 6. számú modelljéből származnak. 
A hőmérsékleti görbe csúcspontja 4,99°C, míg a csapadék minden millimétere 
lineárisan csökkenti a részvételi hajlandóságot.
""")

st.markdown("""
    <p style='font-size: 0.9rem; font-style: italic;'>
        Forrás: <a href='https://poltudszemle.hu/wp-content/uploads/2024/10/1SZAVAZUNK.pdf' target='_blank'>
        SZAVAZUNK, HA ESIK, HA FÚJ?</a>
    </p>
    """, unsafe_allow_html=True)
