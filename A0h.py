A0h_0_desc = 'Идентификатор интерфейса'
A0h_0 = {
    0x00: 'Неизвестный',
    0x01: 'GIBIC',
    0x02: 'Впаян в материнскую плату',
    0x03: 'SFP или SFP+',
    0x04: '300 pin XBI',
    0x05: 'Xenpak',
    0x06: 'XFP',
    0x07: 'XFF',
    0x08: 'XFP-E',
    0x09: 'XPak',
    0x0a: 'X2',
    0x0b: 'DWDM-SFP',
    0x0c: 'QSFP',
}
for i in range(0x0d,0x7f+1):
    A0h_0[i] = hex(i)+' Не определен'
for i in range(0x80,0xff+1):
    A0h_0[i] = hex(i)+' Определен вендором'

A0h_1_desc = 'Расширенный идентификатор'
A0h_1 = {
    0x00: 'Не ссответсвует MOD_DEF',
    0x01: 'GIBIC MOD_DEF 1',
    0x02: 'GIBIC MOD_DEF 2',
    0x03: 'GIBIC MOD_DEF 3',
    0x04: 'GIBIC/SFP',
    0x05: 'GIBIC MOD_DEF 5',
    0x06: 'GIBIC MOD_DEF 6',
    0x07: 'GIBIC MOD_DEF 7',
}
for i in range(0x08,0xff+1):
    A0h_1[i] = hex(i)+' Не определен'

A0h_2_desc = 'Тип Коннектора'
A0h_2 = {
    0x00: 'Неизвестный',
    0x01: 'SC',
    0x02: 'Медный разъем типа 1',
    0x03: 'Медный разъем типа 2',
    0x04: 'BNC/TNC',
    0x05: 'Коаксиальный (оптика)',
    0x06: 'FiberJack',
    0x07: 'LC',
    0x08: 'MT-RJ',
    0x09: 'MU',
    0x0a: 'SG',
    0x0b: 'Оптический Пигтейл',
    0x0c: 'MPO Parallel Optic',
    0x20: 'HSSDC II',
    0x21: 'Медный Пигтейл',
    0x22: 'RJ45',
}
for i in range(0x23,0x7f+1):
    A0h_2[i] = hex(i)+' Не определен'
for i in range(0x80,0xff+1):
    A0h_2[i] = hex(i)+' Определен вендором'

A0h_3_desc = ['Соответствие 10G Ethernet', 'Соответствие InfiniBand']
A0h_3 = [
    {
    7: '10G Base-ER',
    6: '10G Base-LRM',
    5: '10G Base-LR',
    4: '10G Base-SR',
    },
    {
    3: '1X SX',
    2: '1X LX',
    1: '1X Copper Active',
    0: '1X Copper Passive',
    }
]

A0h_4_desc = 'ESCON/SONET'
A0h_4 = {
    7: 'ESCON MMF, 1310 LED',
    6: 'ESCON SMF, 1310 Laser',
    5: 'OC-192, short',
    4: 'SONET reach specifier bit 1',
    3: 'SONET reach specifier bit 2',
    2: 'OC-48, long',
    1: 'OC-48, inter.',
    0: 'OC-48, short',
}

A0h_5_desc = 'SONET'
A0h_5 = {
    7: 'Unallocated',
    6: 'OC-12, single, long',
    5: 'OC-12, single, inter.',
    4: 'OC-12, short',
    3: 'Unallocated',
    2: 'OC-3, single,long',
    1: 'OC-3, single, inter.',
    0: 'OC-3, short',
}

A0h_6_desc = 'Соответствие Ethernet'
A0h_6 = {
    7: 'BASE-PX',
    6: 'BASE-BX10',
    5: '100BASE-FX',
    4: '100BASE-LX/LX10',
    3: '1000BASE-T',
    2: '1000BASE-CX',
    1: '1000BASE-LX',
    0: '1000BASE-SX',
}

