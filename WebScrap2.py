import requests
from bs4 import BeautifulSoup
import pandas as pd

def extrair_texto_div(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontra a div com a classe "wf-container-main"
        div_wf_container = soup.find('div', class_='wf-container-main')

        # Inicializa uma lista para armazenar os textos extraídos
        textos = []

        if div_wf_container:
            # Encontra todos os blocos <p> dentro da div "wf-container-main"
            paragrafos = div_wf_container.find_all('p')

            # Extrai o texto de cada bloco <p> e adiciona à lista
            for p in paragrafos:
                texto = p.get_text(separator='\n', strip=True)
                textos.append(texto)

        # Retorna o texto concatenado em uma única string com quebra de linha
        return '\n'.join(textos) if textos else None

    except requests.exceptions.Timeout:
        return f"Tempo limite de conexão excedido para: {url}"

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro ao tentar acessar a URL {url}: {e}"

# Função para ler os URLs de um arquivo de texto
def ler_urls(filename):
    with open(filename, 'r') as file:
        urls = file.readlines()
        # Remover quebras de linha e espaços em branco extras
        urls = [url.strip() for url in urls]
    return urls

# Caminho do arquivo de texto contendo os URLs
caminho_arquivo = r"C:\Users\mgoul\OneDrive\Área de Trabalho\Empresas.txt"

# Ler os URLs do arquivo de texto
urls = ler_urls(caminho_arquivo)

# Inicializa uma lista para armazenar os textos extraídos de cada URL
textos_extraidos = []

# Itera sobre a lista de URLs e extrai o texto de cada bloco <div> de conteúdo
for i, url in enumerate(urls, start=1):
    resultados = extrair_texto_div(url)
    textos_extraidos.append(resultados)
    print(f"Processando URL {i} de {len(urls)}...")

# Verifica se o número de URLs e de textos extraídos são iguais
if len(urls) == len(textos_extraidos):
    # Cria um DataFrame com as listas de URLs e textos extraídos
    df = pd.DataFrame({'URL': urls, 'Texto': textos_extraidos})

    # Salva os resultados em uma planilha Excel
    df.to_excel(r"C:\Users\mgoul\OneDrive\Área de Trabalho\result.xlsx", index=False)

    print("Os resultados foram salvos com sucesso em 'result.xlsx'.")
else:
    print("O número de URLs e de textos extraídos não é igual. Verifique os URLs ou tente novamente.")
