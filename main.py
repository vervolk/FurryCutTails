# (c) 2021 vervolk Davide Norton
# FurryCutTails скрипт разбиения двух текстов на пропорциональные фрагменты.
# при запуске два входных параметра имя файла исходного текста и имя файла перевода
# файлы должны быть в кодировке cp1251
# pyinstaller --onefile main.py
from dataclasses import dataclass, field
import sys, os
import configparser

def createConfig(config_path):
    """
    Создание файла конфигурации
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "cut_list_string", "' ',' ','\\n'")
    config.set("Settings", "min_length", "200")
    with open(config_path, "w") as config_file:
        config.write(config_file)

# создание конфига если его нет, если есть  - читаем его
def crudConfig(config_path):
    """
    Чтение файла конфигурации
    """
    if not os.path.exists(config_path):
        createConfig(config_path)

    config = configparser.ConfigParser()
    config.read(config_path)

    # Читаем некоторые значения из конфиг. файла.
    cut_list_string = config.get("Settings", "cut_list_string")
    min_length = config.get("Settings", "min_length")
    return cut_list_string, min_length

# разделение текста по первому разрешённому символу после середины фрагмента
def cut_twice(st):
    global csl
    ftp = st
    stp = ''
    lst = len(st)
    if lst > 2:
        middle_cut = lst // 2
        ftp = st[0:middle_cut]
        while middle_cut < lst:
            if st[middle_cut:middle_cut + 1] not in csl:
                ftp = ftp + st[middle_cut:middle_cut + 1]
                middle_cut = middle_cut + 1
            else:
                break
        stp = st[middle_cut:]
    return ftp ,stp

# разделение текста по первому разрешённому символу до середины фрагмента
def cut_twice_left(st):
    ftp = st
    stp = ''
    lst = len(st)
    if lst > 2:
        middle_cut = lst // 2
        while middle_cut > 0:
            if st[middle_cut-1:middle_cut] not in ('.'):
                middle_cut = middle_cut - 1
                ftp = st[0:middle_cut]
                stp = st[middle_cut+1:]
            else:
                break
    return ftp ,stp

# рекурсивная функция резки фрагментов
def cut_list(slist:list):
    # склейка списков
    def add_sublist(inlist:list, applist:list):
        somelist = list()
        for item in inlist:
            somelist.append(item)
        for item in applist:
           somelist.append(item)
        return somelist

    if len(slist) == 0:
        return slist
    st = ''
    st = slist[0]
    stp, ftp = cut_twice(st)
    if (st != stp) & (ftp != stp):
        slist = list()
        stpl = list()
        ftpl = list()
        stpl.append(stp)
        ftpl.append(ftp)
        slist = add_sublist(cut_list(slist),cut_list(stpl))
        slist = add_sublist(cut_list(slist),cut_list(ftpl))
    return slist

@dataclass
class ListData():
    sourse:list
    translated:list
    min_length:int = 1

flag = True

# не рекурсивная резка фрагментов
def process_data(rrr: ListData):
    k = 0
    global flag
    flag = not flag
    while k < len( rrr.sourse):
        ftp ,stp = cut_twice(rrr.sourse[k])
        if (len(ftp)>rrr.min_length) & (len(stp)>rrr.min_length):
            tftp, tstp = cut_twice(rrr.translated[k])
            rrr.sourse.pop(k)
            rrr.translated.pop(k)
            rrr.sourse.insert(k,ftp)
            rrr.translated.insert(k,tftp)
            rrr.sourse.insert(k+1,stp)
            rrr.translated.insert(k+1, tstp)
        else:
             k = k +1
    return rrr

config_path = './furrycuttails.conf'
cut_list_string, min_length = crudConfig(config_path)
# длинна минимального куска
min_length = int(min_length)
# множество символов по которым происходит рез
csl = set()
for item in cut_list_string.split(','):
    csl.add(item[1:-1])

# исходный файл исходного языка
ss_file = ''
# исходный переводной файл
st_file = ''
# целевой файл исходного языка
ts_file = ''
# целевой файл перевода
tt_file = ''

print(sys.argv)
ss_file = sys.argv[1]
st_file = sys.argv[2]
# min_length = int(sys.argv[3])
ts_file = 'ts '+ss_file
tt_file = 'tt '+st_file


with open(ss_file,'rt', errors="ignore") as ssf:
    sst = ssf.read()
with open(st_file,'rt', errors="ignore") as stf:
    stt = stf.read()
sstl = len(sst)
sttl = len(stt)

ss_list = list()
ss_list.append(sst)
st_list = list()
st_list.append(stt)

rrr = ListData(
    sourse = list(),
    translated = list(),
    min_length = 10
)
rrr.sourse.append(sst)
rrr.translated.append(stt)
rrr.min_length = min_length
#print(rrr)
rrr = process_data(rrr)
#print(rrr)

k=0
with open(ts_file,'wt') as tsf:
    for item in rrr.sourse:
        tsf.write('<{}>. {}'.format(str(k).rjust(5,'0'),item))
        k = k+1
k=0
with open(tt_file,'wt') as ttf:
    for item in rrr.translated:
        ttf.write('<{}>. {}'.format(str(k).rjust(5,'0'),item))
        k=k+1



