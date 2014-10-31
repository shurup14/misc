import os
import datetime
import urllib.request
import xml.etree.ElementTree as etree
import subprocess

def make_cert(name,stuff):
    for i in range(0,len(stuff)):
        with open (name + '-'+ str(i+1) + '.cer','a') as file:
            file.write(stuff[i])
            
def check_cert(data):
    if datetime.datetime.now() <= datetime.datetime.strptime(data[0:10]+data[12:19],'%Y-%m-%d%H:%M:%S'):
        return True
    else:
        return False
 
def parsing_xml(url):
    data = urllib.request.urlopen(url).read()
    xml = etree.fromstring(data)    
    for UC in xml.findall('.//УдостоверяющийЦентр'):
        name_file = UC.find('ИНН').text
        cert_stuff=[]
        for cert in UC.findall('.//ДанныеСертификата'):
            if check_cert(str(cert.find('ПериодДействияДо').text)):
                cert_stuff.append(str(cert.find('Данные').text))
        make_cert(name_file,cert_stuff)

def install_certs(ext):    
    list_certs = [fname for fname in os.listdir('.') if (os.path.splitext(fname))[-1] == ext ]
    with open ('install.bat','a') as install:
        for cert in list_certs:
            install.write('certmgr -add -c '+ cert + ' -s -r localMachine CA ' + '\n')      
    proc = subprocess.Popen('install.bat')
    proc.wait()
    os.remove('install.bat')
    for cer in list_certs:
        os.remove(cer)
    
def main():
    ext = '.cer'
    url='http://e-trust.gosuslugi.ru/CA/DownloadTSL?schemaVersion=0'
    parsing_xml(url)
    install_certs(ext)
    
if __name__ == '__main__': 
    main() 
