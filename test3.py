import requests

proxy = "Royal001:SmallLike1%21@109.69.62.127:42361"  # или backconnect-формат

for _ in range(3):
    response = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy})
    print("Текущий IP:", response.json()["origin"])