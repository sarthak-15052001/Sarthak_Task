import argparse
import requests
import json
import csv

class RestfulClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method, endpoint, outfile, data):
        self.method = method
        self.endpoint = endpoint
        self.outfile = outfile
        self.data = data

    def make_request(self):
        url = f"{self.BASE_URL}{self.endpoint}"
        response = None

        try:
            if self.method.lower() == 'get':
                response = requests.get(url)
            elif self.method.lower() == 'post':
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=json.dumps(self.data), headers=headers)
            else:
                raise ValueError("Invalid method. Use 'get' or 'post'.")

            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            exit(1)

        return response

    def process_response(self, response):
        status_code = response.status_code
        print(f"HTTP Status Code: {status_code}")

        if status_code // 100 == 2:
            if self.outfile:
                self.save_to_file(response.text)

            else:
                print(response.text)

    def save_to_file(self, data):
        if self.outfile.endswith('.json'):
            with open(self.outfile, 'w') as json_file:
                json.dump(json.loads(data), json_file, indent=2)
        elif self.outfile.endswith('.csv'):
            pass
        else:
            raise ValueError("Invalid outfile format. Use '.json' or '.csv'.")

def main():
    parser = argparse.ArgumentParser(description="Simple command-line REST client for JSONPlaceholder.")
    parser.add_argument("METHOD", choices=["get", "post"], help="HTTP method to use (get or post)")
    parser.add_argument("ENDPOINT", help="URI fragment, e.g., /posts/1")
    parser.add_argument("-o", "--output", help="Output file (ending with .json or .csv)")
    parser.add_argument("--data", nargs='*', action='append', help="Data to send with the request (for post requests)")

    args = parser.parse_args()

    data = None
    if args.data:
        data = {key: value for key, value in (item.split('=') for item in args.data[0])}

    restful_client = RestfulClient(args.METHOD, args.ENDPOINT, args.output, data)
    response = restful_client.make_request()
    restful_client.process_response(response)

if __name__ == "__main__":
    main()
