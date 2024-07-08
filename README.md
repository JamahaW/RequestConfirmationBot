# Request Confirmation Bot

### Дискорд-бот для упрощения процесса подачи заявок и удобного интерфейса для их рассмотрения.

# Реализации

## NETHEX

`src/reqconfbot.bots.nethex.NethexBot`

### команды (все admin-only)

- `forms_output` - Указать канал нужно отправлять заявки на рассмотрение
- `commands_output` - Указать канал для отправки команд майнкрафт
- `commands_player_add` - Установить команды, которые будут отправлены при одобрении заявки
- `open_panel_creator` - Отправить в текущий канал сообщение с кнопкой для отправки заявок

## ZAPRETNIKI

`src/reqconfbot.bots.zapretniki.ZapretnikiBot`

### команды

- `coords_set_channel` (admin-only) - указать канал для вывода координат
- `coords` - Отправить в канал для координат оформленные значения координат

# Запуск

1. Создать файл `.env` и записать в него следующие переменные окружения:
    - `DISCORD_BOT_TOKEN` - Ваш токен дискорд бота
    - `DISCORD_BOT_PREFIX` - Любой префикс (Например `&`)
    - `LOG_FOLDER` - Путь в папке с логами (папка должна существовать)
    - `JSON_DATABASES_FOLDER` - Путь к каталогу JSON настроек экземпляров ботов (папка должна существовать)

2. Установить `Python 3.10`

3. Установить пакеты
    - `py-cord`
    - `dotenv-python`

4. В скрипте `src/main.py`
    - задать значение PATH_TO_DOT_ENV
    - выбрать реализацию бота

5. Запустить `src/main.py`