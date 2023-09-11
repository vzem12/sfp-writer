#Rostelecom SFP Writer
#ПО для работы с программатором SFP/SFP+ ProgrammatorSFP_2.5 by ZemtsovVA vladimir-a-zemtsov@ya.ru
#Для подробностей читай ReadMe.txt файл

import PySimpleGUI as sg
from bitsOper import *
from A0h import *
from A2h import *
# from conf_cisco import *
# from conf_juniper import *
from threading import Thread
import serial
import serial.tools.list_ports
import time
import math
import re
import os
from threading import Thread
# import colorama
# from colorama import Fore, Back, Style
from image import *
import struct
import datetime
from datetime import datetime
import copy
from hashlib import md5
from zlib import crc32
import json

release_version = '2.3.3'
email = 'vladimir-a-zemtsov@ya.ru'
programm_name = f'Rostelecom SFP Writer v.{release_version}'

file_handler = open('theme.cfg', 'r')
active_theme = int(file_handler.read().strip())
file_handler.close()

juniper_data = json.load(open('conf_juniper.json', 'r'))
juniper_pn = juniper_data['pn']
juniper_rev = juniper_data['rev']

cisco_data = json.load(open('conf_cisco.json', 'r'))
cisco_sfp_type = cisco_data['sfp_type']
cisco_vendor_id = cisco_data['vendor_id']
cisco_security_key = cisco_data['security_key']
cisco_pids = cisco_data['pids']
cisco_vids = cisco_data['vids']
            
# colorama.init()
# INFO = Back.CYAN + Fore.WHITE
# FAIL = Back.RED + Fore.WHITE + Style.BRIGHT
# OK = Back.GREEN + Fore.WHITE
# RST = Style.RESET_ALL
INFO,FAIL,OK,RST = '','','',''
themes = ['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 
'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 
'DarkBlue16', 'DarkBlue17', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 
'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkGreen', 
'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGrey', 'DarkGrey1', 'DarkGrey2', 
'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 
'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 
'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 
'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 
'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 
'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 
'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 
'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 
'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 
'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Reddit', 'Reds', 'SandyBeach', 
'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']
fav_themes = [9,13,14,16,19,44,47,62,63,68,71,72,73,74,75,76,77,79,81,83,84,85,90,91,94,95,96,97,98,105,108,109,111,117,118,119,121,123,128,129,130,132,133,134,135,136,137,138]
sg.theme(themes[active_theme])
comlist = serial.tools.list_ports.comports()
COMS = []
for el in comlist:
    COMS.append(el.device)

sfp_bytes_len = 256
read_timeout = 10
debug = True
setup_sleep = 2

v0, k0 = list(A0h_0.values()), list(A0h_0.keys())
v1, k1 = list(A0h_1.values()), list(A0h_1.keys())
v2, k2 = list(A0h_2.values()), list(A0h_2.keys())
v3_0, k3_0 = list(A0h_3[0].values()), list(A0h_3[0].keys())
v3_1, k3_1 = list(A0h_3[1].values()), list(A0h_3[1].keys())
v4, k4 = list(A0h_4.values()), list(A0h_4.keys())
v5, k5 = list(A0h_5.values()), list(A0h_5.keys())
v6, k6 = list(A0h_6.values()), list(A0h_6.keys())
v7_0, k7_0 = list(A0h_7[0].values()), list(A0h_7[0].keys())
v7_1, k7_1 = list(dict(list(A0h_7[1].items())+list(A0h_8[0].items())).values()), list(dict(list(A0h_7[1].items())+list(A0h_8[0].items())).keys())
v8_1, k8_1 = list(A0h_8[1].values()), list(A0h_8[1].keys())
v9, k9 = list(A0h_9.values()), list(A0h_9.keys())
v10, k10 = list(A0h_10.values()), list(A0h_10.keys())
v11, k11 = list(A0h_11.values()), list(A0h_11.keys())
v13, k13 = list(A0h_13.values()), list(A0h_13.keys())
v64, k64 = list(A0h_64.values()), list(A0h_64.keys())
v65, k65 = list(A0h_65.values()), list(A0h_65.keys())
v92, k92 = list(A0h_92.values()), list(A0h_92.keys())
v93, k93 = list(A0h_93.values()), list(A0h_93.keys())
v94, k94 = list(A0h_94.values()), list(A0h_94.keys())
v2_110, k2_110 = list(A2h_110.values()), list(A2h_110.keys())
v2_112, k2_112 = list(A2h_112.values()), list(A2h_112.keys())
v2_113, k2_113 = list(A2h_113.values()), list(A2h_113.keys())
v2_116, k2_116 = list(A2h_116.values()), list(A2h_116.keys())
v2_117, k2_117 = list(A2h_117.values()), list(A2h_117.keys())
v2_118, k2_118 = list(A2h_118.values()), list(A2h_118.keys())

A0h_cisco_sfp_type_val, A0h_cisco_sfp_type_key = list(cisco_sfp_type.values()), list(cisco_sfp_type.keys())
A0h_cisco_vendor_id_val, A0h_cisco_vendor_id_key = list(cisco_vendor_id.values()), list(cisco_vendor_id.keys())
A0h_cisco_security_key_val, A0h_cisco_security_key_key = list(cisco_security_key.values()), list(cisco_security_key.keys())
A0h_cisco_pids = cisco_pids

def toHexKey(key, length):
    hexKey = hex(key)[2:]
    if len(hexKey) < length: hexKey = '0'*(length - len(hexKey)) + hexKey
    hexKey = '0x' + hexKey.upper()
    return hexKey

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def i2cScan(COM_PORT, parent):
    i2c=[]
    parent += 'Сканиррование I2C шины: '
    if debug: print(f'{parent}Начало сканирования I2C {INFO} INFO {RST}')
    try:
        SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
    except serial.serialutil.SerialException:
        return 'serial error'
    if setup_sleep > 0: time.sleep(setup_sleep)
    if debug: print(f'{parent}Открыт порт {COM_PORT} {INFO} INFO {RST}')
    SFP.write(b'\xee')
    if debug: print(f'{parent}Отправлена команда 0xEE {INFO} INFO {RST}')
    FlagOk = False
    # Flag = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {type(m)} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            # if not Flag and m == b'\xdd\r\n':
                # Flag = True
            if m == b'\xee\r\n':
                if debug: print(f'{parent}Сканирование I2C завершено {OK} OK {RST}')
                FlagOk = True
            else:
                i2c.append(m)
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
    return i2c

def ishexdigit(h):
    try:
        int(h,16)
        return True
    except:
        return False

def timeoutReadLine(SFP, parent):
    tic = time.time()
    buff = b''
    while (time.time() - tic) < read_timeout:
        buff += SFP.read()
        if b'\n' in buff:
            return '{OK} OK {RST}', buff
    if buff == b'':
        return 'empty', 0
    else:
        return 'error', buff
        
