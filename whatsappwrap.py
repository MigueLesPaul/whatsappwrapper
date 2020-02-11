#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pdb
import time




databases={                                                              #PorDefecto   TODO tomar de configuracion
    'msgstore':"/home/miguel/Data/Whatsapp databases/msgstore.db",
    'contacts':"/home/miguel/Data/Whatsapp databases/wa.db"
    
}




def importContacts():
    """ Import contacts from the wa.db database if present """
    
    conn=sqlite3.connect(databases['contacts'])
    cursor=conn.cursor()
    
    query=""" SELECT jid, display_name,wa_name  FROM wa_contacts;"""
    
    result=cursor.execute(query).fetchall()
    contacts={}
    for q in result:
        contacts[q[0]]={'display_name':q[1], 'wa_name':q[2]}
    print(contacts)


conn = sqlite3.connect(databases['msgstore'])
cursor=conn.cursor()
# # command="select * from messages where key_remote_jid == '5354414448-1549139529@g.us' ;"
# command="select * from messages;"
# command="select key_remote_jid,data,remote_resource,received_timestamp from messages; "
# cursor.execute(command)

# result=[]

importContacts()


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
