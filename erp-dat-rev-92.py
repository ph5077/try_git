"""
Purpose: Handling *.dat, ERP print format, files in SM82C_data

Replace the content btw [inherited lblNote1: TQRLabel]   ......... [end]
With the content btw    [inherited lblSignIn1: TQRLabel] ......... [end]

lblSignIn1 --- lblNote1
lblSignIn2 --- lblNote2
lblSignIn3 --- lblNote3

Running env:
./DAT.ORG	dir for orginal *.dat files, excluding Assist.dat (??? bin file)
./DAT.NEW 	dir for NEW *.dat files
$ python erp-dat-rev-92.py

"""
from os import listdir
from os.path import isfile, join
import sys

def match_line(file_name, sign_to_match):
    """
    Return content, str, btw sign_to_match and "end" in file_name
    if not found, return None
    """
    sign_content = ""
    s_flag = False
    found = False
    fh = open(file_name, "r")

    for line in fh:
	if (line.strip() == sign_to_match) and (s_flag == False):   # Line with sign_to_match
	    s_flag = True
	    found = True
	elif	(line.strip() != "end") and (s_flag == True) :	    # to capture the content
	    sign_content=sign_content+line
	elif	line.strip() == "end":				    # Line with "end"
	    s_flag = False
    
    fh.close()
	
    if not found:
	print "Pattern ...", sign_to_match, "  NOT found in file  ", file_name
	return None
    else:
	return sign_content

def replace_line(in_file, out_file, note1, note2, note3, sign1, sign2, sign3):
    """
    Replace the content from in_file, output to out_file 
    """
    fi = open(in_file, "r")
    fo = open(out_file, "w")
    n1_flag = False
    n2_flag = False
    n3_flag = False
    n1_update = False
    n2_update = False
    n3_update = False


    for line in fi:
	if [n1_flag, n2_flag, n3_flag].count(True) > 1:		# only one True allowable
	    print "Error...................."

	if   (line.strip() == note1) and (n1_flag == False):	# Check note1
	    fo.write(line)
	    n1_flag = True					# start of replacement
	    n1_update = True 

	elif (line.strip() == note2) and (n2_flag == False):	# Check note2
	    fo.write(line)
	    n2_flag = True					# start of replacement
	    n2_update = True 

	elif (line.strip() == note3) and (n3_flag == False):	# Check note3
	    fo.write(line)
	    n3_flag = True					# start of replacement    
	    n3_update = True 

	elif (line.strip() != "end") and (n1_flag == True) :	# in-btw do nothing
	    pass

	elif (line.strip() != "end") and (n2_flag == True) :
	    pass

	elif (line.strip() != "end") and (n3_flag == True) :
	    pass

	elif (line.strip() == "end") and (n1_flag == True):	# "end", insert sign1 in to out_file
	    fo.write(sign1)
	    fo.write(line)					# insert end
	    n1_flag = False					# end of replacement 

	elif    (line.strip() == "end") and (n2_flag == True):
	    fo.write(sign2)
	    fo.write(line)
	    n2_flag = False

	elif    (line.strip() == "end") and (n3_flag == True):
	    fo.write(sign3)
	    fo.write(line)
	    n3_flag = False

	elif	(n1_flag == False) and (n2_flag == False) and (n3_flag == False):   # copy the content
	    fo.write(line)
	
    if not n1_update:
        print ">>>>>> Pattern ", note1, " NOT Found  in file....  ", in_file, "\n"
    if not n2_update:
        print ">>>>>> Pattern ", note2, " NOT Found  in file....  ", in_file, "\n"
    if not n3_update:
        print ">>>>>> Pattern ", note3, " NOT Found  in file....  ", in_file, "\n"
	
    fi.close()
    fo.close()

# Main
#
org_path='.\\DAT.ORG'
new_path='.\\DAT.NEW'

files_list = [f for f in listdir(org_path) if isfile(join(org_path, f))]

#
# get the content
#
for file in files_list:
    file_name = org_path+"\\"+file
    print "Processing File ..... ", file_name, "\n"

    signs = ["inherited lblSignIn1: TQRLabel",  "inherited lblSignIn2: TQRLabel",  "inherited lblSignIn3: TQRLabel"] 
    sign_content = ["0","1","2"]		# dummy
    i=0
    for sign in signs:
    	sign_content[i] = match_line(file_name, sign) 

	# Filtering sign enabled
	if sign_content[i] and ("Enabled" in sign_content[i]):
		print "In file ...", file, " \t\t\t.............Sign Enabled found in ", sign
		print sign_content[i]
	i = i +1
	
    notes = ["inherited lblNote1: TQRLabel", "inherited lblNote2: TQRLabel", "inherited lblNote3: TQRLabel"]
    for note in notes:
	note_content = match_line(file_name, note)

	# Filtering note enabled
	if note_content and ("Enabled" in note_content):
	    print "In file ...", file, " \t\t\t.............Note Enabled found in ", note
	    print note_content
      
#	
# replace the data btw "inherited lblNote1: TQRLabel" and "end"
#
	new_file_name = new_path+"\\"+file
#	note1="inherited lblNote1: TQRLabel"
#	note2="inherited lblNote2: TQRLabel"
#	note3="inherited lblNote3: TQRLabel"
	
    replace_line(file_name, new_file_name, notes[0], notes[1], notes[2], sign_content[0], sign_content[1], sign_content[2]) 

