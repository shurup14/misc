import os
directory = 'C:\out'
files = os.listdir(directory)
print(files)
for filename in files:
    outf = open(directory +'\\'+ 'OUT_'+filename, 'a')
    inf = open(directory + '\\'+ filename)
    for line in inf:
        try:
            temp_list= line.split('^')
            new_list=temp_list[1]+','+temp_list[4]+','+temp_list[9]
            outf.write(new_list + '\n')
        except:
            continue
    inf.close()
    outf.close() 
    
