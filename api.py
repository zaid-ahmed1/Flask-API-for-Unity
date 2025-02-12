import requests
import json

def capture_chrome_window():
    WINDOW_NAME = "Oculus - Google Chrome"
    url = "http://localhost:5000/analyze_screen"
    
    # Send the request to capture
    data = {
        "window_title": WINDOW_NAME
    }
    
    try:
        print(f"Sending request to capture window: {WINDOW_NAME}")
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"Screenshot saved to: {result['result']['filepath']}")
                return True
            else:
                print("Error:", result.get('error'))
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse response: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    return False

if __name__ == "__main__":
    if capture_chrome_window():
        print("Successfully captured window")
    else:
        print("Failed to capture window")
