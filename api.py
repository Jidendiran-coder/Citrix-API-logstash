import requests

# Replace with the appropriate URL based on your region
url = 'https://api.cloud.com/cctrustoauth2/root/tokens/clients'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'grant_type': 'client_credentials',
    'client_id': '24dbf7ce-7270-40a9-909b-9173a743de0c',
    'client_secret': 'U-VS9SJyvQy3pL2c9kO63A=='
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print('Access Token:', access_token)
else:
    print('Error:', response.status_code, response.text)
