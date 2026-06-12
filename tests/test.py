import requests

url = "http://34.131.182.113/api/dcim/sites/"

payload = {}
headers = {
  'Authorization': 'Bearer UZkz1GbAF3DzMYmrfjazQnYaahANPf8J1HiMtAE1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
