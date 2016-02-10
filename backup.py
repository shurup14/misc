import os
import zipfile
import datetime
import glob
import requests
from subprocess import Popen, PIPE
from email.mime.text import MIMEText
from requests.exceptions import ConnectionError

date = str(datetime.datetime.now())
back_file = '/webapp/backup/middle/{}.zip'.format(date)

class YaDiskException(Exception):
    """Common exception class for YaDisk. Arg 'code' have code of HTTP Error."""
    code = None

    def __init__(self, code, text):
        super(YaDiskException, self).__init__(text)
        self.code = code

    def __str__(self):
        return "%d. %s" % (self.code, super(YaDiskException, self).__str__())


class YaDisk(object):
    """Main object for work with Yandex.disk."""

    login = None
    password = None
    url = "https://webdav.yandex.ru/"
    namespaces = {'d': 'DAV:'}

    def __init__(self, login, password):
        super(YaDisk, self).__init__()
        self.login = login
        self.password = password
        if self.login is None or self.password is None:
            raise Exception("Please, set login and password to Yandex.Disk.")

    def _sendRequest(self, type, addUrl="/", addHeaders={}, data=None):
        headers = {"Accept": "*/*"}
        headers.update(addHeaders)
        url = self.url + addUrl
        req = requests.Request(type, url, headers=headers, auth=(self.login, self.password), data=data)
        with requests.Session() as s:
            return s.send(req.prepare())

    def upload(self, file, path):
        """Upload file."""

        with open(file, "rb") as f:
            resp = self._sendRequest("PUT", path, data=f)
            if resp.status_code != 201:
                raise YaDiskException(resp.status_code, resp.content)


def get_newest():
    return max(glob.iglob('/webapp/backup/dbbackup/*.gz'), key=os.path.getctime)

def send_mail(checker):
    if checker:
        SUBJECT = "Автоматический backup your site успешно выполнен"
        text= 'Бэкап сайта your site успешно выполнен и загружен на ЯндексДиск your site'
    else:
        SUBJECT = "Автоматический backup your site завершился с ошибкой"
        text= 'Во время выполения бэкапа произошла ошибка, необходимо проверить на сервере'
    TO = ['11@yandex.ru', '22@gmail.com']
    FROM = 'backup@your.site'
    msg = MIMEText(text, 'plain')
    msg['FROM'] = FROM
    msg['TO'] = ','.join(TO)
    msg['SUBJECT'] = SUBJECT
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_bytes())

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile(back_file, 'w')
    zipdir('/webapp/', zipf)
    zipf.write(get_newest())
    zipf.close()
    try:
        disk = YaDisk('login','password')
        disk.upload(back_file,'backup/' + date + '.zip')
    except ConnectionError as er:
        send_mail(False)
    send_mail(True)
    os.remove(back_file)
