import os
import shutil
import datetime
import time
dirpath = 'C:\\test'
ext='.xls'
distdir = 'C:\\test2'
date=str(datetime.date.today())
listofdirs = [os.path.join(dirpath,name) for name in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, name))]
for namedir in listofdirs:
    listfiles=[file for file in os.listdir(namedir)]
    for file in listfiles:                 
        pathfile=os.path.join(namedir,file)
        if (os.path.splitext(pathfile))[-1] == ext:
            if os.path.exists(os.path.join(distdir,date)) is False:
                os.mkdir(os.path.join(distdir,date))                
            shutil.move(pathfile,os.path.join(distdir,date))
            now_time = datetime.datetime.now() 
            cur_hour = str(now_time.hour)
            cur_minute = str(now_time.minute)
            cur_second = str(now_time.second) 
            os.rename(os.path.join(distdir,date)+'\\'+file,os.path.join(distdir,date)+'\\'+cur_hour+'_'+cur_minute+'_'+cur_second+'_'+file)
            
        
             
                              
                              
