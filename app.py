import sys
import os
import streamlit as st
import pandas as pd
import random
from dotenv import load_dotenv
from utils.b2 import B2

# Add the utils directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))

# Load environment variables
load_dotenv()

# Set Backblaze connection
b2 = B2(
    endpoint=os.getenv('B2_ENDPOINT', 's3.us-east-005.backblazeb2.com'),
    key_id=os.getenv('B2_KEYID'),
    secret_key=os.getenv('B2_APPKEY')
)

@st.cache_data
def fetch_data():
    try:
        b2.set_bucket('AirBnB-CSV')  # Set the bucket
        obj = b2.get_object('Airbnb Dataset_Long.csv')  # Use the EXACT file name
        return pd.read_csv(obj)
    except Exception as e:
        st.error(f"Error fetching data from Backblaze: {e}")
        return None

# APPLICATION
st.title("Airbnb Data Viewer")

# Main Page with Buyer and Seller buttons
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    st.header("Welcome to the Airbnb Explorer!")
    buyer = st.button("Buyer")
    seller = st.button("Seller")

    if buyer:
        st.session_state.page = "buyer"
    if seller:
        st.session_state.page = "seller"

# Fetch data from Backblaze
data = fetch_data()
if data is not None:
    st.write("Data loaded successfully.")
    st.dataframe(data.head())

# Placeholder for Buyer 
if st.session_state.page == "buyer":
    #Start Code here for Buyer side, replace the code below.
    st.write("Buyer window placeholder. Replace with  implementation.")

#Rough Draft Seller
elif st.session_state.page == "seller":
    # Sidebar for Seller Input Form
    st.sidebar.title("Seller's Property Details")

# Dropdown for Property Type
    property_type = st.sidebar.selectbox("Property Type", property_types)

    # Dropdown for Price Range
    price_range = st.sidebar.selectbox("Price Range", price_ranges)

    # Number inputs for Bedrooms, Bathrooms, Beds, etc.
    bedrooms = st.sidebar.number_input("Number of Bedrooms", min_value=1, max_value=10, value=1)
    bathrooms = st.sidebar.number_input("Number of Bathrooms", min_value=1, max_value=10, value=1)
    beds = st.sidebar.number_input("Number of Beds", min_value=1, max_value=10, value=1)

    # Flag to check if the submit button has been clicked
    submitted = st.sidebar.button("Submit Property")

    # Main Page Content
    if not submitted:
        # Display introductory text only if not submitted
        st.title("Seller's Property Submission")
        st.write("Fill in the property details on the sidebar to submit your listing.")
    else:
        # Display submitted property details
        st.markdown("### Property Details Submitted")
        st.write(f"**Property Type:** {property_type}")
        st.write(f"**Price Range:** {price_range}")
        st.write(f"**Bedrooms:** {bedrooms}")
        st.write(f"**Bathrooms:** {bathrooms}")
        st.write(f"**Beds:** {beds}")
        
    # Generate and display a prominent random score
        random_score = random.randint(1, 5)
        st.markdown(f"## 🔥 **Predicted Score: {random_score}** 🔥")

    # Back button to go back to main page
if st.button("Back"):
    st.session_state.page = "main"