def A2h_read(COM_PORT, parent):
    parent += 'Чтение A2h: '
    if debug: print(f'{parent}Начало чтения {INFO} INFO {RST}')
    firmwareDec=[]
    firmwareByte = b''
    try:
        SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
    except serial.serialutil.SerialException:
        return 'serial error'
    if setup_sleep > 0: time.sleep(setup_sleep)
    if debug: print(f'{parent}Открыт порт {COM_PORT} {INFO} INFO {RST}')
    SFP.write(b'\x01')
    if debug: print(f'{parent}Отправлена команда 0x01 {INFO} INFO {RST}')
    SFP.write(b'\x51')
    if debug: print(f'{parent}Отправлен адрес регистра 0x50 {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\x99\r\n':
            if debug: print(f'{parent}Успешно отправлен адрес регистра 0x50 {OK} OK {RST}')
            FlagOk = True
    if debug: print(f'{parent}Начало чтения 256 байт с A2h {INFO} INFO {RST}')
    readFlag = False
    counter = 0
    while not readFlag and counter != 5: 
        counter += 1
        firmwareDec.clear()
        firmwareByte = b''
        error = ''
        for i in range(sfp_bytes_len):
            try:    
                err,rcv = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    return 'read error 1'
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    return 'read error 2'
                firmwareDec.append(int(rcv.decode("utf-8")))
                firmwareByte += bytes([firmwareDec[-1]])
                if debug: print(f'{parent}Считан байт {hex(i)} со значением {hex(int(rcv.decode("utf-8")))} {OK} OK {RST}')
                readFlag = True
            except UnicodeDecodeError:
                if debug: print(f'{parent}Ошибка чтения байта {i} - UnicodeDecodeError  {FAIL} FAIL {RST}')
                error = 'read error 3'
                break
            except ValueError:
                if debug: print(f'{parent}Ошибка чтения байта {i} - ValueError  {FAIL} FAIL {RST}')
                error = 'read error 4'
                break
    
    SFP.close()
    if error == '':
        if debug: print(f'{parent}регистр A2h успешно считан! {OK} OK {RST}')
        return firmwareByte
    else:
        if debug: print(f'{parent}Ошибка чтения регистра A2h {FAIL} FAIL {RST}')
        return error
    
def SFP_read(COM_PORT, parent):
    parent += 'Чтение EEPROM: '
    if debug: print(f'{parent}Начало чтения {INFO} INFO {RST}')
    firmwareDec=[]
    firmwareByte = b''
    try:
        SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
    except serial.serialutil.SerialException:
        return 'serial error'
    if setup_sleep > 0: time.sleep(setup_sleep)
    if debug: print(f'{parent}Открыт порт {COM_PORT} {INFO} INFO {RST}')
    SFP.write(b'\x01')
    if debug: print(f'{parent}Отправлена команда 0x01 {INFO} INFO {RST}')
    SFP.write(b'\x50')
    if debug: print(f'{parent}Отправлен адрес регистра 0x50 {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\x99\r\n':
            if debug: print(f'{parent}Успешно отправлен адрес регистра 0x50 {OK} OK {RST}')
            FlagOk = True
    if debug: print(f'{parent}Начало чтения {sfp_bytes_len} байт с SFP/SFP+ {INFO} INFO {RST}')
    readFlag = False
    counter = 0
    while not readFlag and counter != 5: 
        counter += 1
        firmwareDec.clear()
        firmwareByte = b''
        error = ''
        for i in range(sfp_bytes_len):
            try:    
                err,rcv = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    return 'read error 1'
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    return 'read error 2'
                firmwareDec.append(int(rcv.decode("utf-8")))
                firmwareByte += bytes([firmwareDec[-1]])
                if debug: print(f'{parent}Считан байт {hex(i)} со значением {hex(int(rcv.decode("utf-8")))} {OK} OK {RST}')
                readFlag = True
            except UnicodeDecodeError:
                if debug: print(f'{parent}Ошибка чтения байта {i} - UnicodeDecodeError  {FAIL} FAIL {RST}')
                error = 'read error 3'
                break
            except ValueError:
                if debug: print(f'{parent}Ошибка чтения байта {i} - ValueError  {FAIL} FAIL {RST}')
                error = 'read error 4'
                break
    
    SFP.close()
    if error == '':
        if debug: print(f'{parent}EEPROM успешно считана! {OK} OK {RST}')
        return firmwareByte
    else:
        if debug: print(f'{parent}Ошибка чтения EEPROM  {FAIL} FAIL {RST}')
        return error

def A2h_write(COM_PORT, firmware, parent): 
    global writeResult, writeOn, writtenBytes
    only_changed = v['A2h_only_changed']
    parent += 'Запись A2h EEPROM: '
    try:
        SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
    except serial.serialutil.SerialException:
        writeResult = 'serial error'
    if setup_sleep > 0: time.sleep(setup_sleep)
    if debug: print(f'{parent}Открыт порт {COM_PORT} {INFO} INFO {RST}')
    if pass_on: 
        err = InputPassword(SFP, len(PassAr), PassAr, parent)
        if err != 0: 
            writeResult = 'password error'
        if debug: print(f'{parent}Пароль {PassAr} успешно введен! {OK} OK {RST}')
    if only_changed and A2hFirmwareOriginal != '':
        firmwareChanged = b''
        firmwareChangedNums = list()
        for i in range(len(A2hFirmwareOriginal)):
            if firmware[i] != A2hFirmwareOriginal[i]:
                if i not in [123,124,125,126]:
                    firmwareChanged += bytes([firmware[i]])
                    firmwareChangedNums.append(i)
        firmware = firmwareChanged
        firmwareNums = firmwareChangedNums
    else:
        firmwareNums = list()
        for i in range(len(firmware)):
            firmwareNums.append(i)
    bNum = 0
    delta = 1000/len(firmware)
    writtenBytes = len(firmware)
    for i in range(len(firmware)):
        if not writeOn:
            break
        else:
            bNum += 1
            if i in [123,124,125,126] and not only_changed:
                writeWindow['write_status'].UpdateBar(bNum*delta)
                continue
            SFP.write(b'\x0a')
            if debug: print(f'{parent}Отправка команды 0x0A {INFO} INFO {RST}')
            SFP.write(b'\x51')
            if debug: print(f'{parent}Отправлен адрес регистра 0x51 {INFO} INFO {RST}')
            FlagOk = False
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    writeResult = 'read error 1'
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    writeResult = 'read error 2'
                    return
                if m == b'\x99\r\n':
                    if debug: print(f'{parent}Успешно отправлен адрес регистра 0x51 {OK} OK {RST}')
                    FlagOk = True
            SFP.write(bytes([firmwareNums[i]]))
            if debug: print(f'{parent}Отправлен адрес смещения {hex(firmwareNums[i])} {INFO} INFO {RST}')
            FlagOk = False
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    writeResult = 'read error 1'
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    writeResult = 'read error 2'
                    return
                if m == b'\x99\r\n':
                    if debug: print(f'{parent}Адрес смещения {hex(firmwareNums[i])} успешно отправлен! {OK} OK {RST}')
                    FlagOk = True
            SFP.write(bytes([firmware[i]]))
            if debug: print(f'{parent}Отправлено значение байта {hex(firmware[i])}')
            FlagOk = False
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    writeResult = 'read error 1'
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    writeResult = 'read error 2'
                    return
                if m == b'\x99\r\n':
                    if debug: print(f'{parent}Значение байта {hex(firmware[i])} успешно отправлено! {OK} OK {RST}')
                    FlagOk = True
            writeWindow['write_status'].UpdateBar(bNum*delta)
    return

def SFP_write(COM_PORT, firmware, parent): 
    global writeResult, writeOn, writtenBytes
    only_changed = v['only_changed']
    parent += 'Запись EEPROM: '
    firmwareOriginal = SFP_read(COM_PORT, '')
    if firmwareOriginal == 'serial error':
        writeResult = 'serial error'
        return
    elif firmwareOriginal == 'read error 1' or firmwareOriginal == 'read error 2':
        writeResult = 'read error 1'
        return
    elif firmwareOriginal == 'read error 3': 
        writeResult = 'read error 3'
        return
    elif firmwareOriginal == 'read error 4': 
        writeResult = 'read error 4'
        return
    else:
        test_byte = 1000
        for i in range(len(firmware)):
            if firmware[i] != firmwareOriginal[i]: 
                test_byte = i
                break
        if test_byte == 1000:
            if debug: print(f'{parent}Ни один байт не был изменен, запись не требуется!')
            writeResult = 'off'
            return
        else:
            if only_changed:
                firmwareChanged = b''
                firmwareChangedNums = list()
                for i in range(len(firmwareOriginal)):
                    if firmware[i] != firmwareOriginal[i]:
                        firmwareChanged += bytes([firmware[i]])
                        firmwareChangedNums.append(i)
                firmware = firmwareChanged
                firmwareNums = firmwareChangedNums
            else:
                firmwareNums = list()
                for i in range(len(firmware)):
                    firmwareNums.append(i)
            
            if debug: print(f'{parent}Оригинальное значение байта {test_byte} равно {hex(firmwareOriginal[test_byte])} {INFO} INFO {RST}')
            if debug: print(f'{parent}Начало записи {INFO} INFO {RST}')
            try:
                SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
            except serial.serialutil.SerialException:
                writeResult = 'serial error'
            if setup_sleep > 0: time.sleep(setup_sleep)
            if debug: print(f'{parent}Открыт порт {COM_PORT} {INFO} INFO {RST}')
            if v['password_on']: 
                err = InputPassword(SFP, len(PassAr), PassAr, parent)
                if err != 0: 
                    writeResult = 'password error'
                if debug: print(f'{parent}Пароль {PassAr} успешно введен! {OK} OK {RST}')
            bNum = 0
            delta = 1000/len(firmware)
            writtenBytes = len(firmware)
            for i in range(len(firmware)):
                if not writeOn:
                    break
                else:
                    bNum += 1
                    SFP.write(b'\x0a')
                    if debug: print(f'{parent}Отправка команды 0x0A {INFO} INFO {RST}')
                    SFP.write(b'\x50')
                    if debug: print(f'{parent}Отправлен адрес регистра 0x50 {INFO} INFO {RST}')
                    FlagOk = False
                    while FlagOk == False:
                        err,m = timeoutReadLine(SFP, parent)
                        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                        if err == '{OK} OK {RST}':
                            pass
                        elif err == 'error':
                            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                            writeResult = 'read error 1'
                            return
                        elif err == 'empty':
                            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                            writeResult = 'read error 2'
                            return
                        if m == b'\x99\r\n':
                            if debug: print(f'{parent}Успешно отправлен адрес регистра 0x50 {OK} OK {RST}')
                            FlagOk = True
                    SFP.write(bytes([firmwareNums[i]]))
                    if debug: print(f'{parent}Отправлен адрес смещения {hex(firmwareNums[i])} {INFO} INFO {RST}')
                    FlagOk = False
                    while FlagOk == False:
                        err,m = timeoutReadLine(SFP, parent)
                        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                        if err == '{OK} OK {RST}':
                            pass
                        elif err == 'error':
                            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                            writeResult = 'read error 1'
                            return
                        elif err == 'empty':
                            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                            writeResult = 'read error 2'
                            return
                        if m == b'\x99\r\n':
                            if debug: print(f'{parent}Адрес смещения {hex(firmwareNums[i])} успешно отправлен! {OK} OK {RST}')
                            FlagOk = True
                    SFP.write(bytes([firmware[i]]))
                    if debug: print(f'{parent}Отправлено значение байта {hex(firmware[i])}')
                    FlagOk = False
                    while FlagOk == False:
                        err,m = timeoutReadLine(SFP, parent)
                        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                        if err == '{OK} OK {RST}':
                            pass
                        elif err == 'error':
                            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                            writeResult = 'read error 1'
                            return
                        elif err == 'empty':
                            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                            writeResult = 'read error 2'
                            return
                        if m == b'\x99\r\n':
                            if debug: print(f'{parent}Значение байта {hex(firmware[i])} успешно отправлено! {OK} OK {RST}')
                            FlagOk = True
                    FlagOk = False
                    if debug: print(f'{parent}Проверка записи байта {INFO} INFO {RST}')
                    while FlagOk == False:
                        err,m = timeoutReadLine(SFP, parent)
                        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                        if err == '{OK} OK {RST}':
                            pass
                        elif err == 'error':
                            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                            writeResult = 'read error 1'
                            return
                        elif err == 'empty':
                            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                            writeResult = 'read error 2'
                            return
                        if m == b'\xDD\r\n':
                            if debug: print(f'{parent}Байт {hex(i)} со значением {hex(firmware[i])} успешно записан! {OK} OK {RST}')
                            FlagOk = True
                    writeWindow['write_status'].UpdateBar(bNum*delta)
            current_byte = ReadByte(SFP,bytes([test_byte]),parent)
            if debug: print(f'{parent}Текущее значение байта {test_byte} равно {hex(int.from_bytes(current_byte, "big"))} {INFO} INFO {RST}')
            if debug: print(f'{parent}Оригинальное значение байта {test_byte} равно {hex(firmwareOriginal[test_byte])} {INFO} INFO {RST}')
            if current_byte != bytes([firmwareOriginal[test_byte]]):
                if debug: print(f'{parent}Проверка записи успешна! {OK} OK {RST}')
                writeResult = ''
            else:
                if debug: print(f'{parent}Данные не записаны!!!  {FAIL} FAIL {RST}')
                writeResult = 'write error'
                return
    return
        
def ReadByte(SFP, byte_add, parent):
    parent += 'Чтение Байта: '
    if debug: print(f'{parent}Начало чтения байта {INFO} INFO {RST}')
    SFP.write(b'\x07')
    if debug: print(f'{parent}Отправлена команда 0x07 {INFO} INFO {RST}')
    SFP.write(byte_add)
    if debug: print(f'{parent}Отправлено значение адреса смещения {hex(int.from_bytes(byte_add, "big"))} {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\x99\r\n':
            if debug: print(f'{parent}Значение адреса смещения {hex(int.from_bytes(byte_add, "big"))} успешно отправлено {OK} OK {RST}')
            FlagOk = True
        err,rcv = timeoutReadLine(SFP, parent)
        if debug: (f'{parent}Считано значение {rcv} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {rcv}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
    if debug: print(f'{parent}Считан байт {hex(int.from_bytes(byte_add, "big"))} со значением {hex(int(rcv.decode("utf-8")))} {OK} OK {RST}')
    Dec_b=int(rcv.decode("utf-8"))
    Byte_b=bytes([Dec_b])
    return Byte_b
    
def InputPassword(SFP, sum, val, parent):
    parent+= 'Ввод Пароля: '
    numPass = [123, 124, 125, 126]
    num = []
    for i in range(sum):
        num.append(numPass[i])
    SFP.write(b'\x03')
    if debug: print(f'{parent}Отправлена команда 0x03')
    SFP.write(b'\x00')
    if debug: print(f'{parent}Отправлен адрес регистра 0x00 {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\x99\r\n':
            FlagOk = True
            if debug: print(f'{parent}Успешно отправлен адрес регистра 0x00 {OK} OK {RST}')
    SFP.write(bytes([sum]))
    if debug: print(f'{parent}Отправлено количество байт {sum} {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\x99\r\n':
            FlagOk = True
            if debug: print(f'{parent}Успешная отправка количества байт {hex(sum)} {OK} OK {RST}')
    for i in num:
        SFP.write(bytes([i]))
        if debug: print(f'{parent}Отправка адреса смещения {hex(i)} {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\x99\r\n':
            FlagOk = True
            if debug: print(f'{parent}Успешно отправлен адрес смещения {hex(i)} {OK} OK {RST}')
    for i in val:
        SFP.write(bytes([i]))
        if debug: print(f'{parent}{parent}Отправка значения байта {hex(i)} {INFO} INFO {RST}')
    FlagOk = False
    while FlagOk == False:
        err,m = timeoutReadLine(SFP, parent)
        if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
        if err == '{OK} OK {RST}':
            pass
        elif err == 'error':
            if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
            return 'read error 1'
        elif err == 'empty':
            if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
            return 'read error 2'
        if m == b'\xdd\r\n':
            FlagOk = True
            if debug: print(f'{parent}Успешная отправка значения байта {hex(i)} {OK} OK {RST}')
    if debug: print(f'{parent}Пароль успешно введен! {OK} OK {RST}')
    return 0

def passSel(Passwords, COM_PORT, parent):
    global passSelOn, AcceptPasswd
    parent += 'Подбор Пароля: '
    if debug: print(f'{parent}Начало подбора пароля {INFO} INFO {RST}')
    try:
        SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
    except serial.serialutil.SerialException:
        AcceptPasswd = 'serial error'
        passSelOn = False
        return
    if setup_sleep > 0: time.sleep(setup_sleep)
    if debug: print(f'{parent}Открыт порт {COM_PORT} {INFO} INFO {RST}')
    AcceptPasswd = ''
    num = 0
    cur_byte = ReadByte(SFP, bytes([num]), parent)
    if debug: print(f'{parent}Считано текущее значение байта {num} равное {hex(int.from_bytes(cur_byte, "big"))} {INFO} INFO {RST}')
    val = 0
    if cur_byte != 255:
        val = 255
        
    OrByte = ReadByte(SFP, bytes([num]), parent)
    if debug: print(f'{parent}Оригинольное значение байта {num} равно {hex(int.from_bytes(OrByte, "big"))} {INFO} INFO {RST}')
    PassAr = []
    numPas = 0
    delta = 1000/len(Passwords)
    for Passwd in Passwords:
        if not passSelOn: 
            break
            if debug: print(f'{parent}Подбор пароля остановлен {INFO} INFO {RST}')
        if debug: print(f'{parent}Проверка пароля {Passwd} {INFO} INFO {RST}')
        passwd = Passwd
        numPas += 1
        passelWindow['status'].UpdateBar(numPas*delta)
        PassAr.clear()
        for i in range(math.ceil(len(passwd)/2)):
            PassAr.append(passwd[:2])
            passwd = passwd[2:]
            PassAr[i] = "0x" + PassAr[i]
        for i in range(len(PassAr)):
            PassAr[i] = int(PassAr[i],16)
        err = InputPassword(SFP, len(PassAr), PassAr, parent)
        if err != 0: 
            if debug: print(f'{parent}Ошибка ввода пароля {Passwd}  {FAIL} FAIL {RST}')
            AcceptPasswd = 'password error'
            passSelOn = False
            return
        
        SFP.write(b'\x0a')
        if debug: print(f'{parent}Отправлена команда 0x0A {INFO} INFO {RST}')
        SFP.write(b'\x50')
        if debug: print(f'{parent}Отправлен адрес регистра 0x50 {INFO} INFO {RST}')
        FlagOk = False
        while FlagOk == False:
            err,m = timeoutReadLine(SFP, parent)
            if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
            if err == '{OK} OK {RST}':
                pass
            elif err == 'error':
                if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 1'
                passSelOn = False
                return
            elif err == 'empty':
                if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 2'
                passSelOn = False
                return
            if m == b'\x99\r\n':
                if debug: print(f'{parent}Успешно отправлен адрес регистра 0x50 {OK} OK {RST}')
                FlagOk = True
        SFP.write(bytes([num]))
        if debug: print(f'{parent}Отправлен адрес смещения {num} {INFO} INFO {RST}')
        FlagOk = False
        while FlagOk == False:
            err,m = timeoutReadLine(SFP, parent)
            if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
            if err == '{OK} OK {RST}':
                pass
            elif err == 'error':
                if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 1'
                passSelOn = False
                return
            elif err == 'empty':
                if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 2'
                passSelOn = False
                return
            if m == b'\x99\r\n':
                if debug: print(f'{parent}Адрес смещения {num} успешно отправлен {OK} OK {RST}')
                FlagOk = True
        SFP.write(bytes([val]))
        if debug: print(f'{parent}Отправлено значение байта {hex(val)} {INFO} INFO {RST}')
        FlagOk = False
        while FlagOk == False:
            err,m = timeoutReadLine(SFP, parent)
            if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
            if err == '{OK} OK {RST}':
                pass
            elif err == 'error':
                if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 1'
                passSelOn = False
                return
            elif err == 'empty':
                if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 2'
                passSelOn = False
                return
            if m == b'\x99\r\n':
                if debug: print(f'{parent}Значение байта {hex(val)} успешно отправлено {OK} OK {RST}')
                FlagOk = True
        FlagOk = False
        if debug: print(f'{parent}Проверка записи байта {INFO} INFO {RST}')
        while FlagOk == False:
            err,m = timeoutReadLine(SFP, parent)
            if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
            if err == '{OK} OK {RST}':
                pass
            elif err == 'error':
                if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 1'
                passSelOn = False
                return
            elif err == 'empty':
                if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                AcceptPasswd = 'read error 2'
                passSelOn = False
                return
            if m == b'\xDD\r\n':
                if debug: print(f'{parent}Успешная запись байта! {OK} OK {RST}')
                FlagOk = True
        
        cur_byte = ReadByte(SFP, bytes([num]), parent)
        if debug: print(f'{parent}Считано текущее значение байта {num} равное {hex(int.from_bytes(cur_byte, "big"))} {INFO} INFO {RST}')
        if cur_byte == OrByte:
            if debug: print(f'{parent}Пароль {Passwd} не подошел {INFO} INFO {RST}')
            pass
        else:
            if debug: print(f'{parent}Пароль {Passwd} подошел! {OK} OK {RST}')
            for i in PassAr:
                AcceptPasswd = AcceptPasswd + hex(i)[2:] if i>15 else AcceptPasswd + "0" + hex(i)[2:]
            SFP.write(b'\x0a')
            if debug: print(f'{parent}Восстановление оригинального значения байта {INFO} INFO {RST}')
            if debug: print(f'{parent}Отправлена команда 0x0A {INFO} INFO {RST}')
            SFP.write(b'\x50')
            if debug: print(f'{parent}Отправлен адрес регистра 0x50 {INFO} INFO {RST}')
            FlagOk = False
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 1'
                    passSelOn = False
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 2'
                    passSelOn = False
                    return
                if m == b'\x99\r\n':
                    if debug: print(f'{parent}Успешно отправлен адрес регистра 0x50 {OK} OK {RST}')
                    FlagOk = True
            SFP.write(bytes([num]))
            if debug: print(f'{parent}Отправлен адрес смещения байта {num} {INFO} INFO {RST}')
            FlagOk = False
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 1'
                    passSelOn = False
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 2'
                    passSelOn = False
                    return
                if m == b'\x99\r\n':
                    if debug: print(f'{parent}Успешно отправлен адрес смещения байта {num} {OK} OK {RST}')
                    FlagOk = True
            SFP.write(OrByte)
            if debug: print(f'{parent}Отправка оригинального значения байта {hex(int.from_bytes(cur_byte, "big"))} {INFO} INFO {RST}')
            FlagOk = False
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 1'
                    passSelOn = False
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 2'
                    passSelOn = False
                    return
                if m == b'\x99\r\n':
                    if debug: print(f'{parent}Оригинальное значение байта {hex(int.from_bytes(cur_byte, "big"))} успешно отправлено {OK} OK {RST}')
                    FlagOk = True
            FlagOk = False
            if debug: print(f'{parent}Проверка записи байта {INFO} INFO {RST}')
            while FlagOk == False:
                err,m = timeoutReadLine(SFP, parent)
                if debug: print(f'{parent}Считано значение {m} {INFO} INFO {RST}')
                if err == '{OK} OK {RST}':
                    pass
                elif err == 'error':
                    if debug: print(f'{parent}Ошибка чтения 1. Считано {m}  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 1'
                    passSelOn = False
                    return
                elif err == 'empty':
                    if debug: print(f'{parent}Ошибка чтения 2. Ничегно не считано  {FAIL} FAIL {RST}')
                    AcceptPasswd = 'read error 2'
                    passSelOn = False
                    return
                if m == b'\xDD\r\n':
                    if debug: print(f'{parent}Байт успешно записан! {OK} OK {RST}')
                    FlagOk = True
            break
    SFP.close()
    if debug: print(f'{parent}Найден пароль - {AcceptPasswd} {OK} OK {RST}' if AcceptPasswd != '' else f'Подходящий пароль отсутсвует в списке  {FAIL} FAIL {RST}')
    return 
            

def CRC(data):
    CRC=0
    for byte in data:
        CRC += byte
    CRC = CRC.to_bytes(6,'big')
    return CRC[len(CRC)-1:]
    
def createFirmwareA2h(v):
    firmware = b''
    firmware += de_twos_comp(float(v['A2h_0_1']),16) if v[f'A2h_0_1']!='' else b'\x00\x00'
    firmware += de_twos_comp(float(v['A2h_2_3']),16) if v[f'A2h_2_3']!='' else b'\x00\x00'
    firmware += de_twos_comp(float(v['A2h_4_5']),16) if v[f'A2h_4_5']!='' else b'\x00\x00'
    firmware += de_twos_comp(float(v['A2h_6_7']),16) if v[f'A2h_6_7']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_8_9'])*10**6/100)) if v[f'A2h_8_9']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_10_11'])*10**6/100)) if v[f'A2h_10_11']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_12_13'])*10**6/100)) if v[f'A2h_12_13']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_14_15'])*10**6/100)) if v[f'A2h_14_15']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_16_17'])*10**3/2)) if v[f'A2h_16_17']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_18_19'])*10**3/2)) if v[f'A2h_18_19']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_20_21'])*10**3/2)) if v[f'A2h_20_21']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_22_23'])*10**3/2)) if v[f'A2h_22_23']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_24_25'])*10**3/0.1)) if v[f'A2h_24_25']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_26_27'])*10**3/0.1)) if v[f'A2h_26_27']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_28_29'])*10**3/0.1)) if v[f'A2h_28_29']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_30_31'])*10**3/0.1)) if v[f'A2h_30_31']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_32_33'])*10**3/0.1)) if v[f'A2h_32_33']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_34_35'])*10**3/0.1)) if v[f'A2h_34_35']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_36_37'])*10**3/0.1)) if v[f'A2h_36_37']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_38_39'])*10**3/0.1)) if v[f'A2h_38_39']!='' else b'\x00\x00'
    for i in range(40,56,1):
        firmware += bytes([int(v[f'Table_A2h_{i}'],16)]) if v[f'Table_A2h_{i}']!='' else b'\x00'
    firmware += struct.pack('>f', float(v['A2h_56_59'])) if v[f'A2h_56_59']!='' else b'\x00\x00'
    firmware += struct.pack('>f', float(v['A2h_60_63'])) if v[f'A2h_60_63']!='' else b'\x00\x00'
    firmware += struct.pack('>f', float(v['A2h_64_67'])) if v[f'A2h_64_67']!='' else b'\x00\x00'
    firmware += struct.pack('>f', float(v['A2h_68_71'])) if v[f'A2h_68_71']!='' else b'\x00\x00'
    firmware += struct.pack('>f', float(v['A2h_72_75'])) if v[f'A2h_72_75']!='' else b'\x00\x00'
    firmware += to_slope(float(v['A2h_76_77'])) if v[f'A2h_76_77']!='' else b'\x00\x00'
    firmware += struct.pack('>h', int(v['A2h_78_79'])) if v[f'A2h_78_79']!='' else b'\x00\x00'
    firmware += to_slope(float(v['A2h_80_81'])) if v[f'A2h_80_81']!='' else b'\x00\x00'
    firmware += struct.pack('>h', int(v['A2h_82_83'])) if v[f'A2h_82_83']!='' else b'\x00\x00'
    firmware += to_slope(float(v['A2h_84_85'])) if v[f'A2h_84_85']!='' else b'\x00\x00'
    firmware += struct.pack('>h', int(v['A2h_86_87'])) if v[f'A2h_86_87']!='' else b'\x00\x00'
    firmware += to_slope(float(v['A2h_88_89'])) if v[f'A2h_88_89']!='' else b'\x00\x00'
    firmware += struct.pack('>h', int(v['A2h_90_91'])) if v[f'A2h_90_91']!='' else b'\x00\x00'
    firmware += bytes([int(v[f'Table_A2h_92'],16)]) if v[f'Table_A2h_92']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_93'],16)]) if v[f'Table_A2h_93']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_94'],16)]) if v[f'Table_A2h_94']!='' else b'\x00'
    firmware += CRC(firmware)
    firmware += de_twos_comp(float(v['A2h_96_97']),16) if v[f'A2h_96_97']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_98_99'])*10**6/100)) if v[f'A2h_98_99']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_100_101'])*10**3/2)) if v[f'A2h_100_101']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_102_103'])*10**3/0.1)) if v[f'A2h_102_103']!='' else b'\x00\x00'
    firmware += struct.pack('>H', int(float(v['A2h_104_105'])*10**3/0.1)) if v[f'A2h_104_105']!='' else b'\x00\x00'
    firmware += bytes([int(v[f'Table_A2h_106'],16)]) if v[f'Table_A2h_106']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_107'],16)]) if v[f'Table_A2h_107']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_108'],16)]) if v[f'Table_A2h_108']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_109'],16)]) if v[f'Table_A2h_109']!='' else b'\x00'
    
    stateByte = []
    stateBitNums = [6,3]
    if v['laser_off']: stateByte.append(6) 
    if v['soft_rs0']: stateByte.append(3) 
    stateByte_b = bitsDetect(int(v['Table_A2h_110'],16)) if v['Table_A2h_110'] != '' else []
    for bit in stateBitNums:
        if (bit in stateByte) and (bit not in stateByte_b):
            stateByte_b.append(bit) 
        elif (bit in stateByte_b) and (bit not in stateByte):
            stateByte_b.remove(bit)
    firmware += bytes([bitsConvert(stateByte_b)])
        
    firmware += bytes([int(v[f'Table_A2h_111'],16)]) if v[f'Table_A2h_111']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_112'],16)]) if v[f'Table_A2h_112']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_113'],16)]) if v[f'Table_A2h_113']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_114'],16)]) if v[f'Table_A2h_114']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_115'],16)]) if v[f'Table_A2h_115']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_116'],16)]) if v[f'Table_A2h_116']!='' else b'\x00'
    firmware += bytes([int(v[f'Table_A2h_117'],16)]) if v[f'Table_A2h_117']!='' else b'\x00'
    
    stateByte = []
    stateBitNums = [7,6,5,4,3,2,0]
    if v['reserved_118_7']: stateByte.append(7) 
    if v['reserved_118_6']: stateByte.append(6) 
    if v['reserved_118_5']: stateByte.append(5) 
    if v['reserved_118_4']: stateByte.append(4) 
    if v['soft_rs1']: stateByte.append(3) 
    if v['reserved_118_2']: stateByte.append(2) 
    if v['power_level_2']: stateByte.append(0)
    stateByte_b = bitsDetect(int(v['Table_A2h_118'],16)) if v['Table_A2h_118'] != '' else []
    for bit in stateBitNums:
        if (bit in stateByte) and (bit not in stateByte_b):
            stateByte_b.append(bit) 
        elif (bit in stateByte_b) and (bit not in stateByte):
            stateByte_b.remove(bit) 
    firmware += bytes([bitsConvert(stateByte_b)])
    
    firmware += bytes([int(v[f'Table_A2h_119'],16)]) if v[f'Table_A2h_119']!='' else b'\x00'
    firmware += bytes([int(v[f'A2h_120'],16)]) if v[f'A2h_120']!='' else b'\x00'
    firmware += bytes([int(v[f'A2h_121'],16)]) if v[f'A2h_121']!='' else b'\x00'
    firmware += bytes([int(v[f'A2h_122'],16)]) if v[f'A2h_122']!='' else b'\x00'
    firmware += bytes([int(v[f'pass_1'],16)]) if v[f'pass_1']!='' else b'\x00'
    firmware += bytes([int(v[f'pass_2'],16)]) if v[f'pass_2']!='' else b'\x00'
    firmware += bytes([int(v[f'pass_3'],16)]) if v[f'pass_3']!='' else b'\x00'
    firmware += bytes([int(v[f'pass_4'],16)]) if v[f'pass_4']!='' else b'\x00'
    firmware += bytes([int(v[f'A2h_127'],16)]) if v[f'A2h_127']!='' else b'\x00'
    for i in range(128,256,1):
        firmware += bytes([int(v[f'Table_A2h_{i}'],16)]) if v[f'Table_A2h_{i}']!='' else b'\x00'
    # with open('Test.bin','w+b') as test_bin:
        # test_bin.write(firmware)
    return firmware
    
