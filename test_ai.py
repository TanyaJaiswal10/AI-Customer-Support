import requests
import json
import time

base = "http://localhost:8000"
unique_id = int(time.time() * 1000)

# Create a customer
cust_resp = requests.post(f"{base}/customers", json={"name": "Test", "email": f"test{unique_id}@test.com"})
print("Customer Status:", cust_resp.status_code)
if cust_resp.status_code != 200:
    print("Customer Error:", cust_resp.text)
else:
    print("Customer:", cust_resp.json())
    cust_id = cust_resp.json()["id"]

    # Create a ticket
    ticket_resp = requests.post(f"{base}/tickets", json={
        "customer_id": cust_id,
        "subject": "Test",
        "message": "I am very happy with the service"
    })
    print("Ticket Status:", ticket_resp.status_code)
    if ticket_resp.status_code != 200:
        print("Ticket Error:", ticket_resp.text)
    else:
        print("Ticket:", ticket_resp.json())
        ticket_id = ticket_resp.json()["id"]

        # Try AI analysis
        try:
            print("\n--- Testing AI Summarize ---")
            ai_resp = requests.post(f"{base}/ai-tools/summarize-ticket/{ticket_id}", timeout=300)
            print("AI Response Status:", ai_resp.status_code)
            print("AI Response:", ai_resp.json() if ai_resp.status_code == 200 else ai_resp.text)
        except Exception as e:
            print(f"Error: {e}")
