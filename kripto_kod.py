import tkinter as tk
from json import decoder
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from pprint import pprint
import logging
from cgitb import text
from textwrap import fill
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv

import pandas_datareader.data as reader
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns




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
            korisnikUnos = int(unos.get()) 
            blockhash = rpc_client.getblockhash(korisnikUnos)
            block_info = rpc_client.getblock(blockhash)
            text=Text(self, width=100, height=60)
            text.insert(END, 'HASH: '+str(block_info['hash'])+ '\nTX: '+str(block_info['tx']) +'\n\nBroj transakcija:'+str(block_info['nTx'])+'\nHeight: '+str(block_info['height'])
                        +'\nBits: '+str(block_info['bits'])+'\nNonce: '+str(block_info['nonce'])+'\nPreviousblockhash: '+str(block_info['previousblockhash'])+'\nNextblockhash: '+str(block_info['nextblockhash']))
            text.pack()

        def transakcija():
            korisnikUnos = str(unos.get())
            transaction = rpc_client.getrawtransaction(korisnikUnos)
            transaction_info = rpc_client.decoderawtransaction(transaction)
            len_output = len(transaction_info["vout"])
        
            lista_adresa = adrese(transaction_info,len_output)    
            Label(self, text = "TRANSAKCIJA INFO: ").pack()
            text=Text(self, width=100, height=60)
            text.insert(END,  'Txid: ' +str(transaction_info['txid']) +'\nSize = ' + str(transaction_info['size'])+'\nBroj izlaza: '+str(len_output) +'\nAdrese: '+ str(lista_adresa) 
                        +'\n\nWeight = ' + str(transaction_info['weight']) +'\nVsize = ' + str(transaction_info['vsize']))
            text.pack()

        def adrese(transaction_info,len_output):
            lista = []
            for x in range(0,len_output):
                adresa = transaction_info["vout"][x]["scriptPubKey"]["addresses"] 
                lista.append(str(adresa))
            lista = '\n'.join(lista)
            return lista
        

        tk.Frame.__init__(self, master)     
        tk.Label(self, text='Blockexplorer', bg='#f0f0f0', font=(20)).pack(side="top", fill="x", pady=20)
        tk.Button(self, text="BlockHashPage",bg="green",fg="white",
                  command=lambda: master.switch_frame(BlockPage)).pack(pady=5)
        tk.Button(self, text="TransactionPage",bg="green",fg="white",
                  command=lambda: master.switch_frame(TransactionPage)).pack(pady=5)
        tk.Button(self, text="HistoryInfo",bg="green",fg="white",
                  command=lambda: master.switch_frame(HistoryInfo)).place(x=5,y=40)
        

        tk.Label(self, text='Unesi block ili transakciju:\t').pack(side="top",fill="x", pady=25)
        unos=Entry(self, width=75)
        unos.pack()
        
        tk.Button(self, text='Block', width=10,bg="purple",fg="white", command=block).pack(side="top", pady=15)
        tk.Button(self, text='Trans', width=10,bg="purple",fg="white", command=transakcija).pack(side="top", pady=5)

        
    
    


class BlockPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=30)

        hashbloka = rpc_client.getbestblockhash()
        blokinfo = rpc_client.getblock(hashbloka)
        Label(self, text = "BEST BLOCK HASH:").pack(pady=50)
        text=Text(self, width=100, height=30)
        #text.place(x=240,y=120)
        text.pack()
        text.insert(END, 'HASH: ' +str(blokinfo['hash'])+'\nTX: '+str(blokinfo['tx']) +'\nNONCE: '+str(blokinfo['nonce'])+ '\nDIFFUCULTY: '
                    +str(blokinfo['difficulty'])+ '\nNtx: '+str(blokinfo['nTx'])+'\nPREVIOUS BLOCK HASH: '+str(blokinfo['previousblockhash']))
        

class TransactionPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=30)

        transactions = rpc_client.getrawmempool()
        Label(self, text = "TRANSACTION LIST:").pack(pady=50)
        text=Text(self, width=90, height=30)
        #text.place(x=240,y=120)
        text.pack()
        i = 1
        for x in transactions:
            text.insert(END, str(i) +'.\t'+ x + '\n')
            i+=1

class HistoryInfo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",bg="green",fg="white",
                  command=lambda: master.switch_frame(StartPage)).pack(side="top", pady=30)

        def TransactionsPer30Days():
            x = []
            y = []
           
            with open('transactions.csv','r') as csvfile:
                lines = csv.reader(csvfile, delimiter=',')
                for row in lines:
                    x.append(row[0])
                    y.append(row[1])
            plt.plot(x, y, color = 'g', linestyle = 'dashed',
                    marker = 'o',label = "Data")
            
            plt.xticks(rotation = 25)
            plt.xlabel('Dates')
            plt.ylabel('Transactions')
            plt.title('Confirmed Transactions Per 30 Days', fontsize = 20)
            plt.grid()
            plt.legend()
            plt.show()

        tk.Button(self, text='TransactionsPer30Days', width=20,bg="purple",fg="white", command=TransactionsPer30Days).pack(side="top", pady=5)
        
        
        def BlockchainSizePer30Days():
            x = []
            y = []
           
            with open('blocks-size.csv','r') as csvfile:
                lines = csv.reader(csvfile, delimiter=',')
                for row in lines:
                    x.append(row[0])
                    y.append(row[1])
            plt.plot(x, y, color = 'g', linestyle = 'dashed',
                    marker = 'o',label = "Data")
            
            plt.xticks(rotation = 25)
            plt.xlabel('Dates')
            plt.ylabel('Blocks')
            plt.title('Blocks Per 30 Days', fontsize = 20)
            plt.grid()
            plt.legend()
            plt.show()

        tk.Button(self, text='BlockchainSizePer30Days', width=20,bg="purple",fg="white", command=BlockchainSizePer30Days).pack(side="top", pady=5)

        def AvgFeePerTransaction():
            x = []
            y = []
           
            with open('fees-usd-per-transaction.csv','r') as csvfile:
                lines = csv.reader(csvfile, delimiter=',')
                for row in lines:
                    x.append(row[0])
                    y.append(row[1])
            plt.plot(x, y, color = 'g', linestyle = 'dashed',
                    marker = 'o',label = "Data")
            
            plt.xticks(rotation = 25)
            plt.xlabel('Dates')
            plt.ylabel('Fee')
            plt.title('Avg Fee Per 30 Days', fontsize = 20)
            plt.grid()
            plt.legend()
            plt.show()

        tk.Button(self, text='AvgFeePerTransaction', width=20,bg="purple",fg="white", command=AvgFeePerTransaction).pack(side="top", pady=5)


if __name__ == "__main__":
    app = SampleApp()
    app.geometry('1000x800')
    app.mainloop()