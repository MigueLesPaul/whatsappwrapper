#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pdb
import time

databases = {  #PorDefecto   TODO tomar de configuracion
    'msgstore': "/home/miguel/Data/Whatsapp databases/msgstore.db",
    'contacts': "/home/miguel/Data/Whatsapp databases/wa.db"
}


class Whatsappdb():
    def __init__(self):
        self.importContacts()
        # print(self.contacts)
        self.importChats()

    def connectCursor(self, dbname):
        conn = sqlite3.connect(dbname)
        return conn.cursor()

    def importContacts(self):
        """ Import contacts names from the wa.db database if present """

        cursor = self.connectCursor(databases['contacts'])

        query = """ SELECT jid, display_name,wa_name  FROM wa_contacts;"""

        result = cursor.execute(query).fetchall()
        self.contacts = {}
        for q in result:
            self.contacts[q[0]] = {'display_name': q[1], 'wa_name': q[2]}

    def getContactName(self, jidstring):
        # print(jidstring)
        if jidstring in self.contacts:
            if self.contacts[jidstring]["display_name"] == None:
                return self.contacts[jidstring]["wa_name"]
            else:
                return self.contacts[jidstring]["display_name"]

    def importChats(self):
        """Get all the chats with its names or descriptions """

        cursor = self.connectCursor(databases['msgstore'])

        jidquery = """SELECT  _id,raw_string FROM jid;"""
        jids = cursor.execute(jidquery).fetchall()
        jid = {}

        for j in jids:
            jid[j[0]] = j[1]

        chatquery = """SELECT key_remote_jid,subject FROM chat_list; """
        chats = cursor.execute(chatquery).fetchall()
        # print(chats)
        self.chats = {}

        for c in chats:
            if c[1] == None:
                self.chats[c[0]] = self.getContactName(c[0])
            else:
                self.chats[c[0]] = c[1]
        self.jid = jid
        # print(self.chats)

    def getChatParticipants(self, jidstring):
        pass

    def getChatMessages(self, jidstring):
        cursor = self.connectCursor(databases['msgstore'])

        msgquery = """SELECT remote_resource,data,received_timestamp FROM messages WHERE key_remote_jid=='{}'""".format(
            jidstring)
        msgs = cursor.execute(msgquery).fetchall()
        print(msgs)

    def __str__(self):
        out = """ """
        for k in self.contacts.keys():
            out = """ """.join([self.contacts[k]['display_name']])


wa = Whatsappdb()
wa.getChatMessages('5353311973-1578884291@g.us')
