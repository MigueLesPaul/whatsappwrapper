#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pdb
import time




databases={                                                              #PorDefecto   TODO tomar de configuracion
    'msgstore':"/home/miguel/Data/Whatsapp databases/msgstore.db",
    'contacts':"/home/miguel/Data/Whatsapp databases/wa.db"
    
}



class Whatsappdb():
    def __init__(self):
        self.importContacts()
        # print(self.contacts)       
        self.importChats()
    def importContacts(self):
        """ Import contacts names from the wa.db database if present """
        
        conn=sqlite3.connect(databases['contacts'])
        cursor=conn.cursor()
        
        query=""" SELECT jid, display_name,wa_name  FROM wa_contacts;"""
        
        result=cursor.execute(query).fetchall()
        self.contacts={}
        for q in result:
            self.contacts[q[0]]={'display_name':q[1], 'wa_name':q[2]}
    
    def getContactName(self,jidstring):
        # print(jidstring)
        if jidstring in self.contacts:
            if self.contacts[jidstring]["display_name"]==None:
                return self.contacts[jidstring]["wa_name"]
            else:
                return self.contacts[jidstring]["display_name"]
            
    def importChats(self):
        """Get all the chats with its names or descriptions """
        conn = sqlite3.connect(databases['msgstore'])
        cursor=conn.cursor()
        
        jidquery="""SELECT  _id,raw_string FROM jid;"""
        jids=cursor.execute(jidquery).fetchall()
        jid={}
        
        for j in jids:
            jid[j[0]]=j[1]
        
    
        chatquery="""SELECT key_remote_jid,subject FROM chat_list; """
        chats=cursor.execute(chatquery).fetchall()
        # print(chats)
        self.chats={}
        
        for c in chats:
            if c[1] == None:
                self.chats[ c[0] ] = self.getContactName(c[0]) 
            else:
                self.chats[ c[0] ] = c[1]
        self.jid=jid        
        print(self.chats)
        
        
    
    
    
    def __str__(self):
        out=""" """
        for k in self.contacts.keys():
            out = """ """.join([self.contacts[k]['display_name']  ])




# # command="select * from messages where key_remote_jid == '5354414448-1549139529@g.us' ;"
# command="select * from messages;"
# command="select key_remote_jid,data,remote_resource,received_timestamp from messages; "
# cursor.execute(command)

# result=[]

wa=Whatsappdb()

# for q in cursor:
#     # result.append(q[0])
#     if q[0]=='5354414448-1549139529@g.us':
#         result=q
#     else:
#         continue
#     if result[2]==None:
#         person="Miguel"
#     else:
#         cmd="select jid,number,display_name,wa_name from wa_contacts where jid=='{}'  ".format(result[2])
#         cursorwa.execute(cmd)
#         query=cursorwa.fetchone()
#         if query[2]==None:
#             person=query[3]
#         else:
#             person=query[2]
            
            
#     print("--{}\n{}:{}   ".format(q[3],person,q[1]))
        
        
    # print(q)

# print (result)
