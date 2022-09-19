import os
import shutil


class LogFile:
    """
    Klasa do obsługi plików .log
    """

    def __init__(self, _path_log):
        """
        Konstruktor klasy
        :param _path_log: lokalizacja pliku
        :type _path_log: str
        """
        self.read_log_lines = None
        self.path_log = _path_log

    def read_file(self):
        """
        Metoda która wczytuje plik
        :return:
        """
        f = open(self.path_log, "r")
        self.read_log_lines = f.readlines()

    def delete_file(self):
        """
        Metoda do usuwania pliku
        :return:
        """
        os.remove(self.path_log)

    def move_file_to_archive(self):
        """
        Metoda do przenoszenia loga do archiwum
        :return:
        """
        original = self.path_log
        target = 'Archive_log\{}'.format(self.path_log)

        shutil.move(original, target)

    def get_mac_from_log(self):
        """
        Metoda do odczytywania adresu MAC z loga programowania
        :return: adres MAC
        :rtype: str
        """
        _line_with_mac = self.read_log_lines[9]
        _split_line_mac = _line_with_mac.split(',')
        _mac = _split_line_mac[2].strip()
        return _mac



def main():
    log = LogFile("mac_2022-09-16_123929.log")
    log.read_file()
    for line in log.read_log_lines:
        data = line.split(',')
        print(data[1])
    print(len(log.read_log_lines))
    # log.get_mac_from_log()
    # log.move_file_to_archive()


if __name__ == '__main__':
    main()
