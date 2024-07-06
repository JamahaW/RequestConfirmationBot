# Request Confirmation Bot

### Дискорд-бот для упрощения процесса подачи заявок и удобного интерфейса для их рассмотрения.

# Что нужно для запуска

1. Создать файл `.env` и записать в него следующие переменные окружения:
    - `DISCORD_BOT_TOKEN` - Ваш токен дискорд бота
    - `DISCORD_BOT_PREFIX` - Любой префикс (Например `&`)
    - `LOG_FOLDER` - Путь в папке с логами (папка должна существовать)
    - `JSON_DATABASES_FOLDER` - Путь к папке JSON базы бота

2. Установить пакеты
    - `py-cord`
    - `dotenv-python`

3. Запустить `src/main.py`
    - В этом файле также нужно указать путь к файлу `.env`

# Экземпляр для работы с заявками - NETHEX.

### Имеет следующие команды (admin-only)

- `forms_output` - Указать канал нужно отправлять заявки на рассмотрение
- `commands_output` - Указать канал для отправки команд майнкрафт
- `commands_player_add` - Установить команды, которые будут отправлены при одобрении заявки
- `open_panel_creator` - Отправить в текущий канал сообщение с кнопкой для отправки заявок
