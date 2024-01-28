from tkinter import *
import xml.etree.ElementTree as ET

import requests, pprint
from bs4 import BeautifulSoup

from threading import Thread
import time



def Clear_Frame(page):
    for widget in page.winfo_children():
        widget.destroy()


#Функция Update_Data_Base делает запрос в ЦБ РФ и получает ответ в виде xml
#После формирует перменную info_currencys типа dict.
def Update_Data_Base():
    while True:
        try:
            page = requests.get('https://cbr.ru/scripts/XML_daily.asp')
            soup = BeautifulSoup(page.content, 'lxml-xml')
            break
        except:
            pass

    names = soup.findAll("Name")
    currencys = soup.findAll("CharCode")
    quantitys = soup.findAll("Value")
    rate = soup.findAll("VunitRate")
    
    info_currencys = {}

    for index, name in enumerate(names):
        info_currencys[currencys[index].text] = {'name':name.text,'price':str(quantitys[index].text).replace(',','.'), \
                                                 'one':str(rate[index].text).replace(',','.'),'code':currencys[index].text}

    #{'USD':{'name':'Доллар США','price': 88,'one':88,'code':'USD'},'KZT':{...},...}
        
    return info_currencys       
    
def Currencys_Page():
    old_quantity = 'Empty'


    while True: 
        quantity = quantiry_entry.get()
        if quantity == '':
            quantity = None
        elif quantity.isdigit() == True:
            quantity = int(quantity)
        else:
            quantity = None
            
        if old_quantity != quantity:#Проврека было ли изменено поле ввода. 
            code_entry = label_currency['text']
            if quantity != None and label_currency['text'] != 'RUB':#Создание Labels если в поле было введено значение + поменяна валюта
                Clear_Frame(currency_frame)
                
                row = 0
                column = 0

                info_currencys = Update_Data_Base()
            
                for code in info_currencys:
                    rubs = quantity*float(info_currencys[code_entry]["one"])
                    result = "%.3f" % float(rubs/float(info_currencys[code]["one"]))
                    Label(currency_frame,text = f'{quantity} {code_entry} = {result} {code} ').grid(row = row, column = column)
                    row+=1
                    if row > 21:
                        column += 1
                        row = 0
                result_rub = "%.3f" % float(rubs/float(info_currencys[code]["one"]))
                Label(currency_frame,text = f'{quantity} {code_entry} = {result_rub} RUB ').grid(row = row, column = column)
                old_quantity = quantity
            if quantity == None:#Создает Labels  с дефолтными натроиками 1 валюта = N рублей 
                Clear_Frame(currency_frame)
                row = 0
                column = 0
                info_currencys = Update_Data_Base()
                for code in info_currencys:
                    price = "%.3f" % float(info_currencys[code]["one"])
                    Label(currency_frame,text = f'1 {code} = {price} RUB ').grid(row = row, column = column)
                    row+=1
                    if row > 21:
                        column += 1
                        row = 0
                old_quantity = quantity
        

        time.sleep(0.1)
        
    


def Change_Currency(widget,setting,change):
    widget[setting] = change


def Menu_Code_Currency():
    def popup(event):
        global x, y
        x = event.x
        y = event.y
        menu.post(event.x_root, event.y_root)

    x = 0
    y = 0
    
    temp = Update_Data_Base()
    window.bind("<Button-3>", popup)
    menu = Menu(tearoff=0)
    for i in temp:
        menu.add_command(label=f"{temp[i]['code']} {temp[i]['name']}", command = lambda x = i:Change_Currency(label_currency,'text',temp[x]['code']))

    listbox = Listbox(currency_frame)
    

    




if __name__ == "__main__":
    
    window = Tk()
    window.title("Конвентер валют")
    window.geometry('300x500')
##    window.resizable(width = False, height = False)

    entry_frame = Frame(window)
    currency_frame = Frame(window)

    entry_frame.pack(side = TOP,fill=X)
    currency_frame.pack(side = TOP,fill=X)

    label_quantity = Label(entry_frame,text = 'Количество : ')
    label_quantity.pack(side = LEFT)

    label_currency = Label(entry_frame,text = 'RUB')
    label_currency.pack(side = RIGHT)

    quantiry_entry = Entry(entry_frame)
##    quantiry_entry.insert(0,'empty')
    quantiry_entry.pack(side = LEFT,fill=BOTH,expand=1)
    
    Menu_Code_Currency()
    
    currency_page = Thread(target=Currencys_Page,name='Currencys_Page',args=())
    currency_page.start()
    window.mainloop()
