#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎰 RULETTT Desktop Application
Полноценное Windows приложение для сбора и анализа данных рулетки
"""

import sys
import os
import threading
import webbrowser
from pathlib import Path

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QGroupBox, QSystemTrayIcon,
        QMenu, QAction, QStyle, QMessageBox, QTabWidget, QStatusBar
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
    from PyQt5.QtGui import QIcon, QFont, QTextCursor
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("❌ PyQt5 не установлен. Установите: pip install PyQt5 PyQtWebEngine")
    sys.exit(1)

# Импорт наших модулей
sys.path.append(str(Path(__file__).parent))

# Для запуска серверов
import subprocess
import socket


class ServerManager:
    """Управление API и Web серверами"""
    
    def __init__(self):
        self.api_process = None
        self.web_process = None
        self.api_port = 5000
        self.web_port = 8080
    
    def is_port_in_use(self, port):
        """Проверка занятости порта"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def start_api_server(self):
        """Запуск API сервера"""
        if self.is_port_in_use(self.api_port):
            return True, "API сервер уже запущен"
        
        try:
            api_script = Path(__file__).parent / "api_server.py"
            self.api_process = subprocess.Popen(
                [sys.executable, str(api_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return True, f"API сервер запущен на порту {self.api_port}"
        except Exception as e:
            return False, f"Ошибка запуска API: {e}"
    
    def start_web_server(self):
        """Запуск Web сервера"""
        if self.is_port_in_use(self.web_port):
            return True, "Web сервер уже запущен"
        
        try:
            webapp_dir = Path(__file__).parent / "webapp"
            self.web_process = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(self.web_port)],
                cwd=str(webapp_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return True, f"Web сервер запущен на порту {self.web_port}"
        except Exception as e:
            return False, f"Ошибка запуска Web: {e}"
    
    def stop_servers(self):
        """Остановка всех серверов"""
        if self.api_process:
            self.api_process.terminate()
            self.api_process = None
        if self.web_process:
            self.web_process.terminate()
            self.web_process = None
    
    def get_status(self):
        """Получить статус серверов"""
        api_status = "🟢 Работает" if self.is_port_in_use(self.api_port) else "🔴 Остановлен"
        web_status = "🟢 Работает" if self.is_port_in_use(self.web_port) else "🔴 Остановлен"
        return api_status, web_status


class LogEmitter(QObject):
    """Эмиттер для логов в GUI"""
    log_signal = pyqtSignal(str)


class RoulettDesktopApp(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        self.server_manager = ServerManager()
        self.log_emitter = LogEmitter()
        self.log_emitter.log_signal.connect(self.append_log)
        
        self.init_ui()
        self.init_tray()
        self.setup_status_timer()
        
        # Автозапуск серверов
        self.auto_start_servers()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("🎰 RULETTT - Система анализа рулетки")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Заголовок
        header = QLabel("🎰 RULETTT - Анализ данных рулетки")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Вкладки
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Вкладка 1: Управление
        control_tab = self.create_control_tab()
        tabs.addTab(control_tab, "📊 Управление")
        
        # Вкладка 2: Логи
        log_tab = self.create_log_tab()
        tabs.addTab(log_tab, "📋 Логи")
        
        # Вкладка 3: О программе
        about_tab = self.create_about_tab()
        tabs.addTab(about_tab, "ℹ️ О программе")
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово к работе")
        
        # Применяем стили
        self.apply_styles()
    
    def create_control_tab(self):
        """Создание вкладки управления"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Группа: Статус серверов
        status_group = QGroupBox("Статус серверов")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        self.api_status_label = QLabel("API Server: 🔴 Остановлен")
        self.web_status_label = QLabel("Web Server: 🔴 Остановлен")
        
        status_layout.addWidget(self.api_status_label)
        status_layout.addWidget(self.web_status_label)
        
        layout.addWidget(status_group)
        
        # Группа: Управление серверами
        control_group = QGroupBox("Управление серверами")
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        self.btn_start_all = QPushButton("🚀 Запустить всё")
        self.btn_start_all.clicked.connect(self.start_all_servers)
        btn_layout.addWidget(self.btn_start_all)
        
        self.btn_stop_all = QPushButton("⏹️ Остановить всё")
        self.btn_stop_all.clicked.connect(self.stop_all_servers)
        btn_layout.addWidget(self.btn_stop_all)
        
        control_layout.addLayout(btn_layout)
        layout.addWidget(control_group)
        
        # Группа: Быстрый доступ
        quick_group = QGroupBox("Быстрый доступ")
        quick_layout = QVBoxLayout()
        quick_group.setLayout(quick_layout)
        
        btn_dashboard = QPushButton("🌐 Открыть Dashboard")
        btn_dashboard.clicked.connect(self.open_dashboard)
        quick_layout.addWidget(btn_dashboard)
        
        btn_logs_dashboard = QPushButton("📊 Открыть Logs Dashboard")
        btn_logs_dashboard.clicked.connect(self.open_logs_dashboard)
        quick_layout.addWidget(btn_logs_dashboard)
        
        btn_main_py = QPushButton("🐍 Запустить Python CLI")
        btn_main_py.clicked.connect(self.open_python_cli)
        quick_layout.addWidget(btn_main_py)
        
        btn_collector = QPushButton("📋 Открыть коллектор (JS)")
        btn_collector.clicked.connect(self.open_collector_code)
        quick_layout.addWidget(btn_collector)
        
        layout.addWidget(quick_group)
        
        # Группа: Документация
        docs_group = QGroupBox("📚 Документация")
        docs_layout = QVBoxLayout()
        docs_group.setLayout(docs_layout)
        
        btn_real_data = QPushButton("📖 Как собрать реальные данные")
        btn_real_data.clicked.connect(lambda: self.open_file("REAL_DATA_START.md"))
        docs_layout.addWidget(btn_real_data)
        
        btn_cheatsheet = QPushButton("📝 Шпаргалка")
        btn_cheatsheet.clicked.connect(lambda: self.open_file("CHEATSHEET.md"))
        docs_layout.addWidget(btn_cheatsheet)
        
        layout.addWidget(docs_group)
        
        # Растяжка
        layout.addStretch()
        
        return widget
    
    def create_log_tab(self):
        """Создание вкладки логов"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        label = QLabel("📋 Логи приложения:")
        layout.addWidget(label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas;")
        layout.addWidget(self.log_text)
        
        # Кнопка очистки
        btn_clear = QPushButton("🗑️ Очистить логи")
        btn_clear.clicked.connect(self.log_text.clear)
        layout.addWidget(btn_clear)
        
        return widget
    
    def create_about_tab(self):
        """Создание вкладки О программе"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        about_text = QLabel("""
        <h2>🎰 RULETTT - Система анализа рулетки</h2>
        <p><b>Версия:</b> 1.0.0 Desktop Edition</p>
        <p><b>Платформа:</b> Windows (macOS в разработке)</p>
        
        <h3>Возможности:</h3>
        <ul>
            <li>✅ Автоматический сбор данных рулетки</li>
            <li>✅ Анализ статистики и паттернов</li>
            <li>✅ Тестирование игровых стратегий</li>
            <li>✅ Система логирования и мониторинга</li>
            <li>✅ Web-интерфейс и API</li>
        </ul>
        
        <h3>⚠️ Важно:</h3>
        <p>Система создана для <b>образовательных целей</b>!</p>
        <p>Не используйте для ставок реальными деньгами.</p>
        
        <h3>📧 Контакты:</h3>
        <p>GitHub: nikolaspablo92-prog/RULETTT</p>
        
        <p style="color: gray; margin-top: 20px;">
        © 2025 RULETTT Project. All rights reserved.
        </p>
        """)
        about_text.setWordWrap(True)
        about_text.setOpenExternalLinks(True)
        layout.addWidget(about_text)
        
        layout.addStretch()
        
        return widget
    
    def init_tray(self):
        """Инициализация иконки в трее"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.log("⚠️ System tray недоступен")
            return
        
        # Иконка (используем стандартную)
        icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("RULETTT - Система анализа рулетки")
        
        # Меню трея
        tray_menu = QMenu()
        
        show_action = QAction("Показать", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        dashboard_action = QAction("Открыть Dashboard", self)
        dashboard_action.triggered.connect(self.open_dashboard)
        tray_menu.addAction(dashboard_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Обработка клика по иконке в трее"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
    
    def setup_status_timer(self):
        """Таймер для обновления статуса"""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_server_status)
        self.status_timer.start(2000)  # Каждые 2 секунды
    
    def update_server_status(self):
        """Обновление статуса серверов"""
        api_status, web_status = self.server_manager.get_status()
        self.api_status_label.setText(f"API Server: {api_status}")
        self.web_status_label.setText(f"Web Server: {web_status}")
    
    def auto_start_servers(self):
        """Автоматический запуск серверов при старте"""
        self.log("🚀 Автозапуск серверов...")
        self.start_all_servers()
    
    def start_all_servers(self):
        """Запуск всех серверов"""
        self.log("▶️ Запуск серверов...")
        
        # Запуск API
        success, msg = self.server_manager.start_api_server()
        self.log(f"API: {msg}")
        
        # Запуск Web
        success, msg = self.server_manager.start_web_server()
        self.log(f"Web: {msg}")
        
        self.status_bar.showMessage("Серверы запущены", 3000)
        
        # Показываем уведомление в трее
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(
                "RULETTT",
                "Серверы успешно запущены!",
                QSystemTrayIcon.Information,
                2000
            )
    
    def stop_all_servers(self):
        """Остановка всех серверов"""
        self.log("⏹️ Остановка серверов...")
        self.server_manager.stop_servers()
        self.log("✅ Серверы остановлены")
        self.status_bar.showMessage("Серверы остановлены", 3000)
    
    def open_dashboard(self):
        """Открыть главный Dashboard"""
        url = f"http://localhost:{self.server_manager.web_port}/dashboard.html"
        webbrowser.open(url)
        self.log(f"🌐 Открыт Dashboard: {url}")
    
    def open_logs_dashboard(self):
        """Открыть Logs Dashboard"""
        url = f"http://localhost:{self.server_manager.web_port}/logs_dashboard.html"
        webbrowser.open(url)
        self.log(f"📊 Открыт Logs Dashboard: {url}")
    
    def open_python_cli(self):
        """Запустить Python CLI"""
        try:
            script_path = Path(__file__).parent / "src" / "main.py"
            subprocess.Popen([sys.executable, str(script_path)])
            self.log("🐍 Запущен Python CLI")
        except Exception as e:
            self.log(f"❌ Ошибка запуска CLI: {e}")
    
    def open_collector_code(self):
        """Открыть файл с коллектором"""
        try:
            file_path = Path(__file__).parent / "auto_collector_with_api.js"
            if sys.platform == 'win32':
                os.startfile(file_path)
            else:
                subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', file_path])
            self.log("📋 Открыт файл коллектора")
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
    
    def open_file(self, filename):
        """Открыть файл документации"""
        try:
            file_path = Path(__file__).parent / filename
            if sys.platform == 'win32':
                os.startfile(file_path)
            else:
                subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', file_path])
            self.log(f"📖 Открыт файл: {filename}")
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
    
    def log(self, message):
        """Добавить запись в лог"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_emitter.log_signal.emit(f"[{timestamp}] {message}")
    
    def append_log(self, message):
        """Добавить текст в лог (вызывается из сигнала)"""
        self.log_text.append(message)
        # Прокрутка вниз
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
    
    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QLabel {
                color: #333333;
            }
        """)
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        reply = QMessageBox.question(
            self, 
            'Выход', 
            "Свернуть в трей или выйти?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Yes:
            # Свернуть в трей
            event.ignore()
            self.hide()
            if hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    "RULETTT",
                    "Приложение свернуто в трей",
                    QSystemTrayIcon.Information,
                    1000
                )
        elif reply == QMessageBox.No:
            # Выход
            self.quit_application()
        else:
            # Отмена
            event.ignore()
    
    def quit_application(self):
        """Полный выход из приложения"""
        self.log("👋 Выход из приложения...")
        self.stop_all_servers()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        QApplication.quit()


def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    app.setApplicationName("RULETTT")
    app.setOrganizationName("RULETTT Project")
    
    # Создаем главное окно
    window = RoulettDesktopApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
