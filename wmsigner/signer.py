import os
import hashlib
import random
from struct import Struct, pack, error

from .exceptions import SignerError


class Signer:
    """
    Класс, который выполняет все функции по созданию подписи для данных
    """

    def __init__(self, wmid, keys, password):
        if not (wmid and password):
            raise ValueError('WMID и/или пароль от файла ключей не установлен')

        self.wmid = wmid
        self.password = password
        self._power = 0
        self._modulus = 0

        if not os.path.isfile(keys):
            raise FileNotFoundError('Файл ключей не найден: %s' % keys)

        try:
            with open(keys, 'rb') as f:
                self.read_key_data(f.read())
        except IOError:
            raise IOError('Ошибка чтения из файла ключей')

    def sign(self, data, debug=False):
        """
        Создание подписи для переданных данных
        """

        if not isinstance(data, str):
            raise TypeError('Для подписи необходимо передавать строку')

        # Создание хэша для данных (16 байт)
        base = self.md4(data)

        if not debug:
            # Добавление 40 случайных байтов
            for _ in range(0, 10):
                base += pack('<L', random.randint(0, 65535))

        # Добавляем длину базы (56 = 16 + 40) как первые 2 байта
        base = pack('<H', len(base)) + base

        # Модульное возведение в степень
        dec = pow(self.reverse_to_decimal(base), self._power, self._modulus)

        # Преобразование в шестнадцатеричное представление
        hexadecimal = '{0:x}'.format(dec)

        # Заполнение пустых байтов нулями
        hexadecimal = '0' * (132 - len(hexadecimal)) + hexadecimal

        # Обратный порядок байт
        hex_reversed = ''
        for i in range(0, len(hexadecimal) // 4):
            mul = i * 4
            hex_reversed = hexadecimal[mul:mul + 4] + hex_reversed

        return hex_reversed.lower()

    def read_key_data(self, binary):
        """
        Чтение данных из файла ключей
        """

        size, data = self.unpack(binary, '< H H 16s L', without_size=False)
        payload = dict(reversed=data[0], signFlag=data[1], hash=data[2],
                       length=data[3], buffer=binary[size:])
        data = self.read_key_buffer(payload)
        if data is None:
            raise SignerError(
                'Проверка хэша не удалась, возможно файл ключей поврежден')

        self.sign_vars(data)

    def sign_vars(self, buff):
        """
        Получение значений `power` и `modulus`
        """

        _, power_len = self.unpack(buff, '< L H')
        _, _, power, mod_len = self.unpack(buff, '< L H %ds H' % power_len)
        _, _, _, _, modulus = self.unpack(
            buff, '< L H %ds H %ds' % (power_len, mod_len))

        self._power = self.reverse_to_decimal(power)
        self._modulus = self.reverse_to_decimal(modulus)

    def read_key_buffer(self, data):
        """
        Проверить буфер ключей и вернуть его, если он равен полученному хэшу
        """

        data['buffer'] = self.encrypt_key(data['buffer'])

        return data['buffer'] if self.verify_hash(data) else None

    def encrypt_key(self, buff):
        """
        Шифрование ключа
        """

        digest = self.md4(self.wmid + self.password)

        return self.xor_strings(buff, digest, 6)

    def verify_hash(self, data):
        """
        Проверка хэша ключа
        """

        verify = (pack('<H', data['reversed']) + pack('<H', 0) +
                  pack('<4L', 0, 0, 0, 0) + pack('<L', data['length']) +
                  data['buffer'])

        return self.md4(verify) == data['hash']

    @staticmethod
    def xor_strings(subject, modifier, shift=0):
        """
        Операция XOR для двух строк
        """

        subject, modifier = list(subject), list(modifier)
        i, j = shift, 0
        while len(subject) > i:
            subject[i] = subject[i] ^ modifier[j]
            i += 1
            j += 1
            if j >= len(modifier):
                j = 0

        return bytearray(subject)

    @staticmethod
    def reverse_to_decimal(value):
        """
        Преобразование двоичных данных в десятичную форму
        """

        return int.from_bytes(value, byteorder='little')

    @staticmethod
    def md4(value):
        """
        Хэширование строки алгоритмом MD4, который содержится в модуле OpenSSL
        """

        algorithm = hashlib.new('md4')

        if isinstance(value, bytes):
            algorithm.update(value)
        else:
            algorithm.update(str.encode(value))

        return algorithm.digest()

    @staticmethod
    def unpack(binary, fmt, without_size=True):
        """
        Получение данных из их бинарного представления
        """

        s = Struct(fmt)

        try:
            unpacked = s.unpack(binary[:s.size])
        except error:
            raise SignerError(
                'Ошибка при распаковке данных, возможно файл ключей поврежден')

        if without_size:
            return unpacked
        else:
            return s.size, unpacked
