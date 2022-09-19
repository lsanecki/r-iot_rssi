from database import Database


# riot_prog gxiFLJb6JRQ5sg9U
# riot_test NO0abCFC6o63PXrb
class DbRiot(Database):
    def __init__(self):
        _host = "10.10.100.99"
        _user = "riot_prog"
        _password = "gxiFLJb6JRQ5sg9U"
        _database = "iir"
        super().__init__(_host, _user, _password, _database)
        self.client = "SweIoT"
        self.product = "R-IOT*"

    def generate_sql_query(self):
        pass

    def read_id_main(self, _serial_number):
        """
        Metoda do odczytu ID z tabeli Main na podstawie SN
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwraca numer ID z tabeli Main
        :rtype: str
        """
        _sql = "SELECT ID  FROM `Main` " \
               "WHERE `Serial` LIKE '{}' AND `Klient` LIKE '{}' AND `Wyrób` LIKE '{}' ORDER BY `ID`  DESC" \
            .format(_serial_number, self.client, self.product)
        _status, _my_result = self.select(_sql)
        if _status and len(_my_result) > 0:
            return _my_result[0][0]
        return

    def insert_record_to_main(self, _serial_number):
        """
        Metoda ktora zapisuje rekord do tabeli main
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwrana nr ID w tabeli Main
        :rtype: int
        """
        _id_main = self.read_id_main(_serial_number)
        if _id_main is None:
            _sql = "INSERT INTO `Main` (`Serial`, `Klient`, `Wyrób`) VALUES ('{}', '{}', '{}');" \
                .format(_serial_number, self.client, self.product)
            _status, _my_result = self.insert(_sql)
            if _status:
                _id_main = self.read_id_main(_serial_number)
        return _id_main

    def count_prog(self, _serial_number):
        """
        Metoda która sprawdza ile dany wyrob byl programowany
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwraca ilosc programowan danego produktu
        :rtype: int
        """
        _sql = "SELECT COUNT(*)  FROM `Programowanie` WHERE `Serial` LIKE '{}' ORDER BY `ID_prog`  DESC" \
            .format(_serial_number)
        _status, _my_result = self.select(_sql)
        if _status and len(_my_result) > 0:
            return _my_result[0][0]
        return

    def insert_record_to_prog_table(self, _id_main, _serial, _name_device, _soft, _check_sum_soft, _status,
                                    _error_code):
        """
        Metoda do zapisu rekordu w tabeli programowanie
        :param _id_main: Nr id w tabeli Main
        :type _id_main: int
        :param _serial: Numer SN produktu
        :type _serial: str
        :param _name_device: Nazwa urzadzenia
        :type _name_device: str
        :param _soft: Soft ktorym byl programowany wyrob
        :type _soft: str
        :param _check_sum_soft: suma kontrolna SHA1 softu
        :type _check_sum_soft: str
        :param _status: Status czy produkt został poprawnie zaprogramowany
        :type _status: str
        :param _error_code: Kod bledu
        :type _error_code: str
        :return:
        """
        _count_prog = self.count_prog(_serial) + 1
        _sql = "INSERT INTO `Programowanie` " \
               "(`ID_prog`, `ID`, `Serial`, `Status`, `Ilosc_prob`, `Nazwa_urzadzenia`, `Dodatkowe_dane`," \
               " `Soft1`, `CheckSum1`, `Soft2`, `CheckSum2`, `Soft3`, `CheckSum3`, `Soft4`, `CheckSum4`, `Data`," \
               " `Blad`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', 'RIOT', '{}', '{}'," \
               " NULL, NULL, NULL, NULL, NULL, NULL, CURRENT_TIMESTAMP, '{}');"\
            .format(_id_main, _serial, _status, _count_prog, _name_device, _soft, _check_sum_soft, _error_code)
        print(_sql)
        _status, _my_result = self.insert(_sql)

    def insert_record_riot_table(self, _serial_number, _address_mac):
        """
        Metoda do zapisu rekordu w tabeli R-IOT
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :param _address_mac: Adres MAC produktu
        :type _address_mac: str
        :return:
        """
        if self.count_riot_table(_serial_number) == 0:
            _sql = "INSERT INTO `R-IOT` (`ID`, `Serial`, `MAC`) VALUES (NULL, '{}', '{}');"\
                .format(_serial_number, _address_mac)
        else:
            _sql = "UPDATE `R-IOT` SET `MAC` = '{}' WHERE `R-IOT`.`Serial` = '{}';"\
                .format(_address_mac, _serial_number)
        _status, _my_result = self.insert(_sql)

    def count_riot_table(self, _serial_number):
        """
        Metoda sprawdza ile jest rekordow z danym SN w tabeli
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwraca ilość rekordów z danym SN
        :rtype: int
        """
        _sql="SELECT COUNT(*)  FROM `R-IOT` WHERE `Serial` LIKE '{}'".format(_serial_number)
        _status, _my_result = self.select(_sql)
        if _status and len(_my_result) > 0:
            return _my_result[0][0]
        return

    def save_to_db(self, _serial_number, _name_device, _soft, _check_sum_soft, _status, _error_code, _mac):
        """
        Metoda do zapisu wyniku programowania do bazy danych
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :param _name_device: Nazwa urzadzenia
        :type _name_device: str
        :param _soft: Soft ktorym byl programowany wyrob
        :type _soft: str
        :param _check_sum_soft: suma kontrolna SHA1 softu
        :type _check_sum_soft: str
        :param _status: Status czy produkt został poprawnie zaprogramowany
        :type _status: str
        :param _error_code: Kod bledu
        :type _error_code: str
        :param _mac: Adres MAC produktu
        :type _mac: str
        :return:
        """
        self.connect()
        _id_main = self.insert_record_to_main(_serial_number)
        self.insert_record_to_prog_table(_id_main, _serial_number, _name_device, _soft, _check_sum_soft, _status,
                                         _error_code)
        if _status == "OK":
            self.insert_record_riot_table(_serial_number, _mac)
        self.disconnect()



def main():
    db = DbRiot()
    sn = "123456789"
    name_device = "testowe_urzadzenie"
    soft = "undagrid_2_0.hex"
    check_sum = "33C9538C1C00A14D8F55F5EBD0ED548FA7CA26B4"
    mac="CB:5A:62:82:93:4F"
    db.save_to_db(sn, name_device, soft, check_sum, "NOK", "0", mac)



if __name__ == '__main__':
    main()
