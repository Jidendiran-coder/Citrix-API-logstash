# Hi I'm **Joel**👋 Please review the below steps to achieve citrix log collection using logstash

# 🛠️Step-by-Step Guide: Integrating Citrix with Logstash, Elasticsearch & Kibana

## Pre-Requisites

### 1️⃣ Get API Access in Citrix Cloud
Before making API requests, you need to register an API client in Citrix Cloud.

#### Step 1: Register an API Client
- Log in to Citrix Cloud.
- Go to **Identity and Access Management > API Access**.
- Click **Create Client** and note:
  - **Client ID**
  - **Client Secret**
- Assign **Monitor Administrator** permissions.

### 2️⃣ Authenticate with Citrix API
Citrix APIs use OAuth 2.0 authentication. You need to get an access token before fetching logs.

#### Base URLs for Authentication (Region-Specific)
- **Asia Pacific South:** `https://api-ap-s.cloud.com/cctrustoauth2/root/tokens/clients`
- **European Union:** `https://api-eu.cloud.com/cctrustoauth2/root/tokens/clients`
- **United States:** `https://api-us.cloud.com/cctrustoauth2/root/tokens/clients`
- **Japan:** `https://api.citrixcloud.jp/cctrustoauth2/root/tokens/clients`

Ensure you replace the base URL with the one corresponding to your Citrix Cloud account's region.

#### Example in Python:
```python
import requests

# Replace with the appropriate URL based on your region
url = 'https://api.cloud.com/cctrustoauth2/root/tokens/clients'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'grant_type': 'client_credentials',
    'client_id': '<YOUR_CLIENT_ID>',
    'client_secret': '<YOUR_CLIENT_SECRET>'
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print('Access Token:', access_token)
else:
    print('Error:', response.status_code, response.text)
```
Ensure that you replace `<YOUR_CLIENT_ID>` and `<YOUR_CLIENT_SECRET>` with your actual Citrix Cloud API credentials.

By using the correct token endpoint URL and ensuring the `Content-Type` is set to `application/x-www-form-urlencoded`, you should be able to successfully obtain an access token for Citrix Cloud API requests.

---

## 🔹 Step 1: Use the Access Token in API Requests
Now that we have an access token, we will use it to authenticate API requests to fetch logs from Citrix.

### 📌 Example Request to Fetch Citrix Audit Logs
#### 1️⃣ Identify the correct Citrix API endpoint for fetching logs
The API endpoint to fetch Audit Logs is:
```bash
https://api.cloud.com/auditlog/v1/logs
```
or for US region:
```bash
https://api-us.cloud.com/auditlog/v1/logs
```

#### 2️⃣ Make an API Request to Fetch Logs
Now, let's use Python to fetch Citrix logs:

```python
import requests

# Define API URL
url = "https://api.cloud.com/auditlog/v1/logs"  # Change URL based on your region

# Access Token (Replace this with the token you obtained)
access_token = "<YOUR_ACCESS_TOKEN>"

# Set headers with authentication
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Make API request
response = requests.get(url, headers=headers)

# Print response
if response.status_code == 200:
    print("Logs Fetched Successfully:")
    print(response.json())  # Logs in JSON format
else:
    print("Error:", response.status_code, response.text)
```

🔹 This script will fetch logs in JSON format, which we will later send to Logstash.

## Step 2: Send Citrix Logs to Logstash
Now that we have Citrix logs in JSON format, we need to forward them to Logstash for further processing.

### 📌 Configure Logstash to Accept Logs
#### 1️⃣ Open your Logstash Configuration File (logstash.conf):
```bash
sudo nano /etc/logstash/conf.d/logstash.conf
```
#### 2️⃣ Modify logstash.conf to accept input from HTTP (Citrix Logs)
```yaml
input {
  http {
    port => 5044
    codec => "json"
  }
}

filter {
  mutate {
    add_field => { "source" => "Citrix API" }
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]  # Elasticsearch URL
    index => "citrix-logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```
#### 3️⃣ Save & Restart Logstash
```bash
sudo systemctl restart logstash
```
Now, Logstash will listen on port 5044 for incoming logs.

## 🔹 Step 3: Push Logs from Python to Logstash
Now, we will modify our Python script to send logs to Logstash.

```python
import requests
import json

# Citrix API URL
citrix_url = "https://api.cloud.com/auditlog/v1/logs"

# Logstash URL
logstash_url = "http://localhost:5044"

# Access Token
access_token = "<YOUR_ACCESS_TOKEN>"

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Fetch Citrix Logs
response = requests.get(citrix_url, headers=headers)

if response.status_code == 200:
    logs = response.json()  # Extract logs
    
    # Send logs to Logstash
    logstash_response = requests.post(logstash_url, json=logs)
    
    if logstash_response.status_code == 200:
        print("Logs successfully sent to Logstash.")
    else:
        print("Error sending logs to Logstash:", logstash_response.status_code, logstash_response.text)
else:
    print("Error fetching Citrix logs:", response.status_code, response.text)
```
✅ Now, your logs are flowing into Logstash!

## 🔹 Step 4: Verify Data in Elasticsearch
Once Logstash processes the logs, they will be indexed in Elasticsearch.

To verify, run:
```bash
curl -X GET "http://localhost:9200/citrix-logs-*/_search?pretty"
```
If logs are indexed correctly, you will see JSON logs as a response.

## 🔹 Step 5: Visualize in Kibana
#### 1️⃣ Open Kibana in your browser:
```bash
http://localhost:5601
```
#### 2️⃣ Go to "Stack Management" → "Index Patterns", then:
- Click "Create Index Pattern"
- Enter `citrix-logs-*`
- Select the timestamp field

#### 3️⃣ Go to "Discover", and you should see the Citrix logs.

🎉 **Congratulations! You have successfully integrated Citrix logs into ELK Stack. 🚀**


