import requests
import time

def fazer_requisicao(url, data=[]):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
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
        print(f"Executando requisição {i+1} de {int(len(data)/15)}")
        for j in range(15):
            response = fazer_requisicao(url, data[i])
            if not response:
                continue

            for dado in response:
                if dado['region'] == "MS":
                    print(f"IP: {dado['query']}, Cidade: {dado['city']}, Estado: {dado['region']}, País: {dado['country']} ({dado['countryCode']})")
        if i+1 == len(data):
            print("Fim das requisições")
            break
        print(f"Tempo restante para próxima requisição: {start_func + 60 - int(time.time())} segundos")
        time.sleep(start_func + 60 - int(time.time()))

def extract_range_ips(ip: str, lista_ips: list):
    for i in range(1,256):
        lista_ips.append(ip.replace("0/24", "") + str(i))
    return lista_ips

def geolocation_by_file():
    url = "http://ip-api.com/batch"
    arquivo = "lista_ips.txt"
    ips = []
    salvar_lista_hosts = False
    try:
        with open(arquivo, "r") as file:
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

def geolocation_by_ip(ip: str):
    url = f"http://ip-api.com/json/{ip}"
    response = fazer_requisicao(url)
    if response:
        print(f"IP: {response['query']}, Cidade: {response['city']}, Estado: {response['region']}, País: {response['country']} ({response['countryCode']})")


def find_ip_in_list_range(ip_to_find: str|list):
    try:
        arquivo = "lista_ips.txt"
        with open(arquivo, "r") as file:
            lista_ips = file.readlines()
            lista_ips = [ip.strip() for ip in lista_ips]
        
        if lista_ips:
            range_ips = []
            for ip in lista_ips:
                if "/32" in ip:
                    range_ips.append(ip.replace("/32", ""))
                elif "/24" in ip:
                    range_ips = extract_range_ips(ip, range_ips)
                
            for atual_ip in ip_to_find:
                if atual_ip in range_ips:
                    print()
                    print(f"IP {atual_ip} encontrado na lista de IPs")
                    print()
                    continue
                print()
                print(f"IP {atual_ip} não encontrado na lista de IPs")
                print()
            
            return
        
        print("Lista de IPs vazia")
        return

    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado")
        return
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return


if __name__ == "__main__":
    while True:
        try:
            print("Bem-vindo ao programa de geolocalização de IPs")
            print("1 - Consultar IP")
            print("2 - Consultar lista de IPs")
            print("3 - Localizar IP em arquivo")
            print("Aperte ctrl + c para sair")

            escolha = input("Digite a opção desejada: ")

            if escolha == "1":
                ip = input("Digite o IP: ")
                geolocation_by_ip(ip)
            elif escolha == "2":
                geolocation_by_file()
            elif escolha == "3":
                ip = input("Digite o IP (separe por ,): ")
                ip = ip.split(",")
                find_ip_in_list_range(ip)
            else:
                raise Exception("Opção inválida")
        except KeyboardInterrupt:
            print("Programa encerrado pelo usuário\n")
            quit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")