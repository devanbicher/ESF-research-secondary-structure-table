import os

def aminoAcidLookup(line):
    #Probably put in something to check if we are dealing with RNA, DNA or protein.
    #print(line)
    aaCode = line[17:20].strip();
    
    ## protein codes
    if aaCode == "ALA":return "A";
    if aaCode == "ARG":return "R";
    if aaCode == "ASN":return "N";
    if aaCode == "ASP":return "D";
    if aaCode == "CYS":return "C";
    if aaCode == "GLU":return "E";
    if aaCode == "GLN":return "Q";
    if aaCode == "GLY":return "G";
    if aaCode == "HIS":return "H";
    if aaCode == "ILE":return "I";
    if aaCode == "LEU":return "L";
    if aaCode == "LYS":return "K";
    if aaCode == "MET":return "M";
    if aaCode == "PHE":return "F";
    if aaCode == "PRO":return "P";
    if aaCode == "SER":return "S";
    if aaCode == "THR":return "T";
    if aaCode == "TRP":return "W";
    if aaCode == "TYR":return "Y";
    if aaCode == "VAL":return "V";
    if aaCode == "MSE":return "M";
    
    ##RNA/DNA codes
    if aaCode == "U":return "U";
    if aaCode == "A":return "A";
    if aaCode == "C":return "C";
    if aaCode == "G":return "G";
    if aaCode == "T":return "T";
    
    
    print("ERROR: AMINO ACID CODE [" + aaCode + "] not identified.  Skipping");


def processFile(pdbName):
    
    fastastring = ''

    currentChain = "@"

    ###open the file
    pdbFile = open(pdbName, 'r');
    line = pdbFile.readline()
    
    while not line.startswith("ATOM"):
        line = pdbFile.readline()
        
        #print(line);
        
    aaChar = aminoAcidLookup(line);
    curAAChar = aaChar;
    chainID = curChainID = line[21];
    resNum = curResNum = line[23:26];
    
    
    while line:
        if not line.startswith("ATOM"):
            continue;
        
        while (aaChar == curAAChar and chainID == curChainID and resNum == curResNum):
            line = pdbFile.readline();
            
            if not line:
                break;
            
            aaChar = aminoAcidLookup(line)
            chainID = line[21];
            resNum = line[23:26];
            
        fastastring += curAAChar
        #set current residue identifiers
        curAAChar = aaChar;
        curChainID = chainID;
        curResNum = resNum;
            
        line = pdbFile.readline();

    pdbFile.close();
    return fastastring
        


def main():

    csvfile = open("secondary-structures.csv",'w')
    sqlfile = open("secondary_structures.sql",'w')
    csvfile.write('filename,secondary_structure,number,pdb,sequence')

    protdir = "/home/dlb213/ESF/newDataSet/allProteins/"
    
    prots = [p for p in os.listdir(protdir) if len(p) == 4]
    
    #seqcount = 0;

    for p in prots:
        print p
        os.chdir(protdir+p)
        pdbquery = "SELECT pr_id FROM protein_rna WHERE pdb='"+p+"'"
        if os.path.exists('2ndary/'):
            secondarystructs = [s for s in os.listdir('2ndary/') if (s.find('[') > 0 and s.find(']') > 0)]
            if(len(secondarystructs) > 0):
                for s in secondarystructs:
                    print s
                    structure = s.split('-')[1].split('[')[0]
                    structnum = s.split('-')[1].split('[')[1].split(']')[0]
                    #print s +" struct:  " + structure + "  num:  "+structnum
                    if os.path.exists('2ndary/'+s):
                        sequence = processFile('2ndary/'+s)
                        #if len(sequence) > seqcount:
                            #seqcount = len(sequence)
                        #print s + " :  "+ fasta;
                        csvfile.write(s+','+structure+','+structnum+','+p+','+sequence+'\n')
                        columns = "(filename,secondary_structure,structure_number,pdb,pr_id,structure_fasta)"
                        values = "('"+s+"','"+structure+"',"+structnum+",'"+p+"',("+pdbquery+"),'"+sequence+"')"
                        query = "INSERT INTO secondary_structures "+columns+" VALUES "+values+";\n"
                        sqlfile.write(query)
                        
                    else:
                        print "No file for "+ s
            else:
                print "No structures in "+ p
        else:
            print "No 2ndary folder in "+p
    
    print "DONE!";

    #print "longest sequence:  " + str(seqcount);

    csvfile.close()
    sqlfile.close()
                        

if __name__ == "__main__":
    main()