def detectFirmwareA2h(v):
    data_byte = b''
    for i in range(256):
        data_byte += bytes([int(v[f'Table_A2h_{i}'],16)]) if v[f'Table_A2h_{i}']!='' else b'\x00'
    editorWindow['A2h_0_1'].update(value=twos_comp(int(data_byte[:2].hex(),16),16))
    editorWindow['A2h_2_3'].update(value=twos_comp(int(data_byte[2:4].hex(),16),16))
    editorWindow['A2h_4_5'].update(value=twos_comp(int(data_byte[4:6].hex(),16),16))
    editorWindow['A2h_6_7'].update(value=twos_comp(int(data_byte[6:8].hex(),16),16))
    editorWindow['A2h_8_9'].update(value=round(struct.unpack('>H', data_byte[8:10])[0]*100*10**-6, 4))
    editorWindow['A2h_10_11'].update(value=round(struct.unpack('>H', data_byte[10:12])[0]*100*10**-6, 4))
    editorWindow['A2h_12_13'].update(value=round(struct.unpack('>H', data_byte[12:14])[0]*100*10**-6, 4))
    editorWindow['A2h_14_15'].update(value=round(struct.unpack('>H', data_byte[14:16])[0]*100*10**-6, 4))
    editorWindow['A2h_16_17'].update(value=round(struct.unpack('>H', data_byte[16:18])[0]*2*10**-3, 4))
    editorWindow['A2h_18_19'].update(value=round(struct.unpack('>H', data_byte[18:20])[0]*2*10**-3, 4))
    editorWindow['A2h_20_21'].update(value=round(struct.unpack('>H', data_byte[20:22])[0]*2*10**-3, 4))
    editorWindow['A2h_22_23'].update(value=round(struct.unpack('>H', data_byte[22:24])[0]*2*10**-3, 4))
    editorWindow['A2h_24_25'].update(value=round(struct.unpack('>H', data_byte[24:26])[0]*0.1*10**-3, 4))
    editorWindow['A2h_26_27'].update(value=round(struct.unpack('>H', data_byte[26:28])[0]*0.1*10**-3, 4))
    editorWindow['A2h_28_29'].update(value=round(struct.unpack('>H', data_byte[28:30])[0]*0.1*10**-3, 4))
    editorWindow['A2h_30_31'].update(value=round(struct.unpack('>H', data_byte[30:32])[0]*0.1*10**-3, 4))
    editorWindow['A2h_32_33'].update(value=round(struct.unpack('>H', data_byte[32:34])[0]*0.1*10**-3, 4))
    editorWindow['A2h_34_35'].update(value=round(struct.unpack('>H', data_byte[34:36])[0]*0.1*10**-3, 4))
    editorWindow['A2h_36_37'].update(value=round(struct.unpack('>H', data_byte[36:38])[0]*0.1*10**-3, 4))
    editorWindow['A2h_38_39'].update(value=round(struct.unpack('>H', data_byte[38:40])[0]*0.1*10**-3, 4))
    
    editorWindow['A2h_56_59'].update(value=struct.unpack('>f',data_byte[56:60])[0])
    editorWindow['A2h_60_63'].update(value=struct.unpack('>f',data_byte[60:64])[0])
    editorWindow['A2h_64_67'].update(value=struct.unpack('>f',data_byte[64:68])[0])
    editorWindow['A2h_68_71'].update(value=struct.unpack('>f',data_byte[68:72])[0])
    editorWindow['A2h_72_75'].update(value=struct.unpack('>f',data_byte[72:76])[0])
    
    editorWindow['A2h_76_77'].update(value=from_slope(data_byte[76:78]))
    editorWindow['A2h_78_79'].update(value=struct.unpack('>h',data_byte[78:80])[0])
    editorWindow['A2h_80_81'].update(value=from_slope(data_byte[80:82]))
    editorWindow['A2h_82_83'].update(value=struct.unpack('>h',data_byte[82:84])[0])
    editorWindow['A2h_84_85'].update(value=from_slope(data_byte[84:86]))
    editorWindow['A2h_86_87'].update(value=struct.unpack('>h',data_byte[86:88])[0])
    editorWindow['A2h_88_89'].update(value=from_slope(data_byte[88:90]))
    editorWindow['A2h_90_91'].update(value=struct.unpack('>h',data_byte[90:92])[0])
    
    editorWindow['A2h_95'].update(value=hex(data_byte[95])[2:].upper())
    
    editorWindow['A2h_96_97'].update(value=twos_comp(int(data_byte[96:98].hex(),16),16))
    editorWindow['A2h_98_99'].update(value=round(struct.unpack('>H', data_byte[98:100])[0]*100*10**-6, 4))
    editorWindow['A2h_100_101'].update(value=round(struct.unpack('>H', data_byte[100:102])[0]*2*10**-3, 4))
    editorWindow['A2h_102_103'].update(value=round(struct.unpack('>H', data_byte[102:104])[0]*0.1*10**-3, 4))
    editorWindow['A2h_104_105'].update(value=round(struct.unpack('>H', data_byte[104:106])[0]*0.1*10**-3, 4))
    
    warningByte1 = bitsDetect(data_byte[116])
    warningByte2 = bitsDetect(data_byte[117])
    alarmByte1 = bitsDetect(data_byte[112])
    alarmByte2 = bitsDetect(data_byte[113])
    editorWindow['hi_temp'].update(text_color="#FF0000") if 7 in alarmByte1 else editorWindow['hi_temp'].update(text_color="#FF8C00") if 7 in warningByte1 else editorWindow['hi_temp'].update(text_color="#008000")
    editorWindow['lo_temp'].update(text_color="#FF0000") if 6 in alarmByte1 else editorWindow['lo_temp'].update(text_color="#FF8C00") if 6 in warningByte1 else editorWindow['lo_temp'].update(text_color="#008000")
    editorWindow['hi_voltage'].update(text_color="#FF0000") if 5 in alarmByte1 else editorWindow['hi_voltage'].update(text_color="#FF8C00") if 5 in warningByte1 else editorWindow['hi_voltage'].update(text_color="#008000")
    editorWindow['lo_voltage'].update(text_color="#FF0000") if 4 in alarmByte1 else editorWindow['lo_voltage'].update(text_color="#FF8C00") if 4 in warningByte1 else editorWindow['lo_voltage'].update(text_color="#008000")
    editorWindow['hi_amp'].update(text_color="#FF0000") if 3 in alarmByte1 else editorWindow['hi_amp'].update(text_color="#FF8C00") if 3 in warningByte1 else editorWindow['hi_amp'].update(text_color="#008000")
    editorWindow['lo_amp'].update(text_color="#FF0000") if 2 in alarmByte1 else editorWindow['lo_amp'].update(text_color="#FF8C00") if 2 in warningByte1 else editorWindow['lo_amp'].update(text_color="#008000")
    editorWindow['hi_tx_power'].update(text_color="#FF0000") if 1 in alarmByte1 else editorWindow['hi_tx_power'].update(text_color="#FF8C00") if 1 in warningByte1 else editorWindow['hi_tx_power'].update(text_color="#008000")
    editorWindow['lo_tx_power'].update(text_color="#FF0000") if 0 in alarmByte1 else editorWindow['lo_tx_power'].update(text_color="#FF8C00") if 0 in warningByte1 else editorWindow['lo_tx_power'].update(text_color="#008000")
    editorWindow['hi_rx_power'].update(text_color="#FF0000") if 7 in alarmByte2 else editorWindow['lo_rx_power'].update(text_color="#FF8C00") if 7 in warningByte2 else editorWindow['hi_rx_power'].update(text_color="#008000")
    editorWindow['lo_rx_power'].update(text_color="#FF0000") if 6 in alarmByte2 else editorWindow['lo_rx_power'].update(text_color="#FF8C00") if 6 in warningByte2 else editorWindow['lo_rx_power'].update(text_color="#008000")
    
    stateByte = bitsDetect(data_byte[110])
    stateByte2 = bitsDetect(data_byte[118])
    editorWindow['laser_state'].update(value='ВЫКЛ', text_color="#FF0000") if 7 in stateByte else editorWindow['laser_state'].update(value='ВКЛ', text_color="#008000") 
    editorWindow['rs1_state'].update(value='ВКЛ', text_color="#008000") if 5 in stateByte else editorWindow['rs1_state'].update(value='ВЫКЛ', text_color="#FF0000")
    editorWindow['rs0_state'].update(value='ВКЛ', text_color="#008000") if 4 in stateByte else editorWindow['rs0_state'].update(value='ВЫКЛ', text_color="#FF0000")
    editorWindow['tx_fault'].update(value='FAULT', text_color="#FF0000") if 2 in stateByte else editorWindow['tx_fault'].update(value='OK', text_color="#008000")     
    editorWindow['los'].update(value='FAULT', text_color="#FF0000") if 1 in stateByte else editorWindow['los'].update(value='OK', text_color="#008000") 
    editorWindow['data_ready'].update(value='OK', text_color="#008000") if 0 in stateByte else editorWindow['data_ready'].update(value='FAULT', text_color="#FF0000") 
    editorWindow['power_levwl_state'].update(value='1.5 Вт', text_color="#000000") if 1 in stateByte2 else editorWindow['power_levwl_state'].update(value='1.0 Вт', text_color="#000000") 
    
    editorWindow['laser_off'].update(value=True) if 6 in stateByte else editorWindow['laser_off'].update(value=False)
    editorWindow['soft_rs0'].update(value=True) if 3 in stateByte else editorWindow['soft_rs0'].update(value=False)
    editorWindow['soft_rs1'].update(value=True) if 3 in stateByte2 else editorWindow['soft_rs1'].update(value=False)
    editorWindow['power_level_2'].update(value=True) if 0 in stateByte2 else editorWindow['power_level_1'].update(value=True) 
    editorWindow['reserved_118_7'].update(value=True) if 7 in stateByte2 else editorWindow['reserved_118_7'].update(value=False)
    editorWindow['reserved_118_6'].update(value=True) if 6 in stateByte2 else editorWindow['reserved_118_6'].update(value=False)
    editorWindow['reserved_118_5'].update(value=True) if 5 in stateByte2 else editorWindow['reserved_118_5'].update(value=False)
    editorWindow['reserved_118_4'].update(value=True) if 4 in stateByte2 else editorWindow['reserved_118_4'].update(value=False)
    editorWindow['reserved_118_2'].update(value=True) if 2 in stateByte2 else editorWindow['reserved_118_2'].update(value=False)
    
    editorWindow['A2h_120'].update(value=hex(data_byte[120])[2:].upper()) 
    editorWindow['A2h_121'].update(value=hex(data_byte[121])[2:].upper()) 
    editorWindow['A2h_122'].update(value=hex(data_byte[122])[2:].upper()) 
    editorWindow['pass_1'].update(value=hex(data_byte[123])[2:].upper()) 
    editorWindow['pass_2'].update(value=hex(data_byte[124])[2:].upper()) 
    editorWindow['pass_3'].update(value=hex(data_byte[125])[2:].upper()) 
    editorWindow['pass_4'].update(value=hex(data_byte[126])[2:].upper()) 
    editorWindow['A2h_127'].update(value=hex(data_byte[127])[2:].upper()) 
    editorWindow['A2h_111'].update(value=hex(data_byte[111])[2:].upper()) 

def openA2hBIN(data_byte):
    i = 0
    for byte in data_byte:
        editorWindow[f'Table_A2h_{i}'].update(value=hex(byte)[2:].upper())
        i+=1

def saveA2hBIN(v):
    firmware = b''
    for i in range(256):
        if i == 95:
            firmware += CRC(firmware)
        else:
            firmware += bytes([int(v[f'Table_A2h_{i}'],16)]) if v[f'Table_A2h_{i}']!='' else b'\x00'
    return firmware    

def openBIN(data_byte):
    for i in range(96,256,1):
        editorWindow[f'A0h_{i}'].update(value='')
    editorWindow['A0h_0'].update(set_to_index = [k0.index(data_byte[0])])
    editorWindow['A0h_1'].update(set_to_index= [k1.index(data_byte[1])])
    editorWindow['A0h_2'].update(set_to_index= [k2.index(data_byte[2])])
    editorWindow['A0h_3[0]'].update(set_to_index= [k3_0.index(x) for x in bitsDetect(data_byte[3]) if x>3])
    editorWindow['A0h_3[1]'].update(set_to_index= [k3_1.index(x) for x in bitsDetect(data_byte[3]) if x<4])
    editorWindow['A0h_4'].update(set_to_index= [k4.index(x) for x in bitsDetect(data_byte[4])])
    editorWindow['A0h_5'].update(set_to_index= [k5.index(x) for x in bitsDetect(data_byte[5])])
    editorWindow['A0h_6'].update(set_to_index= [k6.index(x) for x in bitsDetect(data_byte[6])])
    editorWindow['A0h_7[0]'].update(set_to_index= [k7_0.index(x) for x in bitsDetect(data_byte[7]) if x>2])
    editorWindow['A0h_7[1]'].update(set_to_index= [k7_1.index(x) for x in bitsDetect(data_byte[7]) if x<3] + [k7_1.index(x) for x in bitsDetect(data_byte[8]) if x>3])
    editorWindow['A0h_8[1]'].update(set_to_index= [k8_1.index(x) for x in bitsDetect(data_byte[8]) if x<4])
    editorWindow['A0h_9'].update(set_to_index= [k9.index(x) for x in bitsDetect(data_byte[9])])
    editorWindow['A0h_10'].update(set_to_index= [k10.index(x) for x in bitsDetect(data_byte[10])])
    editorWindow['A0h_11'].update(set_to_index= [k11.index(data_byte[11])])
    editorWindow['A0h_13'].update(set_to_index= [k13.index(data_byte[13])])
    editorWindow['A0h_64'].update(set_to_index= [k64.index(x) for x in bitsDetect(data_byte[64])])
    editorWindow['A0h_65'].update(set_to_index= [k65.index(x) for x in bitsDetect(data_byte[65])])
    editorWindow['A0h_92'].update(set_to_index= [k92.index(x) for x in bitsDetect(data_byte[92])])
    editorWindow['A0h_93'].update(set_to_index= [k93.index(x) for x in bitsDetect(data_byte[93])])
    editorWindow['A0h_94'].update(set_to_index= [k94.index(data_byte[94])])
    editorWindow['A0h_12'].update(value=data_byte[12])
    editorWindow['A0h_66'].update(value=data_byte[66])
    editorWindow['A0h_67'].update(value=data_byte[67])
    editorWindow['A0h_14'].update(value=data_byte[14])
    editorWindow['A0h_15'].update(value=data_byte[15])
    editorWindow['A0h_16'].update(value=data_byte[16])
    editorWindow['A0h_17'].update(value=data_byte[17])
    editorWindow['A0h_18'].update(value=data_byte[18])
    editorWindow['A0h_19'].update(value=data_byte[19])
    editorWindow['A0h_60&A0h_61'].update(value=int.from_bytes(data_byte[60:62], 'big'))
    editorWindow['A0h_63'].update(value=hex(data_byte[63])[2:].upper() if len(hex(data_byte[63])[2:])>1 else '0'+hex(data_byte[63])[2:].upper())
    editorWindow['A0h_95'].update(value=hex(data_byte[95])[2:].upper() if len(hex(data_byte[95])[2:])>1 else '0'+hex(data_byte[95])[2:].upper())
    editorWindow['A0h_vendorName'].update(value=data_byte[20:36].decode('cp1251').strip())
    editorWindow['A0h_36'].update(value=data_byte[36])
    editorWindow['A0h_62'].update(value=data_byte[62])
    editorWindow['A0h_vendorOUI_1'].update(value=hex(data_byte[37])[2:].upper() if len(hex(data_byte[37])[2:])>1 else '0'+hex(data_byte[37])[2:].upper())
    editorWindow['A0h_vendorOUI_2'].update(value=hex(data_byte[38])[2:].upper() if len(hex(data_byte[38])[2:])>1 else '0'+hex(data_byte[38])[2:].upper())
    editorWindow['A0h_vendorOUI_3'].update(value=hex(data_byte[39])[2:].upper() if len(hex(data_byte[39])[2:])>1 else '0'+hex(data_byte[39])[2:].upper())
    editorWindow['A0h_vendorPN'].update(value=data_byte[40:56].decode('cp1251').strip())
    editorWindow['A0h_vendorRev'].update(value=data_byte[56:60].decode('cp1251').strip())
    editorWindow['A0h_vendorSN'].update(value=data_byte[68:84].decode('cp1251').strip())
    editorWindow['A0h_year'].update(value=data_byte[84:86].decode('cp1251').strip() if data_byte[84:86] != b'\x00\x00' else '0')
    editorWindow['A0h_month'].update(value=data_byte[86:88].decode('cp1251').strip() if data_byte[86:88] != b'\x00\x00' else '0')
    editorWindow['A0h_day'].update(value=data_byte[88:90].decode('cp1251').strip() if data_byte[88:90] != b'\x00\x00' else '0')
    editorWindow['A0h_vSpec'].update(value=data_byte[90:92].decode('cp1251').strip() if data_byte[90:92] != b'\x00\x00' else '0')
    
    for i in range(96,len(data_byte),1):
        editorWindow[f'A0h_{i}'].update(value=hex(data_byte[i])[2:].upper() if len(hex(data_byte[i])[2:])==2 else '0'+hex(data_byte[i])[2:].upper())
    for i in range(96,len(data_byte),16):
        b_val = ''
        for x in data_byte[i:i+16]:
            try:
                x_char = bytes([x]).decode('cp1251') if x != 0 else ' '
            except ValueError:
                x_char = ' '
            if x_char == '': x_char = ' '
            b_val += x_char
        editorWindow[f'A0h_text_{i}'].update(value=b_val)

    pid = data_byte[192:212]
    vid = data_byte[148:152]
    editorWindow['A0h_cisco_pid'].update(value=pid.decode('cp1251'))
    v['A0h_cisco_pid'] = pid.decode('cp1251')
    editorWindow['A0h_cisco_vid'].update(value=vid.decode('cp1251'))
    v['A0h_cisco_vid'] = vid.decode('cp1251')
    sfp_type = int.from_bytes(data_byte[96:98], 'big')
    vendor_id = data_byte[98]
    try:
        editorWindow['A0h_cisco_sfp_type'].update(value=cisco_sfp_type[toHexKey(sfp_type,4)])
    except:
        editorWindow['A0h_cisco_sfp_type'].update(value='')
    try:
        editorWindow['A0h_cisco_vendor_id'].update(value=cisco_vendor_id[toHexKey(vendor_id,2)])
    except:
        editorWindow['A0h_cisco_vendor_id'].update(value='')

