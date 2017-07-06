
import cgi
import cx_Oracle

def main(): 
    form = cgi.FieldStorage()   # cgi script line
    theStr = form.getfirst('fileName', '') 
    contents = processInput(theStr)
    print contents

def processInput(theFile):

    # To read in the contents of the data file.
    with open(theFile, 'r') as fl:
        # given substring to be inserted as starting position
        BEGIN_STRING = '_**gene_seq_starts_here**_'  
        strL = '' 
        for line in fl:
            strL += line.strip('\r\n')

  
            if '>' in line:
                strL += BEGIN_STRING 

    # To take out the gi number and nucleotide sequence of each gene
    totalLen = len(strL)
    end     = 0
    numGene   = strL.count('>gi')
    giList  = [] # list of all gi number
    sequenceList = [] # list of all gene seq 
    freq_A_List  = [] # list of all freq_A
    freq_C_List  = []
    freq_G_List  = []
    freq_T_List  = []
    freq_GC_List = []
	
    for i in range(numGene):
        # for gi number 
        start = strL.find('>gi|',end) + 4
        end   = strL.find('|', start) 
        gi = strL[start : end]
        giList.append(gi)

    	# for gene sequence
        start = strL.find(BEGIN_STRING, end) + len(BEGIN_STRING)
        end = strL.find('>gi|', start)
        if end == -1:
      	    end = totalLen
        seq = strL[start : end]
        sequenceList.append(seq)

    # to calculate the frequencies of each nucleotide 
        seqLen = len(seq)
        freq_A = seq.count('A') / float(seqLen)
        freq_C = seq.count('C') / float(seqLen)
        freq_G = seq.count('G') / float(seqLen)
        freq_T = seq.count('T') / float(seqLen)
        freq_A_List.append(freq_A)
        freq_C_List.append(freq_C)
        freq_G_List.append(freq_G)
        freq_T_List.append(freq_T)

    # to calculate the combined frequencies of G and C.
        freq_GC = freq_C + freq_G
        freq_GC_List.append(freq_GC)

    # Connection of Python to the Oracle DB.
    
    con = cx_Oracle.connect('Tapasya/nanu_stsci@127.0.0.1/xe')
    cur = con.cursor()

    # Create beeGenes table on oracle

    cur.execute('drop table beeGenes')
    cur.execute('''create table beeGenes (
                   gi varchar2(10),
                   sequence clob,
                   freq_A number, 
                   freq_C number,
                   freq_G number,
                   freq_T number,
                   freq_GC number
                   )''')

    # to find the sequence input size.
    maxGene   = max(map(len,sequenceList)) 
    tableSize = len(giList)
    
    cur.bindarraysize = tableSize
    cur.setinputsizes(10, maxGene, float, float, float, float, float)
	
    # data into DB table using bind variable approach
    for i in range(len(giList)):
        cur.execute('''insert into beeGenes (gi, sequence, 
                    freq_A, freq_C, freq_G, freq_T, freq_GC) values(
                    :v1, :v2, :v3, :v4, :v5, :v6, :v7)''', (giList[i], 
                    sequenceList[i], freq_A_List[i], freq_C_List[i], 
                    freq_G_List[i], freq_T_List[i], freq_GC_List[i]))

    con.commit()

    cur.close()
    con.close()

    return makePage('FormTemplate2.html', ('Uploading finished!'))

def fileToStr(fileName):
    ''' return a string '''
    fin = open(fileName);
    contents = fin.read();
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
