# Hi I'm **Joel**👋 Please review the below steps to achieve citrix log collection using logstash

# 🛠️Step-by-Step Guide: Integrating Citrix with Logstash, Elasticsearch & Kibana
# Citrix Logs Integration with ELK (Logstash, Elasticsearch, Kibana)

## 📌 Overview
This guide explains how to collect logs from **Citrix Cloud**, send them to **Logstash**, store them in **Elasticsearch**, and visualize them in **Kibana**.

## 🔹 Step 1: Get Access to Citrix Logs
### 1️⃣ Get Citrix API Credentials
- Log in to **Citrix Cloud**.
- Go to **Identity and Access Management > API Access**.
- Create an API client and note down the **Client ID** and **Client Secret**.

### 2️⃣ Obtain an Access Token
Use the following **Python script** to get an access token:

```python
import requests

url = "https://api-us.cloud.com/cctrustoauth2/root/tokens/clients"
data = {
    "grant_type": "client_credentials",
    "client_id": "<YOUR_CLIENT_ID>",
    "client_secret": "<YOUR_CLIENT_SECRET>"
}

response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Access Token:", access_token)
else:
    print("Error:", response.status_code, response.text)
```

Replace `<YOUR_CLIENT_ID>` and `<YOUR_CLIENT_SECRET>` with your actual Citrix credentials.

---

## 🔹 Step 2: Fetch Logs from Citrix API
Use this **Python script** to fetch logs from Citrix and send them to Logstash:

```python
import requests
import json
import time

citrix_url = "https://api-us.cloud.com/auditlog/v1/logs"  # Change region if needed
logstash_url = "http://<LOGSTASH_IP>:5044"  # Logstash input URL
access_token = "<YOUR_ACCESS_TOKEN>"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

def fetch_logs():
    logs = []
    next_page = None

    while True:
        params = {"page": next_page} if next_page else {}
        response = requests.get(citrix_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            logs.extend(data.get("logs", []))
            next_page = data.get("next_page", None)
            if not next_page:
                break
        else:
            print("Error:", response.status_code, response.text)
            break
    return logs

def send_to_logstash(logs):
    if logs:
        response = requests.post(logstash_url, json=logs)
        if response.status_code == 200:
            print("Logs sent to Logstash.")
        else:
            print("Error sending logs:", response.status_code, response.text)

while True:
    logs = fetch_logs()
    if logs:
        send_to_logstash(logs)
    time.sleep(300)  # Fetch logs every 5 minutes
```

Replace `<LOGSTASH_IP>` and `<YOUR_ACCESS_TOKEN>` with actual values.

---

## 🔹 Step 3: Configure Logstash
### 1️⃣ Create Logstash Configuration File
```bash
sudo nano /etc/logstash/conf.d/citrix_logs.conf
```

### 2️⃣ Add Logstash Input & Output Configuration
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
    hosts => ["http://<ELASTICSEARCH_IP>:9200"]
    index => "citrix-logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

Replace `<ELASTICSEARCH_IP>` with the correct Elasticsearch server address.

### 3️⃣ Restart Logstash
```bash
sudo systemctl restart logstash
```

---

## 🔹 Step 4: Verify Logs in Elasticsearch
Check if logs are stored in Elasticsearch:
```bash
curl -X GET "http://<ELASTICSEARCH_IP>:9200/citrix-logs-*/_search?pretty"
```

---

## 🔹 Step 5: View Logs in Kibana
### 1️⃣ Open Kibana
- Go to: `http://<KIBANA_IP>:5601`

### 2️⃣ Create an Index Pattern
- **Stack Management > Index Patterns**
- Click **Create Index Pattern**
- Enter: `citrix-logs-*`
- Select **timestamp field**

### 3️⃣ View Logs
- Go to **Discover**
- Select `citrix-logs-*` index
- Search & analyze Citrix logs 🎉

---

## 🔹 Automate Script Execution
Schedule the Python script using **Cron Job**:
```bash
crontab -e
```
Add this line:
```bash
*/5 * * * * /usr/bin/python3 /path/to/citrix_log_script.py
```

---

## 🔹 Security & Best Practices
✅ **Use `.env` files** to store API credentials securely.
✅ **Enable Role-Based Access Control (RBAC)** in Kibana to restrict log access.
✅ **Set up Alerts in Kibana** to monitor critical Citrix events.

---

## 🎉 Conclusion
You have successfully integrated Citrix logs into your existing ELK stack. Now you can monitor, search, and analyze Citrix logs in Kibana. 🚀