def saveBIN(v):
    firmware = b''
    firmware += bytes([k0[v0.index(v['A0h_0'][0])] if len(v['A0h_0']) > 0 else 0])
    firmware += bytes([k1[v1.index(v['A0h_1'][0])] if len(v['A0h_1']) > 0 else 0])
    firmware += bytes([k2[v2.index(v['A0h_2'][0])] if len(v['A0h_2']) > 0 else 0])
    firmware += bytes([bitsConvert([k3_0[v3_0.index(x)] for x in v['A0h_3[0]']]+[k3_1[v3_1.index(x)] for x in v['A0h_3[1]']])])
    firmware += bytes([bitsConvert([k4[v4.index(x)] for x in v['A0h_4']])])
    firmware += bytes([bitsConvert([k5[v5.index(x)] for x in v['A0h_5']])])
    firmware += bytes([bitsConvert([k6[v6.index(x)] for x in v['A0h_6']])])
    firmware += bytes([bitsConvert([k7_0[v7_0.index(x)] for x in v['A0h_7[0]']] + [k7_1[v7_1.index(x)] for x in v['A0h_7[1]'] if k7_1[v7_1.index(x)] < 3])])
    firmware += bytes([bitsConvert([k8_1[v8_1.index(x)] for x in v['A0h_8[1]']] + [k7_1[v7_1.index(x)] for x in v['A0h_7[1]'] if k7_1[v7_1.index(x)] > 2])])
    firmware += bytes([bitsConvert([k9[v9.index(x)] for x in v['A0h_9']])])
    firmware += bytes([bitsConvert([k10[v10.index(x)] for x in v['A0h_10']])])
    firmware += bytes([k11[v11.index(v['A0h_11'][0])] if len(v['A0h_11']) > 0 else 0])
    firmware += bytes([int(v['A0h_12']) if v['A0h_12'] != '' else 0])
    firmware += bytes([k13[v13.index(v['A0h_13'][0])] if len(v['A0h_13']) > 0 else 0])
    firmware += bytes([int(v['A0h_14']) if v['A0h_14'] != '' else 0])
    firmware += bytes([int(v['A0h_15']) if v['A0h_15'] != '' else 0])
    firmware += bytes([int(v['A0h_16']) if v['A0h_16'] != '' else 0])
    firmware += bytes([int(v['A0h_17']) if v['A0h_17'] != '' else 0])
    firmware += bytes([int(v['A0h_18']) if v['A0h_18'] != '' else 0])
    firmware += bytes([int(v['A0h_19']) if v['A0h_19'] != '' else 0])
    vName = v['A0h_vendorName'].strip() if len(v['A0h_vendorName'].strip()) == 16 else v['A0h_vendorName'].strip() + (' ' * (16-len(v['A0h_vendorName'].strip()))) if len(v['A0h_vendorName'].strip()) < 16 else v['A0h_vendorName'].strip()[:16]
    vOUI = bytes([int(v['A0h_vendorOUI_1'].strip(),16) if v['A0h_vendorOUI_1'].strip() != '' and ishexdigit(v['A0h_vendorOUI_1'].strip()) and int(v['A0h_vendorOUI_1'].strip(),16) <= 255 else 0,\
        int(v['A0h_vendorOUI_2'].strip(),16) if v['A0h_vendorOUI_2'].strip() != '' and ishexdigit(v['A0h_vendorOUI_2'].strip()) and int(v['A0h_vendorOUI_2'].strip(),16) <= 255 else 0,\
        int(v['A0h_vendorOUI_3'].strip(),16) if v['A0h_vendorOUI_3'].strip() != '' and ishexdigit(v['A0h_vendorOUI_3'].strip()) and int(v['A0h_vendorOUI_3'].strip(),16) <= 255 else 0]) 
    vPN = v['A0h_vendorPN'].strip() if len(v['A0h_vendorPN'].strip()) == 16 else v['A0h_vendorPN'].strip() + (' ' * (16-len(v['A0h_vendorPN'].strip()))) if len(v['A0h_vendorPN'].strip()) < 16 else v['A0h_vendorPN'].strip()[:16]
    vRev = v['A0h_vendorRev'].strip() if len(v['A0h_vendorRev'].strip()) == 4 else v['A0h_vendorRev'].strip() + (' ' * (4-len(v['A0h_vendorRev'].strip()))) if len(v['A0h_vendorRev'].strip()) < 4 else v['A0h_vendorRev'].strip()[:4]
    firmware += vName.encode('cp1251') + bytes([int(v['A0h_36']) if v['A0h_36'] != '' else 0]) + vOUI + vPN.encode('cp1251') + vRev.encode('cp1251')
    firmware += int(v['A0h_60&A0h_61'].strip()).to_bytes(2,'big') if v['A0h_60&A0h_61'].strip() != '' else b'\x00\x00'
    firmware += bytes([int(v['A0h_62']) if v['A0h_62'] != '' else 0])
    firmware += CRC(firmware)
    firmware += bytes([bitsConvert([k64[v64.index(x)] for x in v['A0h_64']])])
    firmware += bytes([bitsConvert([k65[v65.index(x)] for x in v['A0h_65']])])
    firmware += bytes([int(v['A0h_66']) if v['A0h_66'] != '' else 0])
    firmware += bytes([int(v['A0h_67']) if v['A0h_67'] != '' else 0])
    vSN = v['A0h_vendorSN'].strip() if len(v['A0h_vendorSN'].strip()) == 16 else v['A0h_vendorSN'].strip() + (' ' * (16-len(v['A0h_vendorSN'].strip()))) if len(v['A0h_vendorSN'].strip()) < 16 else v['A0h_vendorSN'].strip()[:16]
    firmware += vSN.encode('cp1251')
    year = v['A0h_year'].strip() if len(v['A0h_year'].strip()) > 1 else '0'+v['A0h_year'].strip() if len(v['A0h_year'].strip()) > 0 else '00'
    month = v['A0h_month'].strip() if len(v['A0h_month'].strip()) > 1 else '0'+v['A0h_month'].strip() if len(v['A0h_month'].strip()) > 0 else '00'
    day = v['A0h_day'].strip() if len(v['A0h_day'].strip()) > 1 else '0'+v['A0h_day'].strip() if len(v['A0h_day'].strip()) > 0 else '00'
    vSpec = '  ' if v['A0h_vSpec'].strip() == '' else v['A0h_vSpec'].strip() if len(v['A0h_vSpec'].strip()) > 1 else '0'+v['A0h_vSpec'].strip() if len(v['A0h_vSpec'].strip()) > 0 else '00'
    firmware += year.encode('cp1251') + month.encode('cp1251') + day.encode('cp1251') + vSpec.encode('cp1251')
    firmware += bytes([bitsConvert([k92[v92.index(x)] for x in v['A0h_92']])])
    firmware += bytes([bitsConvert([k93[v93.index(x)] for x in v['A0h_93']])])
    firmware += bytes([k94[v94.index(v['A0h_94'][0])] if len(v['A0h_94']) > 0 else 0])
    firmware += CRC(firmware[64:])
    if v['A0h_cisco_adapt_enable']:
        # global A0h_cisco_sfp_type, A0h_cisco_vendor_id, A0h_cisco_pid, A0h_cisco_vid, A0h_vendorName, A0h_vendorSN, A0h_cisco_security_key, A0h_cisco_key, A0h_slip, A0h_cisco_crc32
        A0h_cisco_sfp_type = b'\x00\x00' if v['A0h_cisco_sfp_type'] == '' else int(A0h_cisco_sfp_type_key[A0h_cisco_sfp_type_val.index(v['A0h_cisco_sfp_type'])],0).to_bytes(2,'big')
        A0h_cisco_vendor_id = b'\x02' if v['A0h_cisco_vendor_id'] == '' else int(A0h_cisco_vendor_id_key[A0h_cisco_vendor_id_val.index(v['A0h_cisco_vendor_id'])],0).to_bytes(1,'big')
        A0h_cisco_pid = b'\x20'*20 if v['A0h_cisco_pid'] == '' else v['A0h_cisco_pid'].encode('cp1251') if len(v['A0h_cisco_pid']) == 20 else v['A0h_cisco_pid'].encode('cp1251')+b'\x20'*(20-len(v['A0h_cisco_pid'])) if len(v['A0h_cisco_pid']) < 20 else v['A0h_cisco_pid'][:20].encode('cp1251')
        A0h_cisco_vid = b'\x20'*4 if v['A0h_cisco_vid'] == '' else v['A0h_cisco_vid'].encode('cp1251') if len(v['A0h_cisco_vid']) == 4 else v['A0h_cisco_vid'].encode('cp1251')+b'\x20'*(4-len(v['A0h_cisco_vid'])) if len(v['A0h_cisco_vid']) < 4 else v['A0h_cisco_vid'][:4].encode('cp1251')
        A0h_vendorName = b'\x20'*16 if v['A0h_vendorName'] == '' else v['A0h_vendorName'].encode('cp1251') if len(v['A0h_vendorName']) == 16 else v['A0h_vendorName'].encode('cp1251')+b'\x20'*(16-len(v['A0h_vendorName'])) if len(v['A0h_vendorName']) < 16 else v['A0h_vendorName'][:16].encode('cp1251')
        A0h_vendorSN = b'\x20'*16 if v['A0h_vendorSN'] == '' else v['A0h_vendorSN'].encode('cp1251') if len(v['A0h_vendorSN']) == 16 else v['A0h_vendorSN'].encode('cp1251')+b'\x20'*(16-len(v['A0h_vendorSN'])) if len(v['A0h_vendorSN']) < 16 else v['A0h_vendorSN'][:16].encode('cp1251')
        A0h_cisco_security_key = bytes.fromhex(cisco_security_key[toHexKey(int.from_bytes(A0h_cisco_vendor_id, 'big'),2)])
        A0h_cisco_key = bytes.fromhex(md5(A0h_cisco_vendor_id+A0h_vendorName+A0h_vendorSN+A0h_cisco_security_key).hexdigest())
        A0h_cisco_slip = b''
        for x in range(115,124,1):
            A0h_cisco_slip += b'\x00'#bytes([int(v[f'A0h_{x}'][:2],16)])
        A0h_cisco_crc32 = crc32(A0h_cisco_sfp_type+A0h_cisco_vendor_id+A0h_cisco_key+A0h_cisco_slip).to_bytes(4,'little')
        firmware += A0h_cisco_sfp_type+A0h_cisco_vendor_id+A0h_cisco_key+A0h_cisco_slip+A0h_cisco_crc32

        otherBytes = b''
        for i in range(128,148,1):
            try:
                otherBytes += bytes([int(v[f'A0h_{i}'][:2],16)])
            except ValueError:
                otherBytes += b'\x00'
        firmware += otherBytes
        firmware += A0h_cisco_vid
        otherBytes = b''
        for i in range(152,192,1):
            try:
                otherBytes += bytes([int(v[f'A0h_{i}'][:2],16)])
            except ValueError:
                otherBytes += b'\x00'
        firmware += otherBytes
        firmware += A0h_cisco_pid
        otherBytes = b''
        for i in range(212,sfp_bytes_len,1):
            try:
                otherBytes += bytes([int(v[f'A0h_{i}'][:2],16)]) 
            except ValueError:
                otherBytes += b'\x00'
        firmware += otherBytes
    elif v['A0h_juniper_adapt_enable']:
        A0h_juniper_pn = v['A0h_juniper_pn'].encode('cp1251')
        A0h_juniper_rev = v['A0h_juniper_rev'].encode('cp1251')
        A0h_juniper_slip1 = b'\x20' * 15
        A0h_juniper_slip2 = b''
        for i in range(128,sfp_bytes_len,1):
            try:
                A0h_juniper_slip2 += bytes([int(v[f'A0h_{i}'][:2],16)])
            except ValueError:
                A0h_juniper_slip2 += b'\x00'
        firmware += A0h_juniper_pn + A0h_juniper_rev + A0h_juniper_slip1 + A0h_juniper_slip2
    else:
        otherBytes = b''
        for i in range(96,sfp_bytes_len,1):
            try:
                otherBytes += bytes([int(v[f'A0h_{i}'][:2],16)])
            except ValueError:
                otherBytes += b'\x00'
        firmware += otherBytes
    return firmware

