# Raiden for Arma 3 Server

Этот проект представляет собой Python-скрипт для автоматической загрузки, обновления и установки сервера Arma 3 и модов из Steam Workshop. Он написан для ОС Windows и взаимодействует со SteamCMD.

## 🚀 Возможности

- **Управление сервером:**
    - Загрузка/обновление выделенного сервера Arma 3 через SteamCMD.
    - Управление через флаги `download_server` и `update_server` в `config.toml`.
- **Управление модами:**
    - Загрузка/обновление модов по Steam Workshop ID через SteamCMD.
    - Включение/отключение установки модов через флаг `enable_mods` в `config.toml`.
    - Автоматическая установка модов в директорию сервера с корректным названием (по данным из `meta.cpp`, если возможно).
- **Общее:**
    - Поддержка кэшированной авторизации SteamCMD (без повторного ввода пароля).
    - Очистка временных файлов после выполнения.
    - Простая конфигурация через `config.toml`.
    - Финальная проверка наличия исполняемого файла сервера и папок установленных модов.

## 🧰 Требования

- Python **3.11** и выше (из-за `tomllib`)
- SteamCMD установлен локально
- Все используемые модули входят в стандартную библиотеку Python:
  - `subprocess`, `tempfile`, `shutil`, `os`, `tomllib`, `re`

## 📁 Структура проекта

```
.
├── main.py                # основной исполняемый скрипт
├── config.toml            # конфигурация для запуска
├── README.md              # описание проекта
└── LICENSE                # лицензия MIT
```

## ⚙️ Пример конфигурации `config.toml`

```toml
[steam]
username = "MyLoginHere"         # Логин Steam аккаунта
password = ""                    # Пароль (можно оставить пустым при использовании кэша)
appid_workshop = 107410          # ID ARMA 3 Workshop
appid_server = 233780            # ID ARMA 3 Server
steamcmd_path = "C:/steamcmd/steamcmd.exe"  # Путь к steamcmd.exe

[server]
install_dir = "C:/arma3server"   # Директория установки сервера
download_server = 1              # Скачивать сервер (1 - да, 0 - нет)
update_server = 1                # Обновлять сервер (1 - да, 0 - нет, если download_server=1, то обновление произойдет в любом случае)

[mods]
enable_mods = 1                  # Устанавливать моды (1 - да, 0 - нет)
mod_ids = [123123123, 123123123]  # ID модов из Workshop через запятую

[paths]
download_temp_dir = "C:/steamcmd/steam_temp"  # Временная директория для загрузок модов
server_mods_dir = "C:/arma3server/mods"       # Финальная директория модов на сервере
```

**Пояснения к флагам:**
- `download_server = 1`: Скачает сервер, если он не установлен. Если установлен, обновит его.
- `update_server = 1`: Обновит сервер, если он установлен. Не будет скачивать, если не установлен.
- `enable_mods = 1`: Включит загрузку и установку модов из списка `mod_ids`.

## 🔐 О кэшированной авторизации SteamCMD

SteamCMD после первого успешного входа с логином и паролем сохраняет **кэш авторизации** (внутри `steamcmd/config/`). Благодаря этому при следующих запусках можно:

- оставить поле `password = ""` пустым,
- не вводить 2FA-коды,
- запускать `steamcmd +login username` без запроса пароля и подтверждения.

**Важно:** кэш работает, пока используется тот же ПК и не сброшены настройки/сессия SteamCMD.

## 🧪 Как создать кэш перед использованием Raiden

Чтобы Raiden работал без необходимости вручную вводить логин и пароль при каждом запуске, нужно **однократно авторизоваться через SteamCMD вручную**:

1. Откройте консоль и выполните:
```bash
C:/steamcmd/steamcmd.exe
```
2. В появившемся интерфейсе SteamCMD введите:
```
login your_steam_username
```
3. Если потребуется, введите пароль и подтвердите через email или мобильное приложение Steam Guard.
4. После успешной авторизации вы увидите сообщение:
```
Logging in user 'your_steam_username' to Steam Public...OK
```
5. Введите `quit` и закройте SteamCMD.

После этого SteamCMD создаст кэш авторизации и Raiden сможет работать без пароля (если поле `password` в `config.toml` пустое).

## 🔧 Использование

1. Установите [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD)
2. Настройте `config.toml` под себя (пути, логин, ID модов, флаги управления).
3. Убедитесь, что у вас установлен Python 3.11 и выше.
4. Запустите скрипт из директории проекта:
```bash
python main.py
```
Скрипт выполнит действия согласно конфигурации (скачает/обновит сервер, скачает/установит моды) и выведет отчет о проверке в конце.

## ⚖️ Лицензия

Проект распространяется под лицензией **MIT**. См. файл `LICENSE`.

## 👤 Автор

Разработано mazix — 2025. Если используете скрипт — оставьте упоминание в README вашего проекта 🙌