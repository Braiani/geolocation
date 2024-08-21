import requests

def fazer_requisicao(url, data=[]):
    try:
        # adicionar o body com o json da requisição
        response = requests.post(url, json=data)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        return response.json()  # Retorna a resposta da API em formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")
        return None

def preparar_range_ips(lista):
    data = []
    for ip in lista:
        data.append({"query": ip, "fields": "city,country,countryCode,region,query,proxy", "lang": "pt-BR" })
    return data

def executar_geolocation(url, lista):
    data = preparar_range_ips(lista)
    # return fazer_requisicao(url, data)

def geolocation_range_ips(ip):
    lista_ips = []
    for i in range(1,256):
        lista_ips.append(ip.replace("0/24", "") + str(i))
    print(lista_ips)

if __name__ == "__main__":
    url = "http://ip-api.com/batch"
    arquivo = "lista_ips.txt"
    ips = []
    try:
        with open(arquivo, "r") as file:
            # Exemplo de ips dentro do arquivo: 24.152.88.0/24, 24.152.17.0/24, 24.152.10.0/24
            ips = file.readlines()
            ips = [ip.strip() for ip in ips]
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado")

    if ips:
        range_ips = []
        for ip in ips:
            if "/32" in ip:
                range_ips.append(ip.replace("/32", ""))
            elif "/24" in ip:
                geolocation_range_ips(ip)
                break

        dados = executar_geolocation(url, range_ips)
        if dados:
            for dado in dados:
                print(f"IP: {dado['query']}, Cidade: {dado['city']}, Estado: {dado['region']}, País: {dado['country']} ({dado['countryCode']})")