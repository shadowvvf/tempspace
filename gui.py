import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QMessageBox, QInputDialog, QStatusBar
import os
import time
import uuid
import shutil

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ScriptTemp Manager')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.text_area = QTextEdit(self)
        self.layout.addWidget(self.text_area)

        create_button = QPushButton('Создать новую временную директорию', self)
        create_button.clicked.connect(self.create_temp_directory)
        self.layout.addWidget(create_button)

        list_button = QPushButton('Список временных директорий', self)
        list_button.clicked.connect(self.list_temp_directories)
        self.layout.addWidget(list_button)

        delete_button = QPushButton('Досрочное удаление временной директории', self)
        delete_button.clicked.connect(self.delete_temp_directory)
        self.layout.addWidget(delete_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Create a status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def create_temp_directory(self):
        reply = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите создать новую временную директорию?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        home_dir = os.path.expanduser('~')
        scripttemp_dir = os.path.join(home_dir, '.ScriptTemp')
        projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')

        if not os.path.exists(scripttemp_dir):
            os.makedirs(scripttemp_dir)
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)

        custom_name, ok = QInputDialog.getText(self, 'Custom Name', 'Введите имя для временной директории:')
        if ok and custom_name:
            new_dir_name = custom_name
        else:
            new_dir_name = str(uuid.uuid4())
        new_dir_path = os.path.join(projects_dir, new_dir_name)
        os.makedirs(new_dir_path)

        deletion_days, ok = QInputDialog.getInt(self, 'Input', 'Введите количество дней до удаления (или 0 для немедленного удаления):')
        if ok:
            meta_file = os.path.join(scripttemp_dir, new_dir_name + '.meta')
            with open(meta_file, 'w') as f:
                f.write(new_dir_path + '\n')
                f.write(str(time.time() + deletion_days * 86400) + '\n')
            self.text_area.append(f'Временная директория создана: {new_dir_path}')
            self.status_bar.showMessage('Создание временной директории...')
            time.sleep(2)  # Simulating a delay
            self.status_bar.showMessage('Временная директория создана.')

    def list_temp_directories(self):
        home_dir = os.path.expanduser('~')
        scripttemp_dir = os.path.join(home_dir, '.ScriptTemp')
        self.text_area.append('Список временных директорий:')
        for meta_file in os.listdir(scripttemp_dir):
            if meta_file.endswith('.meta'):
                meta_path = os.path.join(scripttemp_dir, meta_file)
                with open(meta_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        project_path = lines[0].strip()
                        deletion_time = float(lines[1].strip())
                        self.text_area.append(f'Директория: {project_path}, Удаление через: {deletion_time}')

    def delete_temp_directory(self):
        reply = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите удалить эту временную директорию?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            home_dir = os.path.expanduser('~')
            scripttemp_dir = os.path.join(home_dir, '.ScriptTemp')
            projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')

            dir_to_delete, ok = QInputDialog.getText(self, 'Input', 'Введите имя директории для удаления:')
            if ok:
                dir_to_delete_path = os.path.join(projects_dir, dir_to_delete)
                if os.path.exists(dir_to_delete_path):
                    shutil.rmtree(dir_to_delete_path)
                    os.remove(os.path.join(scripttemp_dir, dir_to_delete + '.meta'))
                    self.text_area.append(f'Директория {dir_to_delete} успешно удалена.')
                    self.status_bar.showMessage('Директория удалена успешно.')
                else:
                    QMessageBox.warning(self, 'Ошибка', f'Директория {dir_to_delete} не найдена.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 