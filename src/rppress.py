#!/usr/bin/env python
# coding: utf-8

# In[191]:


import numpy as np
import csv
import pandas as pd
import scipy as sp
import re
import string
from collections import OrderedDict
import operator
import datetime
import matplotlib.pyplot as plt
import time
import sys
# In[192]:


subjects = []


def check_ctrl_words(line):
    words = ['added', 'now an admin', 'removed', 'changed the group',
             'created group', 'changed this group', 'changed the subject', 'left']
    for w in words:
        if w in line:
            if 'changed the subject' in line:
                  #  print(line)
                subjects.append(line)
            return True


def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = input.lower()
    #input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
    #
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput


def ngrams(input, n):

    #input = input.split(' ')
    input = cleanInput(input)
    output = []
    if n > len(input):
        n = len(input)
    for i in range(len(input)):
        if i > len(input)-n:
            n -= 1
        for j in range(1, n+1):
            output.append(' '.join(input[i:i+j]))
    return output

# In[269]:




rpfile="/home/miguel/Documents/RadioPatio/WhatsApp Chat with Radio Patio es Cuba.txt"
rpfile = sys.argv[1]
#rpfile = "/home/miguel/Documents/RadioPatio/Musulungos.txt"

ff = open(rpfile, 'r')
data = []
datadic = {"Person": [], "Hora": [], "Fecha": [], "Mensaj": [], "Epoch": []}

count = 0

markdowntxt = """
# Radio Patio Andante

Película de Miyazaki sobre un discreto pero peligroso patio en Moscú, en un castillo vagabundo japonés que es un bombón en pleno cerro de Caracas, donde discuten y dan chucho jóvenes y no tan jóvenes sobre el universo, mientras piden Mcdonalds, los observan ninjas y agentes de la KGB, enjuician terroristas sumarísimamente, y una poderosa fuerza los empuja a mudarse  o a desaparecer por la fuerza. Seguro son talibanes que escriben libros en defensa del machismo. Qué no los cojan las feministas feminazis.



"""


thisday = "UnDia"
thishour = "UnaHora"

mdfile = open("radiopatio.md", 'w')
mdfile.write(markdowntxt)
vecinos = []

corpus = {}

while True:
    count += 1
#    if count == 10:
#        break
    line = ff.readline()
#    print line
    if line == "":
        break

    if 'Messages to this group are now secured with end' in line:
        continue
    if check_ctrl_words(line) == True:
        system = line.split('-')[1]
        mdfile.write("\n\n### ")
        mdfile.write(system)

        continue

    try:
        print("here")
        fecha = line.split(",")[0]
        if len(fecha) > 8 or fecha == '\n' or fecha == ".\n":
            continue
        hora = line.split(",")[1].split("-")[0]

        if len(hora) > 7:  # Fast jumping some errors
            continue
        vecino = line.split(",")[1].split("-")[1].split(": ")[0]
        mensaj = line.split(",")[1].split("-")[1].split(": ")[1]
        if len(mensaj) == 0:
            continue

    except:
        pass
#        print "Error line %s: %s"%(count,line)
#    print fecha,vecino

    justhora = hora.split(":")[0]

    if fecha.strip(" ").lstrip(" ") != thisday.strip(" ").lstrip(" "):
        thisday = fecha

        mdfile.write("\n## ")
        mdfile.write(thisday)
    if justhora != thishour.split(":")[0]:
        thishour = justhora
        mdfile.write("\n### Las "+thishour+":00 horas\n")

    mdfile.write("\n**")
    try:
        mdfile.write(vecino)
        mdfile.write(":**  ")
        mdfile.write(mensaj)
    except: 
        pass
    try:
        if mensaj[-1] != "\n":
            mdfile.write('\n')
    except:
        continue

    try:
        epoch = time.strftime("%s", time.strptime(
            ' '.join([fecha, hora.strip()]), '%m/%d/%y %H:%M'))
    except:
        continue  # revisar porque se salta

    datadic["Person"].append(vecino)
    datadic["Hora"].append(justhora)
    datadic["Fecha"].append(fecha)
    datadic["Mensaj"].append(mensaj.strip())
    datadic["Epoch"].append(epoch)
    data.append([fecha.strip().lstrip(), hora.strip().lstrip(),
                 justhora, vecino.strip().lstrip(), mensaj.strip()])
    if vecino.strip() not in vecinos:
        vecinos.append(vecino.strip())

    ngram = ngrams(mensaj, 5)

    for gr in ngram:
        if gr not in corpus:
            corpus[gr] = 0
        corpus[gr] += 1


