__author__ = 'gord0as'
import pymysql, xlsxwriter, datetime, locale

#Можно указать пользователей, которых не отображать в статистике
ignore=('#UserGate Server#')

#Можно указать сайты, которые не отображать в статистике
ignore_sites=('cft.ru','supportobject.cft.ru','www.cft.ru','private.fintender.ru',
                'zakupki.gov.ru','my-bg.ru','www.spark-interfax.ru',)

#Создаем подключение к БД
try:
    print('Подключаемся к Базе Данных...')
    conn = pymysql.connect(host='10.10.10.10', port=3306, user='ug_user', passwd='pass', db='usergate', charset='utf8')
    cur = conn.cursor()
except Exception as e:
    print(e)

#функция получения названия текущего месяца
def get_month():
    d = datetime.date.today()
    locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')
    return str(d.strftime('%B'))

#функция запроса топа качков (первые 40)
def select_top():
                # Запрос к неагрегированным таблицам, работает очень медленно
    #cur.execute("SELECT  users.USER_NAME, SUM(connections.BYTES_RECV+connections.BYTES_SENT) as COMMON, connections.USER_ID "
     #           "FROM users LEFT JOIN connections ON users.USER_ID=connections.USER_ID GROUP BY users.USER_ID ORDER BY COMMON desc LIMIT 40")
    cur.execute("SELECT users.USER_NAME ,SUM(BYTES_RECV+BYTES_SENT) as COMMON, stat_traffic.USER_ID "
                "FROM stat_traffic LEFT JOIN users ON users.USER_ID=stat_traffic.USER_ID GROUP BY USER_ID ORDER BY COMMON desc LIMIT 45")
    return cur.fetchall()

#функция получения трафика по каждому пользователю
def select_traf(ID):
                # Запрос к неагрегированным таблицам, работает очень медленно
   # cur.execute("SELECT  resources.RESOURCE_NAME, SUM(BYTES_RECV+BYTES_SENT) as TRAF, COUNT(RESOURCE_ID) "
    #            "FROM connections LEFT JOIN  resources ON connections.RESOURCE_ID=resources.ID "
     #           "WHERE connections.USER_ID=%s GROUP BY resources.ID ORDER BY TRAF desc LIMIT 105" %ID)
    cur.execute("SELECT  RESOURCE, SUM(BYTES_RECV+BYTES_SENT) as TRAF, SUM(REQUESTS) "
                "FROM stat_resources WHERE USER_ID=%s  GROUP BY RESOURCE ORDER BY TRAF desc LIMIT 105" % ID)
    return cur.fetchall()

#Провверяем пользователя на игнор
def validated_lists():
    s=[]
    for r in select_top():
        if r[0] not in ignore:
            s.append(r)
    return s

#Генерим excel
try:
    print('Создаем новый Excel документ...')
    workbook = xlsxwriter.Workbook('Отчет за %s.xlsx' % get_month())
    worksheet = workbook.add_worksheet('main')
except Exception as e:
    print(e)

#инициализируем параметры форматирования
bold = workbook.add_format({'bold': True})
align_c = workbook.add_format()
align_c.set_align('center')
align_r = workbook.add_format().set_align('right')
url=workbook.add_format({'color': 'blue', 'underline': 1, 'align': 'center'})

#Генерируем главную страницу отчета
worksheet.set_column(0, 0, 19)
worksheet.set_column(1, 1, 40)
worksheet.set_column(2, 2, 70)
worksheet.set_column(3, 3, 15)
worksheet.set_column(4, 4, 15)
worksheet.set_row(1, 25)
worksheet.write('A2', 'Отчётный период:', bold)
worksheet.write('B2', get_month())
worksheet.write('B5', 'Ф.И.О', bold)
worksheet.write('C5', 'Подразделение', bold)
worksheet.write('D5', 'трафик в Mb', bold)

# Начальные значения колонок
row = 6
col = 0
i = 1
cell_ind = 7
print ('Делаем запрос к Базе данных...Работает долго, нужно подождать')
user_list = validated_lists()
print ('..Выгрузился!')
for user in user_list:
    print ('Создаем статистику по пользователю:%s' % user[0])
    worksheet.write(row, col, i, align_c)
    worksheet.write(row, col + 1, user[0])
    worksheet.write(row, col + 3, str(user[1]//1048576) + ' Mb')
    worksheet.write_url('E%s' % cell_ind,  'internal:%s!A1' % i, url, 'Подробности')
    #Генерим отдельную страничку по трафику юзера
    worksheet_traf = workbook.add_worksheet('%s' % i)
    worksheet_traf.set_row(0,17)
    worksheet_traf.write('A1', 'Сотрудник', align_r)
    worksheet_traf.write('B1', '%s' % user[0], bold)
    worksheet_traf.write_url('D1', 'internal:main!A1', url, '<<= Назад')
    worksheet_traf.set_column(0, 0, 12)
    worksheet_traf.set_column(1, 1, 40)
    worksheet_traf.set_column(2, 2, 15)
    worksheet_traf.set_column(3, 3, 15)
    worksheet_traf.write('B2', 'Посещенные сайты:', bold)
    worksheet_traf.write('C2', 'Мбайт', bold)
    worksheet_traf.write('D2', 'Запросов', bold)
    row_t = 2
    for x in select_traf(str(user[2])):
        if x[0] not in ignore_sites:
            worksheet_traf.write(row_t, 1, x[0])
            worksheet_traf.write(row_t, 2, round(int(x[1])/1048576, 1), align_r)
            worksheet_traf.write(row_t, 3, x[2])
            row_t += 1
    cell_ind += 1
    row += 1
    i += 1

workbook.close()
cur.close()
conn.close()
print('Статистика сформированна успешно!')