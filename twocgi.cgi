
import cgi
import cx_Oracle

def main():
    contents = processInput()
    print contents

def processInput():		
	
    con = cx_Oracle.connect('Tapasya/nanu_stsci@127.0.0.1/xe')
    cur = con.cursor()
    aaList = ['A', 'C', 'G', 'T']
    fList = [() for t in range(4)]
    for i in range(4):
        myDict = {'aa': aaList[i]}
        obj = cur.execute('''select gi, freq_%(aa)s from beeGenes, 
                            (select max(freq_%(aa)s) as max%(aa)s from 
                          beeGenes) where freq_%(aa)s = max%(aa)s''' % myDict)
        for x in obj:
            fList[i] = x

    myTuple=()
    for t in range(4):
        myTuple = myTuple + fList[t]

    cur.close()
    con.close()
    return makePage('ResultsPage.html', myTuple)

def fileToStr(fileName):
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitution):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitution


try:
    print 'Content-type: text/html\n\n'
    main()
except:
    cgi.print_exception()
