material = { '0':'Не выбрано', '101': 'Сталь СТ3', '102':'Сталь СТ4', '103':'Сталь А30', '104':'Сталь А20', '105':'Сталь А12', '106':'Сталь А40Г', '107':'Сталь 10',
            '108':'Сталь 20', '109':'Сталь 25', '110':'Сталь 30', '111':'Сталь 35', '112':'Сталь 40', '113':'Сталь 45', '114':'Сталь 50', '115':'Сталь 55',
            '116':'Сталь 60', '117':'Сталь 70', '118':'Сталь 80', '119':'Сталь АС11', '120':'Сталь АС14', '122':'У8', '123':'У9', '124':'У10', '125':'«Серебрянка»',
            '126':'У11', '127':'У12', '128':'ХВГ', '140':'20Х13', '141':'30Х13', '142':'14Х17H2', '143':'20Х17H2', '144':'Х18И9', '145':'12Х18Н9Т', '146':'40Х13',
            '147':'17Х18Н9', '148':'08Х18Н10Т', '149':'12Х13', '150':'12Х17', '151':'25Х13Н2', '152':'12Х13Н2', '170':'15Х', '171':'20Х', '172':'30Х', '173':'35Х',
            '174':'38ХА', '175':'40Х', '176':'45Х', '177':'50Х', '178':'15ХФ', '179':'40ХФА', '180':'40ХС', '181':'33ХС', '182':'38ХС', '183':'30ХГСА', '184':'38Х2М0А',
            '185':'20ХГНР', '186':'35ХГСА', '187':'30ХГСН2А', '188':'38Х20', '189':'20ХН4ФА', '190':'36Х2Н2МФА', '201':'СЧ 12-28', '202':'СЧ 15-32', '203':'СЧ 18-36',
            '204':'СЧ 21-40', '205':'СЧ 24-44', '206':'СЧ 28-48', '207':'СЧ 32-52', '216':'ВЧ 38-17', '217':'ВЧ 42-12', '218':'ВЧ 45-5', '219':'ВЧ 50-2', '301':'Бр0Ф10-1',
            '302':'БрАМц9-2', '303':'БрАЖ9-4', '304':'Бр-0Ф6,5-1,5', '305':'Бр0Ф7-0,2', '306':'БрКМЦЗ-1', '307':'БрБ2', '308':'Броц 4-3', '336':'М1', '337':'М2', '338':'М3',
            '339':'М4', '360':'ЛС-59-1 В', '361':'Л96', '362':'Л90', '363':'ЛС-59-1', '364':'Л69', '365':'ЛМц59-2', '366':'Л80', '367':'Л63', '368':'ЛЖМц59-1-1', '369':'ЛАЖ60-1-1',
            '401':'В95', '402':'Д16Т', '403':'АД31', '404':'АМг6', '405':'АМг2', '406':'АД33', '407':'Д-1', '408':'Д1Т', '409':'АЛ2', '410':'АЛ4', '411':'АЛ9', '412':'В93',
            '413':'АК6', '414':'АК8', '415':'Д20', '501':'ВТ1-0', '502':'ВТ3-1', '503':'ВТ1-1', '504':'ВТ5', '505':'ВТ5-1', '506':'48Т2', '507':'480Т3', '508':'ВТ18',
            '509':'ЛТ20', '510':'ВТ14', '511':'ВТ16', '512':'ПТ7М', '513':'ПТ38', '514':'0Т4', '515':'0Т4-0'}

profile = {'0':'Не выбрано','1':'Круг', '2':'Квадрат', '3':'Шестигранник', '4':'Трехгранник', '5':'Прямоугольник', '6':'Труба'}

type_workpiece = {'0':'Не выбрано', '1':'Прокат калиброванный', '2':'Прокат горячекатанный', '3':'Литьё', '4': 'Лист', '5':'Штамповка', '6':'Поковка', '7':'Заготовка получена спеканием из порошка',
                  '10':'Пруток шлифованный', '11':'Проволока', '12':'Труба холоднотянутая', '13':'Труба горячекатанная'}

type_HTO = {'0':'Не выбрано', '01': 'Закалка (полная обработка)', '02':'Отжиг(полная обработка)', '03':'Нормализация (полная обработка)', '04':'Цементация (полная обработка)', '05':'Азотирование (полная обработка)',
            '11': 'Закалка (частичная обработка)', '12':'Отжиг (частичная обработка)', '13':'Нормализация (частичная обработка)', '14': 'Цементация (частичная обработка)', '15':'Азотирование (частичная обработка)'}

