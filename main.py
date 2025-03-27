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

def create_steamcmd_script(install_dir_server, download_temp_dir, appid_server, appid_workshop, mod_ids):
    commands = [
        f"force_install_dir {install_dir_server}",
        f"app_update {appid_server} validate",
        f"force_install_dir {download_temp_dir}"
    ]
    commands += [f"workshop_download_item {appid_workshop} {mod}" for mod in mod_ids]
    commands.append("quit")
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
        mod_ids=mods["mod_ids"]
    )

    with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as tmpfile:
        tmpfile.write(script_content)
        script_path = tmpfile.name

    process = subprocess.Popen([
        steam["steamcmd_path"],
        "+login", steam["username"],
        "+runscript", script_path
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print("🚀 Запуск SteamCMD...\n")

    for line in iter(process.stdout.readline, ''):
        print(line.strip())

    process.wait()
    os.remove(script_path)

    print("📂 Копирование модов...")
    copy_mods(
        appid_workshop=steam["appid_workshop"],
        mod_ids=mods["mod_ids"],
        source_dir=paths["download_temp_dir"],
        target_dir=paths["server_mods_dir"]
    )

    print("\n✅ Завершено.")

if __name__ == "__main__":
    main()
