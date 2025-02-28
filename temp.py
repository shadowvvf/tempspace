import os
import time
import uuid
import platform
import subprocess
import shutil

def main():
    home_dir = os.path.expanduser("~")
    scripttemp_dir = os.path.join(home_dir, ".ScriptTemp")
    projects_dir = os.path.join(home_dir, "ScriptTemp_projects")

    if not os.path.exists(scripttemp_dir):
        os.makedirs(scripttemp_dir)
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)

    print("Проверка директорий на удаление...")
    for meta_file in os.listdir(scripttemp_dir):
        if meta_file.endswith(".meta"):
            meta_path = os.path.join(scripttemp_dir, meta_file)
            project_path = ""
            deletion_time = 0
            
            try:
                with open(meta_path, "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        project_path = lines[0].strip()
                        deletion_time = float(lines[1].strip())
                
                current_time = time.time()
                if deletion_time == -1 or (deletion_time > 0 and current_time > deletion_time):
                    if os.path.exists(project_path) and project_path.startswith(projects_dir):
                        print(f"Удаление устаревшей директории: {project_path}")
                        shutil.rmtree(project_path)
                    time.sleep(0.1)
                    try:
                        os.remove(meta_path)
                    except PermissionError:
                        print(f"Не удалось удалить мета-файл: {meta_path}")
            except Exception as e:
                print(f"Ошибка при обработке мета-файла {meta_file}: {e}")
                continue

    print("Создание новой временной директории проекта...")
    project_uuid = str(uuid.uuid4())
    project_path = os.path.join(projects_dir, project_uuid)
    os.makedirs(project_path)

    print(f"Открытие директории: {project_path}")
    try:
        if platform.system() == "Windows":
            os.startfile(project_path)
        elif platform.system() == "Darwin":
            subprocess.call(['open', project_path])
        else:  # Linux
            subprocess.call(['xdg-open', project_path])
    except Exception as e:
        print(f"Не удалось открыть директорию: {e}")

    print("Введите количество дней, через которое удалить эту директорию (0 — при следующем запуске): ")
    days_input = input()
    try:
        days = float(days_input)
    except ValueError:
        days = 0

    if days == 0:
        deletion_time = -1
    else:
        deletion_time = time.time() + days * 86400

    meta_file = os.path.join(scripttemp_dir, project_uuid + ".meta")
    with open(meta_file, "w") as f:
        f.write(project_path + "\n")
        f.write(str(deletion_time) + "\n")

    print(f"Временная директория проекта создана по адресу: {project_path}")
    print(f"Она будет удалена {'при следующем запуске' if days == 0 else f'через {days} дней'}.")

if __name__ == "__main__":
    main()