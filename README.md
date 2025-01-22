        Проект: Автоматизация обработки школьного расписания
Этот проект предназначен для автоматизации обработки, проверки и преобразования 
школьного расписания выгруженого из АВЕРС в различные форматы. Проект включает в себя несколько скриптов, 
которые взаимодействуют между собой для выполнения задач парсинга, проверки и преобразования данных.

    Описание проекта
        Проект состоит из следующих скриптов:
            rasp_to_json.py: Парсит CSV-файл с расписанием (rasp.csv) и преобразует его в JSON-файл (schedule.json).
            FindError.py: Проверяет расписание на наличие ошибок, используя список допустимых предметов из файла Spravosh.csv.
            json_to_GIS_SO.py: Преобразует JSON-файл с расписанием в CSV-файл для использования в системе GIS.
            Lider.py: Основной скрипт, который управляет выполнением всех вышеуказанных скриптов и логирует процесс.

    Требования
        Для работы проекта необходимы:
            Python 3.x
            Установленные библиотеки: json, csv, os, time, subprocess
            Все необходимые библиотеки входят в стандартную поставку Python, поэтому дополнительная установка не требуется.

    Установка
        Установка Python
            Если у вас еще не установлен Python, выполните следующие шаги:
                Для Linux (Ubuntu/Debian):
                    sudo apt update
                    sudo apt install python3 python3-pip
                Для macOS:
                    brew install python3
                Для Windows:
                    Скачайте установщик Python с официального сайта.
                    Запустите установщик и следуйте инструкциям. Убедитесь, что вы выбрали опцию "Add Python to PATH".
            После установки проверьте, что Python установлен:
                python --version
            
            Установка необходимых пакетов
                Проект использует стандартные библиотеки Python (json, csv, os, time, subprocess), 
                которые входят в стандартную поставку Python. Однако, если вы хотите убедиться, что 
                все зависимости установлены, выполните следующую команду:
                    pip install -r requirements.txt
    Клонирование репозитория
        Клонируйте репозиторий:
            git clone https://github.com/LeonArchie/journal_SO.git
        Убедитесь, что у вас есть файлы rasp.csv и Spravosh.csv в директории /home/archie/EDU/. 
        Если файлы находятся в другом месте, измените пути в скриптах.

    Использование
        Парсинг CSV-файла
            Для преобразования CSV-файла с расписанием в JSON-файл выполните:
                python3 rasp_to_json.py
                    Этот скрипт создаст файл schedule.json в директории /home/archie/EDU/.

        Проверка расписания на ошибки
            Для проверки расписания на наличие ошибок выполните:
                python3 FindError.py
                    Скрипт проверит расписание на наличие предметов, которые не указаны в списке 
                    допустимых (Spravosh.csv). В случае обнаружения ошибок, они будут записаны в 
                    файл error.txt, а соответствующие поля в расписании будут очищены.

        Преобразование JSON в CSV
            Для преобразования JSON-файла в CSV-файл выполните:
                python3 json_to_GIS_SO.py
                    Этот скрипт создаст файл GIS.csv в директории /home/archie/EDU/, 
                    который можно использовать в системе GIS.

        Основной скрипт управления
            Для автоматического выполнения всех шагов (парсинг, проверка, преобразование) используйте основной скрипт:
                python3 Lider.py
                    Этот скрипт:
                        Проверит наличие и корректность файлов.
                        Запустит все необходимые скрипты по очереди.
                        В случае обнаружения ошибок, процесс будет остановлен, и вы получите уведомление.

    Лицензия
        Проект распространяется под лицензией Apache License, Version 2.0. 
        Полный текст лицензии доступен по ссылке: http://www.apache.org/licenses/LICENSE-2.0.

        Краткое описание лицензии:
            Вы можете свободно использовать, модифицировать и распространять данный проект как 
            в коммерческих, так и в некоммерческих целях.
            Обязательным условием является указание авторства и сохранение уведомления об авторских правах.
            Лицензия не предоставляет гарантий на использование проекта, и авторы не несут ответственности 
            за возможные убытки или проблемы, возникшие в результате использования данного проекта.

                        Лицензионное уведомление:
                Copyright 2025 Petunin Lev Mikhailovish

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.

    Автор: Петунин Лев Михайлович
    Email: levmikhailovish@yandex.ru
    GitHub: https://github.com/LeonArchie
    Дата: 22.01.2025
    Версия: 1.0
        
        Если у вас возникли вопросы или предложения по улучшению проекта, пожалуйста, свяжитесь с автором.