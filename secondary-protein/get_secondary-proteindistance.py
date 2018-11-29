import os, sys, tempfile


## this script will get the distance from each secondary structure to the protein

protdir = '/home/dlb213/ESF/newDataSet/allProteins/'

prots = [p for p in os.listdir(protdir) if len(p) == 4]

surfpdbdist = '/home/dlb213/software/surfaceExtractor -surfPdbDistance '

sqlfile = open('update-protdist-secondary_structures.sql','w');

#testing
#prots = ['4M4O']

insert = 'UPDATE secondary_structures SET protein_distance = '

for p in prots:
    os.chdir(protdir+p)
    if os.path.exists('2ndary'):
        protein = p+'/'+p+'.SURF'
        secondarystructs = [s for s in os.listdir('2ndary') if (s.find('[') > 0 and s.find(']') > 0)]
        if len(secondarystructs)> 0:
            print "Running on "+p
            for s in secondarystructs:
                where = " WHERE filename = '"+s+"'"
                tempoutput = tempfile.NamedTemporaryFile()
                os.system(surfpdbdist+protein+' 2ndary/'+s+' > '+tempoutput.name);
                templines = tempoutput.file.readlines()
                for t in templines:
                    if t.startswith('TEMPCLOSEST'):
                        #print t.split(':')[1].strip()
                        sqlfile.write(insert+t.split(':')[1].strip()+where+";\n")
                                            
                tempoutput.file.close()


sqlfile.close();
