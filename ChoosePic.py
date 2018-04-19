import sys

import Initialisation

def ChoosePic(a, i):
    #chtenie = xlrd.open_workbook('file' + '.xls', formatting_info=True)

    # выбираем активный лист
    #sheetch = chtenie.sheet_by_index(0)

    k = int
    j = int
    knl = int
    knp = int
    kvl = int
    kvp = int
    knlt = int
    nemd = int
    kne = int
    koe1 = int
    nso = int
    nepvp = int
    nepvl = int
    neso = int
    #knl = sheetch.row_values(12)[1]
    #knp = sheetch.row_values(13)[1]
    # kvl = sheetch.row_values(14)[1]
    # kvp = sheetch.row_values(15)[1]
    knl = int(a[12][0])
    knp = int(a[13][0])
    kvl = int(a[14][0])
    kvp = int(a[15][0])

    knlt = 2 + knl
    nemd = 2 + knl + 1
    kne = 2 + knl + knp
    neso = 2 + knl + knp + kvl + 1
    koe1 = 2 + knl + knp + kvl + kvp
    nepvl = 2 + knl + knp + kvl
    nepvp = 2 + knl + knp + kvl + 1
    nso = int(a[18][0])

    def algoritm(i):

        if i == 1:
            j = 100
        elif i == 2:
            j = 200
        elif i <= koe1:
            if i == nemd:
                if i == 3:
                    if i == kne:
                        j = 1
                    else:
                        j = 2
                else:
                    if i == kne:
                        j = 3
                    else:
                        j = 4
            else:
                if i <= kne:
                    if i < nemd:
                        j = 5
                    else:
                        j = 6
                else:
                    if nso == 1:
                        if neso == 2 + knl + knp + kvl + 1:
                            if i == neso:
                                if kvl == 0:
                                    if kvp == 1:
                                        j = 7
                                    else:
                                        j = 8
                                else:
                                    if kvp == 1:
                                        j = 9
                                    else:
                                        j = 10
                            else:
                                if i < neso:
                                    j = 11
                                else:
                                    j = 12
                        else:
                            j = 0
                    else:
                        if kvl == 0:
                            if nepvp == 2 + knl + knp + kvl + 1:
                                if i == nepvp:
                                    if kvp == 1:
                                        j = 13
                                    else:
                                        j = 14
                                else:
                                    j = 12
                            else:
                                j = 0
                        else:
                            if kvp == 0:
                                if nepvl == 2 + knl + knp + kvl:
                                    if i == nepvl:
                                        if kvl == 1:
                                            j = 15
                                        else:
                                            j = 16
                                    else:
                                        j = 11
                                else:
                                    j = 0
                            else:
                                if nepvl == 2 + knl + knp + kvl and nepvp == 2 + knl + knp + kvl + 1:
                                    if i > nepvl:
                                        if i == nepvp:
                                            if kvp == 1:
                                                j = 13
                                            else:
                                                j = 14
                                        else:
                                            j = 12
                                    else:
                                        if i == nepvl:
                                            if kvl == 1:
                                                j = 15
                                            else:
                                                j = 16
                                        else:
                                            j = 11
                                else:
                                    j = 0

        else:
            j = 0
        # 0 ошибка
        # 100 левый торец
        # 200 правый торец
        #print(j)
        return (j)
    if algoritm(i) == 100:
        pic_name = '100.PNG'
        return pic_name
    elif algoritm(i) == 200:
        pic_name = '200.PNG'
        return pic_name
    elif algoritm(i) == 1:
        pic_name = '1.PNG'
        return pic_name
    elif algoritm(i) == 2:
        pic_name = '2.PNG'
        return pic_name
    elif algoritm(i) == 3:
        pic_name = '3.PNG'
        return pic_name
    elif algoritm(i) == 4:
        pic_name = '4.PNG'
        return pic_name
    elif algoritm(i) == 5:
        pic_name = '5.PNG'
        return pic_name
    elif algoritm(i) == 6:
        pic_name = '6.PNG'
        return pic_name
    elif algoritm(i) == 7:
        pic_name = '7.PNG'
        return pic_name
    elif algoritm(i) == 8:
        pic_name = '8.PNG'
        return pic_name
    elif algoritm(i) == 9:
        pic_name = '9.PNG'
        return pic_name
    elif algoritm(i) == 10:
        pic_name = '10.PNG'
        return pic_name
    elif algoritm(i) == 11:
        pic_name = '11.PNG'
        return pic_name
    elif algoritm(i) == 12:
        pic_name = '12.PNG'
        return pic_name
    elif algoritm(i) == 13:
        pic_name = '13.PNG'
        return pic_name
    elif algoritm(i) == 14:
        pic_name = '14.PNG'
        return pic_name
    elif algoritm(i) == 15:
        pic_name = '15.PNG'
        return pic_name
    elif algoritm(i) == 16:
        pic_name = '16.PNG'
        return pic_name
    else:
        None


if __name__ == '__main__':
    a = Initialisation.createMatrix(32,1)
    a[12][0] = 2
    a[13][0] = 0
    a[14][0] = 1
    a[15][0] = 2
    a[18][0] = 0
    for i in range(1,15):
        print(ChoosePic(a,i))
    sys.exit()