A0h_7_desc = ['Длина соединения (оптика)', 'Оптическая технология']
A0h_7 = [
    {
    7: 'V (very long)',
    6: 'S (short)',
    5: 'I (inter.)',
    4: 'L (long)',
    3: 'M (medium)',
    },
    {
    2: 'Shortwave laser, linear Rx (SA)',
    1: 'Longwave laser (LC)',
    0: 'Electrical inter (EL)',
    }
]

A0h_8_desc = ['Оптическая технология',  'Технология SFP+ кабеля']
A0h_8 = [
    {
    7: 'Electrical intra (EL)',
    6: 'Shortwave laser w/o OFC (SN)',
    5: 'Shortwave laser with OFC (SL)',
    4: 'Longwavw laser (LL)',
    },
    {
    3: 'Активный кабель',
    2: 'Пассивный кабель',
    1: 'Не определено',
    0: 'Не определено',
    }
]

A0h_9_desc = 'Среда передачи'
A0h_9 = {
    7: 'Сдвоенная пара (TW)',
    6: 'Витая пара (TP)',
    5: 'Коаксиальный мини(MI)',
    4: 'Коаксиальный видео (TV)',
    3: 'Мультимод. ОВ 62.5нм (M6)',
    2: 'Мультимод. ОВ, 50нм (M5, M5E)',
    1: 'Не определен',
    0: 'Одномод. ОВ (SM)',
}

A0h_10_desc = 'Скорость передачи'
A0h_10 = {
    7: '1200 МБ/сек',
    6: '800 МБ/сек',
    5: '1600 МБ/сек',
    4: '400 МБ/сек',
    3: 'Не определено',
    2: '200 МБ/сек',
    1: 'Не определено',
    0: '100 МБ/сек',
}

A0h_11_desc = 'Кодировка'
A0h_11 = {
    0x00: 'Не определено',
    0x01: '8B/10B',
    0x02: '4B/5B',
    0x03: 'NRZ',
    0x04: 'Manchester',
    0x05: 'SONET Scrambled',
    0x06: '64B/66B',
}
for i in range(0x07,0xff+1):
    A0h_11[i] = hex(i)+' Не определено'

A0h_12_desc = 'Номинальная скорость'

A0h_13_desc = 'Идентификатор скорости'
A0h_13 = {
    0x00: 'Не определен',
    0x01: 'SFF-8079 (4/2/1G)',
    0x02: 'SFF-8431 (8/4/2G Rx)',
    0x03: 'Не определен',
    0x04: 'SFF-8431 (8/4/2G Tx)',
    0x05: 'Не определен',
    0x06: 'SFF-8431 (8/4/2G Rx&Tx)',
    0x07: 'Не определен',
    0x08: 'FC-PI-5 (10/8/4G Rx,Tx)',
    0x0a: 'Не определен',
}
for i in range(0x0b,0xff+1):
    A0h_13[i] = hex(i)+' Не определен'

A0h_14_desc = 'Длина (SM) км'

A0h_15_desc = 'Длина (SM) 100м'

A0h_16_desc = 'Длина (50um, OM2) 10м'

A0h_17_desc = 'Длина (65.2um, OM1) 10м'

A0h_18_desc = 'Длина (Медь) м'

A0h_19_desc = 'Длина (50um, OM3) 10м'

A0h_vendorName = [20 - 35]

A0h_vendorOUI = [37-39]

A0h_vendorPN = [40-55]

A0h_vendorRev = [56-59]

#------------------------------------------------
#---Optical or Passive/active cable (A0h_3 to 10)
#------------------------------------------------

A0h_60_desc = 'Длина волны 1'

A0h_61_desc = 'Длина волны 2'

A0h_60_passive_desc = 'Passive Cabble Spec. 1'

A0h_61_passive_desc = 'Passive Cable Spec. 2'

