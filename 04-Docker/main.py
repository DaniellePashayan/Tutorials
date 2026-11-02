import time
import requests

def main():
    print("Starting basic Python Docker project...")

    try:
        response = requests.get("https://github.com")
        print(f"GitHub API Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)