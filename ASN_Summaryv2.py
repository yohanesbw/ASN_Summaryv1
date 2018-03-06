import json
import sys
import requests
reload(sys)
sys.setdefaultencoding("UTF8")

#Receive AS Number as argument 
try:
        if sys.argv[1]:
                ASN= sys.argv[1]
except:
        print "Usage: 'ASN_Summary [AS_Number]'"
        sys.exit()

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

                       
# Create the Detail summary for reporting
Exchange_Total=0
Total_Uniq=0
Total_Speed=0
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
        html_detail+='<td width="180">IPV6 Peering Address</td>'
        html_detail+='<td>'+ j['ipaddr6'] +'</td>'
        html_detail+='<td width="100">Speed</td>'
        html_detail+='<td width="80">'+ str(j['speed']) +' M</td></tr>'
    html_detail+='</tr>'
    html_detail+='<tr></td><td></td><td></td><td></td><td></td><td>Total Speed</td><td>'+ str(Total_Speed)+' M</td> </tr>'


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
f=open("Summary.html","w")
f.write(html)
f.close()

#print feedback
print "Summary File created > Summary.html, Please open the file for the summary"