A0h_60_passive = {
    7: 'Unallocated',
    6: 'Unallocated',
    5: 'SFF-8461',
    4: 'SFF-8461',
    3: 'SFF-8461',
    2: 'SFF-8461',
    1: 'FC-PI-4 Appendix H',
    0: 'SFF-8431 Appendix E',
}

A0h_61_passive = {
    7: 'Unallocated',
    6: 'Unallocated',
    5: 'Unallocated',
    4: 'Unallocated',
    3: 'Unallocated',
    2: 'Unallocated',
    1: 'Unallocated',
    0: 'Unallocated',
}

A0h_60_active_desc = 'Active Cabble Spec. 1'

A0h_61_active_desc = 'Active Cable Spec. 2'

A0h_60_active = {
    7: 'Unallocated',
    6: 'Unallocated',
    5: 'Unallocated',
    4: 'Unallocated',
    3: 'FC-PI-4',
    2: 'SFF-8431',
    1: 'FC-PI-4 Appendix H',
    0: 'SFF-8431 Appendix E',
}

A0h_61_active = {
    7: 'Unallocated',
    6: 'Unallocated',
    5: 'Unallocated',
    4: 'Unallocated',
    3: 'Unallocated',
    2: 'Unallocated',
    1: 'Unallocated',
    0: 'Unallocated',
}

#----------------------------------------------------
#---End Optical or Passive/active cable (A0h_3 to 10)
#----------------------------------------------------

A0h_63_desc = 'Контрольная сумма 0-62'

A0h_64_desc = 'Опции 1'

A0h_64 = {
    7: 'Не определено',
    6: 'Не определено',
    5: 'Не определено',
    4: 'Не определено',
    3: 'Не определено',
    2: 'Охлаждаемый лазер',
    1: 'Ур. мощн. (0 - Уровень 1, 1 - 2)',
    0: 'Линеный выход премника',
}

A0h_65_desc = 'Опции 2'

A0h_65 = {
    7: 'Не определено',
    6: 'Не определено',
    5: 'Поддержка RATE_SELECT',
    4: 'Поддержка TX_DISABLE',
    3: 'Поддержка TX_FAULT',
    2: 'Поддержка Обнаружения синала',
    1: 'Поддержка LOS',
    0: 'Не определено',
}

A0h_66_desc = 'Скорость max'

A0h_67_desc = 'Скорость min'

A0h_vendorSN = [68-83]

A0h_dataCode = [84-91]

A0h_92_desc = 'Тип диагностики и мониторинга'

A0h_92 = {
    7: 'Устаревший (Legacy)',
    6: 'DDM',
    5: 'Внутренняя Калибровка',
    4: 'Внешняя Калибровка',
    3: 'Вх. мощн.(0 - OMA, 1 - Ср. знач.)',
    2: 'Требуется изменение адреса',
    1: 'Не определен',
    0: 'Не определен',
}

A0h_93_desc = 'Расширенные опции'

A0h_93 = {
    7: 'Поддержка флага Alarm/Warning',
    6: 'Программное управление TX_DISABLE',
    5: 'Программный мониторинг TX_FAULT',
    4: 'Программный мониторинг RX_LOS',
    3: 'Программное управление RATE_SELECT',
    2: 'Application Select control (SFF-8079)',
    1: 'Soft Rate Select control (SFF-8431)',
    0: 'Не определено',
}

A0h_94_desc = 'Соответствие SFF-8472'

A0h_94 = {
    0x00: 'Неизвестно',
    0x01: 'Rev.9.3 of SFF-8472',
    0x02: 'Rev.9.5 of SFF-8472',
    0x03: 'Rev.10.2 of SFF-8472',
    0x04: 'Rev.10.4 of SFF-8472',
    0x05: 'Rev.11.0 of SFF-8472',
}
for i in range(0x06,0xff+1):
    A0h_94[i] = hex(i)+' Не определено'
    
A0h_95_desc = 'Контрольная сумма 64-94'

