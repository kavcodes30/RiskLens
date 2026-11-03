import requests
import streamlit as st

# URL of your running FastAPI backend
API_URL = "http://127.0.0.1:8000/predict"

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune",
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri",
]

OCCUPATIONS = [
    "retired", "student", "freelancer", "government_job",
    "private_job", "business_owner", "unemployed",
]

st.set_page_config(page_title="Insurance Premium Predictor", page_icon="🏥")
st.title("🏥 Insurance Premium Predictor")
st.write("Fill in your details to get the predicted premium category.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=499.0, value=70.0, step=0.5)
        height = st.number_input("Height (m)", min_value=0.5, max_value=2.99, value=1.70, step=0.01)
        smoker = st.checkbox("Smoker")

    with col2:
        income_lpa = st.number_input("Income (LPA)", min_value=0.1, value=10.0, step=0.5)
        city = st.selectbox("City", CITIES)
        occupation = st.selectbox("Occupation", OCCUPATIONS, index=OCCUPATIONS.index("private_job"))

    submitted = st.form_submit_button("Predict Premium")

if submitted:
    payload = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "smoker": smoker,
        "city": city,
        "occupation": occupation,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted premium category: **{result['predicted_category']}**")
        elif response.status_code == 422:
            st.error("The backend rejected the input. Please check your values.")
            st.json(response.json())
        else:
            st.error(f"Backend error ({response.status_code})")
            st.text(response.text)

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the FastAPI backend. "
            "Make sure it is running: python -m uvicorn app:app --reload"
        )
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")