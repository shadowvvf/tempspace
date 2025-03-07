import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                              QVBoxLayout, QWidget, QTextEdit, QMessageBox, 
                              QInputDialog, QStatusBar, QHBoxLayout, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
import os
import time
import uuid
import shutil

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ScriptTemp Manager')
        self.setGeometry(100, 100, 800, 600)
        self.is_dark_theme = True
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create header
        header = QFrame()
        header.setFrameShape(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header)
        
        title = QLabel('ScriptTemp Manager')
        title.setStyleSheet('font-size: 24px; font-weight: bold;')
        header_layout.addWidget(title)
        
        theme_button = QPushButton('🌙 Dark Mode')
        theme_button.setFixedWidth(120)
        theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(theme_button, alignment=Qt.AlignRight)
        self.theme_button = theme_button
        
        main_layout.addWidget(header)
        
        # Create text area with styling
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setMinimumHeight(300)
        main_layout.addWidget(self.text_area)
        
        # Create button container
        button_container = QFrame()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(10)
        
        # Style for buttons
        button_style = '''
            QPushButton {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        '''
        
        # Create buttons
        create_button = QPushButton('📁 Create New Temporary Directory')
        create_button.clicked.connect(self.create_temp_directory)
        create_button.setStyleSheet(button_style)
        
        list_button = QPushButton('📋 List Temporary Directories')
        list_button.clicked.connect(self.list_temp_directories)
        list_button.setStyleSheet(button_style)
        
        delete_button = QPushButton('🗑️ Delete Temporary Directory')
        delete_button.clicked.connect(self.delete_temp_directory)
        delete_button.setStyleSheet(button_style)
        
        button_layout.addWidget(create_button)
        button_layout.addWidget(list_button)
        button_layout.addWidget(delete_button)
        
        main_layout.addWidget(button_container)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.setCentralWidget(main_widget)
        self.apply_theme()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        
    def apply_theme(self):
        if self.is_dark_theme:
            self.theme_button.setText('☀️ Light Mode')
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
                QTextEdit {
                    background-color: #34495e;
                    color: #ecf0f1;
                    border: 1px solid #7f8c8d;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                }
                QFrame {
                    background-color: #34495e;
                    border-radius: 5px;
                }
                QLabel {
                    color: #ecf0f1;
                }
                QStatusBar {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
            ''')
        else:
            self.theme_button.setText('🌙 Dark Mode')
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #f5f6fa;
                    color: #2c3e50;
                }
                QTextEdit {
                    background-color: white;
                    color: #2c3e50;
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                }
                QFrame {
                    background-color: white;
                    border-radius: 5px;
                }
                QLabel {
                    color: #2c3e50;
                }
                QStatusBar {
                    background-color: #f5f6fa;
                    color: #2c3e50;
                }
            ''')

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
        projects_dir = os.path.join(home_dir, 'ScriptTemp_projects')
        
        if not os.path.exists(scripttemp_dir) or not os.path.exists(projects_dir):
            self.text_area.append('No temporary directories found.')
            return
            
        self.text_area.clear()
        current_time = time.time()
        
        # Header
        self.text_area.append('📂 Temporary Directories List\n')
        self.text_area.append('=' * 80 + '\n')
        
        # Find all meta files
        meta_files = [f for f in os.listdir(scripttemp_dir) if f.endswith('.meta')]
        
        if not meta_files:
            self.text_area.append('No temporary directories found.')
            return
            
        for meta_file in sorted(meta_files):
            meta_path = os.path.join(scripttemp_dir, meta_file)
            try:
                with open(meta_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        project_path = lines[0].strip()
                        deletion_time = float(lines[1].strip())
                        
                        # Get directory info
                        dir_name = os.path.basename(project_path)
                        exists = os.path.exists(project_path)
                        time_left = deletion_time - current_time
                        
                        # Calculate size if directory exists
                        size_str = 'N/A'
                        if exists:
                            try:
                                total_size = sum(
                                    os.path.getsize(os.path.join(dirpath, filename))
                                    for dirpath, _, filenames in os.walk(project_path)
                                    for filename in filenames
                                )
                                # Convert to appropriate unit
                                for unit in ['B', 'KB', 'MB', 'GB']:
                                    if total_size < 1024:
                                        size_str = f"{total_size:.1f} {unit}"
                                        break
                                    total_size /= 1024
                            except Exception:
                                size_str = 'Error'
                        
                        # Format time remaining
                        if time_left <= 0:
                            time_str = '⚠️ Expired'
                            status = '🔴 To be deleted'
                        else:
                            days = int(time_left // 86400)
                            hours = int((time_left % 86400) // 3600)
                            minutes = int((time_left % 3600) // 60)
                            
                            if days > 0:
                                time_str = f"⏳ {days}d {hours}h remaining"
                            elif hours > 0:
                                time_str = f"⏳ {hours}h {minutes}m remaining"
                            else:
                                time_str = f"⏳ {minutes}m remaining"
                            
                            status = '🟢 Active' if exists else '🟡 Missing'
                        
                        # Format creation time
                        try:
                            creation_time = os.path.getctime(project_path)
                            creation_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
                        except:
                            creation_str = 'Unknown'
                        
                        # Output formatted information
                        self.text_area.append(f'Directory: {dir_name}')
                        self.text_area.append(f'Status: {status}')
                        self.text_area.append(f'Path: {project_path}')
                        self.text_area.append(f'Size: {size_str}')
                        self.text_area.append(f'Created: {creation_str}')
                        self.text_area.append(f'Time Status: {time_str}')
                        self.text_area.append('-' * 80 + '\n')
                        
            except Exception as e:
                self.text_area.append(f'Error reading directory info: {str(e)}\n')
                
        self.status_bar.showMessage('Directory list updated successfully', 3000)

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