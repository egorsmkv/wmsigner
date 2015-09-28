"""
WebMoney Signer

Модуль для создания подписей с использованием файла
ключей WebMoney Keeper Classic.

Пример:
    from wmsigner import Signer

    signer = Signer(wmid='000000000000',
                    keys='./data/000000000000.kwm',
                    password='************')
    signature = signer.sign('Данные, которые будут подписаны.')
"""

from .signer import Signer

__title__ = 'wmsigner'
__version__ = '0.1.1'
__author__ = 'Egor Smolyakov'
__license__ = 'MIT'
__credits__ = [
    'Andrei Baibaratsky (github.com/baibaratsky/php-wmsigner)'
]
