+----------+------------------------------------------------------------+
| WebMoney Signer                                                       |
+==========+============================================================+
| Описание | Модуль для создания подписей с использованием файла ключей |
|          | WebMoney Keeper Classic                                    |
+----------+------------------------------------------------------------+
| Версия   | 0.1.1                                                      |
+----------+------------------------------------------------------------+

    Предназначен для взаимодействия с программными `X-интерфейсами`_
    WebMoney, `XML-интерфейсами`_ WebMoney Exchanger и др.

Установка
---------

.. code:: shell

    # через pip
    [sudo] pip3 install wmsigner

    # из репозитория
    git clone https://github.com/egorsmkv/wmsigner
    cd wmsigner
    [sudo] python setup.py install

Использование
-------------

.. code:: python

    from wmsigner import Signer

    # Файл ключей должен быть резервным, а не основным
    signer = Signer(wmid='000000000000',
                    keys='./data/000000000000.kwm',
                    password='************')
    signature = signer.sign('Данные, которые будут подписаны.')

Тесты
-----

Для запуска тестов необходимо изменить данные в файле `tests/test_signer.py`.

.. _X-интерфейсами: http://www.webmoney.ru/rus/developers/api.shtml
.. _XML-интерфейсами: http://wm.exchanger.ru/asp/rules_xml.asp
