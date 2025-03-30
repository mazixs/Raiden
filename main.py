# main.py
import subprocess
import tempfile
import shutil
import os
import tomllib
import re

def load_config(path="config.toml") -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)

def create_steamcmd_script(install_dir_server, download_temp_dir, appid_server, appid_workshop, mod_ids, download_server, update_server, enable_mods, username, password):
    commands = [
        f"force_install_dir {install_dir_server}",
        f"login {username} {password}"
    ]
    
    if download_server or update_server:
        commands.append(f"app_update {appid_server} validate")
    
    if enable_mods:
        commands += [
            f"force_install_dir {download_temp_dir}",
            *[f"workshop_download_item {appid_workshop} {mod}" for mod in mod_ids]
        ]
    
    commands.append("quit")
    commands.append("quit") # Ensure quit is the last command
    return "\n".join(commands)

def get_mod_name(mod_path):
    meta_path = os.path.join(mod_path, "meta.cpp")
    if not os.path.isfile(meta_path):
        return None
    with open(meta_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    match = re.search(r'name\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1).replace(" ", "_")
    return None

def copy_mods(appid_workshop, mod_ids, source_dir, target_dir):
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)
    print(f"ℹ️  Целевая директория модов: {target_dir}")

    for modid in mod_ids:
        source = os.path.join(source_dir, "steamapps", "workshop", "content", str(appid_workshop), str(modid))
        if not os.path.exists(source):
            print(f"❌ Мод {modid} не найден по пути: {source}")
            continue

        mod_name = get_mod_name(source)
        if not mod_name:
            print(f"⚠️  Не удалось определить имя мода {modid}, используется ID.")
            mod_name = modid

        target = os.path.join(target_dir, f"@{mod_name}")

        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"✅ Мод {modid} скопирован в {target}")

def main():
    config = load_config()

    steam = config["steam"]
    server = config["server"]
    paths = config["paths"]
    mods = config["mods"]

    script_content = create_steamcmd_script(
        install_dir_server=server["install_dir"],
        download_temp_dir=paths["download_temp_dir"],
        appid_server=steam["appid_server"],
        appid_workshop=steam["appid_workshop"],
        mod_ids=mods["mod_ids"],
        download_server=server["download_server"],
        update_server=server["update_server"],
        enable_mods=mods["enable_mods"],
        username=steam["username"],
        password=steam["password"]
    )

    with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as tmpfile:
        tmpfile.write(script_content)
        script_path = tmpfile.name

    process = subprocess.Popen(
        [steam["steamcmd_path"], "+runscript", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1 # Force line buffering
    )

    print("🚀 Запуск SteamCMD...\n")

    for line in iter(process.stdout.readline, ''):
        print(line.strip(), flush=True) # Revert to readline with flush

    process.wait()
    os.remove(script_path)

    if mods["enable_mods"]:
        if mods["enable_mods"]:
            print("📂 Копирование модов...")
            copy_mods(
                appid_workshop=steam["appid_workshop"],
                mod_ids=mods["mod_ids"],
                source_dir=paths["download_temp_dir"],
                target_dir=paths["server_mods_dir"]
            )
        else:
            print("⏩ Пропуск копирования модов (отключено в конфиге)")

    print("\n🔍 Проверка установки...")
    
    # Check server installation
    if server["download_server"] or server["update_server"]:
        server_exe_path = os.path.join(server["install_dir"], "arma3server_x64.exe")
        if os.path.exists(server_exe_path):
            print(f"✅ Файл сервера найден: {server_exe_path}")
        else:
            print(f"❌ Файл сервера НЕ найден: {server_exe_path}")
            
    # Check mods installation
    if mods["enable_mods"]:
        all_mods_found = True
        print(f"📂 Проверка модов в: {paths['server_mods_dir']}")
        if not os.path.exists(paths['server_mods_dir']):
             print(f"❌ Директория модов НЕ найдена: {paths['server_mods_dir']}")
             all_mods_found = False
        else:
            installed_mods = [d for d in os.listdir(paths['server_mods_dir']) if os.path.isdir(os.path.join(paths['server_mods_dir'], d)) and d.startswith('@')]
            print(f"  Найденные папки модов: {installed_mods}")
            
            for modid in mods["mod_ids"]:
                found = False
                # Attempt to find by ID in folder name (simple check)
                for mod_folder in installed_mods:
                    if str(modid) in mod_folder:
                        found = True
                        print(f"  ✅ Мод {modid} найден (папка: {mod_folder})")
                        break
                if not found:
                    # If not found by ID, try getting name from temp dir (if exists)
                    temp_mod_path = os.path.join(paths["download_temp_dir"], "steamapps", "workshop", "content", str(steam["appid_workshop"]), str(modid))
                    mod_name_from_meta = get_mod_name(temp_mod_path)
                    if mod_name_from_meta:
                         expected_folder = f"@{mod_name_from_meta}"
                         if expected_folder in installed_mods:
                             found = True
                             print(f"  ✅ Мод {modid} найден (папка по имени: {expected_folder})")
                         
                if not found:
                    print(f"  ❌ Мод {modid} НЕ найден в {paths['server_mods_dir']}")
                    all_mods_found = False

        if all_mods_found:
            print("✅ Все ожидаемые моды найдены.")
        else:
            print("❌ Не все ожидаемые моды найдены.")

    print("\n🏁 Процесс завершен.")

if __name__ == "__main__":
    main()
