from cProfile import label
from ctypes import windll
import tkinter as tk
from tkinter import ttk #combobox
from json import decoder
from turtle import bgcolor, position, update, width
from urllib import response
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from pprint import pprint
import logging
from cgitb import text
from textwrap import fill
from tkinter import *
from tkinter import messagebox
from matplotlib import image
import matplotlib.pyplot as plt
import csv
import pandas_datareader.data as reader
import datetime as dt
import matplotlib.pyplot as plt
from requests import request
import requests
import seaborn as sns
from datetime import datetime, timedelta

import pandas as pd
import pandas_datareader as pdr
import plotly.graph_objects as go



logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = ""
rpc_pass = ""
rpc_host = ""
rpc_client = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@{rpc_host}:8332", timeout=120)


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        def block():
            top=Toplevel()
            korisnikUnos = int(unos.get()) 
            blockhash = rpc_client.getblockhash(korisnikUnos)
            block_info = rpc_client.getblock(blockhash)
            block_stats = rpc_client.getblockstats(blockhash)
            print("\n\tBlock Reward (subsidy): "+str(block_stats["subsidy"]/100000000)+" BTC")
            print("\tFee Reward: "+str(block_stats["totalfee"]/100000000)+" BTC")
            print("\tTransaction volume: "+str(block_stats["total_out"]/100000000)+" BTC")
            
            Label(top, text= 'Block information:', font=("poppins",20,"bold"), pady=10, bg='green').pack()
            Label(top, text='\nHASH: \n' +str(block_info['hash']) +'\n\nNumber of transactions: \n'+str(block_info['nTx'])+ '\nHeight: '+str(block_info['height'])+'\nNonce: '+str(block_info['nonce'])
                +'\n\nBlock reward: \n'+str(block_stats["subsidy"]/100000000)+' BTC'+'\nFee reward: \n'+str(block_stats["totalfee"]/100000000)+' BTC'+'\nTransaction volume: \n'+str(block_stats["total_out"]/100000000)+' BTC'
                +'\n\nPreviousblockhash: \n'+str(block_info['previousblockhash'])+'\n\nNextblockhash: \n'+str(block_info['nextblockhash'])+'\n\n', font=("poppins",14,"normal")).pack()
            
            def blockTransactions():
                top=Toplevel()
                textTX=Text(top, width=100, height=40)
                textTX.tag_configure("tag_name", justify='center')
                textTX.insert("1.0", 'TX: \n'+str(block_info['tx']) +'\n\n')
                textTX.tag_add("tag_name", "1.0", "end")
                textTX.pack()
            tk.Button(top, text='Transactions of block', width=30,bg="purple",fg="white", command=blockTransactions).pack(side="top", pady=20)


        def adrese(transaction_info,len_output):
            lista = []
            for x in range(0,len_output): 
                try:
                    adresa = transaction_info["vout"][x]["scriptPubKey"]["addresses"]
                    value = transaction_info["vout"][x]["value"]
                    lista.append(str(adresa).lstrip("['").rstrip("']"))
                    lista.append("("+str(value)+" BTC"+")")
                    print("\taddress: "+str(adresa)+" value: "+str(value))  
                except:
                    x+=1
                    continue 
            lista = '\n'.join(lista)
            return lista


        def transakcija():
            top=Toplevel()
            korisnikUnos = str(unos.get())
            transaction = rpc_client.getrawtransaction(korisnikUnos)
            transaction_info = rpc_client.decoderawtransaction(transaction)
            len_output = len(transaction_info["vout"])
            
            dict1 = {}
            total_output, total_input = 0, 0
            for x in range(0, len_output):
                total_output = total_output+transaction_info["vout"][x]["value"]
            print("Total Output: ", total_output)

            duljina_vin_ = len(transaction_info["vin"])
            for x in range(0, duljina_vin_):
                dict1[transaction_info["vin"][x]["vout"]] = transaction_info["vin"][x]["txid"]
            print("\nTxId: ",dict1)
            
            for key, value in dict1.items():
                dict_tran = rpc_client.getrawtransaction(dict1[key])
                decoded = rpc_client.decoderawtransaction(dict_tran)
                total_input = total_input+decoded["vout"][key]["value"]
            print("\nTotal Input: ",total_input)
            fees = total_input-total_output
            print("\nFees: ", fees)

            lista_adresa = adrese(transaction_info,len_output)    
            Label(top, text = "Transaction details: ",font=("poppins",20,"bold"), pady=10, bg='green').pack()
            Label(top, text='\n\nHash: '+str(transaction_info['hash'])+'\nTxid: '+str(transaction_info['txid'])+'\nSize: '+str(transaction_info['size'])+ " bytes"+ '\nWeight: '+str(transaction_info['weight'])
                +'\n\nTotal Input: '+str(total_input)+" BTC"+'\nTotal Output: '+str(total_output)+" BTC" +'\nFees: '+str(fees)+" BTC"+ '\n\nAddresses: \n'+str(lista_adresa)
                +'\nBroj izlaza: '+str(len_output) +'\n\n',font=("poppins",14,"normal")).pack()
            
        
        tk.Frame.__init__(self, master)    
        tk.Label(self, text='Blockexplorer', bg='#f0f0f0', font=("poppins",20,"bold")).pack(side="top", fill="x", pady=20)
        
        photo = PhotoImage(file= './chart1.png') # Creating a photoimage object to use image 
        photoimg = photo.subsample(50,50) # Resizing image to fit on button
        label = tk.Label(self, image=photoimg)
        label.image = photoimg
        label.place(x=120, y=70)
        tk.Button(self, text="Historical info",bg="green",fg="white",
                  command=lambda: master.switch_frame(HistoryInfo)).pack(pady=15)
        
        '''photo = PhotoImage(file= './wallet.png') # Creating a photoimage object to use image 
        photoimg = photo.subsample(40,40) # Resizing image to fit on button
        label = tk.Label(self, image=photoimg)
        label.image = photoimg
        label.place(x=240, y=120)
        tk.Button(self, text="Wallet",bg="green",fg="white",
                  command=lambda: master.switch_frame(Wallet)).pack(pady=20) #BlockPage
        '''

        photo = PhotoImage(file= './transaction.png') # Creating a photoimage object to use image 
        photoimg = photo.subsample(50,50) # Resizing image to fit on button
        label = tk.Label(self, image=photoimg)
        label.image = photoimg
        label.place(x=120, y=130)
        tk.Button(self, text="MempoolTransactions",bg="green",fg="white",
                  command=lambda: master.switch_frame(TransactionPage)).pack(pady=5)

        photo = PhotoImage(file= './cryptoBtc.png') # Creating a photoimage object to use image 
        photoimg = photo.subsample(60,60) # Resizing image to fit on button
        label = tk.Label(self, image=photoimg)
        label.image = photoimg
        label.place(x=120, y=195)
        btn = tk.Button(self, text="Cryptocurrency prices",bg="green",fg="white",
                  command=lambda: master.switch_frame(CryptocurrencyPrices))
        btn.pack(padx=30, pady=30)

        tk.Label(self, text='Search your transaction or a block:\t', font=("poppins",14,"bold")).pack(side="top",fill="x", pady=10)
        unos=Entry(self, width=75)
        unos.insert(0,'Insert...')
        unos.pack(side="top")
        
        tk.Button(self, text='Block', width=10,bg="purple",fg="white", command=block).pack(side="left", pady=10)
        tk.Button(self, text='Transaction', width=10,bg="purple",fg="white", command=transakcija).pack(side="right", pady=10)
    
    


class BlockPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=30)

        hashbloka = rpc_client.getbestblockhash()
        blokinfo = rpc_client.getblock(hashbloka)
        Label(self, text = "INFO OF BEST BLOCK HASH:", font=("poppins",18,"bold")).pack(pady=30)
        text=Text(self, width=100, height=30)
        #text.place(x=240,y=120)
        text.tag_configure("tag_name", justify='center')
        text.insert("1.0", '\nHASH: \n' +str(blokinfo['hash'])+'\n\nTX: \n'+str(blokinfo['tx']) +'\n\nNONCE: \n'+str(blokinfo['nonce'])+ '\n\nDIFFUCULTY: \n'
                    +str(blokinfo['difficulty'])+ '\n\nnTX: \n'+str(blokinfo['nTx'])+'\n\nPREVIOUS BLOCK HASH: \n'+str(blokinfo['previousblockhash']+'\n\n'))
        text.tag_add("tag_name", "1.0", "end")
        text.pack()

class Wallet(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=10)
        Label(self, text = "Bitcoin Wallet", font=("poppins",18,"bold")).pack(pady=10)

        '''
        my_private_key = random_key()
        public_key = privtopub(my_private_key)
        wallet_address = pubtoaddr(public_key)
        

        def generateaddress():
            addressentry.delete(0,END)
            addressentry.insert(END,wallet_address)
        '''

        Balance = Label(self,text="Balance:",font=('bold',14),border=0)
        Balance.pack(padx=5, pady=5)

        Btcbalance = Label(self,text="0.000000Btc",font=('bold',12),border=0)
        Btcbalance.pack(pady=10)

        recentwithdraw = Label(self,text="Withdraw:",font=('bold',14),border=0)
        recentwithdraw.pack(pady=10)

        withdrawtext = Label(self,text="0.00000000Btc",font=('bold',12),border=0)
        withdrawtext.pack(pady=10)
