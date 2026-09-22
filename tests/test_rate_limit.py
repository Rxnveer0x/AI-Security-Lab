import requests


URL = "http://127.0.0.1:5000/chat"


print("\nRATE LIMIT TEST")
print("Sending 6 invalid requests...")
print("These requests should be rejected by input validation, so Ollama will not be called.")


for i in range(1, 7):
    try:
        response = requests.post(
            URL,
            json={"message": ""},
            timeout=10
        )

        print(f"\nRequest {i}")
        print("Status:", response.status_code)
        print("Response:", response.text)
        print("-" * 60)

    except requests.exceptions.RequestException as error:
        print(f"\nRequest {i}")
        print("ERROR:", repr(error))
        print("-" * 60)