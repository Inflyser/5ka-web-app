import requests

cookies = {
    'spid': '1749845165342_d9758ee051d22005b531d79bc8a52ce9_6rxd6xewi00r4vup',
    '_ym_uid': '1749845167776844367',
    '_ym_d': '1749845167',
    '_ga': 'GA1.1.955548613.1749847022',
    'tmr_lvid': '24326f0c87c187980b45074a326a3e14',
    'tmr_lvidTS': '1749847022146',
    '_ga_YJHF8Y9KXK': 'GS2.1.s1749847022$o1$g1$t1749847686$j60$l0$h0',
    '_ym_isad': '2',
    'spjs': '1750456433027_3df645ec_0134ff91_1011a336dd8b8bc26b1a952a2680870b_bcqJBS1wYJ1D9qdChH4cGnBfdMAIOsmRHWHEGEbPSnevUzy9sGC1BHqO7iqWhwcs1Hh8gO0CYrzJaOr2uzRPC8MHpbOJbk6eXLWVTADpLEPrMiOaonSUtVloyHmCkwMDi/94oZyhYZ1luSlUDLPCGNDhcIHZfmuKFrcyExGIGHW9IWfO1iub8m3cyQ1hsHWV634am/OgcAx1ibnAPiIXeucbJKD4vYj5N+OWMm7qD2GpF/LehH38lV1Z0GyNVya0PqjafxfyIoK0qUhVDDcUiyM/36O+OwrZQeWksQoPaG5Wl0CcNT1p9Q9jpUoDvq5GvSkKbBV3FsJ7jk9rbbHnqkM+/RdPNiYK9aWjJVyI2OtTcRJXrs09xb3hkSzmu4oWL3Iq7ZVQ8bTbDv5qcldXfec7qleO80F9xOn4VAO8nsrCdiXTiT/MzTllQGwlG7q1mlZyCaFmx8RtrHt/UJVCN5lcfYFt57evZd//sQy0wwtDdgan/KsL37eDlfDTzZ3guLRz2bO/zmKdrg/fNDFA5x/qegkghwVoBA64wiqXd/qBWVdTmj7PO1XDInf+aj4SyzdA24D+v+PaFQJsg5ZG5N15Kx8XAvPW0Q1JoIxkFOszD+6GWglovbQg9IUP+wsYxtVQ7JRp+YVesuJ+R6s7MOhcbZmRFsaCW9usX6wjwylF+Uj1rlOinEFXpHN/yPj/h4JT4yhY+AWt8EFaJVp6J76TLTjwJbWAqu6uDYCxxGuBLBxhyMbpvVRM3qL9yalIxuDD42G8/7Fv4yPQqbKiNZxyIvwEl6eDSv6/WcMXJZp4XavVrwLyjkdZadUNsGGbwXckUok97plDVOTQBrtvFsryIvglmigVyv/+2xC35JD6fX9YhDPnH0P6r/ZaljPJ4S4n1Qs57p3AfaVBADx8Hs9jE9F2e8hV7CT3CyVAYUA+qNrvt8OVsGDc+vd9kLRbUw+/lgDwAGS9CVmt9k1+vFDV01eHy+EWzHmhrww46rLduTg8xQPThk6ue18pJbUJ4esItQUwEZSzhndRBFosSc1zEJIAOxifznMC7oQ4aJUccCfYcTbkn4nJgZkRlSS/oZxMQMin8L1FWM5C3Lk4PJBWJHnJLGy5brfVqfDMrEfJ58buZjVjdi5q6s4TJMBU3JhfE90wZnshbe3BHnJk/qfjYkaYOZvNJgOCZlW+TlNMcRLe1jrqF0x8rFgBtUVCSj++3MakxclxuZ4VHqNme/GLciCJOemvsqBWU8q4LyOMYDBMpvyfw2hGNx4GwTE2vryNvPdiwCbQuYlRaNR0C+NKLpeKXGnYcXU1EXqePluGZ3X89FyM8Gvi8s+PCFuzS28+ypIl9YFcWmzaHpJjliwT+eSEX8hcYn+vXAVOnzjB+sot+FrneoSik9YNtmbkPdCPV0iqja0pfKD5IpSrX/g7FZaxcd7de7ia0QifD5rzdhRRnTHc3UADtv+mOmsVzPEi3Ia34bPqIKTidfQ8uVuoDVuApreU+nT2+o+VsBvEg2',
    'spsc': '1750456433027_a418f8553dc99f2eb912466f24b394ee_o.BMQKXO2BUovdIfFrIniU8BcbhsMHl41Vc0Mw8Y12Tay.GJ3Wg5EQGUHCtbxNAaZ',
    '_ym_visorc': 'b',
    'SRV': '73886aee-6a12-46c9-9c9d-5a6f809da3ee',
    'TS018c7dc5': '01a2d8bbf4e402fc69a61b9a64ffa786927fb34ef8f4b4d470759c67ba475125ab6845930e79364acccb913f8531916007f185d39631da6ff0594dab225db9b4936f940b40',
    'TS01658276': '01a2d8bbf47014ab33ec93cce769957c35a50399299f365610af2d5d43f13c7a40caf3f7dc8d93a6ce7c0540ce745cd69440bb87f6e69372c2ac7a645a7280b353ff3c8c79b8093a6a4390c297971c6994294d590464e22d0ad6289c11bca5db5d1dbdb78f',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://5ka.ru',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-app-version': '0.1.1.dev',
    'x-device-id': 'afc296b4-0312-461f-98cd-e1755c4ed629',
    'x-platform': 'webapp',
    # 'cookie': 'spid=1749845165342_d9758ee051d22005b531d79bc8a52ce9_6rxd6xewi00r4vup; _ym_uid=1749845167776844367; _ym_d=1749845167; _ga=GA1.1.955548613.1749847022; tmr_lvid=24326f0c87c187980b45074a326a3e14; tmr_lvidTS=1749847022146; _ga_YJHF8Y9KXK=GS2.1.s1749847022$o1$g1$t1749847686$j60$l0$h0; _ym_isad=2; spjs=1750456433027_3df645ec_0134ff91_1011a336dd8b8bc26b1a952a2680870b_bcqJBS1wYJ1D9qdChH4cGnBfdMAIOsmRHWHEGEbPSnevUzy9sGC1BHqO7iqWhwcs1Hh8gO0CYrzJaOr2uzRPC8MHpbOJbk6eXLWVTADpLEPrMiOaonSUtVloyHmCkwMDi/94oZyhYZ1luSlUDLPCGNDhcIHZfmuKFrcyExGIGHW9IWfO1iub8m3cyQ1hsHWV634am/OgcAx1ibnAPiIXeucbJKD4vYj5N+OWMm7qD2GpF/LehH38lV1Z0GyNVya0PqjafxfyIoK0qUhVDDcUiyM/36O+OwrZQeWksQoPaG5Wl0CcNT1p9Q9jpUoDvq5GvSkKbBV3FsJ7jk9rbbHnqkM+/RdPNiYK9aWjJVyI2OtTcRJXrs09xb3hkSzmu4oWL3Iq7ZVQ8bTbDv5qcldXfec7qleO80F9xOn4VAO8nsrCdiXTiT/MzTllQGwlG7q1mlZyCaFmx8RtrHt/UJVCN5lcfYFt57evZd//sQy0wwtDdgan/KsL37eDlfDTzZ3guLRz2bO/zmKdrg/fNDFA5x/qegkghwVoBA64wiqXd/qBWVdTmj7PO1XDInf+aj4SyzdA24D+v+PaFQJsg5ZG5N15Kx8XAvPW0Q1JoIxkFOszD+6GWglovbQg9IUP+wsYxtVQ7JRp+YVesuJ+R6s7MOhcbZmRFsaCW9usX6wjwylF+Uj1rlOinEFXpHN/yPj/h4JT4yhY+AWt8EFaJVp6J76TLTjwJbWAqu6uDYCxxGuBLBxhyMbpvVRM3qL9yalIxuDD42G8/7Fv4yPQqbKiNZxyIvwEl6eDSv6/WcMXJZp4XavVrwLyjkdZadUNsGGbwXckUok97plDVOTQBrtvFsryIvglmigVyv/+2xC35JD6fX9YhDPnH0P6r/ZaljPJ4S4n1Qs57p3AfaVBADx8Hs9jE9F2e8hV7CT3CyVAYUA+qNrvt8OVsGDc+vd9kLRbUw+/lgDwAGS9CVmt9k1+vFDV01eHy+EWzHmhrww46rLduTg8xQPThk6ue18pJbUJ4esItQUwEZSzhndRBFosSc1zEJIAOxifznMC7oQ4aJUccCfYcTbkn4nJgZkRlSS/oZxMQMin8L1FWM5C3Lk4PJBWJHnJLGy5brfVqfDMrEfJ58buZjVjdi5q6s4TJMBU3JhfE90wZnshbe3BHnJk/qfjYkaYOZvNJgOCZlW+TlNMcRLe1jrqF0x8rFgBtUVCSj++3MakxclxuZ4VHqNme/GLciCJOemvsqBWU8q4LyOMYDBMpvyfw2hGNx4GwTE2vryNvPdiwCbQuYlRaNR0C+NKLpeKXGnYcXU1EXqePluGZ3X89FyM8Gvi8s+PCFuzS28+ypIl9YFcWmzaHpJjliwT+eSEX8hcYn+vXAVOnzjB+sot+FrneoSik9YNtmbkPdCPV0iqja0pfKD5IpSrX/g7FZaxcd7de7ia0QifD5rzdhRRnTHc3UADtv+mOmsVzPEi3Ia34bPqIKTidfQ8uVuoDVuApreU+nT2+o+VsBvEg2; spsc=1750456433027_a418f8553dc99f2eb912466f24b394ee_o.BMQKXO2BUovdIfFrIniU8BcbhsMHl41Vc0Mw8Y12Tay.GJ3Wg5EQGUHCtbxNAaZ; _ym_visorc=b; SRV=73886aee-6a12-46c9-9c9d-5a6f809da3ee; TS018c7dc5=01a2d8bbf4e402fc69a61b9a64ffa786927fb34ef8f4b4d470759c67ba475125ab6845930e79364acccb913f8531916007f185d39631da6ff0594dab225db9b4936f940b40; TS01658276=01a2d8bbf47014ab33ec93cce769957c35a50399299f365610af2d5d43f13c7a40caf3f7dc8d93a6ce7c0540ce745cd69440bb87f6e69372c2ac7a645a7280b353ff3c8c79b8093a6a4390c297971c6994294d590464e22d0ad6289c11bca5db5d1dbdb78f',
}

params = {
    'lon': '36.098231582031225',
    'lat': '52.95438117060808',
}

response = requests.get('https://5d.5ka.ru/api/orders/v1/orders/stores/', params=params, cookies=cookies, headers=headers)

with open("result3.html", "w") as file:
    file.write(response.text)