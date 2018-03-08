#!/usr/bin/python

import mysql.connector
import datetime
import json
import sys
import requests
import cgi
import cgitb
cgitb.enable()
reload(sys)
sys.setdefaultencoding("UTF8")

#CGI to get input from HTML
form = cgi.FieldStorage()
param1=form["param1"].value

#Receive AS Number as argument 
try:
        if sys.argv[1]:
                ASN= sys.argv[1]
except:
        ASN=param1
        #print "Usage: 'ASN_Summary [AS_Number]'"
        #sys.exit()

#Took the content from API
content= json.loads(requests.get("https://peeringdb.com/api/netixlan?asn="+str(ASN)).content)


# create dictionary to have primary key in ix_id
# and content as List of peering detail                      
Exchange={}
for i in content['data']:
    Peer_Detail=[]
    if ( Exchange.has_key(str(i['ix_id'])) ):
        Peer_Detail=Exchange[str(i['ix_id'])]
    Peer_Detail.insert(0,i)
    Exchange[str(i['ix_id'])]=Peer_Detail

# MySQLDB
config = {
  'user': 'yohanesbw',
  'password': 'test123',
  'host': '127.0.0.1',
  'database': 'Summary_DB',
  'raise_on_warnings': True,
  'use_pure': False,
}
conn = mysql.connector.connect(**config)
conn.close()
# date_time
# ASN
# Exchange_Total
# Total_Uniq
# Total Speed
# content

#process the content
html_detail='''
<br>
<br>
<font size="+2"><font size="+2"><font
 style="font-weight: bold; font-style: italic;" size="+1">Detail:</font><br>
</font></font>
<table style="text-align: left; width: 900px; height: 87px;"
 border="1" cellpadding="2" cellspacing="2">
  <tbody>
'''

# Process the data for reporting
Exchange_Total=0
Total_Uniq=0
Total_Speed=0

for i in Exchange:
    Total_Uniq+=1
    Speed=0
    html_detail+= '<tr bgcolor="#5d7b9d"> <td colspan="6">' + Exchange[i][0]['name'] + '</td></tr> <tr>'
    for j in Exchange[i]:
        Total_Speed+=j['speed']
        Speed+=j['speed']
        Exchange_Total+=1
        html_detail+='<tr>'
        html_detail+='<td width="180">IPV4 Peering Address</td>'
        html_detail+='<td>'+ j['ipaddr4'] +'</td>'
        if j['ipaddr6'] :
                html_detail+='<td width="180">IPV6 Peering Address</td>'
                html_detail+='<td>'+ j['ipaddr6'] +'</td>'          
        else:
                html_detail+='<td width="180">IPV6 Peering Address</td>'
                html_detail+='<td></td>'                
        html_detail+='<td width="100">Speed</td>'
        html_detail+='<td width="80">'+ str(j['speed']) +' M</td></tr>'
    html_detail+='<tr></td><td></td><td></td><td></td><td></td><td>Total Speed</td><td>'+ str(Speed)+' M</td> </tr>'
html_detail+='<\table>'

#print the output to HTML instead of files
print html



