# Citrix Logs Integration with ELK Stack

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

