# Raiden for Arma 3

Этот проект представляет собой Python-скрипт для автоматической загрузки и установки модов из Steam Workshop для серверов Arma 3. Он написан для ОС Windows и взаимодействует со SteamCMD. 

## 🚀 Возможности

- Загрузка модов по Steam Workshop ID через SteamCMD.
- Поддержка кэшированной авторизации (без повторного ввода пароля при запуске).
- Автоматическая установка модов в директорию сервера с корректным названием (по данным из `meta.cpp`).
- Очистка временных файлов после выполнения.
- Простая конфигурация через `config.toml`.

## 🧰 Требования

- Python **3.13** и выше
- SteamCMD установлен локально
- Все используемые модули входят в стандартную библиотеку Python:
  - `subprocess`, `tempfile`, `shutil`, `os`, `tomllib`, `re`, `time`

## 📁 Структура проекта

```
.
├── main.py                 # основной исполняемый скрипт
├── config.toml            # конфигурация для запуска
├── README.md              # описание проекта
└── requirements.txt       # не обязателен (все зависимости встроены в Python)
```

## ⚙️ Пример конфигурации `config.toml`

```toml
[steam]
username = "MyLoginHere" # замени "MyLoginHere" на свой логин steam 
password = ""  # можешь оставить пустым, если используешь кэш 
appid_workshop = 107410
appid_server = 233780
steamcmd_path = "C:/steamcmd/steamcmd.exe"

[server]
install_dir = "C:/arma3server"

[mods]
mod_ids = [123123123, 123123123, 123123123]

[paths]
download_temp_dir = "C:/steamcmd/steam_temp" # место для загрузки
server_mods_dir = "C:/arma3server/mods"      # место для импорта
```

## 🔐 О кэшированной авторизации SteamCMD

SteamCMD после первого успешного входа с логином и паролем сохраняет **кэш авторизации** (внутри `steamcmd/config/`). Благодаря этому при следующих запусках можно:

- оставить поле `password = ""` пустым,
- не вводить 2FA-коды,
- запускать `steamcmd +login username` без запроса пароля и подтверждения.

**Важно:** кэш работает, пока используется тот же ПК и[ не сбро](https://developer.valvesoftware.com/wiki/SteamCMD)шены настройки/сессия SteamCMD.

## 🧪 Как создат[ь кэш пе](https://developer.valvesoftware.com/wiki/SteamCMD)ред использованием Raiden

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

После этого SteamCMD создаст кэш авторизации и Raiden сможет работать без пароля.

## 🔧 Использование

1. Установите [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD)
2. Настройте `config.toml` под себя
3. Убедитесь, что у вас установлен Python 3.13 и выше
4. Запустите:

```bash
python main.py
```

## ⚖️ Лицензия

Проект распространяется под лицензией **MIT**.

```
MIT License

Copyright (c) 2025 mazix

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👤 Автор

Разработано mazix — 2025. Если используете скрипт — оставьте упоминание в README вашего проекта 🙌