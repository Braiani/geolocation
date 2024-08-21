import requests
import time

def fazer_requisicao(url, data=[]):
    try:
        # adicionar o body com o json da requisição
        response = requests.post(url, json=data)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        return response.json()  # Retorna a resposta da API em formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")
        return None

def preparar_range_ips(lista: list):
    data = []
    temp = []
    count = 0
    for ip in lista:
        if count == 100:
            data.append(temp)
            temp = []
            count = 0
        
        temp.append({"query": ip, "fields": "city,country,countryCode,region,query,proxy", "lang": "pt-BR" })
        count += 1
    if temp:
        data.append(temp)
    return data

def executar_geolocation(url, lista):
    data = preparar_range_ips(lista)
    for i in range(len(data)):
        start_func = int(time.time())
        print(f"Executando requisição {i+1} de {len(data)}")
        response = fazer_requisicao(url, data[i])
        if response:
            for dado in response:
                print(f"IP: {dado['query']}, Cidade: {dado['city']}, Estado: {dado['region']}, País: {dado['country']} ({dado['countryCode']})")
        time.sleep(start_func + 60 - int(time.time()))

def extract_range_ips(ip: str, lista_ips: list):
    for i in range(1,256):
        lista_ips.append(ip.replace("0/24", "") + str(i))
    return lista_ips


if __name__ == "__main__":
    url = "http://ip-api.com/batch"
    arquivo = "lista_ips.txt"
    ips = []
    salvar_lista_hosts = False
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
                range_ips = extract_range_ips(ip, range_ips)

        if salvar_lista_hosts:
            try:
                with open("lista_hosts.txt", "+w") as file:
                    for ip in range_ips:
                        file.write(ip + "\n")
            except FileNotFoundError:
                print(f"Arquivo não encontrado")
        
        executar_geolocation(url, range_ips)

        # dados = executar_geolocation(url, range_ips)
        # if dados:
        #     for dado in dados:
        #         print(f"IP: {dado['query']}, Cidade: {dado['city']}, Estado: {dado['region']}, País: {dado['country']} ({dado['countryCode']})")