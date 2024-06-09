# trading-bot-tinkoff

Торговый бот для брокера "Т-инвестиции" (бывший "Тинькофф инвестиции").

## Возможности

Данный бот позволяет автоматизировать выполнение торговых стратегий.

Сохранение и обновление информации о статусах торговых поручений может выполняться с помощью SQLite в базе данных, либо через telegram-бота в личном чате.

Модульная структура позволяет дополнять функционал бота, а также реализовывать собственные торговые стратегии.

В качестве примера представлена стратегия [sma](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/strategies/sma/strategy.py) на основе скользящих средних (не является индивидуальной инвестиционной рекомендацией).

## Структура приложения

![](/img/structure.png)

## Входные данные

Для работы торгового робота необходимо заполнить файлы [.env](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/.env) и [instruments.json](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/instruments.json) согласно представленным примерам.

#### Содержание файла [.env](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/.env):

* Токен инвестора. Можно получить в личном кабинете в приложении брокера.
* ID аккаунта. Можно оставить пустым - будет использоваться первый найденный аккаунт.
* SANDBOX. Если `FALSE`, то торговля будет вестись на реальном брокерском счёте. Значение по умолчанию - `TRUE`, дляторговли в "Песочнице".

#### Содержание файла [instruments.json](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/instruments.json):

* figi - идентификатор финансового иструмента
* strategy - параметры стратегии
    * name - название стратегии, согласно тому, как оно указано в [fabric.py](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/strategies/fabric.py)
    * parameters - набор параметров для работы стратегии
* statistics - параметры обработчика статистики
    * name - название обработчика, согласно тому, как оно указано в [handler.py](https://github.com/DarenskyRoman/trading-bot-tinkoff/blob/main/statistics/handler.py)
    * parameters - набор параметров для работы стратегии

## Запуск

1. Клонируйте репозиторий в любую папку на компьютере:

    ```bash
    git clone https://github.com/DarenskyRoman/trading-bot-tinkoff.git
    ```

2. Перейдите в папку с приложением:

    ```bash
    cd trading-bot-tinkoff
    ```

3. Установите необходимые зависимости:

    ```bash
    pip install -r trading-bot-tinkoff.txt
    ```

4.  Запустите приложение:

    ```bash
    python main.py
    ```

## Запуск через Docker

1. Клонируйте репозиторий в любую папку на компьютере:

    ```bash
    git clone https://github.com/DarenskyRoman/trading-bot-tinkoff.git
    ```

2. Перейдите в папку с приложением:

    ```bash
    cd trading-bot-tinkoff
    ```

3.  Создайте Docker image:

    ```bash
    docker build -t trading-robot-image .
    ```

4.  Запустите Docker container:

    ```bash
    docker run --name trading-robot-container trading-robot-image
    ```

## Отмена торговых поручений 

После остановки торгового бота может быть необходимо отменить все ещё неисполненные торговые поручения. Для этого, после остановки контейнера/системного процесса с ботом, нужно в терминале в папке с приложением выполнить:

```bash
python cancel_orders.py
```