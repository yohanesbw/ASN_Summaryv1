#!/usr/bin/python

import mysql.connector
from datetime import date, datetime
import json
import sys
import requests
import cgi
import cgitb
cgitb.enable()
reload(sys)
sys.setdefaultencoding("UTF8")

#Get the parameter from HTML 
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

#Take the content from API
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

#Prepare the html
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
Peering={}

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
    Peering[Exchange[i][0]['name']]=str(Speed)
        
#Create HTML File as an Output Result
html='''
<html>
<body>
<font size="+2"><span
 style="color: rgb(0, 102, 0); font-weight: bold;">Executive
Summary for AS-'''+str(ASN)+\
'''
:<br>
</span></font>
<table style="text-align: left; width: 523px; height: 116px;"
 border="0" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td style="font-weight: bold;">Total Peering</td>
      <td>'''+ str(Exchange_Total) +\
'''
</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Total Unique
Organization Peering</td>
      <td>'''+str(Total_Uniq) +\
'''
</td>
    </tr>
    <tr>
      <td style="font-weight: bold;">Total Aggregate Speed</td>
      <td>'''+str(Total_Speed/1000) +\
'''
G</td>
    </tr>
  </tbody>
</table>
<font size="+2"><span
 style="color: rgb(0, 102, 0); font-weight: bold;"></span></font>
'''
html+=html_detail
html+='''
</tbody> </table>
</body>
</html>
'''

#print the output to HTML format
print html

# Storing the result to MySQLDB
config = {
  'user': 'admin',
  'password': 'admin123',
  'host': '127.0.0.1',
  'database': 'ASN_Summary',
  'raise_on_warnings': True,
  'use_pure': False,
}
conn = mysql.connector.connect(**config)
cursor=conn.cursor()
Report_Time=datetime.now().isoformat()
# ASN
# Report_Time
# Exchange_Total
# Total_Uniq
# Total Speed
# html_detail
query="INSERT INTO Report_Summary ASN,Report_Time,Exchange_Total,Total_Uniq,Total_Speed,html_detail\
                VALUES {0},{1},{2},{3},{4},{5}".format(ASN,Report_Time,Exchange_Total,Total_Uniq,Total_Speed,html_detail)
cursor.execute(query)
conn.commit()

#additional table for charting #next feature if
for i in Peering:
        query="INSERT into Peering_Detail peer,totalspeed VALUE {0},{1}".format(i,Peering[i])
        cursor.execute(query)
        conn.commit()
        
cursor.close()
conn.close()
