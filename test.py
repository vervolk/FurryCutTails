from dataclasses import dataclass, field

st = '  \\'

@dataclass
class ListData():
    sourse:list
    translated:list
    min_length:int = 1

def cut_twice(st):
    ftp = st
    stp = ''
    lst = len(st)
    if lst > 2:
        middle_cut = lst // 2
        ftp = st[0:middle_cut]
        while middle_cut < lst:
            if st[middle_cut:middle_cut + 1] not in (' ', "\\"):
                ftp = ftp + st[middle_cut:middle_cut + 1]
                middle_cut = middle_cut + 1
            else:
                break
        stp = st[middle_cut:]
    return ftp ,stp

def cut_list(slist, tslist:list, ml:int):
    def add_sublist(inlist:list, applist:list):
        somelist = list()
        for item in inlist:
            somelist.append(item)
        for item in applist:
           somelist.append(item)
        return somelist

    # print('На входе: {}'.format(slist))
    if len(slist) == 0:
        return slist, tslist
    st = ''
    st = slist[0]
    stp, ftp = cut_twice(st)
    if len(stp) < ml or len(ftp) < ml:
        return slist, tslist
    #print(st)
    #print(stp)
    #print(ftp)
    if (st != stp) & (ftp != stp):
        slist = list()
        stpl = list()
        ftpl = list()
        stpl.append(stp)
        ftpl.append(ftp)
        # print('Ныряем: {}'.format(stpl))
        # print('Ныряем: {}'.format(ftpl))
        if len(stp) > ml:
            # slist = add_sublist(cut_list(slist, tslist,ml)[0], cut_list(stpl, tslist,ml)[0])
            slist = [*cut_list(slist, tslist,ml)[0], *cut_list(stpl, tslist,ml)[0]]
        else:
            slist = add_sublist(slist, stpl)
        if len(ftp) > ml:
            slist = add_sublist(cut_list(slist, tslist,ml)[0],cut_list(ftpl,tslist,ml)[0])
        else:
            slist = add_sublist(slist,ftpl)

    # print('На выходе: {}'.format(slist))
    return slist, tslist

def cut_twolist(rrr:ListData, n:int):
    rrr1:ListData
    ftp,stp = cut_twice(rrr.sourse.pop(n))
    rrr.sourse.insert(n,ftp)
    rrr.source.insert(n,stp)
    ftp, stp =  cut_twice(rrr.translated.pop(n))
    rrr.translated.insert(n,ftp)
    rrr.translated.insert(n+1,stp)
    return rrr1

s = 'sadfhadf234234 njadfadfh adf had fhda fhj adfahj adf hjad fjh ds fj df j fd j ds j df j dsfgjsfgjdgfjdfhghjdfg x fgjgffs'
sl = list()
sl.append(s)

ts = 'sadfhadf234234 njadfadfh adf had fhda fhj adfahj adf hjad fjh ds fj df j fd j ds j df j dsfgjsfgjdgfjdfhghjdfg x fgjgffs'
tsl = list()
tsl.append(s)

sl, tsl = cut_list(sl, tsl ,10)

rrr = ListData(
    sourse = list(),
    translated = list(),
    min_length = 10
)

rrr.sourse.append('sadfhadf234234 njadfadfh adf had fhda fhj adfahj adf hjad fjh ds fj df j fd j ds j df j dsfgjsfgjdgfjdfhghjdfg x fgjgffs')
rrr.translated.append('sadfhadf234234 njadfadfh adf had fhda fhj adfahj adf hjad fjh ds fj df j fd j ds j df j dsfgjsfgjdgfjdfhghjdfg x fgjgffs')
n = len( rrr.sourse)
k = 0
print('start')

def process_data(rrr: ListData):
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