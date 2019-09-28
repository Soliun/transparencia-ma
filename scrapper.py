import requests
from bs4 import BeautifulSoup as BS
from babel.numbers import parse_decimal
def despesas_total (ano):
    url_base = "http://www.transparencia.ma.gov.br/app"
    url = url_base + "/despesas/por-funcao/"+ano
    return extrai_despesas (url)
    
def despesas_por_funcao (cod, ano):
    url_base = "http://www.transparencia.ma.gov.br/app"
    url = url_base + "/despesas/por-funcao/"+ano+"/funcao/"+cod
    return extrai_despesas (url)

def despesas_por_orgao (orgao, funcao, ano):
    url = "http://www.transparencia.ma.gov.br/app/despesas/por-funcao/"+ano+"/funcao/"+funcao+"/orgao/"+orgao+"?#lista"
    response = requests.get(url)
    page = BS(response.text, 'lxml')
    table = page.find ('table')
    rows = table.find_all('tr')
    despesas = []
    for row in rows[1:]:
        cols =row.find_all("td")
        despesa = {}
        despesa["nome"] = cols[0].find("a").get_text().strip()
        despesa["url_detalhe"] = cols[0].find("a").get('href')
        despesa["cpf/cnpj"] = cols[0].find("small").get_text().strip().replace ("CPF/CNPJ: ","")
        despesa["empenhado"] =  parse_decimal(cols[1].get_text().strip(), locale='pt_BR')
        despesa["liquidado"] =  parse_decimal(cols[2].get_text().strip(), locale='pt_BR')
        despesa["pago"] = parse_decimal (cols[3].get_text().strip(), locale='pt_BR')
        despesas.append(despesa)
    return despesas

def extrai_despesas (url):
   response = requests.get(url)
   page = BS(response.text, 'lxml')
   table = page.find ('table')
   rows = table.find_all('tr')
   despesas = []
   for row in rows[1:]:
       cols =row.find_all("td")
       despesa = {}
       despesa["codigo"]  = cols[0].get_text().strip()
       despesa["nome"] = cols[1].find("a").get_text().strip()
       despesa["url_detalhe"] = cols[1].find("a").get('href')
       despesa["empenhado"] =   parse_decimal (cols[2].get_text().strip(), locale='pt_BR')
       despesa["liquidado"] =  parse_decimal (cols[3].get_text().strip(), locale='pt_BR')
       despesa["pago"] =  parse_decimal (cols[4].get_text().strip(), locale='pt_BR')
       despesas.append(despesa)

   return despesas  