# ## Stats

# In[270]:


rpbd = pd.DataFrame(datadic)
rpbd1 = pd.DataFrame(data)


# In[ ]:


# In[271]:


#rpbd1.describe()


# In[272]:


# writer = pd.ExcelWriter('RadioPatio.xlsx')
# rpbd.to_excel(writer, 'RadioPatio')
rpbd1.to_csv(open('RadioPatio.csv', 'w'), sep='\t')
# 

# In[273]:


def freq(data, interval=100000):   # intervalo listo para que de bugs dentro de 2500 años !!!
    """ Intervalo, cantidad de dias a mostrar"""
    freqs = {"Personas": {}, "Horas": {}, "Dias": {}}
    print(freqs)
    hoy = datetime.date.today()
    for msg in data:
        try:
            msgd = list(map(int, msg[0].split('/')))
        except:                            # si llega al final o a una linea con mensajes del sistema
            continue
        if msgd[2] < 100:
            msgd[2] = 2000+msgd[2]
        # print msgd,int(msgd[2]),int(msgd[0]),int(msgd[1])
        d = datetime.date(msgd[2], msgd[0], msgd[1])
        # print d,hoy,hoy-d

        if hoy - d > datetime.timedelta(interval):
            continue

        if msg[0] not in freqs["Dias"]:
            freqs["Dias"][msg[0]] = 1
        if msg[2] not in freqs["Horas"]:
            freqs['Horas'][msg[2]] = 1
        if msg[3] not in freqs["Personas"]:
            freqs["Personas"][msg[3]] = 1
        freqs["Dias"][msg[0]] += 1
        freqs["Horas"][msg[2]] += 1
        freqs["Personas"][msg[3]] += 1
    return freqs


# In[274]:


f = pd.DataFrame(freq(data))
freqs = freq(data, interval=45)


# In[275]:


Pers = pd.DataFrame({"Personas": list(freqs["Personas"].keys(
)), "Mensajes": list(freqs['Personas'].values())}, index=list(freqs['Personas'].keys()))
Dias = pd.DataFrame(
    {"Dias": list(freqs["Dias"].keys()), "Mensajes": list(freqs["Dias"].values())})
Horas = pd.DataFrame({"Horas": list(freqs["Horas"].keys(
)), "Mensajes": list(freqs["Horas"].values())}, index=list(freqs['Horas'].keys()))


# In[279]:


Dias.sort_values(by=["Mensajes"], ascending=False)
Horas = Horas.sort_values(by=["Horas"])
Pers.sort_values(by=["Mensajes"], ascending=False)


# In[277]:


Pers.to_csv(open('Personas.csv', 'w'))
Dias.to_csv(open('Dias.csv', 'w'))
Horas.to_csv(open('Horas.csv', 'w'))


# In[278]:


fig = plt.figure(figsize=(30, 14), dpi=250)
fig.suptitle('Estadisticas del Grupo')
ax1 = fig.add_subplot(121)
ax1.set_title('Los 10 + activos')
Pers.sort_values(by=["Mensajes"], ascending=False).head(10).plot(
    kind='pie', y='Mensajes', ax=ax1, legend=False, autopct='%1.1f%%', fontsize=18)
ax2 = fig.add_subplot(122)
ax2.set_title('Mensajes distribuidos por hora')
Horas.plot(kind='bar', y='Mensajes', ax=ax2, legend=False)
plt.savefig('stats.png')

# In[14]:


a = OrderedDict()


# In[15]:


a['23'] = 1

sorted(list(corpus.items()), key=operator.itemgetter(1), reverse=True)
