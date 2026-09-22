import requests


# Flask API endpoint
url = "http://127.0.0.1:5000/chat"


# JSON payload
payload = {
    "message": "Hello"
}


# Request headers
headers = {
    "Content-Type": "application/json"
}


try:
    # Send POST request
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=120
    )

    # Print status code
    print("Status code:", response.status_code)

    # Print request information
    print("Request headers:", response.request.headers)
    print("Request body:", response.request.body)

    # Print server response
    print("Response:", response.text)


except requests.exceptions.ConnectionError:
    print("ERROR: Flask server is not running.")


except requests.exceptions.Timeout:
    print("ERROR: Request timed out.")


except requests.exceptions.RequestException as error:
    print("REQUEST ERROR:", repr(error))


except Exception as error:
    print("ERROR:", repr(error))