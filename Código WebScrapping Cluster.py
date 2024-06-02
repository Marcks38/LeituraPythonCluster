import re
from bs4 import BeautifulSoup
import pandas as pd

with open('C:\\Users\\mgoul\\OneDrive\\Área de Trabalho\\Empresas - Parque de Inovação Tecnológica São José dos Campos.txt', 'r', encoding='utf-8') as arquivo:
    html_string = arquivo.read()

# Função para extrair os detalhes da empresa
def extrair_detalhes_empresa(html):
    # Inicializa o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Encontra todas as divs com a classe 'search-filter-ficha'
    empresas = soup.find_all('div', class_='search-filter-ficha')
    
    # Lista para armazenar os detalhes das empresas
    detalhes_empresas = []
    
    # Itera sobre cada div de empresa
    for empresa in empresas:
        # Extrai o título da empresa
        titulo = empresa.find('h4').text.strip()
        
        # Extrai o telefone da empresa
        telefone_match = re.search(r'\(\d{2}\) \d{1,5}-\d{4}', str(empresa))
        telefone = telefone_match.group() if telefone_match else None
        
        # Extrai os sites da empresa
        sites = [a['href'] for a in empresa.find_all('a', href=re.compile(r'http|https'))]
        
        # Adiciona os detalhes da empresa à lista
        detalhes_empresas.append({'empresa': titulo, 'telefone': telefone, 
                                  'site1': sites[0] if sites else None, 
                                  'site2': sites[1] if len(sites) > 1 else None, 
                                  'site3': sites[2] if len(sites) > 2 else None})
    
    return detalhes_empresas

# Extrai os detalhes das empresas da string HTML
detalhes_empresas = extrair_detalhes_empresa(html_string)

# Criar um DataFrame pandas com os detalhes das empresas
df = pd.DataFrame(detalhes_empresas)

# Exporta o DataFrame para um arquivo Excel
df.to_excel('detalhes_empresas.xlsx', index=False)
