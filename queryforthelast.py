import cx_Oracle
con = cx_Oracle.connect('Tapasya/nanu_stsci')
cur = con.cursor()
cur.execute('''select sequence from beeGenes where gi = 147907436''')
result=cur.fetchall()
print result[0][0]

cur.close()
con.close()