def updUTF8(v, nn):
    n_text = int((nn-96)/16//1) + 96 + (15*int((nn-96)/16//1))
    n_char = int((nn-96)/16%1*16)
    try:
        cell_char = bytes([int(v[f'A0h_{nn}'][:2],16)]).decode('cp1251') if int(v[f'A0h_{nn}'][:2],16) != 0 else ' '
    except ValueError:
        cell_char = ' '
    cell_char = cell_char if cell_char != '' else ' '
    text_string = v[f'A0h_text_{n_text}']
    text_string = 16*' ' if text_string == '' else text_string
    text_string = text_string[:n_char] + cell_char + text_string[n_char+1:]
    editorWindow[f'A0h_text_{n_text}'].update(value=text_string)

    # for i in range(96,sfp_bytes_len,1):
    #     try:
    #         otherBytes += bytes([int(v[f'A0h_{i}'][:2],16)])
    #     except ValueError:
    #         otherBytes += b'\x00'
    # for i in range(96,len(otherBytes),16):
    #     b_val = ''
    #     for x in otherBytes[i-96:i+16]:
    #         b_val += bytes([x]).decode('cp1251')
    #         editorWindow[f'A0h_text_{i}'].update(value=b_val if b_val != '' else ' ')


def ciscoGetSFPType(v):
    if len(v['A0h_6']) > 0:
        if v['A0h_6'][0] == '1000BASE-T': 
            return {'type':'Undefined', 'pid':'SFP-GE-T'} 
        elif v['A0h_6'][0] == 'BASE-BX10' and int(v['A0h_12']) < 10:
            return {'type':'100Base-BX10-U', 'pid':'SFP-FE-100BX-U'}
        elif v['A0h_6'][0] == 'BASE-BX10' and int(v['A0h_12']) >= 10:
            return {'type':'1000Base-BX10-U', 'pid':'GLC-BX-U'}
        elif v['A0h_6'][0] == '100BASE-FX':
            return {'type':'100Base-FX', 'pid':'SFP-FE-100FX'}
        elif v['A0h_6'][0] == '100BASE-LX/LX10':
            return {'type':'100Base-LX-FE', 'pid':'SFP-FE-100LX'}
        elif v['A0h_6'][0] == '1000BASE-CX':
            return {'type':'1000BaseCX-Cable', 'pid':'Undefined'}
        elif v['A0h_6'][0] == '1000BASE-LX':
            return {'type':'Undefined', 'pid':'SFP-GE-L'}
        elif v['A0h_6'][0] == '1000BASE-SX':
            return {'type':'Undefined', 'pid':'SFP-GE-S'}
        else: 
            return {'type':'Undefined', 'pid':'Undefined'}
    else:
        if v['A0h_3[0]'][0] == '10G Base-ER':
            return {'type':'10Gbase-ER', 'pid':'SFP-10G-ER'}
        elif v['A0h_3[0]'][0] == '10G Base-LRM':
            return {'type':'10Gbase-LR', 'pid':'SFP-10G-LR-X'}
        elif v['A0h_3[0]'][0] == '10G Base-LR':
            return {'type':'10Gbase-LR', 'pid':'SFP-10G-LR'}
        elif v['A0h_3[0]'][0] == '10G Base-SR':
            return {'type':'10Gbase-SR', 'pid':'SFP-10G-SR'}
        else: 
            return {'type':'Undefined', 'pid':'Undefined'}
    

def createWindow():   
    #Окно Vendor spec
    cols2 = [[[sg.Input(s=3,key=f'A0h_{x}', enable_events=True)] for x in range(i,sfp_bytes_len,16)] for i in range(96,112,1)]
    for x in range(len(cols2)):
        cols2[x].insert(0,[sg.Text('0x0'+hex(x)[2:].upper())])
    cols1 = [[sg.Text('0x'+hex(x)[2:].upper()) if x != 80 else sg.Text('')] for x in range(80,sfp_bytes_len,16) ]
    cols3 = [[sg.Input(s=16,key=f'A0h_text_{x}', enable_events=True, font=('Courier',10)) if x != 80 else sg.Text('\tUTF-8')] for x in range(80,sfp_bytes_len,16)]
    cols2.insert(0,cols1)
    cols2.append(cols3)
    cisco_adapt = [sg.Frame('Адаптация к Cisco',[
        [
            sg.Checkbox('Адаптировать к Cisco', key='A0h_cisco_adapt_enable', default=False, enable_events=True),
        ],
        [
            sg.Text('Тип SFP:', s=15), sg.Combo(A0h_cisco_sfp_type_val, key='A0h_cisco_sfp_type', enable_events=True, disabled=True, s=20),
        ],
        [
            sg.Text('Производитель:', s=15), sg.Combo(A0h_cisco_vendor_id_val, key='A0h_cisco_vendor_id', enable_events=True, default_value=A0h_cisco_vendor_id_val[0], disabled=True, s=20),
        ],
        [
            sg.Text('PID (PartNum):', s=15), sg.Combo(A0h_cisco_pids, s=20, key='A0h_cisco_pid', enable_events=True, disabled=True),
        ],
        [
            sg.Text('VID (Rev):', s=15), sg.Combo(cisco_vids,s=20,key='A0h_cisco_vid', enable_events=True, disabled=True, default_value=cisco_vids[0]),
        ],
    ])]
    juniper_adapt = [sg.Frame('Адаптация к Juniper',[
        [
            sg.Checkbox('Адаптировать к Juniper', key='A0h_juniper_adapt_enable', default=False, enable_events=True),
        ],
        [
            sg.Text('PN (PartNum):', s=15), sg.Combo(juniper_pn, key='A0h_juniper_pn', enable_events=True, disabled=True, s=20),
        ],
        [
            sg.Text('Ревизия:', s=15), sg.Combo(juniper_rev,s=20,key='A0h_juniper_rev', enable_events=True, disabled=True),
        ],
    ])]
    layout_vSpec = [[sg.Column(x ,vertical_alignment='top') for x in cols2]]  
    layout_vSpec.append([sg.Text('')])
    layout_vSpec.append(cisco_adapt)
    layout_vSpec.append([sg.Text('')])
    layout_vSpec.append(juniper_adapt)

    #Главное окно (A0h)
    length = [sg.Frame('Длина кабеля',[
        [
            sg.Text(A0h_14_desc, size=(25,1)),
            sg.Input(size=(5,1), key='A0h_14'),
        ],
        [
            sg.Text(A0h_15_desc, size=(25,1)),
            sg.Input(size=(5,1), key='A0h_15'),
        ],
        [
            sg.Text(A0h_16_desc, size=(25,1)),
            sg.Input(size=(5,1), key='A0h_16'),
        ],
        [
            sg.Text(A0h_17_desc, size=(25,1)),
            sg.Input(size=(5,1), key='A0h_17'),
        ],
        [
            sg.Text(A0h_18_desc, size=(25,1)),
            sg.Input(size=(5,1), key='A0h_18'),
        ],
        [
            sg.Text(A0h_19_desc, size=(25,1)),
            sg.Input(size=(5,1), key='A0h_19'),
        ],
    ],border_width=1)]

    bitrate = [sg.Frame('Скорость передачи',[
            [
                sg.Text(A0h_12_desc +', 100Мб/c: ', size=(25,1)),
                sg.Input(size=(5,1), key='A0h_12'),
            ],
            [
                sg.Text(A0h_66_desc, size=(25,1)),
                sg.Input(size=(5,1), key='A0h_66'),
            ],
            [
                sg.Text(A0h_67_desc, size=(25,1)),
                sg.Input(size=(5,1), key='A0h_67'),
            ],
        ],border_width=1)] 
        
    unspec = [sg.Frame('Не определены', [
            [
            sg.Text('A0h#36: ', size=(25,1)),
            sg.Input(size=(5,1), key='A0h_36'),
            ],
            [
            sg.Text('A0h#62: ', size=(25,1)),
            sg.Input(size=(5,1), key='A0h_62'),
            ]
        ], border_width=1)]
        
    vendorInfo = [sg.Frame('Информация производителя',[
            [
                sg.Text('Имя Производителя: ', size=(15,1)),
                sg.Input(size=(19,1), key='A0h_vendorName'),
            ],
            [
                sg.Text('OUI Производителя: ', size=(15,1)),
                sg.Input(size=(5,1), key='A0h_vendorOUI_1'),
                sg.Input(size=(5,1), key='A0h_vendorOUI_2'),
                sg.Input(size=(5,1), key='A0h_vendorOUI_3'),
            ],
            [
                sg.Text('Номенклатурный №: ', size=(15,1)),
                sg.Input(size=(19,1), key='A0h_vendorPN'),
            ],
            [
                sg.Text('Ревизия: ', size=(15,1)),
                sg.Input(size=(19,1), key='A0h_vendorRev'),
            ],
            [
                sg.Text('Серийный номер: ', size=(15,1)),
                sg.Input(size=(19,1), key='A0h_vendorSN'),
            ],
        ], border_width=1)]
        
    other = [sg.Frame('Другое',[
            [
                sg.Text('Длина Волны (нм): ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_60&A0h_61'),
            ],
            [
                sg.Text(A0h_63_desc + ': ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_63', disabled=True),
            ],
            [
                sg.Text(A0h_95_desc + ': ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_95', disabled=True),
            ],
            [
                sg.Text('Год (XX): ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_year'),
            ],
            [
                sg.Text('Месяц (XX): ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_month'),
            ],
            [
                sg.Text('День (XX): ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_day'),
            ],
            [
                sg.Text('Спец.поле (XX): ', size=(20,1)),
                sg.Input(size=(5,1), key='A0h_vSpec'),
            ],
        ], border_width=1)]
        
    layout_main = [
        [sg.HorizontalSeparator()],
        [
        sg.Button('', image_data=upload_img, key='read',size=(20,4), image_subsample=7, tooltip='СЧИТАТЬ С SFP'),
        sg.Text('',s=3),
        sg.Button('', image_data=download_img, key='write',size=(20,4), image_subsample=7, tooltip='ЗАПИСАТЬ НА SFP'),
        sg.Text('',s=3),
        sg.Checkbox('Записать\nтолько\nизмененные\nбайты', key='only_changed', default=False, enable_events=True),
        sg.Column([
        [sg.Text('COM ПОРТ: ', s=15), sg.Combo(COMS,key='comport', s=8, enable_events=True)],
        [sg.Text('Пароль: ' , s=15), sg.Input(default_text='00000000',s=10, key='password', enable_events=True),sg.Checkbox('ВКЛ', key='password_on', default=False, enable_events=True)], 
        [sg.Text('Количество байт: ', s=15), sg.Input(default_text='256', s=10,key='sfp_bytes_len')],
        ]
        ),
        # sg.Button('ПОДБОР ПАРОЛЯ',key='passel',size=(20,4)),
        sg.Button('', image_data=password_img, key='passel',size=(20,4), image_subsample=7, tooltip='ПОДБОР ПАРОЛЯ'),
        sg.Text('',s=3),
        # sg.Button('СКАНИРОВАНИЕ РЕГИСТРОВ',key='i2cscan',size=(20,4)),
        sg.Button('', image_data=scan_img, key='i2cscan',size=(20,4), image_subsample=7, tooltip='СКАНИРОВАНИЕ РЕГИСТРОВ'),
        sg.Text('',s=3),
        sg.Column([
        [sg.Text('Регистры')],
        [sg.Text('A0h',text_color='#A9A9A9', font='Verdana 12 bold', key='i2c_A0h')],
        [sg.Text('A2h',text_color='#A9A9A9', font='Verdana 12 bold', key='i2c_A2h')],
        ]),
        # sg.Button('ОТКРЫТЬ ФАЙЛ',key='open', s=(20,4)),
        sg.Button('', image_data=open_img, key='open',size=(20,4), image_subsample=7, tooltip='ОТКРЫТЬ ФАЙЛ'),
        sg.Text('',s=3),
        # sg.Button('СОХРАНИТЬ ФАЙЛ',key='save',size=(20,4)),
        sg.Button('', image_data=save_img, key='save',size=(20,4), image_subsample=7, tooltip='СОХРАНИТЬ ФАЙЛ'),
        sg.Text('',s=3),
        ],
        [sg.HorizontalSeparator()],
        [
        sg.Text(A0h_0_desc, size=(28,1)),
        sg.Text(A0h_1_desc, size=(28,1)),
        sg.Text(A0h_2_desc, size=(28,1)),
        sg.Text(A0h_3_desc[0], size=(28,1)),
        sg.Text(A0h_3_desc[1], size=(28,1)),
        sg.Text(A0h_4_desc, size=(28,1)),
        ],
        
        [
        sg.Listbox(values=v0, size=(30,8), select_mode='single', key='A0h_0', enable_events=True),
        sg.Listbox(values=v1, size=(30,8), select_mode='single', key='A0h_1', enable_events=True),
        sg.Listbox(values=v2, size=(30,8), select_mode='single', key='A0h_2', enable_events=True),
        sg.Listbox(values=v3_0, size=(30,8), select_mode='extended', key='A0h_3[0]', enable_events=True),
        sg.Listbox(values=v3_1, size=(30,8), select_mode='extended', key='A0h_3[1]', enable_events=True),
        sg.Listbox(values=v4, size=(30,8), select_mode='extended', key='A0h_4', enable_events=True),
        ],
        
        [
        sg.Text(A0h_5_desc, size=(28,1)),
        sg.Text(A0h_6_desc, size=(28,1)),
        sg.Text(A0h_7_desc[0], size=(28,1)),
        sg.Text(A0h_7_desc[1], size=(28,1)),
        sg.Text(A0h_8_desc[1], size=(28,1)),
        sg.Text(A0h_9_desc, size=(28,1)),
        ],
        
        [
        sg.Listbox(values=v5, size=(30,8), select_mode='extended', key='A0h_5', enable_events=True),
        sg.Listbox(values=v6, size=(30,8), select_mode='extended', key='A0h_6', enable_events=True),
        sg.Listbox(values=v7_0, size=(30,8), select_mode='extended', key='A0h_7[0]', enable_events=True),
        sg.Listbox(values=v7_1, size=(30,8), select_mode='extended', key='A0h_7[1]', enable_events=True),
        sg.Listbox(values=v8_1, size=(30,8), select_mode='extended', key='A0h_8[1]', enable_events=True),
        sg.Listbox(values=v9, size=(30,8), select_mode='extended', key='A0h_9', enable_events=True),
        ],
        
        [
        sg.Text(A0h_10_desc, size=(28,1)),
        sg.Text(A0h_11_desc, size=(28,1)),
        sg.Text(A0h_13_desc, size=(28,1)),
        sg.Text(A0h_64_desc, size=(28,1)),
        sg.Text(A0h_65_desc, size=(28,1)),
        sg.Text(A0h_92_desc, size=(28,1)),
        ],
        
        [
        sg.Listbox(values=v10, size=(30,8), select_mode='extended', key='A0h_10', enable_events=True),
        sg.Listbox(values=v11, size=(30,8), select_mode='single', key='A0h_11', enable_events=True),
        sg.Listbox(values=v13, size=(30,8), select_mode='single', key='A0h_13', enable_events=True),
        sg.Listbox(values=v64, size=(30,8), select_mode='extended', key='A0h_64', enable_events=True),
        sg.Listbox(values=v65, size=(30,8), select_mode='extended', key='A0h_65', enable_events=True),
        sg.Listbox(values=v92, size=(30,8), select_mode='extended', key='A0h_92', enable_events=True),
        ],
            
        [
        sg.Column([
            [
                sg.Column([
                    [sg.Text(A0h_93_desc, size=(28,1)),], 
                    [sg.Listbox(values=v93, size=(30,8), select_mode='extended', key='A0h_93', enable_events=True),],
                    [sg.Text('')],
                    [sg.Text('')],
                    [sg.Button('', image_data=about_img, button_color=(sg.theme_background_color(),sg.theme_background_color()),border_width=0, key='about'),],
                ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                sg.Column([
                    [sg.Text(A0h_94_desc, size=(28,1)),], 
                    [sg.Listbox(values=v94, size=(30,8), select_mode='single', key='A0h_94', enable_events=True),]
                ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left')
            ],
        ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left', justification='center'),
        sg.Column([vendorInfo,bitrate], vertical_alignment='top'),
        sg.Column([length, unspec], vertical_alignment='top'),
        sg.Column([other], vertical_alignment='top'),
        ],   
    ]

    #Окно A2h
    alarms = [sg.Frame('Пороги аварий',[
        [sg.Column([
                    [
                        sg.Text(A2h_0_1_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_0_1', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_2_3_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_2_3', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_4_5_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_4_5', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_6_7_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_6_7', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_8_9_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_8_9', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_10_11_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_10_11', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_12_13_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_12_13', disabled=True, enable_events=True),
                    ],
                ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left',pad=(0,0)),
        sg.Column([
                    
                    [
                        sg.Text(A2h_14_15_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_14_15', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_16_17_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_16_17', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_18_19_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_18_19', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_20_21_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_20_21', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_22_23_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_22_23', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_24_25_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_24_25', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_26_27_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_26_27', disabled=True, enable_events=True),
                    ],
                ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left',pad=(0,0)),
        sg.Column([
                    
                    [
                        sg.Text(A2h_28_29_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_28_29', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_30_31_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_30_31', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_32_33_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_32_33', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_34_35_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_34_35', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_36_37_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_36_37', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_38_39_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_38_39', disabled=True, enable_events=True),
                    ],
                ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left',pad=(0,0)),]
    ],border_width=1,pad=(2,0))]

    caliber = [sg.Frame('Калибровочные значения',[
        [sg.Column([
                    [
                        sg.Text(A2h_56_59_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_56_59', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_60_63_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_60_63', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_64_67_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_64_67', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_68_71_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_68_71', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_72_75_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_72_75', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_76_77_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_76_77', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_78_79_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_78_79', disabled=True, enable_events=True),
                    ],
        ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
        sg.Column([    
                    [
                        sg.Text(A2h_80_81_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_80_81', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_82_83_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_82_83', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_84_85_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_84_85', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_86_87_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_86_87', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_88_89_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_88_89', disabled=True, enable_events=True),
                    ],
                    [
                        sg.Text(A2h_90_91_desc, size=(29,1)),
                        sg.Input(size=(7,1), key='A2h_90_91', disabled=True, enable_events=True),
                    ],
                ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),]
    ],border_width=1, vertical_alignment='top',pad=(2,0))]

    current = [sg.Frame('Текущие значения',[
                   [sg.Column([[
                        sg.Text(A2h_96_97_desc),
                        sg.Input(size=(7,1), key='A2h_96_97', disabled=True, enable_events=True),
                    ]], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    sg.Column([[
                        sg.Text(A2h_98_99_desc),
                        sg.Input(size=(7,1), key='A2h_98_99', disabled=True, enable_events=True),
                    ]], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    sg.Column([[
                        sg.Text(A2h_100_101_desc),
                        sg.Input(size=(7,1), key='A2h_100_101', disabled=True, enable_events=True),
                    ]], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    sg.Column([[
                        sg.Text(A2h_102_103_desc),
                        sg.Input(size=(7,1), key='A2h_102_103', disabled=True, enable_events=True),
                    ]], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    sg.Column([[
                        sg.Text(A2h_104_105_desc),
                        sg.Input(size=(7,1), key='A2h_104_105', disabled=True, enable_events=True),
                    ]], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),]
    ],border_width=1, vertical_alignment='top',pad=(2,0))]

    flags = [sg.Frame('Текущие аварии',[
                   [sg.Column([
                        [sg.Text('Высокая температура', key='hi_temp', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Низкая температура', key='lo_temp', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Высокое напряжение', key='hi_voltage', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Низкое напряжение', key='lo_voltage', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Высокий ток', key='hi_amp', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Низкий ток', key='lo_amp', text_color='#A9A9A9', font='Verdana 10 bold')],
                   ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                   sg.Column([
                        [sg.Text('Высокая вх. мощность', key='hi_rx_power', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Низкая вх. мощность', key='lo_rx_power', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Высокая исх. мощность', key='hi_tx_power', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Низкая исх. мощность', key='lo_tx_power', text_color='#A9A9A9', font='Verdana 10 bold')],
                        [sg.Text('Warning', text_color='#FF8C00', font='Verdana 10 bold'), sg.Text('OK', text_color='#008000', font='Verdana 10 bold')],
                        [sg.Text('Alarm', text_color='#FF0000', font='Verdana 10 bold'), sg.Text('Clear', text_color='#A9A9A9', font='Verdana 10 bold')],
                   ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),]
    ],border_width=1, vertical_alignment='top',pad=(2,0))]

    controls = [sg.Frame('Контроль и статус',[
                   [sg.Column([
                        [sg.Text('Статус лазера: ')],
                        [sg.Text('Выключить лазер: ')],
                        [sg.Text('Статус контакта RS1: ')],
                        [sg.Text('Статус контакта RS0: ')],
                        [sg.Text('Программный RS0: ')],
                        [sg.Text('TX Fault: ')],
                        [sg.Text('LOS: ')],
                        [sg.Text('Готов к приему: ')],
                    ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    
                    sg.Column([
                        [sg.Text('N/A', key='laser_state', text_color='#A9A9A9', font='Verdana 9 bold')],
                        [sg.Checkbox('',default=False, key='laser_off', disabled=True, enable_events=True)],
                        [sg.Text('N/A', key='rs1_state', text_color='#A9A9A9', font='Verdana 9 bold')],
                        [sg.Text('N/A', key='rs0_state', text_color='#A9A9A9', font='Verdana 9 bold')],
                        [sg.Checkbox('', default=False, key='soft_rs0', disabled=True, enable_events=True)],
                        [sg.Text('N/A', key='tx_fault', text_color='#A9A9A9', font='Verdana 9 bold')],
                        [sg.Text('N/A', key='los', text_color='#A9A9A9', font='Verdana 9 bold')],
                        [sg.Text('N/A', key='data_ready', text_color='#A9A9A9', font='Verdana 9 bold')],
                    ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    
                    sg.Column([
                        [sg.Text('Программный RS1: ')],
                        [sg.Text('Максимальная мощность: ')],
                        [sg.Text('Максимальная мощность: ')],
                        [sg.Text('Reserved 118_7: ')],
                        [sg.Text('Reserved 118_6: ')],
                        [sg.Text('Reserved 118_5: ')],
                        [sg.Text('Reserved 118_4: ')],
                        [sg.Text('Reserved 118_2: ')],
                    ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left'),
                    
                    sg.Column([
                        [sg.Checkbox('', default=False, key='soft_rs1', disabled=True, enable_events=True)],
                        [sg.Text('N/A', key='power_levwl_state', text_color='#A9A9A9', font='Verdana 9 bold')],
                        [sg.Radio('1.0 Вт', 'power_level', key='power_level_1', font='Verdana 9 bold', disabled=True, enable_events=True), sg.Radio('1.5 Вт','power_level',  key='power_level_2', font='Verdana 9 bold', disabled=True, enable_events=True)],
                        [sg.Checkbox('', default=False, key='reserved_118_7', pad=(4,0), disabled=True, enable_events=True)],
                        [sg.Checkbox('', default=False, key='reserved_118_6', pad=(4,0), disabled=True, enable_events=True)],
                        [sg.Checkbox('', default=False, key='reserved_118_5', pad=(4,0), disabled=True, enable_events=True)],
                        [sg.Checkbox('', default=False, key='reserved_118_4', pad=(4,0), disabled=True, enable_events=True)],
                        [sg.Checkbox('', default=False, key='reserved_118_2', pad=(4,0), disabled=True, enable_events=True)],
                    ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left')]
                    
    ],border_width=1, vertical_alignment='top',pad=(2,0))]

    vs1 = [sg.Frame('Поля вендора',[
                   [sg.Column([
                        [sg.Text('Пароль: '), sg.Input(key='pass_1', size=(5,1), disabled=True, enable_events=True), sg.Input(key='pass_2', size=(5,1), disabled=True, enable_events=True), 
                        sg.Input(key='pass_3', size=(5,1), disabled=True, enable_events=True), sg.Input(key='pass_4', size=(5,1), disabled=True, enable_events=True),],
                        [sg.Text('0x78: '), sg.Input(key='A2h_120', size=(5,1), disabled=True, enable_events=True), sg.Text('0x79: '), sg.Input(key='A2h_121', size=(5,1), disabled=True, enable_events=True)],
                        [sg.Text('0x7A: '), sg.Input(key='A2h_122', size=(5,1), disabled=True, enable_events=True), sg.Text('0x7F: '), sg.Input(key='A2h_127', size=(5,1), disabled=True, enable_events=True)],
                        [sg.Text('0x6F: '), sg.Input(key='A2h_111', size=(5,1), disabled=True, enable_events=True), sg.Text('Checksum: '), sg.Input(key='A2h_95', size=(5,1), disabled=True, enable_events=True)],
                    ], vertical_alignment='top', size_subsample_width=0, size_subsample_height=0, element_justification='left', pad=(2,0))]
                    
    ],border_width=1, vertical_alignment='top',pad=(0,0))]

    table_header = ['       ','0x00','0x01','0x02','0x03','0x04','0x05','0x06','0x07','0x08','0x09','0x0A','0x0B','0x0C','0x0D','0x0E','0x0F']
    table_values = [['0x00'],['0x10'],['0x20'],['0x30'],['0x40'],['0x50'],['0x60'],['0x70'],['0x80'],['0x90'],['0xA0'],['0xB0'],['0xC0'],['0xD0'],['0xE0'],['0xF0']]
    fware = [sg.Frame('Байтовый вид',[
        [sg.Table(values=table_values, headings=table_header,
                    def_col_width = 8,
                    auto_size_columns=False,
                    display_row_numbers=False,
                    expand_x=True,
                    justification='center',
                    num_rows=15,
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    row_height=15,
                    tooltip='This is a table')]
    ],border_width=1, element_justification='center',pad=(1,0))]

    cols2 = [[[sg.Input(s=(4,1),key=f'Table_A2h_{x}',pad=(0,0), font='Arial 8', disabled=True, enable_events=True)] for x in range(i,256,16)] for i in range(0,16,1)]
    for x in range(len(cols2)):
        cols2[x].insert(0,[sg.Text('0x0'+hex(x)[2:].upper(),pad=(0,0))])
    cols1 = [[sg.Text('0x'+hex(x)[2:].upper(),pad=((0,0),(0,0)),font='Arial 8') if x != -16 else sg.Text('',pad=((0,0),(0,0)))] for x in range(-16,256,16) ]
    cols2.insert(0,cols1)
    user_data = [sg.Frame('Байтовый вид',[[sg.Column(x ,vertical_alignment='top', expand_x = False, pad=(2,2)) for x in cols2]],border_width=1, vertical_alignment='top', expand_x = False)]

    buttons = [[
        sg.Column([[sg.Button('', image_data=upload_img, key='A2h_read',size=(20,4), image_subsample=7, tooltip='СЧИТАТЬ С SFP'),
        sg.Text('',s=3),],[sg.Button('', image_data=open_img, key='A2h_open',size=(20,4), image_subsample=7, tooltip='ОТКРЫТЬ ФАЙЛ'),
        sg.Text('',s=3),],[sg.Text('COM ПОРТ: ', s=15)],[sg.Text('Пароль: ' , s=15)]]),
        sg.Column([[sg.Button('', image_data=download_img, key='A2h_write',size=(20,4), image_subsample=7, tooltip='ЗАПИСАТЬ В SFP'),
        sg.Text('',s=3),],[sg.Button('', image_data=save_img, key='A2h_save',size=(20,4), image_subsample=7, tooltip='СОХРАНИТЬ ФАЙЛ'),
        sg.Text('',s=3),], [sg.Combo(COMS,key='A2h_comport', s=8, enable_events=True)],
        [sg.Input(default_text='00000000',s=10, key='A2h_password', enable_events=True),sg.Checkbox('ВКЛ', key='A2h_password_on', default=False, enable_events=True)]],pad=((0,0),(4,0)))],
        [sg.Text('')],
        [sg.Checkbox('Записать только измененные байты', default=False, key='A2h_only_changed', enable_events=True)],
        [sg.Checkbox('Разрешить редактирование', default=False, key='write_allow', enable_events=True)],
        ]

    layout_a2h = [
        [sg.Column([user_data], vertical_alignment='top',pad=(0,0)),sg.Column(buttons, vertical_alignment='top',pad=((0,0),(65,0)),expand_x=True,element_justification='center')],
        [sg.Column([alarms,current], vertical_alignment='top',pad=(0,0)),sg.Column([caliber], vertical_alignment='top',pad=(0,0))],
        [sg.Column([flags], vertical_alignment='top',pad=(0,0)),sg.Column([controls], vertical_alignment='top',pad=(0,0)), sg.Column([vs1], vertical_alignment='top',pad=(0,0))],
    ]
    
    layout_debug = [
        [sg.Multiline(s=(150,40), key='debug')]
    ]

    layout = [[sg.TabGroup([[sg.Tab('Раздел A0h', layout_main, key='A0h_tab', element_justification='center'),
                             sg.Tab('Байты Вендора раздела A0h', layout_vSpec, key='vSpec_tab', element_justification='center'),
                             sg.Tab('Раздел A2h', layout_a2h, key='A2h_tab', element_justification='center'),
                             sg.Tab('Отладочная информация', layout_debug, key='debug_tab', element_justification='center')]],
                           key='TabGroup_1', tab_location='topleft',s=(1600,900))]] 
    return sg.Window(programm_name,layout,return_keyboard_events = True, grab_anywhere = True, element_justification='center',icon='app_icon.ico', finalize=True)


editorWindow = createWindow()
editorWindow.set_icon(icon='app_icon.ico')
passSelOn = False
AcceptPasswd = ''
writeOn = False
writeResult = ''
writtenBytes = 0
i2c = []
A0h_available = True
A2h_available = True
# editorWindow['debug'].reroute_stdout_to_here()
# editorWindow['debug'].reroute_stderr_to_here()
# editorWindowResize = True
# editorWindow.size=(917,48)
# editorWindow.read(timeout=1)
# editorWindow.Move(235,20)
theme_choise = 1

write_Allow = [
    'A2h_0_1','A2h_2_3','A2h_4_5','A2h_6_7','A2h_8_9','A2h_10_11','A2h_12_13','A2h_14_15','A2h_16_17','A2h_18_19','A2h_20_21','A2h_22_23','A2h_24_25','A2h_26_27','A2h_28_29',
    'A2h_30_31','A2h_32_33','A2h_34_35','A2h_36_37','A2h_38_39','A2h_56_59','A2h_60_63','A2h_64_67','A2h_68_71','A2h_72_75','A2h_76_77','A2h_78_79','A2h_80_81','A2h_82_83',
    'A2h_84_85','A2h_86_87','A2h_88_89','A2h_90_91','laser_off','soft_rs0','soft_rs1','power_level_1','power_level_2','pass_1','pass_2','pass_3','pass_4','A2h_120','A2h_121',
    'A2h_122','A2h_127','A2h_111','reserved_118_2','reserved_118_4','reserved_118_5','reserved_118_6','reserved_118_7',
]
write_Allow2 = write_Allow.copy()
for i in A2h_writeAllow:
    write_Allow.append(f'Table_A2h_{i}')
A2h_twos_comp = ['A2h_0_1','A2h_2_3','A2h_4_5','A2h_6_7']
A2h_slope = ['A2h_76_77','A2h_80_81','A2h_84_85','A2h_88_89']
A2h_float_4 = ['A2h_56_59','A2h_60_63','A2h_64_67','A2h_68_71','A2h_72_75']
# A2h_unsign_short = ['A2h_8_9','A2h_10_11','A2h_12_13','A2h_14_15','A2h_16_17','A2h_18_19','A2h_20_21','A2h_22_23','A2h_24_25','A2h_26_27','A2h_28_29',
# 'A2h_30_31','A2h_32_33','A2h_34_35','A2h_36_37','A2h_38_39']
A2h_voltage = ['A2h_8_9','A2h_10_11','A2h_12_13','A2h_14_15']
A2h_current = ['A2h_16_17','A2h_18_19','A2h_20_21','A2h_22_23']
A2h_power = ['A2h_24_25','A2h_26_27','A2h_28_29','A2h_30_31','A2h_32_33','A2h_34_35','A2h_36_37','A2h_38_39']
A2h_sign_short = ['A2h_78_79','A2h_82_83','A2h_86_87','A2h_90_91']
A2h_bits = ['A2h_110','A2h_112','A2h_113','A2h_116','A2h_117','A2h_118']
A2h_simple_byte = ['pass_1','pass_2','pass_3','pass_4','A2h_120','A2h_121','A2h_122','A2h_127','A2h_111']

editorWindow['read'].set_cursor(cursor='hand2')
editorWindow['write'].set_cursor(cursor='hand2')
editorWindow['passel'].set_cursor(cursor='hand2')
editorWindow['i2cscan'].set_cursor(cursor='hand2')
editorWindow['open'].set_cursor(cursor='hand2')
editorWindow['save'].set_cursor(cursor='hand2')
editorWindow['A2h_read'].set_cursor(cursor='hand2')
editorWindow['A2h_write'].set_cursor(cursor='hand2')
editorWindow['A2h_open'].set_cursor(cursor='hand2')
editorWindow['A2h_save'].set_cursor(cursor='hand2')

def _onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode==88 and ctrl and event.keysym.lower() != 'x':
        event.widget.event_generate('<<Cut>>')

    if event.keycode==86 and ctrl and event.keysym.lower() != 'v':
        event.widget.event_generate('<<Paste>>')

    if event.keycode==67 and ctrl and event.keysym.lower() != 'c':
        event.widget.event_generate('<<Copy>>')

editorWindow.TKroot.bind_all('<<Key>>', _onKeyRelease, '+')

while True:
    try:
        e,v = editorWindow.read()
        if debug: print(f'event: {e}')
        if e == sg.WIN_CLOSED or e == 'Exit':
            break
        else:
            ref = True if not re.match(r'.+:\d+', e) else False if re.match(r'A0h_[1-2]{0,1}[0-9]{1}[0-9]{1}',e) else False
            comlist = serial.tools.list_ports.comports()
            COMS = []
            _,val = editorWindow.read(timeout=1)
            for el in comlist:
                COMS.append(el.device)
            COM_PORT = val['comport']
            editorWindow['comport'].update(value=COM_PORT if COM_PORT in COMS else '',values=COMS)
            #Проверка ввода количества считываемых байтов
            if val['sfp_bytes_len'] == '' and re.match(r'.+:\d+',e):
                ref = False
            elif len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['sfp_bytes_len'].update(value=''.join(re.findall(r'\d',val['sfp_bytes_len'])))
            if int(val['sfp_bytes_len'] if val['sfp_bytes_len'] != '' else '0') < 96 and not re.match(r'.+:\d+', e) and not (len(e) == 1 and re.match(r'[\w ]',e)):
                sfp_bytes_len = 96
                editorWindow['sfp_bytes_len'].update(value=96)
            elif int(val['sfp_bytes_len'] if val['sfp_bytes_len'] != '' else '0') > 256:
                sfp_bytes_len = 256
                editorWindow['sfp_bytes_len'].update(value=256)
            elif not re.match(r'.+:\d+', e) and not (len(e) == 1 and re.match(r'[\w ]',e)):
                sfp_bytes_len = int(val['sfp_bytes_len'])    
            #Проверка ввода пароля 
            if val['password'] == '' and re.match(r'.+:\d+',e):
                pass
            elif len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['password'].update(value=''.join(re.findall(r'[a-fA-F0-9]',val['password'].upper())))
            if len(val['password'])>8: editorWindow['password'].update(value=val['password'][:8].upper())
            editorWindow['A2h_password'].update(value = val['password'])
            #Проверка длины имени производителя
            if len(val['A0h_vendorName'])>16: editorWindow['A0h_vendorName'].update(value=val['A0h_vendorName'][:16])
            #Проверка OUI
            if len(e) == 1 and re.match(r'[\w ]',e):
                for i in range(3):
                    editorWindow[f'A0h_vendorOUI_{i+1}'].update(value=''.join(re.findall(r'[a-fA-F0-9]',val[f'A0h_vendorOUI_{i+1}'].upper())))
                    val[f'A0h_vendorOUI_{i+1}'] = ''.join(re.findall(r'[a-fA-F0-9]',val[f'A0h_vendorOUI_{i+1}'].upper()))
                    if len(val[f'A0h_vendorOUI_{i+1}'])>2: 
                        editorWindow[f'A0h_vendorOUI_{i+1}'].update(value=val[f'A0h_vendorOUI_{i+1}'][:2].upper())
                        val[f'A0h_vendorOUI_{i+1}'] = val[f'A0h_vendorOUI_{i+1}'][:2].upper()
            elif re.match(r'.+:\d+', e):
                pass
            else:
                for i in range(3):
                    if len(val[f'A0h_vendorOUI_{i+1}'])<2: 
                        editorWindow[f'A0h_vendorOUI_{i+1}'].update(value='0'+val[f'A0h_vendorOUI_{i+1}'].upper())
                        val[f'A0h_vendorOUI_{i+1}'] = '0'+val[f'A0h_vendorOUI_{i+1}'].upper()
                    if val[f'A0h_vendorOUI_{i+1}']=='': 
                        editorWindow[f'A0h_vendorOUI_{i+1}'].update(value='00')
                        val[f'A0h_vendorOUI_{i+1}'] = '00'
            #Проверка длины номенклатурного номера
            if len(val['A0h_vendorPN'])>16: 
                editorWindow['A0h_vendorPN'].update(value=val['A0h_vendorPN'][:16])
                val['A0h_vendorPN'] = val['A0h_vendorPN'][:16]
            #Проверка длины ревизии
            if len(val['A0h_vendorRev'])>4: 
                editorWindow['A0h_vendorRev'].update(value=val['A0h_vendorRev'][:4])
                val['A0h_vendorRev'] = val['A0h_vendorRev'][:4]
            #Проверка длины серийного номера
            if len(val['A0h_vendorSN'])>16: 
                editorWindow['A0h_vendorSN'].update(value=val['A0h_vendorSN'][:16])
                val['A0h_vendorSN'] = val['A0h_vendorSN'][:16]
            #Проверка корректности байтов [12,14,15,16,17,18,19,66,67]
            if len(e) == 1 and re.match(r'[\w ]',e):
                datas = [12,14,15,16,17,18,19,36,62,66,67]
                for i in datas:
                    editorWindow[f'A0h_{i}'].update(value=''.join(re.findall(r'\d',val[f'A0h_{i}'])))
                    val[f'A0h_{i}'] = ''.join(re.findall(r'\d',val[f'A0h_{i}']))
                    if (int(val[f'A0h_{i}']) if val[f'A0h_{i}'] != '' else 0) > 255: 
                        editorWindow[f'A0h_{i}'].update(value=255)
                        val[f'A0h_{i}'] = '255'
                    if val[f'A0h_{i}'] == '': 
                        editorWindow[f'A0h_{i}'].update(value=0)
                        val[f'A0h_{i}'] = '0'
            elif re.match(r'.+:\d+', e):
                pass
            else:
                datas = [12,14,15,16,17,18,19,36,62,66,67]
                for i in datas:
                    if val[f'A0h_{i}'] == '': 
                        editorWindow[f'A0h_{i}'].update(value=0)
                        val[f'A0h_{i}'] = '0'
                    if (int(val[f'A0h_{i}']) if val[f'A0h_{i}'] != '' else 0) > 255: 
                        editorWindow[f'A0h_{i}'].update(value=255)
                        val[f'A0h_{i}'] = '255'
                    
            #Проверка дня
            if len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['A0h_day'].update(value=''.join(re.findall(r'\d',val['A0h_day'])))
                val['A0h_day'] = ''.join(re.findall(r'\d',val['A0h_day']))
                if val['A0h_day'] == '': 
                    editorWindow['A0h_day'].update(value='00')
                    val['A0h_day'] = '00'
                if int(val['A0h_day'])>31: 
                    editorWindow['A0h_day'].update(value='31')
                    val['A0h_day'] = '31'
                if len(val['A0h_day'])>2: 
                    editorWindow['A0h_day'].update(value=val['A0h_day'][:2])
                    val['A0h_day'] = val['A0h_day'][:2]
            elif re.match(r'.+:\d+', e):
                pass
            else: 
                if val['A0h_day'] == '': 
                    editorWindow['A0h_day'].update(value='00')
                    val['A0h_day'] = '00'
                if int(val['A0h_day'])>31: 
                    editorWindow['A0h_day'].update(value='31')
                    val['A0h_day'] = '31'
                if len(val['A0h_day'])<2:
                    editorWindow['A0h_day'].update(value='0'+val['A0h_day'])
                    val['A0h_day'] = '0'+val['A0h_day']
                if len(val['A0h_day'])>2: 
                    editorWindow['A0h_day'].update(value=val['A0h_day'][:2])
                    val['A0h_day'] = val['A0h_day'][:2]
            #Проверка месяца
            if len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['A0h_month'].update(value=''.join(re.findall(r'\d',val['A0h_month'])))
                val['A0h_month'] = ''.join(re.findall(r'\d',val['A0h_month']))
                if val['A0h_month'] == '': 
                    editorWindow['A0h_month'].update(value='00')
                    val['A0h_month'] = '00'
                if int(val['A0h_month'])>12: 
                    editorWindow['A0h_month'].update(value='12')
                    val['A0h_month'] = '00'
                if len(val['A0h_month'])>2: 
                    editorWindow['A0h_month'].update(value=val['A0h_month'][:2])
                    val['A0h_month'] = val['A0h_month'][:2]
            elif re.match(r'.+:\d+', e):
                pass
            else:
                if val['A0h_month'] == '': 
                    editorWindow['A0h_month'].update(value='00')
                    val['A0h_month'] = '00'
                if int(val['A0h_month'])>12: 
                    editorWindow['A0h_month'].update(value='12')
                    val['A0h_month'] = '12'
                if len(val['A0h_month'])<2:
                    editorWindow['A0h_month'].update(value='0'+val['A0h_month'])
                    val['A0h_month'] = '0'+val['A0h_month']
                if len(val['A0h_month'])>2: 
                    editorWindow['A0h_month'].update(value=val['A0h_month'][:2])
                    val['A0h_month'] = val['A0h_month'][:2]
            #Проверка года
            if len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['A0h_year'].update(value=''.join(re.findall(r'\d',val['A0h_year'])))
                val['A0h_year'] = ''.join(re.findall(r'\d',val['A0h_year']))
                if val['A0h_year'] == '': 
                    editorWindow['A0h_year'].update(value='00')
                    val['A0h_year'] = '00'
                if int(val['A0h_year'])>99: 
                    editorWindow['A0h_year'].update(value='99')
                    val['A0h_year'] = '99'
                if len(val['A0h_year'])>2: 
                    editorWindow['A0h_year'].update(value=val['A0h_year'][:2])
                    val['A0h_year'] = val['A0h_year'][:2]
            elif re.match(r'.+:\d+', e):
                pass
            else:
                if val['A0h_year'] == '': 
                    editorWindow['A0h_year'].update(value='00')
                    val['A0h_year'] = '00'
                if int(val['A0h_year'])>99: 
                    editorWindow['A0h_year'].update(value='99')
                    val['A0h_year'] = '99'
                if len(val['A0h_year'])<2:
                    editorWindow['A0h_year'].update(value='0'+val['A0h_year'])
                    val['A0h_year'] = '0'+val['A0h_year']
                if len(val['A0h_year'])>2: 
                    editorWindow['A0h_year'].update(value=val['A0h_year'][:2])
                    val['A0h_year'] = val['A0h_year'][:2]
            #Проверка vSpec
            if len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['A0h_vSpec'].update(value=''.join(re.findall(r'\d',val['A0h_vSpec'])))
                val['A0h_vSpec'] = ''.join(re.findall(r'\d',val['A0h_vSpec']))
                if val['A0h_vSpec'] == '': 
                    editorWindow['A0h_vSpec'].update(value='  ')
                    val['A0h_vSpec'] = '  '
                if val['A0h_vSpec'] != '  ':
                    if int(val['A0h_vSpec'])>99: 
                        editorWindow['A0h_vSpec'].update(value='99')
                        val['A0h_vSpec'] = '99'
                    if len(val['A0h_vSpec'])>2: 
                        editorWindow['A0h_vSpec'].update(value=val['A0h_vSpec'][:2])
                        val['A0h_vSpec'] = val['A0h_vSpec'][:2]
            elif re.match(r'.+:\d+', e):
                pass
            else:
                if val['A0h_vSpec'] == '': 
                    editorWindow['A0h_vSpec'].update(value='  ')
                    val['A0h_vSpec'] = '  '
                if val['A0h_vSpec'] != '  ':
                    if int(val['A0h_vSpec'])>99: 
                        editorWindow['A0h_vSpec'].update(value='99')
                        val['A0h_vSpec'] = '99'
                    if len(val['A0h_vSpec'])<2:
                        editorWindow['A0h_vSpec'].update(value='0'+val['A0h_vSpec'])
                        val['A0h_vSpec'] = '0'+val['A0h_vSpec']
                    if len(val['A0h_vSpec'])>2: 
                        editorWindow['A0h_vSpec'].update(value=val['A0h_vSpec'][:2])
                        val['A0h_vSpec'] = val['A0h_vSpec'][:2]
            #Проверка длины волны
            if len(e) == 1 and re.match(r'[\w ]',e):
                editorWindow['A0h_60&A0h_61'].update(value=''.join(re.findall(r'\d',val['A0h_60&A0h_61'])))
                val['A0h_60&A0h_61'] = ''.join(re.findall(r'\d',val['A0h_60&A0h_61']))
                if val['A0h_60&A0h_61'] == '': 
                    editorWindow['A0h_60&A0h_61'].update(value='0')
                    val['A0h_60&A0h_61'] = '0'
                if int(val['A0h_60&A0h_61'])>9999: 
                    editorWindow['A0h_60&A0h_61'].update(value='9999')
                    val['A0h_60&A0h_61'] = '9999'
            elif re.match(r'.+:\d+', e):
                pass
            else:
                if val['A0h_60&A0h_61'] == '': 
                    editorWindow['A0h_60&A0h_61'].update(value='0')
                    val['A0h_60&A0h_61'] = '0'
                if int(val['A0h_60&A0h_61'])>9999: 
                    editorWindow['A0h_60&A0h_61'].update(value='9999')
                    val['A0h_60&A0h_61'] = '9999'
            # Проверка VSpec 
            if len(e) == 1 and re.match(r'[\w ]',e):
                for i in range(96,256,1):
                    # print(vsval[f'A0h_{i}'])
                    editorWindow[f'A0h_{i}'].update(value=''.join(re.findall(r'[a-fA-F0-9]',val[f'A0h_{i}'].upper())))
                    val[f'A0h_{i}'] = ''.join(re.findall(r'[a-fA-F0-9]',val[f'A0h_{i}'].upper()))
                    if val[f'A0h_{i}']=='': 
                        editorWindow[f'A0h_{i}'].update(value='00')
                        val[f'A0h_{i}'] = '00'
                    if len(val[f'A0h_{i}'])>2: 
                        editorWindow[f'A0h_{i}'].update(value=val[f'A0h_{i}'][:2].upper())
                        val[f'A0h_{i}'] = val[f'A0h_{i}'][:2].upper()
            elif re.match(r'.+:\d+', e):
                pass
            else:
                for i in range(96,256,1):
                    if val[f'A0h_{i}'] == '' and not('A0h' in e):
                        editorWindow[f'A0h_{i}'].update(value='00')
                        val[f'A0h_{i}'] = '00'
                    if len(val[f'A0h_{i}'])<2 and not('A0h' in e): 
                        editorWindow[f'A0h_{i}'].update(value='A'+val[f'A0h_{i}'].upper())
                        val[f'A0h_{i}'] = 'A'+val[f'A0h_{i}'].upper()
            if re.match(r'A0h_[1-2]{0,1}[0-9]{1}[0-9]{1}',e):
                nn = int(e[4:])
                if int(nn) >= 96:
                    updUTF8(val,nn)
            lists = [0,1,2,11,13,94]        
            for i in lists:
                if val[f'A0h_{i}'] == []:
                    editorWindow[f'A0h_{i}'].update(set_to_index=[0])
            #Контрольные суммы ONLINE
            if ref:
                firmware = saveBIN(val)
                editorWindow[f'A0h_63'].update(value=hex(firmware[63])[2:].upper() if len(hex(firmware[63])[2:])>1 else '0'+hex(firmware[63])[2:].upper())
                editorWindow[f'A0h_95'].update(value=hex(firmware[95])[2:].upper() if len(hex(firmware[95])[2:])>1 else '0'+hex(firmware[95])[2:].upper())
        if e == 'open':
            editorWindow['A0h_cisco_adapt_enable'].update(value=False)
            v['A0h_cisco_adapt_enable'] = False
            editorWindow['A0h_juniper_adapt_enable'].update(value=False)
            v['A0h_juniper_adapt_enable'] = False
            try:
                file_handler = open(sg.PopupGetFile('Path', save_as=False, file_types=(('BINARY','*.bin'),('All Files', '*.*')), no_window=True), "rb")
                data_byte = file_handler.read()
                file_handler.close()
                if len(data_byte) > 256: data_byte[:256]
                openBIN(data_byte)
            except Exception as e: 
                if debug: print(e)

        if e == 'save':
            # eVS, vVS = editorWindow.read(timeout=5)
            # v.update(vVS)
            fw = saveBIN(v)
            try:
                file_handler = open(sg.PopupGetFile('Path', save_as=True,file_types=(('BINARY','*.bin'),('All Files', '*.*')), no_window=True, 
                default_path=f'{v["A0h_vendorPN"]}_{v["A0h_vendorSN"]}'), 'w+b')
                file_handler.write(fw)
                file_handler.close()
            except Exception as e: 
                if debug: print(e)

        if e == 'read':
            if A0h_available:
                editorWindow['A0h_cisco_adapt_enable'].update(value=False)
                v['A0h_cisco_adapt_enable'] = False
                editorWindow['A0h_juniper_adapt_enable'].update(value=False)
                v['A0h_juniper_adapt_enable'] = False
                COM_PORT = v['comport']
                data_byte = SFP_read(COM_PORT, '')
                if data_byte == 'serial error':
                    sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
                elif data_byte == 'read error 1' or data_byte == 'read error 2':
                    sg.Popup(f"\nОшибка чтения COM порта (timeout)\n", keep_on_top=True)
                elif data_byte == 'read error 3': sg.Popup(f"\nОшибка чтения байта (UnicodeDecodeError)\n")
                elif data_byte == 'read error 4': sg.Popup(f"\nОшибка чтения байта (ValueError)\n")
                else:
                    openBIN(data_byte)
            else: sg.Popup(f"\nСтраница A0h EEPROM Недоступна!\n",keep_on_top=True)
            
        if e == 'write':
            # eVS, vVS = editorWindow.read(timeout=5)
            # v.update(vVS)
            if A0h_available:
                firmware = saveBIN(v)
                pass_on = v['password_on']
                if pass_on:
                    if len(v['password']) != 8 or not re.fullmatch(r'[0-9A-Fa-f]+',v['password']):
                        sg.Popup(f"\nПроверьте правильность введенного пароля\n",keep_on_top=True)
                        continue
                    else:
                        PassAr = [int(v['password'][x:x+2],16) for x in range(0,len(v['password']),2)]
                writeLayout = [[sg.Text('Запись прошивки в EEPROM...')],[sg.ProgressBar(1000, key='write_status', s=(36,20))],[sg.Button('НАЧАТЬ', key='start_write')]]
                writeWindow = sg.Window('Запись EEPROM SFP', writeLayout,finalize=True,keep_on_top=True)
                writeWindow.make_modal()
                while True:
                    eWr, vWr = writeWindow.read(timeout=100)
                    if eWr == sg.WIN_CLOSED:
                        writeOn = False
                        break
                    if eWr == 'start_write':
                        COM_PORT = v['comport']
                        writeWindow['start_write'].update(disabled=True)
                        writeTask = Thread(target=SFP_write, args=(COM_PORT, firmware, ''))
                        writeOn = True
                        writeTask.start()
                    if eWr == '__TIMEOUT__':
                        try:
                            if not writeTask.is_alive() and writeOn:
                                if writeResult == 'serial error':
                                    sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
                                    writeWindow.close()
                                elif writeResult == 'read error 1' or writeResult == 'read error 2':
                                    sg.Popup(f"\nОшибка записи COM порта (timeout)\n",keep_on_top=True)
                                    writeWindow['start_write'].update(disabled=True)
                                elif writeResult == 'password error':
                                    sg.Popup(f"\nОшибка при вводе пароля\n",keep_on_top=True)
                                    writeWindow.close()
                                elif writeResult == 'off':
                                    sg.Popup(f"\nНи один байт не был изменен\nЗапись не требуется!\n",keep_on_top=True)
                                    writeWindow.close()
                                elif writeResult == 'write error':
                                    sg.Popup(f"\nНе удалось записать SFP\nВозможно установлен пароль или физическая защита\n",keep_on_top=True)
                                    writeWindow.close()
                                elif writeResult == 'read error 3': 
                                    sg.Popup(f"\nОшибка чтения байта (UnicodeDecodeError)\n")
                                    writeWindow['start_write'].update(disabled=False)
                                elif writeResult == 'read error 4': 
                                    sg.Popup(f"\nОшибка чтения байта (ValueError)\n")
                                    writeWindow['start_write'].update(disabled=False)
                                else:
                                    sg.Popup(f"\nУспешно записано {writtenBytes} байт в EEPROM!\n",keep_on_top=True)
                                    writeWindow.close()
                        except Exception as e: 
                            if debug: print(e)
            else: sg.Popup(f"\nСтраница A0h EEPROM Недоступна!\n",keep_on_top=True)        
                
        if e == 'passel':
            if A0h_available and A2h_available:
                layoutPasSel =[
                    [
                        sg.Column([[sg.Multiline('',key='passwords',s=(15,9))]],vertical_alignment='top'), 
                        sg.Column([
                            [sg.Button('ЗАГРУЗИТЬ СПИСОК ПАРОЛЕЙ',key='passfile',s=(30,4))],
                            [sg.Button('НАЧАТЬ ПОДБОР',key='passel',s=(30,4))],
                        ],vertical_alignment='top'),
                    ],
                    [sg.ProgressBar(max_value=1000, s=(36,20),key='status')],
                ]
                passelWindow = sg.Window('Подбор Пароля', layoutPasSel, finalize=True,keep_on_top=True)
                try:
                    file = open('PasswordsDict.lst', 'r')
                    lines = file.readlines()
                    passwords = [line.strip() for line in lines]
                    file.close()
                    pasVal = ''
                    for password in passwords:
                        pasVal += password + '\n' 
                    passelWindow['passwords'].update(value=pasVal)
                    passelWindow.make_modal()
                except Exception as e: 
                    if debug: print(e)
                while True:
                    ePas, vPas = passelWindow.read(timeout=100)
                    e, v = editorWindow.read(timeout=100)
                    if ePas == sg.WIN_CLOSED:
                        break
                    if ePas == 'passfile':
                        try:
                            file = open(sg.PopupGetFile('Path', save_as=False, no_window=True), 'r')
                            lines = file.readlines()
                            passwords = [line.strip() for line in lines]
                            file.close()
                            pasVal = ''
                            for password in passwords:
                                pasVal += password + '\n' 
                            passelWindow['passwords'].update(value=pasVal)
                        except Exception as e:
                            if debug: print(e)
                    if ePas == 'passel':
                        if passSelOn: 
                            passSelOn = False
                            time.sleep(1)
                            # passelWindow['passel'].update('START')
                            passelWindow['passel'].update('НАЧАТЬ ПОДБОР')
                            if AcceptPasswd == 'serial error':
                                sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
                            elif AcceptPasswd == 'read error 1' or AcceptPasswd == 'read error 2':
                                sg.Popup(f"\nОшибка чтения COM порта (timeout)\n",keep_on_top=True)
                            elif AcceptPasswd == 'password error':
                                sg.Popup(f"\nОшибка при вводе пароля\n",keep_on_top=True)
                            elif AcceptPasswd != '':
                                AcceptPasswd = AcceptPasswd.upper()
                                sg.Popup(f"\nПароль {AcceptPasswd} найден!\n",keep_on_top=True)
                                editorWindow['password'].update(value=AcceptPasswd)
                                editorWindow['password_on'].update(value=True)
                                editorWindow['A2h_password'].update(value=AcceptPasswd)
                                editorWindow['A2h_password_on'].update(value=True)
                                passelWindow.close()
                            else: 
                                sg.Popup(f"\nПодходящий пароль отсутсвует в списке\n",keep_on_top=True)
                        else:
                            COM_PORT = v['comport']
                            passwords = vPas['passwords'].split('\n')
                            Passwords = []
                            for password in passwords:
                                password = password.strip()
                                if re.fullmatch(r'[0-9A-Fa-f]+',password):
                                    if len(password) < 8:
                                        password += '0'*(8-len(password))
                                    if len(password) > 8:
                                        password = password[:8]
                                    Passwords.append(password)
                            # print(Passwords)
                            passSelOn = True
                            passelWindow['passel'].update('ОТСАНОВИТЬ')
                            passSelTask = Thread(target=passSel,args=(Passwords, COM_PORT, ''))
                            passSelTask.start()
                    if ePas == '__TIMEOUT__':
                        try:
                            if not passSelTask.is_alive() and passSelOn:
                                passSelOn = False
                                passelWindow['passel'].update('НАЧАТЬ ПОДБОР')
                                if AcceptPasswd == 'serial error':
                                    sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
                                elif AcceptPasswd == 'read error 1' or AcceptPasswd == 'read error 2':
                                    sg.Popup(f"\nОшибка чтения COM порта (timeout)\n",keep_on_top=True)
                                elif AcceptPasswd == 'password error':
                                    sg.Popup(f"\nОшибка при вводе пароля\n",keep_on_top=True)
                                elif AcceptPasswd != '':
                                    AcceptPasswd = AcceptPasswd.upper()
                                    sg.Popup(f"\nПароль {AcceptPasswd} найден!\n",keep_on_top=True)
                                    editorWindow['password'].update(value=AcceptPasswd)
                                    editorWindow['password_on'].update(value=True)
                                    passelWindow.close()
                                else: 
                                    sg.Popup(f"\nПодходящий пароль отсутсвует в списке\n",keep_on_top=True)
                        except Exception as e:
                            if debug: print(e)
            elif not A0h_available:
                sg.Popup(f"\nСтраница A0h EEPROM Недоступна!\n",keep_on_top=True)    
            else: 
                sg.Popup(f"\nСтраница A2h EEPROM Недоступна!\n",keep_on_top=True)    
        if e == 'i2cscan':
            COM_PORT = v['comport']
            i2c = i2cScan(COM_PORT,'')
            if i2c == 'serial error':
                sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
            elif i2c == 'read error 1' or i2c == 'read error 2':
                sg.Popup(f"\nОшибка чтения COM порта (timeout)\n",keep_on_top=True)
            else:
                if int.from_bytes(i2c[0].strip(),'big') != 0:
                    pages = []
                    for i in range(len(i2c)):
                        i2c[i] = int.from_bytes(i2c[i].strip(),'big')
                    if 80 in i2c: 
                        A0h_available = True
                        editorWindow['i2c_A0h'].update(text_color='#008000')
                    else:
                        A0h_available = False
                        editorWindow['i2c_A0h'].update(text_color='#FF0000')
                    if 81 in i2c: 
                        A2h_available = True
                        editorWindow['i2c_A2h'].update(text_color='#008000')
                    else:
                        A2h_available = False
                        editorWindow['i2c_A2h'].update(text_color='#FF0000')
                else:
                    editorWindow['i2c_A2h'].update(text_color='#FF0000')
                    editorWindow['i2c_A0h'].update(text_color='#FF0000')
        if e == 'resize':
            if editorWindowResize:
                editorWindow.size=(917,308)
                editorWindow['resize'].Update(' ▲ ')
                editorWindowResize = False
            else:
                editorWindow.size=(917,48)
                editorWindow['resize'].Update(' ▼ ')
                editorWindowResize = True
        if e == 'comport':
            comlist = serial.tools.list_ports.comports()
            COMS = []
            _,val = editorWindow.read(timeout=5)
            for el in comlist:
                COMS.append(el.device)
            COM_PORT = val['comport']
            editorWindow['comport'].update(value=COM_PORT if COM_PORT in COMS else '',values=COMS)
            try:
                SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
                SFP.write(b'\x00')
                SFP.close()
                editorWindow['A2h_comport'].update(value=v['comport'])
                editorWindow['A2h_password'].update(value=v['password'])
                editorWindow['A2h_password_on'].update(value=v['password_on'])
            except serial.serialutil.SerialException:
                pass
        if e == 'password_on':
            if v['password_on']:
                if len(v['password']) != 8: 
                    sg.Popup(f'\nПроверьте правильность пароля\n(8 символов HEX)\n',keep_on_top=True)
                    editorWindow['password_on'].update(value=False)
        if e == 'password':
            editorWindow['password_on'].update(value=False)
        if e == 'about':
            layout_about = [
                [sg.Text(f'Программатор SFP/SFP+ модулей v{release_version}')],
                [sg.Text('Разработал ZemtsovVA')],
                [sg.Text(email, key='email', text_color='blue', font='Arial 12 underline', enable_events=True, tooltip='Скопировать')],
                [sg.Text('F1: изменить тему')],
                [sg.Button('OK', key='close_about', s=(20,1))]
            ]
            aboutWindow = sg.Window('О программе', layout_about, finalize=True, element_justification='center')
            aboutWindow.make_modal()
            while True:
                eAbout,_ = aboutWindow.read()
                if eAbout == sg.WIN_CLOSED or eAbout == 'close_about':
                    aboutWindow.close()
                    break
                if eAbout == 'email':
                    os.system('echo ' + email.strip() + '\r| clip')
                    sg.Popup('Скопировано!')
                    aboutWindow.close()
                    break
        if e == 'F1:112':
            if theme_choise >= len(fav_themes): theme_choise = 1
            sg.theme(themes[fav_themes[theme_choise]])
            editorWindow.refresh()
            print(f'Активная тема: {fav_themes[theme_choise]}')
            editorWindow.close()
            editorWindow = createWindow()
            editorWindow.set_icon(icon='app_icon.ico')
            file_handler = open('theme.cfg', 'w+')
            file_handler.write(str(fav_themes[theme_choise]))
            file_handler.close()
            theme_choise += 1                    
        if e == 'A2h_read':
            if A2h_available:
                COM_PORT = v['A2h_comport']
                data_byte = A2h_read(COM_PORT, '')
                A2hFirmwareOriginal = b''
                if data_byte == 'serial error':
                    sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
                elif data_byte == 'read error 1' or data_byte == 'read error 2':
                    sg.Popup(f"\nОшибка чтения COM порта (timeout)\n", keep_on_top=True)
                elif data_byte == 'read error 3': sg.Popup(f"\nОшибка чтения байта (UnicodeDecodeError)\n")
                elif data_byte == 'read error 4': sg.Popup(f"\nОшибка чтения байта (ValueError)\n")
                else:
                    openA2hBIN(data_byte)
                    _,v = editorWindow.read(timeout=5)
                    detectFirmwareA2h(v)
                    A2hFirmwareOriginal = copy.copy(data_byte)
            else: sg.Popup(f"\nСтраница A2h EEPROM Недоступна!\n",keep_on_top=True)    
        if e == 'A2h_write':
            if A2h_available:
                firmware = saveA2hBIN(v)
                pass_on = v['A2h_password_on']
                if pass_on:
                    if len(v['A2h_password']) != 8 or not re.fullmatch(r'[0-9A-Fa-f]+',v['A2h_password']):
                        sg.Popup(f"\nПроверьте правильность введенного пароля\n",keep_on_top=True)
                        continue
                    else:
                        PassAr = [int(v['A2h_password'][x:x+2],16) for x in range(0,len(v['A2h_password']),2)]
                writeLayout = [[sg.Text('Запись прошивки в EEPROM...')],[sg.ProgressBar(1000, key='write_status', s=(36,20))],[sg.Button('НАЧАТЬ', key='start_write')]]
                writeWindow = sg.Window('Запись EEPROM SFP', writeLayout,finalize=True,keep_on_top=True)
                writeWindow.make_modal()
                while True:
                    eWr, vWr = writeWindow.read(timeout=100)
                    if eWr == sg.WIN_CLOSED:
                        writeOn = False
                        break
                    if eWr == 'start_write':
                        COM_PORT = v['A2h_comport']
                        writeWindow['start_write'].update(disabled=True)
                        writeTask = Thread(target=A2h_write, args=(COM_PORT, firmware, ''))
                        writeOn = True
                        writeTask.start()
                    if eWr == '__TIMEOUT__':
                        try:
                            if not writeTask.is_alive() and writeOn:
                                if writeResult == 'serial error':
                                    sg.Popup(f"\nПорт {COM_PORT} Недоступен\n",keep_on_top=True)
                                    writeWindow.close()
                                elif writeResult == 'read error 1' or writeResult == 'read error 2':
                                    sg.Popup(f"\nОшибка записи COM порта (timeout)\n",keep_on_top=True)
                                    writeWindow['start_write'].update(disabled=True)
                                elif writeResult == 'password error':
                                    sg.Popup(f"\nОшибка при вводе пароля\n",keep_on_top=True)
                                    writeWindow.close()
                                else:
                                    sg.Popup(f"\nУспешно записано {writtenBytes} байт в EEPROM!\n",keep_on_top=True)
                                    writeWindow.close()
                        except Exception as e:
                            if debug: print(e)
            else: sg.Popup(f"\nСтраница A2h EEPROM Недоступна!\n",keep_on_top=True) 
        if e == 'A2h_open':
            try:
                file_handler = open(sg.PopupGetFile('Path',file_types=(('BINARY','*.bin'),('All Files', '*.*')), no_window=True), 'rb')
                fw = file_handler.read()
                file_handler.close()
                openA2hBIN(fw)
                _,v = editorWindow.read(timeout=5)
                detectFirmwareA2h(v)
                A2hFirmwareOriginal = copy.copy(fw)
            except Exception as e: 
                if debug: print(e)
        if e == 'A2h_save':
            e,v = editorWindow.read(timeout=5)
            fw = saveBIN(v)
            try:
                file_handler = open(sg.PopupGetFile('Path', save_as=True,file_types=(('BINARY','*.bin'),('All Files', '*.*')), no_window=True, default_path='A2h_'+datetime.today().strftime("%Y-%m-%d-%H.%M.%S")), 'w+b')
                file_handler.write(fw)
                file_handler.close()
            except Exception as e: 
                if debug: print(e)
        if e == 'write_allow':
            for el in write_Allow:
                editorWindow[el].update(disabled = not v['write_allow'])
        if 'Table_A2h_' in e: 
            _,v = editorWindow.read(timeout=5)
            for i in range(255):
                v[f'Table_A2h_{i}'] = ''.join(re.findall(r'[a-fA-F0-9]',v[f'Table_A2h_{i}'].upper()))
                if len(v[f'Table_A2h_{i}']) > 2: v[f'Table_A2h_{i}'] = v[f'Table_A2h_{i}'][:2]
                editorWindow[f'Table_A2h_{i}'].update(value=v[f'Table_A2h_{i}'])  
                if v[f'Table_A2h_{i}'] == '': v[f'Table_A2h_{i}']='0'
            v['Table_A2h_95'] = hex(saveA2hBIN(v)[95])[2:].upper()
            editorWindow[f'Table_A2h_95'].update(value=v[f'Table_A2h_95']) 
            detectFirmwareA2h(v)
        if e in write_Allow2:
            _,v = editorWindow.read(timeout=5)
            if e in A2h_twos_comp:
                for el in A2h_twos_comp:
                    v[el] = ''.join(re.findall(r'[\-\.0-9]',v[el]))
                    try:
                        if float(v[el]) > 127.996: v[el]='127.996'
                        if float(v[el]) < -128.000: v[el]='-128.000'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el]=''
                    if v[el] == '': v[el]='0.000'
            if e in A2h_slope:
                for el in A2h_slope:
                    v[el] = ''.join(re.findall(r'[\.0-9]',v[el]))
                    try:
                        if float(v[el]) > 255.9961: v[el]='255.9961'
                        if float(v[el]) < 0: v[el]='0.0000'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el]=''
                    if v[el] == '': v[el]='0.0000'
            if e in A2h_float_4:
                for el in A2h_float_4:
                    v[el] = ''.join(re.findall(r'[\-e\.0-9]',v[el]))
                    try:
                        if float(v[el]) > struct.unpack('>f',b'\x7f\x7f\xff\xff')[0]: v[el]=str(struct.unpack('>f',b'\x7f\x7f\xff\xff')[0])
                        if float(v[el]) < 0.0: v[el]='0.0'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el] = ''
                    if v[el] == '': v[el]='0.0'
            # if e in A2h_unsign_short:
            #     for el in A2h_unsign_short:
            #         v[el] = ''.join(re.findall(r'[0-9]',v[el]))
            #         try:
            #             if int(v[el]) > 65535: v[el]='65535'
            #             if int(v[el]) < 0: v[el]='0'
            #             editorWindow[el].update(value=v[el])
            #         except:
            #             v[el] = ''
            #         if v[el] == '': v[el]='0'
            if e in A2h_voltage:
                for el in A2h_voltage:
                    v[el] = ''.join(re.findall(r'[0-9\.]',v[el]))
                    try:
                        if float(v[el]) > 6.55: v[el]='6.55'
                        if float(v[el]) < 0: v[el]='0.0'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el] = ''
                    if v[el] == '': v[el]='0.0'
            if e in A2h_current:
                for el in A2h_current:
                    v[el] = ''.join(re.findall(r'[0-9\.]',v[el]))
                    try:
                        if float(v[el]) > 131.0: v[el]='131.0'
                        if float(v[el]) < 0: v[el]='0.0'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el] = ''
                    if v[el] == '': v[el]='0.0'
            if e in A2h_power:
                for el in A2h_power:
                    v[el] = ''.join(re.findall(r'[0-9\.]',v[el]))
                    try:
                        if float(v[el]) > 6.5: v[el]='6.5'
                        if float(v[el]) < 0: v[el]='0.0'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el] = ''
                    if v[el] == '': v[el]='0.0'
            if e in A2h_sign_short:
                for el in A2h_sign_short:
                    v[el] = ''.join(re.findall(r'[\-0-9]',v[el]))
                    try:
                        if int(v[el]) > 32767: v[el]='32767'
                        if int(v[el]) < -32768: v[el]='-32768'
                        editorWindow[el].update(value=v[el])
                    except:
                        v[el] = ''
                    if v[el] == '': v[el]='0'
            if e in A2h_simple_byte:
                for el in A2h_simple_byte:
                    v[el] = ''.join(re.findall(r'[a-fA-F0-9]',v[el])).upper()
                    if len(v[el]) > 2: v[el] = v[el][:2]
                    editorWindow[el].update(value=v[el])  
                    if v[el] == '': v[el]='0'
            fw = createFirmwareA2h(v)
            openA2hBIN(fw)
            editorWindow['A2h_95'].update(value=hex(fw[95])[2:].upper())
        if e == 'A2h_password':
            v['A2h_password'] = ''.join(re.findall(r'[a-fA-F0-9]',v['A2h_password'])).upper()
            if len(v['A2h_password'])>8: v['A2h_password']=v['A2h_password'][:8]
            editorWindow['A2h_password'].update(value=v['A2h_password'])
            editorWindow['password'].update(value=v['A2h_password'])
        if e == 'A2h_password_on':
            editorWindow['password_on'].update(value=v['A2h_password_on'])         
        if e == 'password_on':
            editorWindow['A2h_password_on'].update(value=v['password_on'])    
        if e == 'A2h_comport':
            comlist = serial.tools.list_ports.comports()
            COMS = []
            _,val = editorWindow.read(timeout=5)
            for el in comlist:
                COMS.append(el.device)
            COM_PORT = v['A2h_comport']
            editorWindow['A2h_comport'].update(value=COM_PORT if COM_PORT in COMS else '',values=COMS)
            try:
                SFP = serial.Serial(COM_PORT, 115200, bytesize=8, parity="N", stopbits=1, timeout=1)
                SFP.write(b'\x00')
                SFP.close()
                editorWindow['comport'].update(value=v['A2h_comport'])
            except serial.serialutil.SerialException:
                pass
        if e == 'A0h_cisco_adapt_enable':
            if v['A0h_cisco_adapt_enable']:
                editorWindow['A0h_juniper_adapt_enable'].update(value=False)
                v['A0h_juniper_adapt_enable'] = False
                editorWindow['A0h_juniper_pn'].update(disabled=True)
                editorWindow['A0h_juniper_rev'].update(disabled=True)
                # pid = b''
                # for x in range(192,212,1):
                #     pid += bytes([int(v[f'A0h_{x}'],16)])
                vid = b''
                for x in range(148,152,1):
                    vid += bytes([int(v[f'A0h_{x}'],16)])
                # print(v['A0h_6'])
                pid = ciscoGetSFPType(v)['pid']
                
                editorWindow['A0h_cisco_pid'].update(value=pid)
                v['A0h_cisco_pid'] = pid
                # editorWindow['A0h_cisco_pid'].update(value=pid.decode('cp1251'))
                # v['A0h_cisco_pid'] = pid.decode('cp1251')
                editorWindow['A0h_cisco_vid'].update(value=vid.decode('cp1251') if vid in cisco_vids else cisco_vids[0])
                v['A0h_cisco_vid'] = vid.decode('cp1251') if vid in cisco_vids else cisco_vids[0]
                sfp_type = int(v['A0h_96']+v['A0h_97'],16)
                vendor_id = int(v['A0h_98'], 16)
                # try:
                #     editorWindow['A0h_cisco_sfp_type'].update(value=cisco_sfp_type[sfp_type])
                #     v['A0h_cisco_sfp_type'] = cisco_sfp_type[sfp_type]
                # except:
                sfpType = ciscoGetSFPType(v)['type']
                editorWindow['A0h_cisco_sfp_type'].update(value=sfpType)
                v['A0h_cisco_sfp_type'] = sfpType
                try:
                    editorWindow['A0h_cisco_vendor_id'].update(value=cisco_vendor_id[vendor_id])
                    v['A0h_cisco_vendor_id'] = cisco_vendor_id[vendor_id]
                except:
                    editorWindow['A0h_cisco_vendor_id'].update(value='Cisco')
                    v['A0h_cisco_vendor_id'] = 'Cisco'
                editorWindow['A0h_cisco_sfp_type'].update(disabled=False)
                editorWindow['A0h_cisco_vendor_id'].update(disabled=False)
                editorWindow['A0h_cisco_pid'].update(disabled=False)
                editorWindow['A0h_cisco_vid'].update(disabled=False)
                fw = saveBIN(v)
                openBIN(fw)

            else: 
                editorWindow['A0h_cisco_sfp_type'].update(disabled=True)
                editorWindow['A0h_cisco_vendor_id'].update(disabled=True)
                editorWindow['A0h_cisco_pid'].update(disabled=True)
                editorWindow['A0h_cisco_vid'].update(disabled=True)

        if e == 'A0h_cisco_sfp_type':
            a96 = hex(int(A0h_cisco_sfp_type_key[A0h_cisco_sfp_type_val.index(v['A0h_cisco_sfp_type'])],0).to_bytes(2,'big')[0])[2:].upper()
            if len(a96) < 2: a96 = '0'+a96
            a97 = hex(int(A0h_cisco_sfp_type_key[A0h_cisco_sfp_type_val.index(v['A0h_cisco_sfp_type'])],0).to_bytes(2,'big')[1])[2:].upper()
            if len(a97) < 2: a97 = '0'+a97
            editorWindow['A0h_96'].update(value=a96)
            v['A0h_96'] = a96
            editorWindow['A0h_97'].update(value=a97)
            v['A0h_97'] = a97
            fw = saveBIN(v)
            openBIN(fw)
        if e == 'A0h_cisco_vendor_id':
            a98 = hex(int(A0h_cisco_vendor_id_key[A0h_cisco_vendor_id_val.index(v['A0h_cisco_vendor_id'])],0))[2:].upper()
            if len(a98) < 2: a98 = '0'+a98
            editorWindow['A0h_98'].update(value=a98)
            v['A0h_98'] = a98
            fw = saveBIN(v)
            openBIN(fw)
        if e == 'A0h_cisco_pid':
            if len(v['A0h_cisco_pid']) > 20: 
                editorWindow['A0h_cisco_pid'].update(value=v['A0h_cisco_pid'][:20])
                v['A0h_cisco_pid'] = v['A0h_cisco_pid'][:20]
            pid = v['A0h_cisco_pid']
            if ('CWDM' in pid) or ('DWDM' in pid):
                pid = pid + v['A0h_60&A0h_61']
                editorWindow['A0h_cisco_pid'].update(value=pid)
                v['A0h_cisco_pid'] = pid
            i = 192
            for c in pid:
                v[f'A0h_{i}'] = c.encode('cp1251')
                i += 1
            if len(pid) < 20: 
                for n in range(20 - len(pid)):
                    v[f'A0h_{i}'] = ' '.encode('cp1251')
                    i += 1
            fw = saveBIN(v)
            openBIN(fw)
            # updUTF8(fw)
        if e == 'A0h_cisco_vid':
            if len(v['A0h_cisco_vid']) > 4: 
                editorWindow['A0h_cisco_vid'].update(value=v['A0h_cisco_vid'][:4])
                v['A0h_cisco_vid'] = v['A0h_cisco_vid'][:4]
            vid = v['A0h_cisco_vid']
            i = 148
            for c in vid:
                v[f'A0h_{i}'] = c.encode('cp1251')
                i += 1
            if len(vid) < 4: 
                for n in range(4 - len(vid)):
                    v[f'A0h_{i}'] = ' '.encode('cp1251')
                    i += 1
            fw = saveBIN(v)
            openBIN(fw)
            # updUTF8(fw)

        if e == 'A0h_juniper_adapt_enable':
            if v['A0h_juniper_adapt_enable']:
                editorWindow['A0h_cisco_adapt_enable'].update(value=False)
                v['A0h_cisco_adapt_enable'] = False
                editorWindow['A0h_cisco_sfp_type'].update(disabled=True)
                editorWindow['A0h_cisco_vendor_id'].update(disabled=True)
                editorWindow['A0h_cisco_pid'].update(disabled=True)
                editorWindow['A0h_cisco_vid'].update(disabled=True)
                pn = b''
                for x in range(96,107,1):
                    try:
                        pn += bytes([int(v[f'A0h_{x}'],16)])
                    except ValueError:
                        pn += b'\x00'
                rev = b''
                for x in range(107,113,1):
                    try:
                        rev += bytes([int(v[f'A0h_{x}'],16)])
                    except ValueError:
                        pn += b'\x00'
                try:
                    if pn.decode('cp1251') in juniper_pn:
                        editorWindow['A0h_juniper_pn'].update(value=pn.decode('cp1251'))
                        v['A0h_juniper_pn'] = pn.decode('cp1251')
                    else:
                        editorWindow['A0h_juniper_pn'].update(value=juniper_pn[0])
                        v['A0h_juniper_pn'] = juniper_pn[0]
                except:
                    editorWindow['A0h_juniper_pn'].update(value=juniper_pn[0])
                    v['A0h_juniper_pn'] = juniper_pn[0]
                try:
                    if rev.decode('cp1251') in juniper_rev:
                        editorWindow['A0h_juniper_rev'].update(value=rev.decode('cp1251'))
                        v['A0h_juniper_rev'] = rev.decode('cp1251')
                    else:
                        editorWindow['A0h_juniper_rev'].update(value=juniper_rev[0])
                        v['A0h_juniper_rev'] = juniper_rev[0]
                except:
                    editorWindow['A0h_juniper_rev'].update(value=juniper_rev[0])
                    v['A0h_juniper_rev'] = juniper_rev[0]
                editorWindow['A0h_juniper_pn'].update(disabled=False)
                editorWindow['A0h_juniper_rev'].update(disabled=False)
                fw = saveBIN(v)
                openBIN(fw)
            else: 
                editorWindow['A0h_juniper_pn'].update(disabled=True)
                editorWindow['A0h_juniper_rev'].update(disabled=True)
        if e == 'A0h_juniper_pn':
            if len(v['A0h_juniper_pn']) > 11: 
                editorWindow['A0h_juniper_pn'].update(value=v['A0h_juniper_pn'][:11])
                v['A0h_juniper_pn'] = v['A0h_juniper_pn'][:11]
            pn = v['A0h_juniper_pn']
            i = 96
            for c in pn:
                v[f'A0h_{i}'] = c.encode('cp1251')
                i += 1
            if len(pn) < 11: 
                for n in range(11 - len(pid)):
                    v[f'A0h_{i}'] = ' '.encode('cp1251')
                    i += 1
            fw = saveBIN(v)
            openBIN(fw)
        if e == 'A0h_juniper_rev':
            if len(v['A0h_juniper_rev']) > 6: 
                editorWindow['A0h_juniper_rev'].update(value=v['A0h_juniper_rev'][:6])
                v['A0h_juniper_rev'] = v['A0h_juniper_rev'][:6]
            rev = v['A0h_juniper_rev']
            i = 107
            for c in rev:
                v[f'A0h_{i}'] = c.encode('cp1251')
                i += 1
            if len(rev) < 6: 
                for n in range(6 - len(rev)):
                    v[f'A0h_{i}'] = ' '.encode('cp1251')
                    i += 1
            fw = saveBIN(v)
            openBIN(fw)
    except Exception as e: 
        if debug: print(e)
            
