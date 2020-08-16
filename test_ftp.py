import platform 
import subprocess  
import ftplib
import os
import sys

def ping(host):
    """
    Возращает true если ping успешный
    """
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def ftp_login(host):
    """
    Возвращает true если login успешный
    """
    try:
        ftp = ftplib.FTP(host)
        return ftp.login() == '230 Login successful.'

    except:
        return False

def check_connection(host):
    """
    Возвращает true если соединение установлено
    """
    try:
        ftp = ftplib.FTP(host)
        ftp.login()
        ftp.voidcmd('NOOP')
        return True
    except:
        return False

def get_size(filename):
    """
    Вспомогательная функция для сортировки файлов по размерам
    """
    try:
        ftp = ftplib.FTP('speedtest.tele2.net')
        ftp.login()
        return ftp.size(filename)
    except ftplib.error_perm:
        return float('inf')

def save_file(host, file_path):
    """
    Возвращает true если самый маленький файл с FTP сервера успешно сохранён
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        ftp = ftplib.FTP(host)
        ftp.login()
        filenames = ftp.nlst()
        filenames_by_size = sorted(filenames, key=get_size) # В порядке возрастания
        with open(file_path, 'wb') as f:
            ftp.retrbinary('RETR ' + filenames_by_size[0], f.write)

        if os.path.exists(file_path): # Очищает временные файлы
            os.remove(file_path)
            return True
        else:
            return False
    except:
        if os.path.exists(file_path):
            os.remove(file_path)
        return False

def upload_file(host):
    """
    Возвращает true если загрузка тестового файла прошла успешно
    """
    file_path = './test.txt'
    with open(file_path, 'w') as f: # Создание небольшого файла
        f.write("simple test")
    try:
        ftp = ftplib.FTP(host)
        ftp.login()
        
        with open(file_path, 'rb') as fobj:
            ftp.cwd('upload')
            ftp.storlines('STOR ' + file_path, fobj) # Сохранение как строчный файл

        if os.path.exists(file_path): # Очищает временные файлы
            os.remove(file_path)

        return True

    except:
        if os.path.exists(file_path): # Очищает временные файлы
            os.remove(file_path)
        return False

class TestFTP:
    """
    Тестовый класс для тестирования работы FTP сервера
    """
    def test_ping(self):
        assert ping('speedtest.tele2.net') == True
    
    def test_login(self):
        assert ftp_login('speedtest.tele2.net') == True
    
    def test_connection(self):
        assert check_connection('speedtest.tele2.net') == True

    def test_save_smallest(self):
        assert save_file('speedtest.tele2.net', './smallest.zip') == True
    
    def test_upload_file(self):
        assert upload_file('speedtest.tele2.net') == True
