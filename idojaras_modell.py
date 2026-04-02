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
        font-size: 1.1rem !important;
        color: #31333F !important; /* Erős sötét szín a számnak */
        font-weight: 700 !important;
    }

    /* Oszlopok közötti rés mobilon */
    [data-testid="column"] {
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
