#!/usr/bin/env python

import requests
import sys
import os
from termcolor import colored, cprint
from bs4 import BeautifulSoup

cep = sys.argv[1:]
rua = []
bairro = []
cidade = []

if len(sys.argv) == 1:
	cprint('''
	 ██████╗███████╗██████╗      ██████╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗██╗  ████████╗███████╗██████╗
	██╔════╝██╔════╝██╔══██╗    ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║   ██║██║  ╚══██╔══╝██╔════╝██╔══██╗
	██║     █████╗  ██████╔╝    ██║     ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     ██║   █████╗  ██████╔╝
	██║     ██╔══╝  ██╔═══╝     ██║     ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██║   ██╔══╝  ██╔══██╗
	╚██████╗███████╗██║         ╚██████╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗██║   ███████╗██║  ██║
	 ╚═════╝╚══════╝╚═╝          ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝
	''', 'yellow', attrs=['bold'])
	cprint('[*]--------------------------------------------------------------------------------------[*]', 'yellow', attrs=['bold'])
	cprint('[!] CEP CONSULTER v1.1', 'yellow', attrs=['bold'])
	cprint('[!] Usage: python3 cep_consulter CEP', 'yellow', attrs=['bold'])
	cprint('[*]--------------------------------------------------------------------------------------[*]', 'yellow', attrs=['bold'])

#Request in site
else:
	url_cep = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'
	payload = {'relaxation':cep,
		   'tipoCEP':'ALL',
		   'semelhante':'N'}
#Response
	response = requests.post(url_cep, data=payload)
	receive = (response.text.encode('utf-8'))

with open('correios.html', 'w') as correios:
    correios.write(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
try:
    #Parsing and printing
    row = soup.find_all('tr')[1:]
    col = soup.find_all('td')
    coluna_rua = col[0].string.strip()
    rua.append(coluna_rua)
    coluna_bairro = col[1].string.strip()
    bairro.append(coluna_bairro)
    coluna_cidade = col[2].string.strip()
    cidade.append(coluna_cidade)
    cprint('********[FOUND]********', 'green', attrs=['bold'])
    cprint('Rua:    '+str(rua), 'green', attrs=['bold'])
    cprint('Bairro: '+str(bairro), 'green', attrs=['bold'])
    cprint('Cidade: '+str(cidade), 'green', attrs=['bold'])
except IndexError:
    cprint('NOT FOUND', 'red', attrs=['bold'])

#Remove html file parsing
remove = os.system('rm correios.html')
