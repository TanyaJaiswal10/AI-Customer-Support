# Import Streamlit and requests libraries

# Set the BASE_URL for FastAPI backend

# Display the main title "AI Customer Support Dashboard"

# Create a form to add a new customer
# Input fields: Customer Name, Customer Email
# On submit, send POST request to /customers and show the response

# Create a form to add a new ticket
# Input fields: Customer ID, Subject, Message
# On submit, send POST request to /tickets and show the response

# Add a text area to input ticket message for AI analysis
# Add three buttons: Summarize Ticket, Analyze Sentiment, Suggest Reply
# On click, call corresponding /ai-tools endpoints and show response
import streamlit as st
import requests
BASE_URL = "http://localhost:8000"
st.title("AI Customer Support Dashboard")
st.header("Add New Customer")
with st.form("customer_form"):
    name = st.text_input("Customer Name")
    email = st.text_input("Customer Email")
    submitted = st.form_submit_button("Add Customer")
    if submitted:
        response = requests.post(f"{BASE_URL}/customers", json={"name": name, "email": email})
        if response.status_code == 200:
            st.success(f"Customer added: {response.json()}")
        else:
            st.error(f"Error adding customer: {response.text}")
st.header("Add New Ticket")
with st.form("ticket_form"):
    customer_id = st.number_input("Customer ID", min_value=1, step=1)
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    submitted = st.form_submit_button("Add Ticket")
    if submitted:
        response = requests.post(f"{BASE_URL}/tickets", json={"customer_id": customer_id, "subject": subject, "message": message})
        if response.status_code == 200:
            st.success(f"Ticket added: {response.json()}")
        else:
            st.error(f"Error adding ticket: {response.text}")
st.header("AI Analysis (Manual Ticket ID)")

# Input ticket ID manually
ticket_id = st.number_input("Enter Ticket ID", min_value=1, step=1)

# Buttons for AI actions
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Summarize Ticket"):
        resp = requests.post(f"{BASE_URL}/ai-tools/summarize-ticket/{ticket_id}")
        if resp.status_code == 200:
            st.success(f"Summary: {resp.json().get('summary')}")
        else:
            st.error(f"Error summarizing ticket: {resp.text}")

with col2:
    if st.button("Analyze Sentiment"):
        resp = requests.post(f"{BASE_URL}/ai-tools/analyze-sentiment/{ticket_id}")
        if resp.status_code == 200:
            st.success(f"Sentiment Analysis: {resp.json().get('result')}")
        else:
            st.error(f"Error analyzing sentiment: {resp.text}")

with col3:
    if st.button("Suggest Reply"):
        resp = requests.post(f"{BASE_URL}/ai-tools/suggest-reply/{ticket_id}")
        if resp.status_code == 200:
            st.success(f"Suggested Reply: {resp.json().get('suggested_reply')}")
        else:
            st.error(f"Error suggesting reply: {resp.text}")
