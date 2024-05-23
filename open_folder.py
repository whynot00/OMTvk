import os, chardet

class OpenFolder:

    def __init__(self, path):
        self.__path = path
        self.__files = self.__get_filenames(self.__path)

    def __get_filenames(self, path) -> list:
        """получаем все файлы из дирректории с расширением .txt"""
        return [item for item in os.listdir(path) if os.path.splitext(item)[1] == ".txt"]

    def _open_txt(self, filename):
        """открываем файл"""

        filepath = self.__path_form(filename)

        encoding = self.__defenititon_encoding(filepath)
        with open(filepath, "r", encoding=encoding) as file:
            return file.readlines()
    
    def __path_form(self, filename) -> str:
        """формируем путь"""
        return f"vk_coresnpondence//{filename}"

    def __defenititon_encoding(self, filepath):
        rawdata = open(filepath, "rb").readline()
        encoding = chardet.detect(rawdata)['encoding']
        return encoding if encoding not in ("ascii", "MacCyrillic") else None

    @property
    def files(self):
        return self.__files