# RequestConfirmationBot

Дискорд-бот для упрощения процесса подачи заявок и удобного интерфейса для их рассмотрения.

# Что нужно для запуска

1. Создать файл `reqconfbot/.env` и записать в него следующие переменные окружения:
   - `DISCORD_BOT_TOKEN` - Ваш токен дискорд бота
   - `DISCORD_BOT_PREFIX` - Любой префикс (Например `&`)
   - `LOG_FOLDER` - Путь в папке с логами (папка должна существовать)
   - `JSON_DATABASE_PATH` - Путь к JSON-файлу конфигурации бота 
   (Должен существовать, инициализация как пустой словарь)