cover = {'0':'Не выбрано','01': 'Фосфатирование (покрытие кругом)', '11': 'Фосфатирование (покрытие выборочно)','02': 'Оксидирование (покрытие кругом)', '12': 'Оксидирование (покрытие выборочно)', '03': 'Анодирование (покрытие кругом)',
         '13': 'Анодирование (покрытие выборочно)', '04': 'Кадмирование (покрытие кругом)', '14': 'Кадмирование (покрытие выборочно)', '05': 'Цинкование (покрытие кругом)', '15': 'Цинкование (покрытие выборочно)',
         '06': 'Никелирование (покрытие кругом)', '16': 'Никелирование (покрытие выборочно)', '07': 'Хромирование (покрытие кругом)', '17': 'Хромирование (покрытие выборочно)', '08': 'Серебрение (покрытие кругом)',
         '18': 'Серебрение (покрытие выборочно)', '09':'Золочение (покрытие кругом)', '19':'Золочение (покрытие выборочно)', '010': 'Оловянирование (покрытие кругом)', '110': 'Оловянирование (покрытие выборочно)',
         '011': 'Сплав олово-никель (покрытие кругом)', '111': 'Сплав олово-никель (покрытие выборочно)', '012': 'Сплав олово-висмут (покрытие кругом)', '112': 'Сплав олово-висмут (покрытие выборочно)', '013': 'Сплав никель-кобальт (покрытие кругом)',
         '113': 'Сплав никель-кобальт (покрытие выборочно)', '014': 'Хим. пас (покрытие кругом)', '114': 'Хим. пас (покрытие выборочно)'}

mashine = {'00':'Не выбрано','0':'Токарно-револьверный автомат', '1':'Многошпиндельный горизонтальный прутковый п/а', '2':'Автомат продольного точения', '3': 'Многошпиндельный вертикальный п/а',
           '4':'Многорезцовый токарный п/а', '5':'Токарно-револьверный станок или п/а', '6':'Токарный станок с ЧПУ', '7':'Токарно-ви6торезный и токарный станок (ручное управление)',
           '8':'Многошпиндельный горизонтальный патрон п/а', '9':'Круглошлифовальный станок','10':'Внутришлифовальный станок', '11':'Плоскошлифовальный станок', '12':'Безцентрошлифовальный станок',
           '13':'Вертикально-фрезерный с ручным управлением', '14':'Горизонтально-фрезерный станок', '15':'Широкоуниверсальные(инструментальные)станки', '16':'Вертикально-фрезерные станки с ЧПУ',
           '17':'Координатно-расточные станки', '18':'Вертикально-сверлильные с ручным управлением', '19':'Вертикально-сверлильные с ЧПУ', '20':'Горизонтально-расточные станки',
           '21':'Алмазно-расточные станки', '22':'Зубофрезерные станки', '23':'Зубодолбежные станки', '24':'Зубошлифовальные станки', '25':'Резьбонарезные станки', '26':'Резьбонакатные станки',
           '27':'Зубострогальные станки', '28':'Протяжные станки', '29':'Радиально-сверлильные станки', '30':'Отрезные станки', '31':'Аппарат газовой резки', '32':'Долбежные станки', '33':'Резьбошлифовальные станки',
           '34':'Щлицешлифовальные станки', '35':'Сверлильно-фрезерно-расточные станки с ЧПУ', '36':'Универсально-шлифовальные станки', '37':'Торцекруглошлифовальные станки', '38':'Электроискровые станки',
           '39':'Координатно-шлифовальные станки', '40': 'Токарно-карусельные станки', '41':'Продольно-фрезерные станки', '42':'Копировально-фрезерные станки', '43':'Вертикально-расточные станки',
           '44':'Зубошевинговальные станки', '45':'Зубопритирочные и обратные станки', '46':'Слесарный верстак', '47':'Фрезерно-центровальный станок'}

