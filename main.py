import requests 
from bs4 import BeautifulSoup
import pandas as pd

r  = requests.get('https://rn.olx.com.br/imoveis/aluguel/apartamentos')
count = 1;

titulos = []
links = []
precos = []
detalhes = []
data = []
dicionario = dict() 

while r.status_code == 200:


	html_doc = r.text #instancia a variavel html_doc com o HTML recebido
	#transforma pagina recebida em um obj do bs4 
	soup = BeautifulSoup(html_doc, 'html.parser') 

	anuncios = soup.findAll('a', {"class": 'OLXad-list-link'})
	divs_precos = soup.findAll('div', {"class": 'col-3'})
	descricoes = soup.findAll('p', {"class": 'text detail-specific'})

	

	for anuncio in anuncios:
		titulos.append(anuncio['title'])

	for anuncio in anuncios:
		links.append(anuncio['href'])

	for divs_preco in divs_precos:
		precos.append(divs_preco.getText())

	for descricao in descricoes:
		detalhes.append(descricao.getText())



	for i in range(0,len(titulos)):
		dicionario['titulo'] = titulos[i]
		dicionario['link'] = links[i]
		dicionario['preco'] = precos[i]
		dicionario['detalhe'] = detalhes[i]
		data.append(dicionario)
		dicionario = {}



	

	count = count + 1;
	try:
		r = requests.get('https://rn.olx.com.br/imoveis/aluguel/apartamentos?o='+str(count))
	except IndexError:
		print ("Erro na requisicao")



df = pd.DataFrame(data).dropna()

df['detalhe'] = df['detalhe'].str.replace('([\n\t])', '')
df['detalhe'] = df['detalhe'].str.replace('(\s{3,})', '')

#print df
df.to_csv('resultados.csv', encoding = 'latin')




