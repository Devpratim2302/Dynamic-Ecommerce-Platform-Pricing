import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Streamlit Page Config
st.set_page_config(
    page_title="Dynamic Pricing Engine",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Fonts + Dark Background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
    }

    .fade-slide-in {
        animation: fadeSlideIn 1.2s ease-out;
    }

    @keyframes fadeSlideIn {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .glow-box {
        background: linear-gradient(135deg, #0f2027, #2c5364, #00c9a7);
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        color: white;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }

    .glow-box h1 {
        margin-bottom: 10px;
        font-size: 36px;
        text-shadow: 0 0 10px rgba(0,255,255,0.6);
    }

    .glow-box p {
        font-size: 18px;
        color: #e0f7fa;
    }
    </style>
""", unsafe_allow_html=True)

# Load Model or Dummy
try:
    model = joblib.load("dynamic_pricing_model.pkl")
except FileNotFoundError:
    class DummyModel:
        def predict(self, X):
            demand, stock, expiry, perishable = X[0]
            base_price = 100.0
            price = base_price + (demand * 0.5) - (stock * 0.2)
            if perishable and expiry > 0:
                price -= (10 - min(expiry, 10)) * 2
            return [max(10, price)]
    model = DummyModel()

# Header Box with Animation + Glow
st.markdown("""
    <div class="glow-box fade-slide-in">
        <h1>💸 Dynamic Pricing Engine</h1>
        <p>
            Predict optimal product prices based on<br>
            <b>Forecasted Demand, Stock, Expiry, and Perishability.</b>
        </p>
    </div>
    <br>
""", unsafe_allow_html=True)

# Product Input Section
st.markdown("""
    <div style="background-color: #1e1e2f; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
        <h3 style="color: white;">📊 Product Information</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    forecasted_demand = st.number_input(
        "📈 Forecasted Demand (Units)", min_value=0.0, value=50.0,
        help="Expected number of units to be sold soon."
    )
    expiry_days = st.number_input(
        "⏰ Days Until Expiry", min_value=0.0, value=10.0,
        help="How many days are left before the product expires?"
    )

with col2:
    stock = st.number_input(
        "📦 Current Stock Level (Units)", min_value=0.0, value=100.0,
        help="Current available units in your inventory."
    )
    is_perishable = st.toggle("🍎 Is the Product Perishable?", value=True)

st.markdown("</div>", unsafe_allow_html=True)

# Prediction + Chart
def predict_price_and_plot(forecasted_demand, stock, expiry_days, is_perishable):
    X = np.array([[forecasted_demand, stock, expiry_days, int(is_perishable)]])
    price = model.predict(X)[0]

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.style.use('dark_background')
    colors = ["#4A90E2", "#50E3C2"]
    bars = ax.bar(['Forecasted Demand', 'Current Stock'], [forecasted_demand, stock], color=colors)
    ax.set_facecolor("#1c1c3c")
    fig.patch.set_facecolor('#1c1c3c')
    ax.set_title("Demand vs Stock Analysis", fontsize=18, color='white')
    ax.set_ylabel("Quantity", color='white')
    ax.tick_params(colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height * 1.01, f'{int(height)}',
                ha='center', va='bottom', fontsize=12, color='white')

    return round(price, 2), fig

# Prediction Button
if st.button("💲 Calculate Optimal Price"):
    price, fig = predict_price_and_plot(forecasted_demand, stock, expiry_days, is_perishable)

    st.markdown(f"""
        <div style="background: white;
                    color: black;
                    border-radius: 12px;
                    padding: 25px;
                    text-align: center;
                    font-size: 28px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            🚀 <b>Recommended Price:</b> ₹{price}
        </div>
        <br>
    """, unsafe_allow_html=True)

    st.pyplot(fig)
