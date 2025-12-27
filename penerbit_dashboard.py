# penerbit_dashboard_cyberpunk.py — CYBERPUNK STYLE EDITION 🎮
"""
🔮 CYBERPUNK PENERBIT DASHBOARD 🔮

Features:
- Neon glow effects
- Holographic UI elements  
- Futuristic cyberpunk theme
- Glowing statistics cards
- Matrix-style animations
- Synth-wave color palette
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from typing import Optional
from app_db_fixed import (
    heartbeat, end_session, 
    create_news, list_my_news, list_published_news
)

# 🎨 CYBERPUNK COLOR PALETTE
CYBER_CYAN = "#00ffff"
CYBER_MAGENTA = "#ff00ff"
CYBER_PURPLE = "#9d00ff"
CYBER_PINK = "#ff007f"
CYBER_BLUE = "#0066ff"
CYBER_GREEN = "#00ff88"
CYBER_YELLOW = "#ffff00"
CYBER_RED = "#ff0040"
CYBER_DARK = "#0a0a0f"
CYBER_DARKER = "#050508"
CYBER_GRID = "#1a1a2e"


class CyberStatCard(QtWidgets.QFrame):
    """Cyberpunk glowing stat card with neon effects"""
    
    def __init__(self, title, value, icon, glow_color, parent=None):
        super().__init__(parent)
        self.glow_color = glow_color
        self.setObjectName("cyberStatCard")
        self.setFixedHeight(140)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Icon with glow
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setObjectName("cyberIcon")
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 42px;
            color: {glow_color};
            text-shadow: 0 0 20px {glow_color},
                         0 0 40px {glow_color},
                         0 0 60px {glow_color};
        """)
        layout.addWidget(icon_label)
        
        # Value with glow
        self.value_label = QtWidgets.QLabel(str(value))
        self.value_label.setObjectName("cyberValue")
        self.value_label.setAlignment(QtCore.Qt.AlignCenter)
        self.value_label.setStyleSheet(f"""
            font-size: 36px;
            font-weight: 900;
            color: {glow_color};
            text-shadow: 0 0 10px {glow_color},
                         0 0 20px {glow_color};
        """)
        layout.addWidget(self.value_label)
        
        # Title
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("cyberTitle")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 700;
            color: {glow_color};
            text-transform: uppercase;
            letter-spacing: 2px;
        """)
        layout.addWidget(title_label)
        
        # Apply glow effect to card
        self.setStyleSheet(f"""
            #cyberStatCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {CYBER_DARKER},
                    stop:1 {CYBER_DARK});
                border: 2px solid {glow_color};
                border-radius: 15px;
            }}
            #cyberStatCard:hover {{
                box-shadow: 0 0 30px {glow_color}60;
            }}
        """)
    
    def update_value(self, value):
        """Update card value"""
        self.value_label.setText(str(value))


class CyberButton(QtWidgets.QPushButton):
    """Cyberpunk style button with glow"""
    
    def __init__(self, text, color=CYBER_CYAN, parent=None):
        super().__init__(text, parent)
        self.color = color
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self._apply_cyber_style()
    
    def _apply_cyber_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {CYBER_DARKER},
                    stop:1 {CYBER_DARK});
                color: {self.color};
                border: 2px solid {self.color};
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {self.color}20;
                box-shadow: 0 0 20px {self.color},
                            0 0 40px {self.color}80;
            }}
            QPushButton:pressed {{
                background: {self.color}40;
            }}
        """)


class CyberTextEdit(QtWidgets.QTextEdit):
    """Cyberpunk text editor"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cyberEditor")
        self.setPlaceholderText("⚡ ENTER YOUR ARTICLE CONTENT HERE ⚡")
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background: {CYBER_DARKER};
                color: {CYBER_CYAN};
                border: 2px solid {CYBER_CYAN}60;
                border-radius: 12px;
                padding: 16px;
                font-size: 15px;
                font-family: 'Consolas', 'Courier New', monospace;
                selection-background-color: {CYBER_CYAN}40;
            }}
            QTextEdit:focus {{
                border: 2px solid {CYBER_CYAN};
                box-shadow: 0 0 20px {CYBER_CYAN}60;
            }}
        """)


