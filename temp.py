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
    # Cleanup expired directories on startup
    cleanup_expired_directories()
    
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
    scripttemp_dir = os.path.join(home_dir, '.ScriptTemp')

    try:
        # Ensure the directories exist
        os.makedirs(projects_dir, exist_ok=True)
        os.makedirs(scripttemp_dir, exist_ok=True)
        
        # Ask for custom name using CLI input
        custom_name = input(f"{YELLOW}Введите имя для временной директории (или нажмите Enter для автоматического имени): {RESET}")
        
        if custom_name:
            new_dir_name = custom_name
        else:
            new_dir_name = str(uuid.uuid4())
            
        temp_dir_path = os.path.join(projects_dir, new_dir_name)
        os.makedirs(temp_dir_path)
        
        # Ask for deletion days
        while True:
            try:
                deletion_days = int(input(f"{YELLOW}Введите количество дней до удаления (или 0 для удаления при следующем запуске): {RESET}"))
                if deletion_days < 0:
                    print(f"{RED}Пожалуйста, введите положительное число.{RESET}")
                    continue
                break
            except ValueError:
                print(f"{RED}Пожалуйста, введите число.{RESET}")
        
        # Create meta file with deletion information
        meta_file = os.path.join(scripttemp_dir, new_dir_name + '.meta')
        with open(meta_file, 'w') as f:
            f.write(temp_dir_path + '\n')
            f.write(str(time.time() + deletion_days * 86400) + '\n')
        
        # Open the directory in the file explorer based on platform
        if platform.system() == 'Windows':
            subprocess.Popen(['explorer', temp_dir_path])
        elif platform.system() == 'Darwin':  # macOS
            subprocess.Popen(['open', temp_dir_path])
        else:  # Linux and others
            subprocess.Popen(['xdg-open', temp_dir_path])
            
        print(f'{GREEN}Временная директория создана: {temp_dir_path}{RESET}')
        print(f'{GREEN}Директория будет удалена через {deletion_days} дней.{RESET}')
        return temp_dir_path
    except Exception as e:
        if isinstance(e, FileExistsError):
            print(f'{RED}Ошибка: Директория уже существует: {e}{RESET}')
        elif isinstance(e, PermissionError):
            print(f'{RED}Ошибка: У вас нет разрешения на создание директории: {e}{RESET}')
        else:
            print(f'{RED}Ошибка при создании временной директории: {e}{RESET}')

def list_temp_directories():
    home_dir = os.path.expanduser('~')
    projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')
    scripttemp_dir = os.path.join(home_dir, '.ScriptTemp')

    try:
        if not os.path.exists(scripttemp_dir):
            os.makedirs(scripttemp_dir)
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)
            
        # Get the list of .meta files
        meta_files = [f for f in os.listdir(scripttemp_dir) if f.endswith('.meta')]
        
        if not meta_files:
            print(f"{YELLOW}Нет временных директорий.{RESET}")
            return
            
        current_time = time.time()
        print(f"\n{GREEN}=========== Список временных директорий ==========={RESET}")
        print(f"{GREEN}ID | Имя директории | Время до удаления | Статус{RESET}")
        print(f"{GREEN}----------------------------------------{RESET}")
        
        for idx, meta_file in enumerate(meta_files, 1):
            meta_path = os.path.join(scripttemp_dir, meta_file)
            with open(meta_path, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    project_path = lines[0].strip()
                    dir_name = os.path.basename(project_path)
                    deletion_time = float(lines[1].strip())
                    time_left = deletion_time - current_time
                    
                    # Check if directory exists
                    dir_exists = os.path.exists(project_path)
                    
                    # Format time remaining
                    if time_left <= 0:
                        time_str = f"{RED}Истек срок{RESET}"
                        status = f"{RED}На удаление{RESET}"
                    else:
                        days_left = int(time_left / 86400)
                        hours_left = int((time_left % 86400) / 3600)
                        time_str = f"{YELLOW}{days_left}д {hours_left}ч{RESET}"
                        status = f"{GREEN}Активен{RESET}" if dir_exists else f"{RED}Отсутствует{RESET}"
                    
                    print(f"{idx} | {dir_name} | {time_str} | {status}")
        print(f"{GREEN}=========================================={RESET}\n")
    except Exception as e:
        print(f'{RED}Ошибка при получении списка временных директорий: {e}{RESET}')

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
        try:
            shutil.rmtree(dir_to_delete_path)
            os.remove(meta_path)
            print(f'{GREEN}Директория {dir_to_delete} успешно удалена.{RESET}')
        except FileNotFoundError:
            print(f'{RED}Ошибка: Директория {dir_to_delete} не найдена для удаления.{RESET}')
        except Exception as e:
            print(f'{RED}Ошибка при удалении директории: {e}{RESET}')
    else:
        print(f"{RED}Директория {dir_to_delete} не найдена.{RESET}")

def cleanup_expired_directories():
    home_dir = os.path.expanduser('~')
    projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')
    current_time = time.time()
    for directory in os.listdir(projects_dir):
        meta_file = os.path.join(home_dir, '.ScriptTemp', directory + '.meta')
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                deletion_time = float(f.readline().strip())
                if current_time >= deletion_time:
                    shutil.rmtree(os.path.join(projects_dir, directory))
                    os.remove(meta_file)
                    print(f'{RED}Директория {directory} была удалена из-за истечения срока действия.{RESET}')

if __name__ == '__main__':
    main()