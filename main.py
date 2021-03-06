#Bibliotecas Necessárias
import time
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import sqlite3

#Conectando o banco de dados
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

#loop para repetiro o processo 100 vezes
i = 0 
while (i < 100): 

    #fazendo um select no banco com todos os dados dos produtos
    cursor.execute ('SELECT * FROM blog_produto')
    row = cursor.fetchone()

    while row is not None:
        
        # Cada iteração eu guardo os campos dos banco nas variáveis
        sku = row [1]
        descricao = row[2]        
        url = row[3]
        habilitado = row [4]
        buybox = row [5]
        menorpreco = row [6]
        loja = row [7]
        site = row [8]

        
        # Perguntando se o produto está habilitado para o monitoramento.
        if (habilitado == "Sim"): 

            # Instanciando o mozila para fazer a pesquisa em background
            option = Options()
            option.headless = True
            driver = webdriver.Firefox(options=option)
            driver.get(url)
            
            # Processo de captura dos dados na pagina usando Xpath
            # No caso do site da americanas o layout quando o vendedor é a propria americanas muda, então aplico um try/except
            try:
                Seller = driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/span/a").text                     
            except: 
                Seller = "Americanas"
            
            Preco  = driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div/section/div/div[2]/div[2]/div[1]/div/div[1]").text

            # Se o seller não for minha loja enviar email pra mim
            if Seller != loja :


                email = ''
                password = ''
                send_to_email = ''
                subject = ''
                message = ''

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                

                # Convertendo e ajustando o servidor para enviar o email
                msg.attach(MIMEText(message, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string() # Convertendo a mensagem em string para enviar!
                server.sendmail(email, send_to_email, text)
                server.quit()

            # Se eu for o vendedor principal, caio dentro deste else    
            else:
                print ("Preço OK!")

            # Fechar o navegador
            driver.close()
            
    
        # Se não estiver sendo monitorado, caio dentro desse else
        else:
            print ("Não monitorado")    

        # Separa os items dentro do loop no banco (Caso exclua fica preso dentro do mesmo item)
        row = cursor.fetchone()


            

    time.sleep(7200)
    connection.commit()
