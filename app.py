"""
NetVide — Modern Tab-less Desktop Browser
Powered by PySide6 & QtWebEngine (Chromium)
"""

import sys
import urllib.parse
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile


HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background-color: #0c0d10;
      color: #eaecef;
      font-family: 'JetBrains Mono', monospace;
      height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      user-select: none;
    }
    .hero {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 10px;
    }
    h1 {
      font-size: 3.2rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: #ffffff;
    }
    p {
      font-size: 1rem;
      color: #64748b;
      letter-spacing: 0.02em;
    }
    .search-box {
      margin-top: 24px;
      display: flex;
      align-items: center;
      background: #14161f;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 6px 16px;
      width: 440px;
      max-width: 90vw;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      transition: border-color 0.2s;
    }
    .search-box:focus-within {
      border-color: #6366f1;
    }
    input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #ffffff;
      font-family: inherit;
      font-size: 0.95rem;
      padding: 8px 4px;
    }
    input::placeholder {
      color: #555c70;
    }
    button {
      background: rgba(255, 255, 255, 0.08);
      border: none;
      border-radius: 8px;
      color: #ffffff;
      padding: 6px 14px;
      font-family: inherit;
      font-size: 0.85rem;
      cursor: pointer;
      transition: background 0.15s;
    }
    button:hover {
      background: #6366f1;
    }
  </style>
</head>
<body>
  <div class="hero">
    <h1>NetVide</h1>
    <p>configure your network & browse</p>
    <form class="search-box" onsubmit="event.preventDefault(); doSearch();">
      <input type="text" id="query" placeholder="search the web or enter url..." autofocus autocomplete="off" />
      <button type="submit">→</button>
    </form>
  </div>

  <script>
    function doSearch() {
      const val = document.getElementById('query').value.trim();
      if (!val) return;
      if (val.startsWith('http://') || val.startsWith('https://')) {
        window.location.href = val;
      } else if (val.includes('.') && !val.includes(' ')) {
        window.location.href = 'https://' + val;
      } else {
        window.location.href = 'https://duckduckgo.com/?q=' + encodeURIComponent(val);
      }
    }
  </script>
</body>
</html>
"""

class NetVideBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetVide")
        self.resize(1140, 740)
        self.setMinimumSize(800, 500)

        # Style central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sleek Minimal Top Navigation Bar
        navbar = QWidget()
        navbar.setFixedHeight(44)
        navbar.setStyleSheet("""
            QWidget {
                background-color: #0d0f15;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                color: #cbd5e1;
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 6px;
                padding: 4px 10px;
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.12);
                color: #ffffff;
            }
            QLineEdit {
                background-color: #141722;
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 4px 12px;
                font-family: 'JetBrains Mono', Consolas, monospace;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 1px solid #6366f1;
            }
        """)

        nav_layout = QHBoxLayout(navbar)
        nav_layout.setContentsMargins(12, 6, 12, 6)
        nav_layout.setSpacing(8)

        # Back & Forward buttons
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedWidth(32)
        self.back_btn.clicked.connect(self._go_back)
        nav_layout.addWidget(self.back_btn)

        self.forward_btn = QPushButton("→")
        self.forward_btn.setFixedWidth(32)
        self.forward_btn.clicked.connect(self._go_forward)
        nav_layout.addWidget(self.forward_btn)

        self.reload_btn = QPushButton("⟳")
        self.reload_btn.setFixedWidth(32)
        self.reload_btn.clicked.connect(self._reload)
        nav_layout.addWidget(self.reload_btn)

        # Home Button
        self.home_btn = QPushButton("NetVide")
        self.home_btn.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_btn)

        # Omnibox URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search web or enter URL...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_layout.addWidget(self.url_bar)

        main_layout.addWidget(navbar)

        # Progress bar for page loads
        self.progress = QProgressBar()
        self.progress.setFixedHeight(2)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
            }
        """)
        main_layout.addWidget(self.progress)

        # Chromium Web View
        self.webview = QWebEngineView()
        main_layout.addWidget(self.webview)

        # Enable modern Chromium settings
        settings = self.webview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

        # Connect signals
        self.webview.urlChanged.connect(self.update_url_bar)
        self.webview.loadProgress.connect(self.update_progress)
        self.webview.loadFinished.connect(self.load_finished)

        # Start on Home Page
        self.go_home()

    def go_home(self):
        self.webview.setHtml(HOME_HTML)
        self.url_bar.setText("")
        self.url_bar.setPlaceholderText("Search web or enter URL...")

    def navigate_to_url(self):
        q = self.url_bar.text().strip()
        if not q:
            return

        if q.startswith("http://") or q.startswith("https://"):
            target = q
        elif "." in q and " " not in q:
            target = "https://" + q
        else:
            target = "https://duckduckgo.com/?q=" + urllib.parse.quote(q)

        self.webview.setUrl(QUrl(target))

    def _go_back(self):
        if self.webview.history().canGoBack():
            self.webview.back()
        else:
            self.go_home()

    def _go_forward(self):
        self.webview.forward()

    def _reload(self):
        self.webview.reload()

    def update_url_bar(self, qurl):
        url_str = qurl.toString()
        if url_str.startswith("data:text/html") or not url_str:
            self.url_bar.setText("")
        else:
            self.url_bar.setText(url_str)

    def update_progress(self, val):
        self.progress.setValue(val)
        if val < 100:
            self.progress.show()
        else:
            self.progress.hide()

    def load_finished(self, success):
        self.progress.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = NetVideBrowser()
    browser.show()
    sys.exit(app.exec())
