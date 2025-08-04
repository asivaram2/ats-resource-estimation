import requests

url = "https://adoberm.my.workfront.com/attask/api/v17.0/PROJ/search"

params = {
    "fields": 'name,status,entryDate,portfolioID,portfolio:name,program:name,DE:Effort Estimate',
    "portfolioID": "62c75e2800b8e647336989ab99280223",  # example one portfolio ID
    "apiKey": "4kocbwab1pws72grj41mhzicung7najj",
    "$$LIMIT": "5"
}

response = requests.get(url, params=params)
data = response.json()

# Example: print first project's name
print(data['data'][0]['name'])
