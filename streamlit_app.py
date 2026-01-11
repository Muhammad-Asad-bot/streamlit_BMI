import streamlit as st

st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚕️",
    layout="centered"
)

def calculate_bmi(weight, height, unit):
    if weight <= 0 or height <= 0:
        return None

    if unit == 'Centimeters':
        height_m = height / 100
    elif unit == 'Meters':
        height_m = height
    else:
        height_m = height / 3.28084

    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    if bmi < 16:
        return "Severely Underweight", "#e74c3c", "⚠️"
    elif bmi < 18.5:
        return "Underweight", "#f39c12", "⚡"
    elif bmi < 25:
        return "Normal Weight", "#27ae60", "✓"
    elif bmi < 30:
        return "Overweight", "#f39c12", "⚡"
    else:
        return "Obese", "#e74c3c", "⚠️"

def get_health_recommendation(bmi):
    if bmi < 16:
        return "Consult with a healthcare provider immediately. Severely low BMI may indicate malnutrition."
    elif bmi < 18.5:
        return "Consider consulting a healthcare provider. A balanced diet with adequate calories may be beneficial."
    elif bmi < 25:
        return "Maintain your current healthy lifestyle with regular exercise and balanced nutrition."
    elif bmi < 30:
        return "Consider incorporating more physical activity and a balanced diet to reach a healthier weight."
    else:
        return "Consult with a healthcare provider for a comprehensive health assessment and personalized plan."

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #2c3e50;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: #7f8c8d;
        font-size: 1rem;
    }
    .stButton button {
        width: 100%;
        background-color: #3498db;
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #2980b9;
    }
    .result-card {
        padding: 2rem;
        border-radius: 12px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin: 1.5rem 0;
        text-align: center;
    }
    .bmi-value {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>BMI Calculator</h1>
        <p>Calculate your Body Mass Index and get personalized health insights</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    weight = st.number_input(
        "Weight (kg)",
        min_value=0.0,
        max_value=500.0,
        value=0.0,
        step=0.1,
        help="Enter your weight in kilograms"
    )

with col2:
    unit = st.selectbox(
        "Height Unit",
        options=['Meters', 'Centimeters', 'Feet'],
        help="Choose your preferred unit for height"
    )

if unit == 'Meters':
    height = st.number_input(
        f"Height ({unit})",
        min_value=0.0,
        max_value=3.0,
        value=0.0,
        step=0.01,
        help="Enter your height in meters (e.g., 1.75)"
    )
elif unit == 'Centimeters':
    height = st.number_input(
        f"Height ({unit})",
        min_value=0.0,
        max_value=300.0,
        value=0.0,
        step=1.0,
        help="Enter your height in centimeters (e.g., 175)"
    )
else:
    height = st.number_input(
        f"Height ({unit})",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.1,
        help="Enter your height in feet (e.g., 5.9)"
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button('Calculate BMI'):
    if weight <= 0 or height <= 0:
        st.error("Please enter valid values for both weight and height.")
    else:
        bmi = calculate_bmi(weight, height, unit)

        if bmi:
            category, color, icon = get_bmi_category(bmi)
            recommendation = get_health_recommendation(bmi)

            st.markdown(f"""
                <div class="result-card">
                    <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">Your Results</h3>
                    <div class="bmi-value" style="color: {color};">{bmi}</div>
                    <div class="category-badge" style="background-color: {color}; color: white;">
                        {icon} {category}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Underweight", "< 18.5", delta="Low" if bmi < 18.5 else None, delta_color="inverse")
            with col2:
                st.metric("Normal", "18.5 - 24.9", delta="Ideal" if 18.5 <= bmi < 25 else None, delta_color="normal")
            with col3:
                st.metric("Overweight", "≥ 25", delta="High" if bmi >= 25 else None, delta_color="inverse")

            st.markdown(f"""
                <div class="info-box">
                    <strong>Health Recommendation:</strong><br>
                    {recommendation}
                </div>
            """, unsafe_allow_html=True)

            st.info("Note: BMI is a screening tool and not a diagnostic measure. Consult with healthcare professionals for personalized health advice.")

with st.expander("ℹ️ About BMI"):
    st.markdown("""
        **Body Mass Index (BMI)** is a measure that uses your height and weight to determine if your weight is in a healthy range.

        **BMI Categories:**
        - **Below 16.0:** Severely Underweight
        - **16.0 - 18.4:** Underweight
        - **18.5 - 24.9:** Normal Weight
        - **25.0 - 29.9:** Overweight
        - **30.0 and above:** Obese

        **Important:** BMI does not distinguish between muscle and fat mass. Athletes and individuals with high muscle mass may have elevated BMI values despite being healthy.
    """)
