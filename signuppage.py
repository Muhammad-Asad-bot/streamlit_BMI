import streamlit as st
from supabase import create_client, Client
import matplotlib.pyplot as plt
# Initialize Supabase client
url: str = "https://rxzmavpunkiblypwfhzm.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4em1hdnB1bmtpYmx5cHdmaHptIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzE0NzQ3MiwiZXhwIjoyMDIyNzIzNDcyfQ.dpNPF2_V6Az_sePy300AD0dKPLDYeYZtEZbchYdtkEA"
supabase: Client = create_client(url, key)

def signup_user(email, password):
    """Sign up a new user with hashed password."""
    hashed_password = password  # Ensure passwords are securely hashed
    user_data = {'email': email, 'password': hashed_password}
    user = supabase.table('sample').select('*').eq('email', email).execute()
    if user.data and user.data[0]['email'] == email:
        return False
    else:
        supabase.table('sample').insert(user_data).execute()
        return True
    

def login_user(email, password):
    """Log in user."""
    user = supabase.table('sample').select('*').eq('email', email).execute()
    if user.data and user.data[0]['password'] == password:
        return True
    return False

def show_login():
    st.header("Login")
    login_email = st.text_input("Email")
    login_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(login_email, login_password):
            st.session_state['user_email'] = login_email
            st.session_state['page'] = 'dashboard'
        else:
            st.error("Invalid credentials")

def show_signup():
    st.header("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if signup_user(email, password):
            st.success("You have successfully signed up!")
            st.session_state['page'] = 'login'  # Redirect to login page after successful signup
        else:
            st.error("Signup failed. This email may already be used.")


def show_dashboard(email):
    st.markdown("""
        <style>
        .title {
            background-color: #4CAF50;  # Green background
            color: white;              # White text
            padding: 10px;             # Padding around the text
            border-radius: 10px;       # Rounded corners
            text-align: center;        # Center-aligned text
            align-items:center;
        }
        </style>
        """, unsafe_allow_html=True)

    # Use the custom class 'title' in your h1 tag
    st.markdown('<h2 class="title">BMI Calculator</h2>', unsafe_allow_html=True)

    weight = st.number_input("Enter your weight (in kgs)", min_value=1.0, max_value=200.0, step=0.1)
    status = st.radio('Select your height format:', ('cms', 'meters', 'feet'))
    if status == 'cms':
        height = st.number_input(f'Height in {status}', min_value=50.0, max_value=300.0, step=1.0)
    elif status == 'meters':
        height = st.number_input(f'Height in {status}', min_value=0.5, max_value=3.0, step=0.01)
    else:  # feet
        height = st.number_input(f'Height in {status}', min_value=1.5, max_value=10.0, step=0.1)

    calculated = False
    try:
        if status == 'cms':
            bmi = weight / ((height / 100) ** 2)
        elif status == 'meters':
            bmi = weight / (height ** 2)
        else:  # feet
            bmi = weight / ((height / 3.28) ** 2)
        calculated = True
    except ZeroDivisionError:
        st.error("Height must be greater than zero for calculation.")

    if st.button('Calculate BMI') and calculated:
        st.text(f"Your BMI Index is {bmi:.2f}.")
        if bmi < 16:
            st.error("You are Extremely Underweight")
        elif 16 <= bmi < 18.5:
            st.warning("You are Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Healthy")
        elif 25 <= bmi < 30:
            st.warning("Overweight")
        elif bmi >= 30:
            st.error("Extremely Overweight")

        # Convert height to a comparable scale with weight for visualization
        height_for_plot = height if status != 'cms' else height / 100
        if status == 'feet':
            height_for_plot = height * 0.3048  # Convert feet to meters for consistency

        # Plotting the weight, adjusted height, and BMI
        fig, ax = plt.subplots()
        categories = ['Weight (kg)', 'Height (m)', 'BMI']
        values = [weight, height_for_plot, bmi]
        ax.bar(categories, values, color=['red', 'green', 'blue'])
        ax.set_ylabel('Values')
        ax.set_title('Weight, Height and BMI Comparison')
        st.pyplot(fig)

    st.write(f"Welcome to your dashboard, {email}!")

# Navigation and other functionalities remain as previously defined
if 'page' not in st.session_state:
    st.session_state['page'] = 'signup'

if st.session_state['page'] == 'login':
    show_login()
elif st.session_state['page'] == 'signup':
    show_signup()
elif st.session_state['page'] == 'dashboard' and 'user_email' in st.session_state:
    show_dashboard(st.session_state['user_email'])
else:
    # If none of the conditions are met, default to login
    st.session_state['page'] = 'login'
