import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Layout beállítása középre
st.set_page_config(page_title="Választási Kalkulátor", layout="centered")

# Egyedi stílus a kompakt megjelenéshez
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
        min-height: 80px !important; /* Legyen elég hely a tartalomnak */
        display: block !important;
    }

    /* A felirat (label) kényszerítése */
    [data-testid="stMetricLabel"] > div {
        font-size: 0.75rem !important;
        color: #555555 !important; /* Sötétszürke felirat */
        overflow: visible !important;
        text-overflow: unset !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }

    /* A számérték (value) kényszerítése */
    [data-testid="stMetricValue"] > div {
        font-size: 1.2rem !important;
        color: #31333F !important; /* Erős sötét szín a számnak */
        font-weight: 700 !important;
    }

    /* Oszlopok közötti rés mobilon */
    [data-testid="column"] {
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.header("🗳️ Az időjárás hatása a választási részvételre")
#st.caption("Dinamikus időjárás-modell (2014-2022)")

# --- BEÁLLÍTÁSOK ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        max_part = st.number_input("Várt részvételi arány (%)", 0.0, 100.0, 70.0, step=0.1, format="%.1f")
    with col2:
        rain = st.number_input("Várható napi csapadékösszeg (mm)", 0, 100, 0)
    
    temp = st.select_slider("Várható napi átlaghőmérséklet (°C)", 
                            options=np.arange(-15.0, 35.5, 0.5).tolist(), value=5.0)

# --- MATEMATIKAI SZÁMÍTÁSOK ---
peak_temp = 4.9943
def calc_temp_p(t):
    raw = (-0.0002628 * (t**2)) + (0.002625 * t)
    peak_raw = (-0.0002628 * (peak_temp**2)) + (0.002625 * peak_temp)
    return (raw - peak_raw) * 100

def calc_rain_p(r):
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

# --- DINAMIKUS GRAFIKONOK PIROS GÖMBBEL ÉS OPTIMUMMAL ---
st.write("---")
g1, g2 = st.columns(2)

def style_plot(ax, title, xlabel):
    ax.set_title(title, fontsize=10, pad=8)
    ax.tick_params(labelsize=8)
    ax.grid(True, alpha=0.15)
    ax.set_xlabel(xlabel, fontsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)

# 1. Hőmérséklet grafikon
with g1:
    t_axis = np.linspace(-15, 35, 100)
    y_temp = calc_temp_p(t_axis)
    fig1, ax1 = plt.subplots(figsize=(4, 2))
    ax1.plot(t_axis, y_temp, color='#1f77b4', lw=2, alpha=0.8)
    
    # ZÖLD SZAGGATOTT VONAL AZ OPTIMUMNÁL (4.99°C)
    ax1.axvline(peak_temp, color='green', linestyle='--', linewidth=1, alpha=0.7, label='Optimum')
    
    # PIROS GÖMB
    ax1.scatter([temp], [c_temp_p], color='red', s=60, zorder=5)
    
    style_plot(ax1, "Hőmérséklet hatás", "°C")
    st.pyplot(fig1)

# 2. Csapadék grafikon
with g2:
    r_axis = np.linspace(0, 50, 100)
    y_rain = calc_rain_p(r_axis)
    fig2, ax2 = plt.subplots(figsize=(4, 2))
    ax2.plot(r_axis, y_rain, color='#ff7f0e', lw=2, alpha=0.8)
    # PIROS GÖMB
    ax2.scatter([rain], [c_rain_p], color='red', s=60, zorder=5)
    style_plot(ax2, "Csapadék hatás", "mm")
    st.pyplot(fig2)

st.markdown("<br>", unsafe_allow_html=True)
#st.info("A zöld szaggatott vonal az elméleti maximumot (4,99°C) jelöli.")

# --- SZÖVEGES ÖSSZEFOGLALÓ A TANULMÁNY ALAPJÁN ---
st.write(f"### Összefoglaló a tanulmány* alapján")
st.write("""
A 2014 és 2022 közötti magyarországi választási adatokat elemző kutatás alapján az időjárás az alábbiak szerint befolyásolja a részvételt:

* **Hőmérséklet:** Az összefüggés **negatív négyzetes**. Ez azt jelenti, hogy létezik egy optimális hőmérsékleti tartomány (kb. **5°C** átlaghőmérséklet), ahol a legmagasabb a választási kedv. Az ennél jóval hidegebb idő diszkomfortot okoz, míg a jelentős melegedés az alternatív szabadidős programok (pl. kirándulás, strand) vonzerejét növeli, így mindkét irányú eltérés csökkenti a részvételt.
* **Csapadék:** A kapcsolat **lineárisan negatív**. Minden egyes milliméternyi csapadék növeli a szavazás „költségét” (kényelmetlenség), ami egyértelműen és arányosan csökkenti a részvételi hajlandóságot.
Fontos, hogy a csapadék eloszlása területenként nagyon változó lehet, így csak azon területek eredményeit korrigáljuk vele ahova ténylegesen várjuk a csapadékot.

""")

st.markdown("""
    <p style='font-size: 0.9rem; font-style: italic;'>
        Forrás: <a href='https://poltudszemle.hu/wp-content/uploads/2024/10/1SZAVAZUNK.pdf' target='_blank'>
        SZAVAZUNK, HA ESIK, HA FÚJ?</a>
    </p>
    """, unsafe_allow_html=True)
