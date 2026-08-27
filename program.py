import os
import subprocess
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QThread, Signal, QPropertyAnimation, QEasingCurve, Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, QPalette, QFontDatabase
import sys
import time
import math


# ─── Color Palette ─────────────────────────────────────────────────────────────
COLORS = {
    "bg":           "#0D0D0F",
    "surface":      "#131318",
    "surface2":     "#1A1A22",
    "border":       "#252530",
    "border_hover": "#3A3A4A",
    "accent":       "#E8A010",
    "accent_dim":   "#A06808",
    "accent_glow":  "#F0B020",
    "text":         "#E8E8F0",
    "text_dim":     "#888898",
    "text_muted":   "#444455",
    "success":      "#22C55E",
    "error":        "#EF4444",
    "white":        "#FFFFFF",
}

STYLESHEET = f"""
QWidget {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-family: 'Courier New', 'Consolas', monospace;
}}

QWidget#MainWindow {{
    background-color: {COLORS['bg']};
}}

/* ── Line Edit ── */
QLineEdit {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 8px 10px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    selection-background-color: {COLORS['accent_dim']};
}}
QLineEdit:hover {{
    border-color: {COLORS['border_hover']};
    background-color: {COLORS['surface2']};
}}
QLineEdit:focus {{
    border-color: {COLORS['accent_dim']};
}}
QLineEdit:disabled {{
    color: {COLORS['text_dim']};
    background-color: {COLORS['surface']};
    border-color: {COLORS['border']};
}}

/* ── Combo Box ── */
QComboBox {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 8px 12px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    min-height: 20px;
    selection-background-color: {COLORS['accent']};
}}
QComboBox:hover {{
    border-color: {COLORS['border_hover']};
    background-color: {COLORS['surface2']};
}}
QComboBox:focus {{
    border-color: {COLORS['accent_dim']};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {COLORS['accent']};
    width: 0;
    height: 0;
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['surface2']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    selection-background-color: {COLORS['accent_dim']};
    outline: none;
    padding: 2px;
}}

/* ── Progress Bar ── */
QProgressBar {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 2px;
    height: 4px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent_dim']}, stop:1 {COLORS['accent_glow']});
    border-radius: 2px;
}}

/* ── Scroll Bar ── */
QScrollBar:vertical {{
    background: {COLORS['surface']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border_hover']};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── Log Area ── */
QPlainTextEdit {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_dim']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 10px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    selection-background-color: {COLORS['accent_dim']};
}}

/* ── Tab Widget ── */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-top: none;
    background-color: {COLORS['bg']};
    top: -1px;
}}
QTabBar::tab {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_dim']};
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    padding: 10px 22px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
}}
QTabBar::tab:selected {{
    background-color: {COLORS['bg']};
    color: {COLORS['accent']};
    border-bottom: 2px solid {COLORS['accent']};
    margin-bottom: -1px;
}}
QTabBar::tab:hover:!selected {{
    color: {COLORS['text']};
    background-color: {COLORS['surface2']};
}}

/* ── Check Box ── */
QCheckBox {{
    color: {COLORS['text']};
    font-family: 'Courier New', monospace;
    font-size: 11px;
    spacing: 10px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {COLORS['border_hover']};
    border-radius: 3px;
    background-color: {COLORS['surface']};
}}
QCheckBox::indicator:hover {{
    border-color: {COLORS['accent_dim']};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}
"""


# ─── Custom Widgets ─────────────────────────────────────────────────────────────

