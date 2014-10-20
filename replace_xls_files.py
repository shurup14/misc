import os
import shutil
import datetime
import time
dirpath = 'C:\\test'
ext='.xls'
ext2='.xlsx'
distdir = 'C:\\test2'
date=str(datetime.date.today())
listofdirs = [os.path.join(dirpath,name) for name in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, name))]
for namedir in listofdirs:
    listfiles=[file for file in os.listdir(namedir)]
    for file in listfiles:                 
        pathfile=os.path.join(namedir,file)
        if (os.path.splitext(pathfile))[-1] == ext or (os.path.splitext(pathfile))[-1] == ext2 :
            if os.path.exists(os.path.join(distdir,date)) is False:
                os.mkdir(os.path.join(distdir,date))                
            shutil.move(pathfile,os.path.join(distdir,date))
            now_time = datetime.datetime.now()
            curr_time = str(now_time.hour)+'_'+str(now_time.minute)+'_'+str(now_time.second)
            os.rename(os.path.join(distdir,date)+'\\'+file,os.path.join(distdir,date)+'\\'+str(curr_time)+'_'+file)
