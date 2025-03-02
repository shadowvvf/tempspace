import os
import time
import uuid
import platform
import subprocess
import shutil

# ANSI escape codes for colors
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"

def main():
    while True:
        print(f"{GREEN}Меню:{RESET}")
        print(f"1. Создать новую временную директорию")
        print(f"2. Список временных директорий")
        print(f"3. Досрочное удаление временной директории")
        print(f"4. Выход")
        choice = input(f"{YELLOW}Выберите опцию: {RESET}")

        if choice == '1':
            create_temp_directory()
        elif choice == '2':
            list_temp_directories()
        elif choice == '3':
            delete_temp_directory()
        elif choice == '4':
            print(f"{GREEN}Выход...{RESET}")
            break
        else:
            print(f"{RED}Неверный выбор, попробуйте снова.{RESET}")

def create_temp_directory():
    home_dir = os.path.expanduser("~")
    scripttemp_dir = os.path.join(home_dir, ".ScriptTemp")
    projects_dir = os.path.join(home_dir, "ScriptTemp_projects")

    if not os.path.exists(scripttemp_dir):
        os.makedirs(scripttemp_dir)
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)

    print(f"{YELLOW}Создание новой временной директории...{RESET}")
    new_dir_name = str(uuid.uuid4())
    new_dir_path = os.path.join(projects_dir, new_dir_name)
    os.makedirs(new_dir_path)
    print(f"{GREEN}Временная директория создана: {new_dir_path}{RESET}")

    deletion_days = input(f"{YELLOW}Введите количество дней до удаления (или 0 для немедленного удаления): {RESET}")
    try:
        deletion_days = int(deletion_days)
        if deletion_days < 0:
            print(f"{RED}Ошибка: количество дней не может быть отрицательным.{RESET}")
            return
    except ValueError:
        print(f"{RED}Ошибка: введите корректное число.{RESET}")
        return

    meta_file = os.path.join(scripttemp_dir, new_dir_name + ".meta")
    with open(meta_file, "w") as f:
        f.write(new_dir_path + "\n")
        f.write(str(time.time() + deletion_days * 86400) + "\n")

    print(f"{GREEN}Временная директория будет удалена {'при следующем запуске' if deletion_days == 0 else f'через {deletion_days} дней'}.{RESET}")

def list_temp_directories():
    home_dir = os.path.expanduser("~")
    scripttemp_dir = os.path.join(home_dir, ".ScriptTemp")
    print(f"{YELLOW}Список временных директорий:{RESET}")
    for meta_file in os.listdir(scripttemp_dir):
        if meta_file.endswith(".meta"):
            meta_path = os.path.join(scripttemp_dir, meta_file)
            with open(meta_path, "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    project_path = lines[0].strip()
                    deletion_time = float(lines[1].strip())
                    print(f"{GREEN}Директория: {project_path}, Удаление через: {deletion_time}{RESET}")

def delete_temp_directory():
    home_dir = os.path.expanduser("~")
    scripttemp_dir = os.path.join(home_dir, ".ScriptTemp")
    projects_dir = os.path.join(home_dir, "ScriptTemp_projects")

    print(f"{YELLOW}Список временных директорий для удаления:{RESET}")
    for meta_file in os.listdir(scripttemp_dir):
        if meta_file.endswith(".meta"):
            meta_path = os.path.join(scripttemp_dir, meta_file)
            with open(meta_path, "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    project_path = lines[0].strip()
                    print(f"{GREEN}{project_path}{RESET}")

    dir_to_delete = input(f"{YELLOW}Введите имя директории для удаления: {RESET}")
    dir_to_delete_path = os.path.join(projects_dir, dir_to_delete)

    if os.path.exists(dir_to_delete_path):
        shutil.rmtree(dir_to_delete_path)
        os.remove(meta_path)
        print(f"{GREEN}Директория {dir_to_delete} успешно удалена.{RESET}")
    else:
        print(f"{RED}Директория {dir_to_delete} не найдена.{RESET}")

if __name__ == '__main__':
    main()