class SectionLabel(QtWidgets.QLabel):
    """Small all-caps section header with amber left bar."""
    def __init__(self, text, parent=None):
        super().__init__(text.upper(), parent)
        self.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent']};
                font-family: 'Courier New', monospace;
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 3px;
                padding-left: 10px;
                border-left: 2px solid {COLORS['accent']};
            }}
        """)


class ValueLabel(QtWidgets.QLabel):
    """Dimmed info label."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_dim']};
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }}
        """)


class GlowButton(QtWidgets.QPushButton):
    """Primary CTA button with amber glow effect."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(48)
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self._active = False
        self._anim_value = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._phase = 0.0
        self._update_style(False)

    def _update_style(self, hover):
        if not self.isEnabled():
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['surface']};
                    color: {COLORS['text_muted']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    font-size: 13px;
                    font-weight: bold;
                    letter-spacing: 4px;
                }}
            """)
        elif hover:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    color: {COLORS['bg']};
                    border: none;
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    font-size: 13px;
                    font-weight: bold;
                    letter-spacing: 4px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['accent']};
                    border: 1px solid {COLORS['accent_dim']};
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    font-size: 13px;
                    font-weight: bold;
                    letter-spacing: 4px;
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['accent_dim']};
                    color: {COLORS['bg']};
                }}
            """)

    def enterEvent(self, event):
        self._update_style(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._update_style(False)
        super().leaveEvent(event)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self._update_style(False)

    def _tick(self):
        self._phase += 0.05
        pulse = int(180 + 75 * math.sin(self._phase))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: rgb({pulse}, {int(pulse*0.63)}, 0);
                border: 1px solid rgb({int(pulse*0.7)}, {int(pulse*0.44)}, 0);
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 4px;
            }}
        """)


class PillBadge(QtWidgets.QLabel):
    """Small colored status pill."""
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color: {color};
                border: 1px solid {color}55;
                border-radius: 10px;
                padding: 2px 10px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
        """)
        self.setFixedHeight(20)


class SeparatorLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setStyleSheet(f"color: {COLORS['border']}; background: {COLORS['border']}; max-height: 1px;")


class AnimatedProgressBar(QtWidgets.QProgressBar):
    """Progress bar that pulses when active."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)
        self.setTextVisible(False)
        self._running = False

    def set_running(self, running):
        self._running = running
        if running:
            self.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {COLORS['surface']};
                    border: none;
                    border-radius: 2px;
                }}
                QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {COLORS['accent_dim']}, stop:0.5 {COLORS['accent_glow']}, stop:1 {COLORS['accent']});
                    border-radius: 2px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {COLORS['surface']};
                    border: none;
                    border-radius: 2px;
                }}
                QProgressBar::chunk {{
                    background: {COLORS['success']};
                    border-radius: 2px;
                }}
            """)


class LogArea(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumHeight(130)
        self.setMinimumHeight(130)

    def append_log(self, message, color=None):
        color = color or COLORS['text_dim']
        self.appendHtml(f'<span style="color:{color}; font-family: Courier New, monospace; font-size: 11px;">{message}</span>')
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


# ─── Worker Thread ──────────────────────────────────────────────────────────────

class ConversionWorker(QThread):
    progress = Signal(str)
    progress_percent = Signal(int)
    current_video = Signal(str)
    conversion_finished = Signal()
    error = Signal(str)

    def __init__(self, input_dir, output_dir, selected_encoder, input_ext, output_ext, delete_original=False):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.selected_encoder = selected_encoder
        self.input_ext = input_ext
        self.output_ext = output_ext
        self.delete_original = delete_original

    def _build_command(self, input_path, output_path, encoder=None):
        enc = encoder or self.selected_encoder
        vf = ["scale=trunc(iw/2)*2:trunc(ih/2)*2"]
        if "nvenc" in enc or "NVIDIA" in enc:
            return ["ffmpeg", "-y", "-i", input_path, "-c:v", "h264_nvenc", "-preset", "fast", "-vf", *vf, output_path]
        elif "amf" in enc or "AMD" in enc:
            return ["ffmpeg", "-y", "-i", input_path, "-c:v", "h264_amf", "-quality", "speed", "-vf", *vf, output_path]
        elif "qsv" in enc or "Intel" in enc:
            return ["ffmpeg", "-y", "-i", input_path, "-c:v", "h264_qsv", "-preset", "fast", "-vf", *vf, output_path]
        else:
            return ["ffmpeg", "-y", "-i", input_path, "-vf", *vf, output_path]

    def _remove_with_retry(self, path, filename):
        time.sleep(0.5)
        for attempt in range(3):
            try:
                os.remove(path)
                return True
            except PermissionError:
                time.sleep(1)
        self.error.emit(f"Could not delete {filename} — file may be locked")
        return False

    def _run_ffmpeg(self, cmd):
        """Run an ffmpeg command without popping up a console window on Windows."""
        kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.PIPE, "text": True}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return subprocess.run(cmd, check=True, **kwargs)

    def run(self):
        try:
            os.makedirs(self.input_dir, exist_ok=True)
            os.makedirs(self.output_dir, exist_ok=True)
            input_files = [f for f in os.listdir(self.input_dir) if f.endswith(f".{self.input_ext}")]

            if not input_files:
                self.progress.emit(f"No .{self.input_ext} files found in /Input")
                self.conversion_finished.emit()
                return

            for idx, filename in enumerate(input_files, 1):
                self.current_video.emit(filename)
                self.progress_percent.emit(int((idx - 1) / len(input_files) * 100))
                self.progress.emit(f"[{idx}/{len(input_files)}] {filename}")

                input_path = os.path.join(self.input_dir, filename)
                output_path = os.path.join(self.output_dir, filename.replace(f".{self.input_ext}", f".{self.output_ext}"))

                try:
                    self._run_ffmpeg(self._build_command(input_path, output_path))
                    if self.delete_original:
                        self._remove_with_retry(input_path, filename)
                except subprocess.CalledProcessError:
                    self.progress.emit(f"GPU failed — falling back to CPU for {filename}")
                    try:
                        self._run_ffmpeg(self._build_command(input_path, output_path, "CPU fallback"))
                        if self.delete_original:
                            self._remove_with_retry(input_path, filename)
                    except subprocess.CalledProcessError as e:
                        err_msg = (e.stderr or "").strip().splitlines()[-1] if e.stderr else str(e)
                        self.error.emit(f"Failed: {filename} — {err_msg}")

            self.progress_percent.emit(100)
            self.progress.emit("All files converted successfully.")
            self.conversion_finished.emit()
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")
            self.conversion_finished.emit()