el_name_tm3 = {'0':'Не выбрано','1':'Конус усеченный', '2':'Сферическая пов-ть в 1-ом квадранте', '3':'Сферическая пов-ть в двух квадранте','5':'Фаска', '6':'Радиусная пов-ть(выпуклая) в 1-ом квадранте', '7':'Радиусная пов-ть(выпуклая) в двух квадрантах',
           '9':'Радиусная пов-ть(вогнутая) в двух квадрантах', '11':'Конус','21':'Резьба метрическая', '22':'Резьба трубная', '23':'Резьба дюймовая(коническая)', '24':'Резьба трапециевидная', '25':'Резьба упорная', '26':'Резьба микрометр',
           '27':'Резьба специальная','30':'Червяк архимедов', '31':'Червяк эвольвентный', '32':'Червяк ковалютный', '33':'Червяк тороидный',
           '35':'Накатка прямая', '36':'Нактка косая', '37':'Накатка сетчатая', '38':'Накатка на торце(буртике)',
           '39':'Рифление', '40': 'Канавка прямоугольная', '41':'Канавка трапецеидальная', '42':'Канавка трапециедальная односторонняя(правая)', '43':'Канавка трапециедальная односторонняя(левая)',
           '44':'Канавка угловая', '45':'Канавка радиусная', '46':'Канавка комбинированная I', '47':'Канавка фасонная', '51':'Канавка торцевая I','52':'Канавка торцевая II','53':'Канавка торцевая III',
           '54':'Канавка торцевая IV','55':'Канавка торцевая V','56':'Канавка торцевая VI','61':'Канавка комбинированная II','62':'Канавка прямоугольная угловая','71':'Канавка винтовая прямоугольная',
           '72': 'Канавка винтовая трапецеидальная','73': 'Канавка винтовая трапецеидальная(односторонняя) правая','74': 'Канавка винтовая трапецеидальная(односторонняя) левая','75': 'Канавка винтовая радиусная',
           '76': 'Канавка винтовая угловая','77': 'Канавка винтовая фасонная','80': 'Щлиц прямобочный','81': 'Щлиц эвольвентный','85': 'Центровое отверстие типа A','86': 'Центровое отверстие типа B',
           '87': 'Центровое отверстие типа C','88': 'Центровое отверстие типа R','89': 'Центровое отверстие типа P','90': 'Центровое отверстие типа T','96': 'Зубья прямые','97': 'Зубья косые',
           '98': 'Прямая на конусе','99': 'Червячные'}


fit = {'0':'Не выбрано', '1':'R для р-ров 1-120 мм\nДля р-ров 80-500', '2':'R(r)', '3':'S(s)', '4':'T(t)', '5':'U(u)', '6':'P(p)', '7':'N(n)', '8':'M(m)', '9':'H(h)', '10':'Js(js)', '11':'C(c)', '12':'K(k)',
       '13':'F(f)', '15':'D(d)', '16':'A(a)', '17':'B(b)', '18':'E(e)', '19':'G(g)','20':'V(v)', '21':'X(x)', '22':'Y(y)', '23':'Z(z)', '24':'ZA(za)', '25':'ZB(zb)', '26':'ZC(zc)', '27':'CD(cd)', '28':'EF(ef)',
       '29':'FG(fg)'}

precision = {'0':'Не выбрано', '10':'5', '20':'6', '21':'7', '30':'8', '31':'10', '32':'9', '40':'11', '50':'12', '52':'13', '70':'14', '80':'15', '90':'16','92':'17', '60':'01', '100':'0', '110':'1', '120':'2',
             '130':'3', '140':'4'}

Rz_Ra = {'0':'Не выбрано', '1':'Rz=320', '2':'Rz=160', '3':'Rz=80', '4':'Rz=40', '5':'Rz=20', '6':'Ra=2.5', '7':'Ra=1.25', '8':'Ra=0.63', '9':'Ra=0.32'}

condition = {'0':'Не выбрано', '1':'Обеспечить притиркой по сопрягаемой детали', '2':'Элемент получен в заготовке окончательно', '3':'Обеспечить при сборке', '4':'Сверлить в сборе', '5':'Пригнать по пуансону',
             '6':'Элемент получен в заготовке предварительно', '7':'Размер до накатки'}

TU = {'00':'Не выбрано','0':'Элемент базовый', '1':'Элемент зависимый', '2':'Элементы равноценные', '3':'Элемент определяет положение общей оси'}

TVR = {'0':'Не выбрано','1':'Биение', '2':'Соосность эксцентриситет', '3':'Перпендикулярность', '4':'Параллельность', '5':'Симметричность'}

El_2 = {'00':'Не выбрано', '0':'Диаметр', '1':'Радиус скругления для прямоугольного паза', '3':'Угол φ', '4':'Угол  φ/2', '5':'Угол дополняющий до 90 градусов', '6':'Линейный размер(длина)','7':'Шаг резьбы или накатки',
        '8':'Модуль', '9':'Ширина', '10':'Глубина', '11':'Шероховатость буртика', '12':'Базовый элемент', '13':'Радиус скругления дна радиусного паза, лыски','14':'Линейный размер H', '15':'Линейный размер H1',
        '16':'Линейный размер H2', '17':'Радиус скругления боковых поверхностей под фрезу','18':'Количество граней щлицы'}

position = {'00':'Не выбрано','3':'Перпендикулярно оси Z','4':'Параллельно оси Z', '5':'Под углом к оси Z', '1':'Совпадает с осью', '6':'Параллельно оси Y', '7':'Параллельно оси X', '8':'Перпендикулярно оси Y',
            '9':'Перпендикулярно оси X', '10':'Под углом к оси Y', '11':'Под углом к оси X', '0':'На одной оси с приоритетным элементом'}

mashine_finprocess = {'0':'Не выбрано'}

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k