'''
        send = Label(self,text="Send:",font=("bold",14),border=0)
        send.place(x=50,y=160)

        sendtext = Label(self,text="0.00000000Btc",font=('bold',12),border=0)
        sendtext.place(x=110,y=163)

        revicced = Label(self,text="Revicced:",font=('bold',14),border=0)
        revicced.place(x=50,y=190)

        reviccedtext = Label(self,text="0.00000000Btc",font=('bold',12),border=0)
        reviccedtext.place(x=137,y=193)

        #recent transaction
        recent_Label = Label(self,text="Recent Transaction",font=("bold",24),border=0)
        recent_Label.place(x=400,y=50)

        Norevviced = Label(self,text="No AnyRecent\nTransaction",font=('bold',28),border=0,foreground="#999999")
        Norevviced.place(x=430,y=130)

        #Button Generate Wallet Adddress
        Generate = Button(self,text="Generate Address",width=20,height=1,relief='groove') #command=generateaddress
        Generate.place(x=260,y=250)

        addressentry = Entry(self,width=50,border=0,font=('bold',18))
        addressentry.place(x=30,y=280)

        #Send Bitcoin
        SendBitcoin = Button(self,text="Send Bitcoin",width=20,height=1,relief='groove')
        SendBitcoin.place(x=260,y=320)

        reviccedsentry = Entry(self,width=50,border=0,font=('bold',18))
        reviccedsentry.place(x=30,y=360)'''


class TransactionPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=30)
        
        def listOfTxs():
            buttons={}
            vars=[] 
            brojac = 0

            transactions = rpc_client.getrawmempool() #getrawmempool will give you all transactions "txid" in mempool
            for i in transactions:
                brojac+=1
            print("\nTRANSAKCIJA IMA: "+str(brojac)+" \n")

            for i,x in enumerate(transactions):

                def adrese(transaction,len_output):
                    lista = []
                    for x in range(0,len_output):
                        try:
                            adresa = transaction["vout"][x]["scriptPubKey"]["addresses"]
                            value = transaction["vout"][x]["value"]
                            lista.append(str(adresa).lstrip("['").rstrip("']"))
                            lista.append("("+str(value)+" BTC"+")")
                            print("\taddress: "+str(adresa)+" value: "+str(value))
                        except:
                            x+=1
                            continue
                    lista = '\n'.join(lista)
                    return lista
                        

                def GetTransactionInfo(id=x):
                    top=Toplevel()
                    print("\n\nTxId IZNOSI: "+str(id)+" \n")
                    txid = rpc_client.getrawtransaction(id)  #it will give you detailed transaction in json
                    transaction = rpc_client.decoderawtransaction(txid)
                    len_output = len(transaction["vout"])
                    print("len_output: "+str(len_output))
                    dict1 = {}
                    total_output, total_input = 0, 0
                    for x in range(0, len_output):
                        total_output = total_output+transaction["vout"][x]["value"]
                    print("Total Output: ", total_output)

                    duljina_vin_ = len(transaction["vin"])
                    for x in range(0, duljina_vin_):
                        dict1[transaction["vin"][x]["vout"]] = transaction["vin"][x]["txid"]
                    print("\nTxId: ",dict1)
                    
                    for key, value in dict1.items():
                        dict_tran = rpc_client.getrawtransaction(dict1[key])
                        decoded = rpc_client.decoderawtransaction(dict_tran)
                        total_input = total_input+decoded["vout"][key]["value"]
                    print("\nTotal Input: ",total_input)
                    fees = total_input-total_output
                    print("\nFees: ", fees)

                    lista_adresa = adrese(transaction,len_output)
                    Label(top, text= 'Transaction details:', font=("poppins",20,"bold"), pady=10, bg='green').pack()
                    Label(top, text= '\n\nHash = ' + transaction['hash'] + '\nTxid = ' + str(transaction['txid'])+ '\nSize = ' +str(transaction['size'])+ " bytes" + '\nWeight = ' + str(transaction['weight']) 
                        +'\n\nTotal Input: '+str(total_input)+" BTC"+'\nTotal Output: '+str(total_output)+" BTC" +'\nFees: '+str(fees)+" BTC"+'\n\nAddresses:\n' +str(lista_adresa) 
                        +'\nBroj izlaza: '+str(len_output) + '\n\n', font=("poppins",14,"normal")).pack()


                var = IntVar(value=0)
                buttons[x]=Button(self, text=str(i+1) +'.\t'+ x + '\n',pady=10,padx=95,command=GetTransactionInfo,bg='#007bff', width=86)
                buttons[x].pack()
                text.window_create("end", window=buttons[x])
                text.insert("end", "\n")
                #buttons.append(b)
                vars.append(var)
            
        button = Button(self, text = "Click here to refresh",command=lambda: master.switch_frame(TransactionPage))
        button.pack()

        #bg = PhotoImage(file="./btcImg.png")
        Label(self, text = "TRANSACTION LIST:",font=("poppins",18,"bold"),pady=30).pack()
        text = Text(self, cursor="arrow",width=100, height=30)
        vsb = Scrollbar(self, command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        text.tag_configure("tag_name", justify='center')
        vsb.pack(side="right", fill="y", pady=15)
        text.pack(side="left", fill="both", expand=True, pady=20)
        
        text.configure(state="disabled")
        listOfTxs()
        



class CryptocurrencyPrices(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="bottom", pady=10)

        OptionList = ["BTC","ETH","LTC","XLM","ADA","XRP"] #XLM-stellar, ADA-cardano, LTC-litecoin, XRP-ripple
        CRYPTOCURRENCIES = ['BTC','ETH','LTC','XLM','ADA','XRP']
        CURRENCY = 'USD'

        variable = tk.StringVar(self)
        variable.set(OptionList[0])
        opt = tk.OptionMenu(self, variable, *OptionList)
        opt.config(width=20, font=('Helvetica', 15))
        opt.pack(pady=30, expand=True)

        labelTest = tk.Label(self, text="", bg='#f0f0f0', font=("poppins",26,"bold"))
        labelTest.pack(side="top", fill="x", pady=10)
        labelTest.configure(text="{} price tracker".format(variable.get()))
        def callback(*args):
            labelTest.configure(text="{} price tracker".format(variable.get()))
        variable.trace("w", callback)

        
        labelPriceDollar=tk.Label(self,bg='#f0f0f0', font=("poppins",20,"bold"))
        labelPriceDollar.pack(side="top", fill="x", pady=50)
        labelPriceEuro=tk.Label(self,bg='#f0f0f0', font=("poppins",20,"bold"))
        labelPriceEuro.pack(side="top", fill="x", pady=5)
        labelTime=tk.Label(self,bg='#f0f0f0', font=("poppins",14,"normal"))
        labelTime.pack(side="bottom", fill="x", pady=90)

        def ispis():
            param = variable.get()
            url = "https://min-api.cryptocompare.com/data/price?fsym="+param+"&tsyms=USD,EUR"
            # https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,XLM,ADA,BTC,LTC,XRP&tsyms=USD,EUR&api_key=e56248b4375d1f77cb0396586a28206704f63699294658d021d97dd5acd8bf8c
            response = requests.get(url).json()
            priceDollar = response["USD"]
            priceEuro = response["EUR"]
            time = datetime.now().strftime("%H:%M:%S")
            print("price: "+str(priceDollar)+" "+str(priceEuro))
            print("time: "+time)
            labelPriceDollar.config(text="Dollar price:\t"+str(priceDollar)+" $")
            labelPriceEuro.config(text="Euro price:\t"+str(priceEuro)+" €")
            labelTime.config(text="Updated at: " +time)
            app.after(1000,ispis) #1sec
        #Button(self, text = "Refresh!", pady=5, padx=10, command=ispis, bg='#007bff').pack()
        ispis()   


        def getData(cryptocurrency):
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            last_year_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")

            start = pd.to_datetime(last_year_date)
            end = pd.to_datetime(current_date)

            data = pdr.get_data_yahoo(f'{cryptocurrency}-{CURRENCY}', start, end)

            return data

        def liveGraph():
            crypto_data = dict()
            for crypto in CRYPTOCURRENCIES:
                crypto_data[crypto] = getData(crypto)
            
            fig = go.Figure()

            # Scatter
            for idx, name in enumerate(crypto_data):
                fig = fig.add_trace(
                    go.Scatter(
                        x = crypto_data[name].index,
                        y = crypto_data[name].Close,
                        name = name,
                    )
                )

            fig.update_layout(
                title = 'The Correlation between Different Cryptocurrencies',
                xaxis_title = 'Date',
                yaxis_title = f'Closing price ({CURRENCY})',
                legend_title = 'Cryptocurrencies'
            )
            fig.update_yaxes(type='log', tickprefix='$')

            fig.show()

        
        tk.Button(self, text='Live graph',width=20, bg="purple",fg="white", command=liveGraph).pack(side="bottom", pady=20)      #.place(x=150, y=530)




class HistoryInfo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=30)
        Label(self, text="Historical information of the blockchain using graph", bg='#f0f0f0', font=("poppins",14,"bold")).pack(pady=20)

        def NumberOfTransactions(paramV):
            date_time = []; xDate = []
            numberOfTransactions = []
            #https://api.blockchain.info/charts/n-transactions?timespan=5weeks&rollingAverage=8hours&format=json - month
            api_url = "https://api.blockchain.info/charts/n-transactions-total?timespan="+paramV+"&format=json"
            response = requests.get(api_url)
            apiData = response.json()
            #print("\nAPI RESPONSE: ", apiData)

            for row in range(0, len(apiData["values"])):
                date_time.append(apiData["values"][row]["x"])
                numberOfTransactions.append(apiData["values"][row]["y"])

            for i in date_time:
                dateTime = dt.datetime.fromtimestamp(i).isoformat()
                date = dateTime[:10]
                time = dateTime[11:]
                xDate.append(date)
                #print("date: "+date+"   time: "+time)

            #print("Date: "+str(xDate)+" NoTX: "+str(numberOfTransactions))
            fig = go.Figure()
            fig = fig.add_trace(
                go.Scatter(
                    x = xDate,
                    y = numberOfTransactions
                )
            )
            fig.update_layout(
                title = 'The total number of transactions on the blockchain per '+paramV,
                xaxis_title = 'Date',
                yaxis_title = 'Transactions'
            )
            fig.update_yaxes(type='log')
            fig.show()           
        #tk.Button(self, text='NumberOfTransactions', width=30,bg="purple",fg="white", command=NumberOfTransactions).pack(side="top", pady=10)


        def TotalTransactionFees(paramV):
            date_time,fees,xDate = [],[],[]
            # https://api.blockchain.info/charts/fees-usd-per-transaction?timespan=1year&format=json
            api_url = "https://api.blockchain.info/charts/transaction-fees?timespan="+paramV+"&format=json"
            response = requests.get(api_url)
            apiData = response.json()

            for row in range(0, len(apiData["values"])):
                date_time.append(apiData["values"][row]["x"])
                fees.append(apiData["values"][row]["y"])

            for i in date_time:
                dateTime = dt.datetime.fromtimestamp(i).isoformat()
                date = dateTime[:10]
                time = dateTime[11:]
                xDate.append(date)
                #print("date: "+date+"   time: "+time)

            fig = go.Figure()
            fig = fig.add_trace(
                go.Scatter(
                    x = xDate,
                    y = fees
                )
            )
            fig.update_layout(
                title = 'The total BTC value of all transaction fees paid to miners over '+paramV,
                xaxis_title = 'Date',
                yaxis_title = 'BTC'
            )
            fig.update_yaxes(type='log')
            fig.show()
        #tk.Button(self, text='Total Transaction Fees (BTC)', width=30,bg="purple",fg="white", command=TotalTransactionFees).pack(side="top", pady=10)
        

        def AverageBlockSize(paramV):
            date_time,fees,xDate = [],[],[]
           
            api_url = "https://api.blockchain.info/charts/avg-block-size?timespan="+paramV+"&format=json"
            response = requests.get(api_url)
            apiData = response.json()

            for row in range(0, len(apiData["values"])):
                date_time.append(apiData["values"][row]["x"])
                fees.append(apiData["values"][row]["y"])

            for i in date_time:
                dateTime = dt.datetime.fromtimestamp(i).isoformat()
                date = dateTime[:10]
                time = dateTime[11:]
                xDate.append(date)
                #print("date: "+date+"   time: "+time)

            fig = go.Figure()
            fig = fig.add_trace(
                go.Scatter(
                    x = xDate,
                    y = fees
                )
            )
            fig.update_layout(
                title = 'The average block size over '+paramV,
                xaxis_title = 'Date',
                yaxis_title = 'MB'
            )
            fig.update_yaxes(type='log')
            fig.show()
        #tk.Button(self, text='Average Block Size (MB)', width=30,bg="purple",fg="white", command=AverageBlockSize).pack(side="top", pady=10)
        

         
        def BlockchainSize(paramV):
            sizeOfBlockChain,date_time,xDate=[],[],[]
            # https://api.blockchain.info/charts/blocks-size?timespan=30days&format=json
            api_url = "https://api.blockchain.info/charts/blocks-size?timespan="+paramV+"&format=json"
            response = requests.get(api_url)
            apiData = response.json()
            print("\n\napiData: ", apiData)

            for row in range(0, len(apiData["values"])):
                date_time.append(apiData["values"][row]["x"])
                sizeOfBlockChain.append(apiData["values"][row]["y"])
            

            for i in date_time:
                dateTime = dt.datetime.fromtimestamp(i).isoformat()
                date = dateTime[:10]
                time = dateTime[11:]
                xDate.append(date)
            print("\nxDate: "+str(xDate))
            
            fig = go.Figure()
            fig = fig.add_trace(
                go.Scatter(
                    x = xDate,
                    y = sizeOfBlockChain
                )
            )
            fig.update_layout(
                title = 'Blockchain Size (MB) of '+paramV,
                xaxis_title = 'Date',
                yaxis_title = 'Blockchain size (MB)',
                legend_title = 'MB'
            )
            fig.update_yaxes(type='log')
            fig.show()


        # Label
        ttk.Label(self, text = "Select timespan: ", 
                font = ("poppins",10,"bold")).pack(pady = 10)
        
        def callback(*arg):
            print("The value at index " + str(monthchoosen.current()) + " is" + " "+ str(n.get()))  
            
        def clickedBlockchainSize():
            choosed = str(n.get())
            BlockchainSize(choosed)
            #print("clicked: ",monthchoosen.get(), " choosed: ", choosed) 

        def clickedAverageBlockSize():
            choosed = str(n.get())
            AverageBlockSize(choosed)
            #print("clicked: ",monthchoosen.get(), " choosed: ", choosed) 
        
        def clickedTotalTransactionFees():
            choosed = str(n.get())
            TotalTransactionFees(choosed)
            #print("clicked: ",monthchoosen.get(), " choosed: ", choosed) 
        def clickedNumberOfTransactions():
            choosed = str(n.get())
            NumberOfTransactions(choosed)
            #print("clicked: ",monthchoosen.get(), " choosed: ", choosed) 

        n = tk.StringVar()
        monthchoosen = ttk.Combobox(self, width = 27, 
                                    textvariable = n)
        # Adding combobox drop down list
        monthchoosen['values'] = ('30days', '60days','180days','1year','3year','all')
        monthchoosen.pack(side="top",pady=20)
        # Shows 30days as a default value
        monthchoosen.current(0)

        n.trace("w",callback)
        tk.Button(self, text='NumberOfTransactions', width=30,bg="purple",fg="white", command=clickedNumberOfTransactions).pack(side="top", pady=10)

        tk.Button(self, text='Total Transaction Fees (BTC)', width=30,bg="purple",fg="white", command=clickedTotalTransactionFees).pack(side="top", pady=10)

        tk.Button(self, text='BlockchainSize', width=30,bg="purple",fg="white", command=clickedBlockchainSize).pack(side="top", pady=10)  

        tk.Button(self, text='Average Block Size (MB)', width=30,bg="purple",fg="white", command=clickedAverageBlockSize).pack(side="top", pady=10)


                  




if __name__ == "__main__":
    app = SampleApp()
    app.geometry('1000x800')
    app.mainloop()


    
