import requests


url = "https://algamarinhabeachwear.online/"

for i in range(10000000000000000000):
    print(f"Acessando o site pela {i}ª vez...")
    response = requests.get(url)
    print(response.status_code)
    
