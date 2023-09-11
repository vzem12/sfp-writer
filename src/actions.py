import PySimpleGUI as sg
from bitsOper import *
from A0h import *
from A2h import *
from threading import Thread
import serial
import serial.tools.list_ports
import time
import math
import re
from threading import Thread
import colorama
from colorama import Fore, Back, Style
from image import *

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

def SFP_write(COM_PORT, firmware, parent): 
    global writeResult, writeOn
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
                    SFP.write(bytes([i]))
                    if debug: print(f'{parent}Отправлен адрес смещения {hex(i)} {INFO} INFO {RST}')
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
                            if debug: print(f'{parent}Адрес смещения {hex(i)} успешно отправлен! {OK} OK {RST}')
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

def openBIN(data_byte):
    for i in range(96,256,1):
        vsWindow[f'A0h_{i}'].update(value='')
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
    editorWindow['A0h_vendorName'].update(value=data_byte[20:36].decode('ascii').strip())
    editorWindow['A0h_36'].update(value=data_byte[36])
    editorWindow['A0h_62'].update(value=data_byte[62])
    editorWindow['A0h_vendorOUI_1'].update(value=hex(data_byte[37])[2:].upper() if len(hex(data_byte[37])[2:])>1 else '0'+hex(data_byte[37])[2:].upper())
    editorWindow['A0h_vendorOUI_2'].update(value=hex(data_byte[38])[2:].upper() if len(hex(data_byte[38])[2:])>1 else '0'+hex(data_byte[38])[2:].upper())
    editorWindow['A0h_vendorOUI_3'].update(value=hex(data_byte[39])[2:].upper() if len(hex(data_byte[39])[2:])>1 else '0'+hex(data_byte[39])[2:].upper())
    editorWindow['A0h_vendorPN'].update(value=data_byte[40:56].decode('ascii').strip())
    editorWindow['A0h_vendorRev'].update(value=data_byte[56:60].decode('ascii').strip())
    editorWindow['A0h_vendorSN'].update(value=data_byte[68:84].decode('ascii').strip())
    editorWindow['A0h_year'].update(value=data_byte[84:86].decode('ascii').strip())
    editorWindow['A0h_month'].update(value=data_byte[86:88].decode('ascii').strip())
    editorWindow['A0h_day'].update(value=data_byte[88:90].decode('ascii').strip())
    editorWindow['A0h_vSpec'].update(value=data_byte[90:92].decode('ascii').strip())
    for i in range(96,len(data_byte),1):
        vsWindow[f'A0h_{i}'].update(value=hex(data_byte[i])[2:].upper() if len(hex(data_byte[i])[2:])==2 else '0'+hex(data_byte[i])[2:].upper())

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
    firmware += vName.encode('ascii') + bytes([int(v['A0h_36']) if v['A0h_36'] != '' else 0]) + vOUI + vPN.encode('ascii') + vRev.encode('ascii')
    firmware += int(v['A0h_60&A0h_61'].strip()).to_bytes(2,'big') if v['A0h_60&A0h_61'].strip() != '' else b'\x00\x00'
    firmware += bytes([int(v['A0h_62']) if v['A0h_62'] != '' else 0])
    firmware += CRC(firmware)
    firmware += bytes([bitsConvert([k64[v64.index(x)] for x in v['A0h_64']])])
    firmware += bytes([bitsConvert([k65[v65.index(x)] for x in v['A0h_65']])])
    firmware += bytes([int(v['A0h_66']) if v['A0h_66'] != '' else 0])
    firmware += bytes([int(v['A0h_67']) if v['A0h_67'] != '' else 0])
    vSN = v['A0h_vendorSN'].strip() if len(v['A0h_vendorSN'].strip()) == 16 else v['A0h_vendorSN'].strip() + (' ' * (16-len(v['A0h_vendorSN'].strip()))) if len(v['A0h_vendorSN'].strip()) < 16 else v['A0h_vendorSN'].strip()[:16]
    firmware += vSN.encode('ascii')
    year = v['A0h_year'].strip() if len(v['A0h_year'].strip()) > 1 else '0'+v['A0h_year'].strip() if len(v['A0h_year'].strip()) > 0 else '  '
    month = v['A0h_month'].strip() if len(v['A0h_month'].strip()) > 1 else '0'+v['A0h_month'].strip() if len(v['A0h_month'].strip()) > 0 else '  '
    day = v['A0h_day'].strip() if len(v['A0h_day'].strip()) > 1 else '0'+v['A0h_day'].strip() if len(v['A0h_day'].strip()) > 0 else '  '
    vSpec = '  ' if v['A0h_vSpec'].strip() == '' else v['A0h_vSpec'].strip() if len(v['A0h_vSpec'].strip()) > 1 else '0'+v['A0h_vSpec'].strip() if len(v['A0h_vSpec'].strip()) > 0 else '  '
    firmware += year.encode('ascii') + month.encode('ascii') + day.encode('ascii') + vSpec.encode('ascii')
    firmware += bytes([bitsConvert([k92[v92.index(x)] for x in v['A0h_92']])])
    firmware += bytes([bitsConvert([k93[v93.index(x)] for x in v['A0h_93']])])
    firmware += bytes([k94[v94.index(v['A0h_94'][0])] if len(v['A0h_94']) > 0 else 0])
    firmware += CRC(firmware[64:])
    otherBytes = b''
    for i in range(96,sfp_bytes_len,1):
        otherBytes += bytes([int(v[f'A0h_{i}'][:2],16)])
    firmware += otherBytes
    return firmware