# ─── Main Window ────────────────────────────────────────────────────────────────

class VideoConverterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.settings = QtCore.QSettings("FFmpegConverter", "VideoConverter")
        self._build_ui()
        self._apply_style()
        self._setup_tray()
        self._load_settings()

    def _make_app_icon(self):
        pix = QtGui.QPixmap(64, 64)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(COLORS['bg'])))
        painter.setPen(QPen(QColor(COLORS['accent']), 3))
        painter.drawEllipse(4, 4, 56, 56)
        painter.setBrush(QBrush(QColor(COLORS['accent'])))
        painter.setPen(Qt.NoPen)
        triangle = QtGui.QPolygon([
            QtCore.QPoint(24, 18),
            QtCore.QPoint(24, 46),
            QtCore.QPoint(48, 32),
        ])
        painter.drawPolygon(triangle)
        painter.end()
        return QtGui.QIcon(pix)

    def _setup_tray(self):
        icon = self._make_app_icon()
        self.setWindowIcon(icon)

        self.tray_icon = QtWidgets.QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("FFMPEG CONVERTER")

        tray_menu = QtWidgets.QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self._restore_from_tray)
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QtWidgets.QApplication.instance().quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_activated)

        if QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()

    def _on_tray_activated(self, reason):
        if reason in (
            QtWidgets.QSystemTrayIcon.ActivationReason.Trigger,
            QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self._restore_from_tray()

    def _restore_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        if (
            getattr(self, "minimize_to_tray_checkbox", None)
            and self.minimize_to_tray_checkbox.isChecked()
            and self.tray_icon.isVisible()
        ):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "FFMPEG CONVERTER",
                "Still running in the background. Right-click the tray icon to quit.",
                QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                3000,
            )
        else:
            event.accept()
            QtWidgets.QApplication.instance().quit()

    def _apply_style(self):
        self.setStyleSheet(STYLESHEET)
        self.setObjectName("MainWindow")

    def _build_ui(self):
        self.setWindowTitle("FFMPEG CONVERTER")
        self.setFixedSize(480, 780)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self._drag_pos = None

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar
        title_bar = self._make_title_bar()
        root.addWidget(title_bar)

        # ── Body
        body = QtWidgets.QWidget()
        body_layout = QtWidgets.QVBoxLayout(body)
        body_layout.setContentsMargins(28, 24, 28, 28)
        body_layout.setSpacing(20)

        # ── Folders Row
        body_layout.addWidget(SectionLabel("Folders"))
        folder_row = QtWidgets.QHBoxLayout()
        folder_row.setSpacing(16)

        in_folder_col = self._make_folder_group("INPUT", "Input")
        self.input_dir_edit = in_folder_col[1]

        out_folder_col = self._make_folder_group("OUTPUT", "Output")
        self.output_dir_edit = out_folder_col[1]

        folder_row.addLayout(in_folder_col[0])
        folder_row.addLayout(out_folder_col[0])
        body_layout.addLayout(folder_row)

        # ── Format Row
        body_layout.addWidget(SectionLabel("Format"))
        fmt_row = QtWidgets.QHBoxLayout()
        fmt_row.setSpacing(16)

        in_col = self._make_combo_group("INPUT", ["webm", "mp4", "avi", "mkv", "mov", "flv", "wmv"], "webm")
        self.input_ext_combo = in_col[1]

        arrow = QtWidgets.QLabel("→")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setStyleSheet(f"color: {COLORS['accent']}; font-size: 20px; padding-top: 18px;")
        arrow.setFixedWidth(30)

        out_col = self._make_combo_group("OUTPUT", ["mp4", "webm", "avi", "mkv", "mov", "flv", "wmv"], "mp4")
        self.output_ext_combo = out_col[1]

        fmt_row.addLayout(in_col[0])
        fmt_row.addWidget(arrow)
        fmt_row.addLayout(out_col[0])
        body_layout.addLayout(fmt_row)

        # ── Encoder
        body_layout.addWidget(SectionLabel("Encoder"))
        self.encoder_combo = QtWidgets.QComboBox()
        self.encoder_combo.addItems([
            "CPU (libx264) — Default",
            "NVIDIA GPU (h264_nvenc)",
            "AMD GPU (h264_amf)",
            "Intel GPU (h264_qsv)",
        ])
        body_layout.addWidget(self.encoder_combo)

        # ── Status Row
        status_row = QtWidgets.QHBoxLayout()
        self.status_badge = PillBadge("IDLE", COLORS['text_muted'])
        self.file_counter = ValueLabel("0 files queued")
        status_row.addWidget(self.status_badge)
        status_row.addStretch()
        status_row.addWidget(self.file_counter)
        body_layout.addLayout(status_row)

        # ── Progress Track
        prog_col = QtWidgets.QVBoxLayout()
        prog_col.setSpacing(6)
        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        pct_row = QtWidgets.QHBoxLayout()
        self.current_file_label = ValueLabel("—")
        self.pct_label = ValueLabel("0%")
        pct_row.addWidget(self.current_file_label)
        pct_row.addStretch()
        pct_row.addWidget(self.pct_label)

        prog_col.addLayout(pct_row)
        prog_col.addWidget(self.progress_bar)
        body_layout.addLayout(prog_col)

        # ── Log
        body_layout.addWidget(SectionLabel("Log"))
        self.log_area = LogArea()
        self.log_area.append_log("System ready. Set your folders and press EXECUTE.", COLORS['text_muted'])
        body_layout.addWidget(self.log_area)

        body_layout.addStretch()

        # ── Button
        self.start_button = GlowButton("EXECUTE")
        self.start_button.clicked.connect(self._on_start)
        body_layout.addWidget(self.start_button)

        # ── Tabs
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(body, "CONVERT")
        self.tabs.addTab(self._build_settings_tab(), "SETTINGS")
        root.addWidget(self.tabs)

    def _build_settings_tab(self):
        content = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(20)

        # ── Default Folders
        layout.addWidget(SectionLabel("Default Folders"))
        folder_row = QtWidgets.QHBoxLayout()
        folder_row.setSpacing(16)

        in_folder_col = self._make_folder_group("INPUT", "Input")
        self.default_input_dir_edit = in_folder_col[1]

        out_folder_col = self._make_folder_group("OUTPUT", "Output")
        self.default_output_dir_edit = out_folder_col[1]

        folder_row.addLayout(in_folder_col[0])
        folder_row.addLayout(out_folder_col[0])
        layout.addLayout(folder_row)

        # ── Default Format
        layout.addWidget(SectionLabel("Default Format"))
        fmt_row = QtWidgets.QHBoxLayout()
        fmt_row.setSpacing(16)

        in_col = self._make_combo_group("INPUT", ["webm", "mp4", "avi", "mkv", "mov", "flv", "wmv"], "webm")
        self.default_input_combo = in_col[1]

        arrow = QtWidgets.QLabel("→")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setStyleSheet(f"color: {COLORS['accent']}; font-size: 20px; padding-top: 18px;")
        arrow.setFixedWidth(30)

        out_col = self._make_combo_group("OUTPUT", ["mp4", "webm", "avi", "mkv", "mov", "flv", "wmv"], "mp4")
        self.default_output_combo = out_col[1]

        fmt_row.addLayout(in_col[0])
        fmt_row.addWidget(arrow)
        fmt_row.addLayout(out_col[0])
        layout.addLayout(fmt_row)

        # ── Default Encoder
        layout.addWidget(SectionLabel("Default Encoder"))
        self.default_encoder_combo = QtWidgets.QComboBox()
        self.default_encoder_combo.addItems([
            "CPU (libx264) — Default",
            "NVIDIA GPU (h264_nvenc)",
            "AMD GPU (h264_amf)",
            "Intel GPU (h264_qsv)",
        ])
        layout.addWidget(self.default_encoder_combo)

        # ── Behavior
        layout.addWidget(SectionLabel("Behavior"))
        self.delete_original_checkbox = QtWidgets.QCheckBox("Delete original file after conversion")
        layout.addWidget(self.delete_original_checkbox)
        self.autoclose_checkbox = QtWidgets.QCheckBox("Automatically close when conversion finishes")
        layout.addWidget(self.autoclose_checkbox)
        self.notify_checkbox = QtWidgets.QCheckBox("Show desktop notification when conversion finishes")
        layout.addWidget(self.notify_checkbox)
        self.sound_checkbox = QtWidgets.QCheckBox("Play sound when conversion finishes")
        layout.addWidget(self.sound_checkbox)
        self.minimize_to_tray_checkbox = QtWidgets.QCheckBox("Minimize to system tray instead of closing")
        layout.addWidget(self.minimize_to_tray_checkbox)

        layout.addStretch()

        self.settings_saved_label = ValueLabel("")
        self.settings_saved_label.setStyleSheet(f"""
            color: {COLORS['success']};
            font-family: 'Courier New', monospace;
            font-size: 11px;
        """)
        self.settings_saved_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.settings_saved_label)

        save_button = GlowButton("SAVE DEFAULTS")
        save_button.clicked.connect(self._on_save_settings)
        layout.addWidget(save_button)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        return scroll

    def _make_title_bar(self):
        bar = QtWidgets.QWidget()
        bar.setFixedHeight(44)
        bar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        bar.mousePressEvent = self._on_bar_press
        bar.mouseMoveEvent = self._on_bar_move

        layout = QtWidgets.QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)

        # Amber dot + title
        dot = QtWidgets.QLabel("▶")
        dot.setStyleSheet(f"color: {COLORS['accent']}; font-size: 10px; background: transparent; border: none;")

        title = QtWidgets.QLabel("FFMPEG CONVERTER")
        title.setStyleSheet(f"""
            color: {COLORS['text']};
            font-family: 'Courier New', monospace;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 4px;
            background: transparent;
            border: none;
        """)

        layout.addWidget(dot)
        layout.addSpacing(8)
        layout.addWidget(title)
        layout.addStretch()

        # Window controls
        for sym, color, fn in [("—", COLORS['text_muted'], self.showMinimized),
                                ("✕", COLORS['error'], self.close)]:
            btn = QtWidgets.QPushButton(sym)
            btn.setFixedSize(28, 28)
            btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLORS['text_muted']};
                    border: none;
                    font-size: 14px;
                    border-radius: 14px;
                }}
                QPushButton:hover {{
                    background: {color}33;
                    color: {color};
                }}
            """)
            btn.clicked.connect(fn)
            layout.addWidget(btn)

        return bar

    def _make_combo_group(self, label_text, items, default):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(6)
        lbl = QtWidgets.QLabel(label_text)
        lbl.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-family: 'Courier New', monospace;
            font-size: 9px;
            letter-spacing: 2px;
        """)
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setCurrentText(default)
        layout.addWidget(lbl)
        layout.addWidget(combo)
        return layout, combo

    def _make_folder_group(self, label_text, default_path):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(6)
        lbl = QtWidgets.QLabel(label_text)
        lbl.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-family: 'Courier New', monospace;
            font-size: 9px;
            letter-spacing: 2px;
        """)

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(8)

        line_edit = QtWidgets.QLineEdit(default_path)
        line_edit.setPlaceholderText("Path to folder...")
        line_edit.setEnabled(False)
        line_edit.setCursor(QtGui.QCursor(Qt.ArrowCursor))

        browse_button = QtWidgets.QPushButton("…")
        browse_button.setFixedSize(36, 36)
        browse_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        browse_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['surface']};
                color: {COLORS['accent']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border-color: {COLORS['accent_dim']};
                background-color: {COLORS['surface2']};
            }}
        """)
        browse_button.clicked.connect(lambda: self._browse_folder(line_edit))

        row.addWidget(line_edit)
        row.addWidget(browse_button)

        layout.addWidget(lbl)
        layout.addLayout(row)
        return layout, line_edit

    def _browse_folder(self, line_edit):
        start_dir = line_edit.text().strip() or os.getcwd()
        if not os.path.isdir(start_dir):
            start_dir = os.getcwd()
        chosen = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", start_dir)
        if chosen:
            line_edit.setText(chosen)

    # ── Drag support for frameless window
    def _on_bar_press(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def _on_bar_move(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    # ── Slots
    def _on_start(self):
        input_dir = self.input_dir_edit.text().strip() or "Input"
        output_dir = self.output_dir_edit.text().strip() or "Output"

        if not os.path.isdir(input_dir):
            self.log_area.append_log(
                f"<span style='color:{COLORS['error']}'>✕</span> Input folder not found: {input_dir}",
                COLORS['error']
            )
            return

        self.start_button.setEnabled(False)
        self.start_button.setText("RUNNING...")
        self.start_button._timer.start(30)

        self.progress_bar.setValue(0)
        self.progress_bar.set_running(True)
        self.pct_label.setText("0%")
        self.current_file_label.setText("Initializing...")

        # Pass raw combo text — _build_command does keyword matching
        selected_encoder = self.encoder_combo.currentText()

        self.worker = ConversionWorker(
            input_dir, output_dir,
            selected_encoder,
            self.input_ext_combo.currentText(),
            self.output_ext_combo.currentText(),
            delete_original=self.delete_original_checkbox.isChecked(),
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.progress_percent.connect(self._on_percent)
        self.worker.current_video.connect(self._on_current_video)
        self.worker.error.connect(self._on_error)
        self.worker.conversion_finished.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, message):
        self.log_area.append_log(f"<span style='color:{COLORS['text_muted']}'>›</span> {message}")

    def _on_percent(self, pct):
        self.progress_bar.setValue(pct)
        self.pct_label.setText(f"{pct}%")

    def _on_current_video(self, name):
        self.current_file_label.setText(name)

    def _on_error(self, message):
        self.log_area.append_log(f"<span style='color:{COLORS['error']}'>✕</span> {message}", COLORS['error'])

    def _on_finished(self):
        self.start_button._timer.stop()
        self.start_button.setEnabled(True)
        self.start_button.setText("EXECUTE")
        self.start_button._update_style(False)
        self.progress_bar.set_running(False)
        self.current_file_label.setText("Complete")
        self.log_area.append_log(
            f"<span style='color:{COLORS['success']}'>✓</span> Conversion complete.",
            COLORS['success']
        )

        if self.notify_checkbox.isChecked() and self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                "Conversion Complete",
                "All files have been converted successfully.",
                QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                4000,
            )

        if self.sound_checkbox.isChecked():
            QtWidgets.QApplication.beep()

        if self.autoclose_checkbox.isChecked():
            self.log_area.append_log(
                f"<span style='color:{COLORS['text_muted']}'>›</span> Auto-close enabled — closing shortly..."
            )
            QTimer.singleShot(1500, self.close)

    # ── Settings persistence
    def _on_save_settings(self):
        self._save_settings()

        # Apply the new defaults immediately to the Convert tab
        self.input_dir_edit.setText(self.default_input_dir_edit.text())
        self.output_dir_edit.setText(self.default_output_dir_edit.text())
        self.input_ext_combo.setCurrentText(self.default_input_combo.currentText())
        self.output_ext_combo.setCurrentText(self.default_output_combo.currentText())
        self.encoder_combo.setCurrentText(self.default_encoder_combo.currentText())

        self.settings_saved_label.setText("✓ Defaults saved")
        QTimer.singleShot(2000, lambda: self.settings_saved_label.setText(""))

    def _save_settings(self):
        self.settings.setValue("default_input_dir", self.default_input_dir_edit.text())
        self.settings.setValue("default_output_dir", self.default_output_dir_edit.text())
        self.settings.setValue("default_input_ext", self.default_input_combo.currentText())
        self.settings.setValue("default_output_ext", self.default_output_combo.currentText())
        self.settings.setValue("default_encoder", self.default_encoder_combo.currentText())
        self.settings.setValue("auto_close", self.autoclose_checkbox.isChecked())
        self.settings.setValue("delete_original", self.delete_original_checkbox.isChecked())
        self.settings.setValue("notify_on_finish", self.notify_checkbox.isChecked())
        self.settings.setValue("play_sound", self.sound_checkbox.isChecked())
        self.settings.setValue("minimize_to_tray", self.minimize_to_tray_checkbox.isChecked())

    def _load_settings(self):
        input_dir = self.settings.value("default_input_dir", "Input")
        output_dir = self.settings.value("default_output_dir", "Output")
        input_ext = self.settings.value("default_input_ext", "webm")
        output_ext = self.settings.value("default_output_ext", "mp4")
        encoder = self.settings.value("default_encoder", "CPU (libx264) — Default")
        auto_close = self.settings.value("auto_close", False, type=bool)
        delete_original = self.settings.value("delete_original", False, type=bool)
        notify_on_finish = self.settings.value("notify_on_finish", True, type=bool)
        play_sound = self.settings.value("play_sound", True, type=bool)
        minimize_to_tray = self.settings.value("minimize_to_tray", False, type=bool)

        # Populate both the Settings tab (the stored defaults) and the
        # Convert tab (so the app "loads them straight up").
        for line_edit, value in (
            (self.default_input_dir_edit, input_dir),
            (self.default_output_dir_edit, output_dir),
            (self.input_dir_edit, input_dir),
            (self.output_dir_edit, output_dir),
        ):
            line_edit.setText(value)

        for combo, value in (
            (self.default_input_combo, input_ext),
            (self.default_output_combo, output_ext),
            (self.default_encoder_combo, encoder),
            (self.input_ext_combo, input_ext),
            (self.output_ext_combo, output_ext),
            (self.encoder_combo, encoder),
        ):
            idx = combo.findText(value)
            if idx >= 0:
                combo.setCurrentIndex(idx)

        self.autoclose_checkbox.setChecked(auto_close)
        self.delete_original_checkbox.setChecked(delete_original)
        self.notify_checkbox.setChecked(notify_on_finish)
        self.sound_checkbox.setChecked(play_sound)
        self.minimize_to_tray_checkbox.setChecked(minimize_to_tray)


# ─── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setQuitOnLastWindowClosed(False)

    # Dark Fusion palette base
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLORS['bg']))
    palette.setColor(QPalette.WindowText, QColor(COLORS['text']))
    palette.setColor(QPalette.Base, QColor(COLORS['surface']))
    palette.setColor(QPalette.AlternateBase, QColor(COLORS['surface2']))
    palette.setColor(QPalette.Text, QColor(COLORS['text']))
    palette.setColor(QPalette.Button, QColor(COLORS['surface']))
    palette.setColor(QPalette.ButtonText, QColor(COLORS['text']))
    palette.setColor(QPalette.Highlight, QColor(COLORS['accent']))
    palette.setColor(QPalette.HighlightedText, QColor(COLORS['bg']))
    app.setPalette(palette)

    window = VideoConverterApp()
    window.show()
    sys.exit(app.exec())