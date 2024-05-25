import chardet

class OpenFolder:

    def __init__(self, paths):
        self.__files = list(paths)

    def _open_txt(self, filename):
        """открываем файл"""

        encoding = self.__defenititon_encoding(filename)
        with open(filename, "r", encoding=encoding) as file:
            return file.readlines()

    def __defenititon_encoding(self, filepath):
        rawdata = open(filepath, "rb").readline()
        encoding = chardet.detect(rawdata)['encoding']
        return encoding if encoding not in ("ascii", "MacCyrillic") else None

    @property
    def files(self):
        return self.__files
    
    @files.setter
    def files(self, value):
        self.__files.remove(value)

 
