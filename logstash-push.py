import requests
import json

# Citrix API URL
citrix_url = "https://api.cloud.com/auditlog/v1/logs"

# Logstash URL
logstash_url = "http://localhost:5044"

# Access Token
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1Zjc5NDA1OS1lNjIzLTRhOTYtOTYzZi1lOGI5Y2E4YzEzMzciLCJ1c2VyX2lkIjoiNWY3OTQwNTktZTYyMy00YTk2LTk2M2YtZThiOWNhOGMxMzM3IiwiZGlzcGxheU5hbWUiOiJGdXR1cmVuZXQgQ2xvdWQiLCJuYW1lIjoiRnV0dXJlbmV0IENsb3VkIiwicHJpbmNpcGFsIjoiZmNsb3VkQGZ1dHVyZW5ldC5pbiIsImVtYWlsIjoiZmNsb3VkQGZ1dHVyZW5ldC5pbiIsImVtYWlsX3ZlcmlmaWVkIjoiVHJ1ZSIsImFtciI6IltcImNsaWVudFwiXSIsImlkcCI6ImNpdHJpeHN0cyIsImN1c3RvbWVycyI6Ilt7XCJDdXN0b21lcklkXCI6XCI2aXF5eGo5NTg3ZDVcIixcIkdlb1wiOlwiVVNcIn1dIiwiYWNjZXNzX3Rva2VuIjoiIiwiYWNjZXNzX3Rva2VuX3Njb3BlIjoiIiwicmVmcmVzaF90b2tlbiI6IiIsImRpc2NvdmVyeSI6IntcIklzc3VlclwiOlwiaHR0cHM6Ly90cnVzdC1hcC1zLmNpdHJpeHdvcmtzcGFjZXNhcGkubmV0XCJ9IiwiY3R4X2F1dGhfYWxpYXMiOiIyNGRiZjdjZS03MjcwLTQwYTktOTA5Yi05MTczYTc0M2RlMGMiLCJjdHhfdXNlciI6IntcIk9pZFwiOlwiT0lEOi9jaXRyaXgvNWY3OTQwNTktZTYyMy00YTk2LTk2M2YtZThiOWNhOGMxMzM3XCIsXCJFbWFpbFwiOlwiRU1BSUw6L2NpdHJpeC9mY2xvdWRAZnV0dXJlbmV0LmluXCJ9IiwiY3R4X2RpcmVjdG9yeV9jb250ZXh0Ijoie1wiSWRlbnRpdHlQcm92aWRlclwiOlwiQ2l0cml4XCJ9IiwibmJmIjoxNzQxMjA0MDQ3LCJleHAiOjE3NDEyMDc2NDcsImlhdCI6MTc0MTIwNDA0NywiaXNzIjoiY3dzIn0.TPMpjkKUKXFCts3YYYCfzMgsm7vzMiwh6Jmvg15hHA6EIz9wHTagxVc8Sj5Qnqit7pEZNgjF0DFsN2lufxn7GoRE_asp9ZXFi0tHYAsYW8QIQ_LGMeZ94XswM1RPqn-u7_apArLSB3PWXdRgSmiey7Ar2IY0PwOeWsHeRitmstklutJZAfa1kiv-XQ6rFHeS4NAmU2lRNiZG49m7sw9VZ2TE61uwJqDpyn3dhQww5m2J93NqQERBDxX9v0Uek2dd1-yaH_Ra2EU5al_oYlHLBCeY93GsIdAAJ-Xqay_q3p0w9Br-sJNYkNitxTai8nxO1nOwgICcE0PshRW2EM6sNg"

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