class PenerbitDashboard(QtWidgets.QMainWindow):
    """🎮 CYBERPUNK PENERBIT DASHBOARD 🎮"""
    
    def __init__(self, username: str, session_id: Optional[int] = None):
        super().__init__()
        self.username = username
        self.session_id = session_id
        
        self.setWindowTitle(f"⚡ CRYPTO INSIGHT — CYBERPUNK EDITION ⚡")
        self.resize(1500, 950)
        
        self._setup_ui()
        self._apply_cyberpunk_theme()
        self._load_statistics()
        self._load_my_articles()
        
        # Heartbeat
        if self.session_id:
            self.hb_timer = QtCore.QTimer(self)
            self.hb_timer.timeout.connect(lambda: heartbeat(self.session_id))
            self.hb_timer.start(20000)
        
        # Auto-refresh
        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.timeout.connect(self._load_statistics)
        self.refresh_timer.start(30000)
    
    def _setup_ui(self):
        """Setup CYBERPUNK UI"""
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        
        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # 🎮 CYBER HEADER
        header = self._create_cyber_header()
        main_layout.addWidget(header)
        
        # 📊 GLOWING STATS
        stats = self._create_cyber_stats()
        main_layout.addLayout(stats)
        
        # 📝 CYBER TABS
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("cyberTabs")
        
        # Tab 1: Create Article
        tab_create = self._create_article_tab()
        self.tabs.addTab(tab_create, "⚡ CREATE ARTICLE")
        
        # Tab 2: My Articles
        tab_articles = self._create_articles_tab()
        self.tabs.addTab(tab_articles, "📡 MY ARTICLES")
        
        # Tab 3: Published Feed
        tab_feed = self._create_feed_tab()
        self.tabs.addTab(tab_feed, "🌐 PUBLISHED FEED")
        
        main_layout.addWidget(self.tabs)
    
    def _create_cyber_header(self):
        """Create cyberpunk header"""
        header = QtWidgets.QFrame()
        header.setObjectName("cyberHeader")
        
        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title with glow
        title = QtWidgets.QLabel(f"⚡ WELCOME {self.username.upper()} ⚡")
        title.setObjectName("cyberHeaderTitle")
        
        subtitle = QtWidgets.QLabel("► PENERBIT CONTROL CENTER ◄")
        subtitle.setObjectName("cyberHeaderSubtitle")
        
        title_layout = QtWidgets.QVBoxLayout()
        title_layout.setSpacing(5)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Logout button
        self.btn_logout = CyberButton("LOGOUT", CYBER_RED)
        self.btn_logout.clicked.connect(self._logout)
        layout.addWidget(self.btn_logout)
        
        return header
    
    def _create_cyber_stats(self):
        """Create glowing statistics cards"""
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(20)
        
        # Cyber stat cards with different glow colors
        self.card_total = CyberStatCard("TOTAL", "0", "📡", CYBER_CYAN)
        self.card_published = CyberStatCard("LIVE", "0", "✨", CYBER_GREEN)
        self.card_draft = CyberStatCard("DRAFT", "0", "💾", CYBER_YELLOW)
        self.card_views = CyberStatCard("VIEWS", "N/A", "👁", CYBER_MAGENTA)
        
        row.addWidget(self.card_total)
        row.addWidget(self.card_published)
        row.addWidget(self.card_draft)
        row.addWidget(self.card_views)
        
        return row
    
    def _create_article_tab(self):
        """Create article editor with cyber theme"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(20)
        
        # Title input
        title_label = QtWidgets.QLabel("⚡ ARTICLE TITLE")
        title_label.setStyleSheet(f"""
            color: {CYBER_CYAN};
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        
        self.input_title = QtWidgets.QLineEdit()
        self.input_title.setObjectName("cyberTitleInput")
        self.input_title.setPlaceholderText("Enter cyberpunk title...")
        self.input_title.setMinimumHeight(55)
        
        layout.addWidget(title_label)
        layout.addWidget(self.input_title)
        
        # Content editor
        content_label = QtWidgets.QLabel("⚡ ARTICLE CONTENT")
        content_label.setStyleSheet(f"""
            color: {CYBER_MAGENTA};
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        
        self.editor = CyberTextEdit()
        
        layout.addWidget(content_label)
        layout.addWidget(self.editor, 1)
        
        # Action buttons
        action_row = QtWidgets.QHBoxLayout()
        action_row.setSpacing(15)
        
        self.btn_save_draft = CyberButton("💾 SAVE DRAFT", CYBER_YELLOW)
        self.btn_save_draft.clicked.connect(lambda: self._save_article(False))
        
        self.btn_publish = CyberButton("🚀 PUBLISH NOW", CYBER_GREEN)
        self.btn_publish.clicked.connect(lambda: self._save_article(True))
        
        self.btn_clear = CyberButton("🗑 CLEAR ALL", CYBER_RED)
        self.btn_clear.clicked.connect(self._clear_form)
        
        action_row.addWidget(self.btn_save_draft, 1)
        action_row.addWidget(self.btn_publish, 2)
        action_row.addWidget(self.btn_clear, 1)
        
        layout.addLayout(action_row)
        
        return widget
    
    def _create_articles_tab(self):
        """Create articles table with cyber theme"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(15)
        
        # Refresh button
        refresh_btn = CyberButton("🔄 REFRESH DATA", CYBER_CYAN)
        refresh_btn.clicked.connect(self._load_my_articles)
        layout.addWidget(refresh_btn)
        
        # Table
        self.table_articles = QtWidgets.QTableWidget(0, 4)
        self.table_articles.setObjectName("cyberTable")
        self.table_articles.setHorizontalHeaderLabels(["ID", "TITLE", "STATUS", "DATE"])
        
        header = self.table_articles.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        
        self.table_articles.setAlternatingRowColors(True)
        self.table_articles.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.table_articles)
        
        return widget
    
    def _create_feed_tab(self):
        """Create feed with cyber theme"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(15)
        
        info = QtWidgets.QLabel("🌐 GLOBAL PUBLISHED FEED")
        info.setStyleSheet(f"""
            color: {CYBER_CYAN};
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 2px;
            padding: 15px;
            background: {CYBER_DARKER};
            border: 2px solid {CYBER_CYAN};
            border-radius: 10px;
            text-shadow: 0 0 10px {CYBER_CYAN};
        """)
        layout.addWidget(info)
        
        self.table_feed = QtWidgets.QTableWidget(0, 4)
        self.table_feed.setObjectName("cyberTable")
        self.table_feed.setHorizontalHeaderLabels(["ID", "TITLE", "AUTHOR", "DATE"])
        
        header = self.table_feed.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        self.table_feed.setAlternatingRowColors(True)
        self.table_feed.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.table_feed)
        
        refresh = CyberButton("🔄 REFRESH FEED", CYBER_MAGENTA)
        refresh.clicked.connect(self._load_feed)
        layout.addWidget(refresh)
        
        return widget
    
    def _save_article(self, publish=True):
        """Save article"""
        title = self.input_title.text().strip()
        content = self.editor.toPlainText().strip()
        
        if not title:
            QtWidgets.QMessageBox.warning(self, "⚠ WARNING", "Please enter article title!")
            self.input_title.setFocus()
            return
        
        if not content:
            QtWidgets.QMessageBox.warning(self, "⚠ WARNING", "Please write article content!")
            self.editor.setFocus()
            return
        
        success = create_news(self.username, title, content, publish)
        
        if success:
            status = "PUBLISHED" if publish else "SAVED AS DRAFT"
            QtWidgets.QMessageBox.information(self, "✅ SUCCESS", f"Article {status}!")
            self._clear_form()
            self._load_statistics()
            self._load_my_articles()
            if publish:
                self._load_feed()
        else:
            QtWidgets.QMessageBox.critical(self, "❌ ERROR", "Failed to save article!")
    
    def _clear_form(self):
        """Clear form"""
        reply = QtWidgets.QMessageBox.question(
            self, "⚠ CONFIRM",
            "Clear all fields? Unsaved changes will be lost!",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.input_title.clear()
            self.editor.clear()
            self.input_title.setFocus()
    
    def _load_statistics(self):
        """Load stats"""
        try:
            articles = list_my_news(self.username, limit=1000)
            total = len(articles)
            published = len([a for a in articles if a[2] == 'published'])
            draft = total - published
            
            self.card_total.update_value(total)
            self.card_published.update_value(published)
            self.card_draft.update_value(draft)
        except Exception as e:
            print(f"Error loading stats: {e}")
    
    def _load_my_articles(self):
        """Load articles table"""
        try:
            articles = list_my_news(self.username, limit=100)
            self.table_articles.setRowCount(len(articles))
            
            for row, (aid, title, status, created) in enumerate(articles):
                self.table_articles.setItem(row, 0, QtWidgets.QTableWidgetItem(str(aid)))
                self.table_articles.setItem(row, 1, QtWidgets.QTableWidgetItem(title))
                
                status_item = QtWidgets.QTableWidgetItem(status.upper())
                if status == 'published':
                    status_item.setForeground(QtGui.QBrush(QtGui.QColor(CYBER_GREEN)))
                else:
                    status_item.setForeground(QtGui.QBrush(QtGui.QColor(CYBER_YELLOW)))
                self.table_articles.setItem(row, 2, status_item)
                
                self.table_articles.setItem(row, 3, QtWidgets.QTableWidgetItem(created or "N/A"))
        except Exception as e:
            print(f"Error loading articles: {e}")
    
    def _load_feed(self):
        """Load feed"""
        try:
            articles = list_published_news(limit=100)
            self.table_feed.setRowCount(len(articles))
            
            for row, (aid, title, author, published) in enumerate(articles):
                self.table_feed.setItem(row, 0, QtWidgets.QTableWidgetItem(str(aid)))
                self.table_feed.setItem(row, 1, QtWidgets.QTableWidgetItem(title))
                
                author_item = QtWidgets.QTableWidgetItem(author)
                author_item.setForeground(QtGui.QBrush(QtGui.QColor(CYBER_MAGENTA)))
                self.table_feed.setItem(row, 2, author_item)
                
                self.table_feed.setItem(row, 3, QtWidgets.QTableWidgetItem(published or "N/A"))
        except Exception as e:
            print(f"Error loading feed: {e}")
    
    def _logout(self):
        """Logout"""
        if hasattr(self, 'hb_timer'):
            self.hb_timer.stop()
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        if self.session_id:
            try:
                end_session(self.session_id)
            except:
                pass
        self.close()
    
    def _apply_cyberpunk_theme(self):
        """Apply FULL CYBERPUNK THEME"""
        self.setStyleSheet(f"""
            /* Global Cyberpunk Background */
            QMainWindow, QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {CYBER_DARKER},
                    stop:0.5 {CYBER_DARK},
                    stop:1 {CYBER_DARKER});
                color: {CYBER_CYAN};
                font-family: 'Segoe UI', sans-serif;
            }}
            
            /* Cyber Header */
            #cyberHeaderTitle {{
                font-size: 32px;
                font-weight: 900;
                color: {CYBER_CYAN};
                text-shadow: 0 0 20px {CYBER_CYAN},
                             0 0 40px {CYBER_CYAN},
                             0 0 60px {CYBER_CYAN};
                letter-spacing: 3px;
            }}
            #cyberHeaderSubtitle {{
                font-size: 14px;
                font-weight: 700;
                color: {CYBER_MAGENTA};
                text-shadow: 0 0 10px {CYBER_MAGENTA};
                letter-spacing: 2px;
            }}
            
            /* Cyber Tabs */
            QTabWidget::pane {{
                border: 2px solid {CYBER_CYAN}60;
                border-radius: 15px;
                background: {CYBER_DARKER};
            }}
            QTabBar::tab {{
                background: {CYBER_DARKER};
                color: {CYBER_CYAN}80;
                border: 2px solid {CYBER_CYAN}40;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                padding: 12px 30px;
                margin-right: 5px;
                font-weight: 700;
                font-size: 13px;
                letter-spacing: 1px;
            }}
            QTabBar::tab:selected {{
                background: {CYBER_DARK};
                color: {CYBER_CYAN};
                border: 2px solid {CYBER_CYAN};
                box-shadow: 0 0 20px {CYBER_CYAN}80;
            }}
            QTabBar::tab:hover:!selected {{
                background: {CYBER_CYAN}10;
                color: {CYBER_CYAN};
            }}
            
            /* Cyber Title Input */
            #cyberTitleInput {{
                background: {CYBER_DARKER};
                color: {CYBER_CYAN};
                border: 2px solid {CYBER_CYAN}60;
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 18px;
                font-weight: 700;
            }}
            #cyberTitleInput:focus {{
                border: 2px solid {CYBER_CYAN};
                box-shadow: 0 0 20px {CYBER_CYAN}60;
            }}
            
            /* Cyber Tables */
            QTableWidget {{
                background: {CYBER_DARKER};
                color: {CYBER_CYAN};
                border: 2px solid {CYBER_CYAN}60;
                border-radius: 12px;
                gridline-color: {CYBER_CYAN}20;
                selection-background-color: {CYBER_CYAN}30;
                font-family: 'Consolas', monospace;
            }}
            QTableWidget::item {{
                padding: 10px;
            }}
            QTableWidget::item:alternate {{
                background: {CYBER_DARK};
            }}
            QHeaderView::section {{
                background: {CYBER_GRID};
                color: {CYBER_CYAN};
                border: 1px solid {CYBER_CYAN}40;
                padding: 12px;
                font-weight: 700;
                font-size: 12px;
                letter-spacing: 2px;
                text-transform: uppercase;
                text-shadow: 0 0 5px {CYBER_CYAN};
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                background: {CYBER_DARKER};
                width: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background: {CYBER_CYAN}60;
                border-radius: 7px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {CYBER_CYAN};
                box-shadow: 0 0 10px {CYBER_CYAN};
            }}
            QScrollBar:horizontal {{
                background: {CYBER_DARKER};
                height: 14px;
                border-radius: 7px;
            }}
            QScrollBar::handle:horizontal {{
                background: {CYBER_CYAN}60;
                border-radius: 7px;
                min-width: 30px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {CYBER_CYAN};
                box-shadow: 0 0 10px {CYBER_CYAN};
            }}
            
            /* Message Boxes */
            QMessageBox {{
                background: {CYBER_DARK};
                color: {CYBER_CYAN};
            }}
            QMessageBox QLabel {{
                color: {CYBER_CYAN};
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background: {CYBER_DARKER};
                color: {CYBER_CYAN};
                border: 2px solid {CYBER_CYAN};
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 700;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background: {CYBER_CYAN}20;
                box-shadow: 0 0 15px {CYBER_CYAN};
            }}
        """)
        
        # Set cyberpunk font
        font = QtGui.QFont("Segoe UI", 10)
        self.setFont(font)
    
    def closeEvent(self, event):
        """Handle close"""
        self._logout()
        event.accept()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = PenerbitDashboard("CYBER_USER", None)
    window.show()
    sys.exit(app.exec_())
