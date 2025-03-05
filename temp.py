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
    home_dir = os.path.expanduser('~')
    projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')

    try:
        os.makedirs(projects_dir, exist_ok=True)
        temp_dir_name = str(uuid.uuid4())
        temp_dir_path = os.path.join(projects_dir, temp_dir_name)
        os.makedirs(temp_dir_path)
        # Open the directory in the file explorer
        subprocess.Popen(['explorer', temp_dir_path])
        print(f'Временная директория создана: {temp_dir_path}')
        return temp_dir_path
    except Exception as e:
        print(f'Ошибка при создании временной директории: {e}')

def list_temp_directories():
    home_dir = os.path.expanduser('~')
    projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')

    try:
        directories = os.listdir(projects_dir)
        if not directories:
            print('Нет временных директорий.')
            return
        print('Список временных директорий:')
        for directory in directories:
            meta_file = os.path.join(home_dir, '.ScriptTemp', directory + '.meta')
            if os.path.exists(meta_file):
                with open(meta_file, 'r') as f:
                    deletion_time = f.readline().strip()
                    print(f' - {directory}: Удаление запланировано на {time.ctime(float(deletion_time))}')
            else:
                print(f' - {directory}: Нет информации о времени удаления.')
    except Exception as e:
        print(f'Ошибка при получении списка временных директорий: {e}')

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