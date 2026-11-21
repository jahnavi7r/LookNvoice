"""Full-screen calibration: 12 dots (each of the 6 card positions twice),
then shows the measured accuracy for a few seconds, or a Retry option if failed."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen
from core.eye_tracker import CALIB_GRID
from ui.theme import CARD_PALETTE, UI_FONT

DOT_MS = 1600        # time per dot
RESULT_MS = 3500     # how long the accuracy result stays on screen when successful

# Instruction screen shown before the dots: short, simple words in 3 languages.
INSTRUCTIONS = [
    (["మీ తలను కదపకండి.", "ప్రతి చుక్కను కళ్లతో చూడండి."], CARD_PALETTE[0]),# Telugu
]
INSTRUCTION_FONTS = ["Nirmala UI", "Noto Sans Telugu", "Noto Sans Devanagari", "Segoe UI", "Arial"]
INSTRUCTION_SIZE = 0.045


class CalibrationOverlay(QWidget):
    finished = pyqtSignal(object)   # accuracy 0..1 when calibration succeeds

    def __init__(self, tracker, sw, sh):
        super().__init__()
        self.tracker, self.sw, self.sh = tracker, sw, sh
        self.idx = -1
        self.result_text = ""
        self.result_color = "#94a3b8"
        self._failed = False
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background:#0b1220;")

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._next)

        # Retry UI shown ONLY when calibration fails
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.addStretch(3)

        self.fail_label = QLabel("")
        self.fail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fail_label.setWordWrap(True)
        self.fail_label.setStyleSheet(
            f"color: #f87171; font-family: {UI_FONT}; font-size: 32px; font-weight: bold;"
        )
        self.fail_label.hide()
        layout.addWidget(self.fail_label)

        layout.addSpacing(30)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.retry_btn = QPushButton("↻  Retry Calibration  /  మళ్లీ ప్రయత్నించండి  /  पुनः प्रयास करें")
        self.retry_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.retry_btn.setMinimumSize(520, 110)
        self.retry_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CARD_PALETTE[1]};
                color: #14161D;
                font-family: {UI_FONT};
                font-size: 28px;
                font-weight: bold;
                border-radius: 22px;
                padding: 18px 36px;
                border: 4px solid #38BDF8;
            }}
            QPushButton:hover {{
                background-color: #8FC9A2;
            }}
        """)
        self.retry_btn.clicked.connect(self.start)
        self.retry_btn.hide()
        btn_row.addWidget(self.retry_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addStretch(2)

    def start(self):
        self.timer.stop()
        self._failed = False
        self.fail_label.hide()
        self.retry_btn.hide()
        self.tracker.recalibrate()
        self.idx = -1
        self.result_text = ""
        self.showFullScreen()
        self.activateWindow()
        self.setFocus()
        self.update()
        QTimer.singleShot(1800, self._next)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif self._failed and event.key() in (
            Qt.Key.Key_R, Qt.Key.Key_C, Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space
        ):
            self.start()

    def _next(self):
        self.tracker.hide_dot()
        self.idx += 1
        if self.idx >= len(CALIB_GRID):
            acc = self.tracker.finish_calibration(self.sw, self.sh)
            self._acc = acc
            if acc is None:
                self._failed = True
                self.fail_label.setText(
                    f"{self.tracker.report_text}\n\n"
                    "Calibration failed — face a light, sit 50–60 cm from the camera, keep your head still,\n"
                    "and click Retry (or press R / C) to try again."
                )
                self.fail_label.show()
                self.retry_btn.show()
                self.update()
                return

            hint = ""
            if acc < 0.6:
                hint = "\nLow accuracy: face a light, sit 50-60 cm away, keep your head still,\nthen press C anytime to recalibrate."
                self.result_color = "#fbbf24"
            else:
                self.result_color = "#4ade80"
            self.result_text = self.tracker.report_text + hint
            self.update()
            QTimer.singleShot(RESULT_MS, self._close_and_emit)
            return

        self.tracker.show_dot(self.idx, self.sw, self.sh)
        self.update()
        self.timer.start(DOT_MS)

    def _close_and_emit(self):
        self.close()
        self.finished.emit(getattr(self, "_acc", None))

    def _draw_instructions(self, p):
        """Bold, centred instructions in Telugu, English and Hindi, sized to the screen."""
        w, h = self.width(), self.height()
        size = max(26, int(h * INSTRUCTION_SIZE))

        while True:
            font = QFont()
            font.setFamilies(INSTRUCTION_FONTS)
            font.setBold(True)
            font.setPixelSize(size)
            fm = QFontMetrics(font)
            longest = max(fm.horizontalAdvance(t) for lines, _ in INSTRUCTIONS for t in lines)
            if longest <= w * 0.88 or size <= 20:
                break
            size -= 2

        p.setFont(font)
        line_h = int(size * 1.45)
        gap = int(size * 0.9)
        n_lines = sum(len(lines) for lines, _ in INSTRUCTIONS)
        total = n_lines * line_h + (len(INSTRUCTIONS) - 1) * gap
        y = (h - total) // 2

        for i, (lines, color) in enumerate(INSTRUCTIONS):
            p.setPen(QColor(color))
            for text in lines:
                p.drawText(QRect(0, y, w, line_h), Qt.AlignmentFlag.AlignCenter, text)
                y += line_h
            if i < len(INSTRUCTIONS) - 1:
                p.setPen(QPen(QColor("#2C3240"), 2))
                p.drawLine(w // 2 - 70, y + gap // 2, w // 2 + 70, y + gap // 2)
                y += gap

    def paintEvent(self, _):
        p = QPainter(self)
        p.setFont(QFont("Arial", 18))
        p.setPen(QColor("#94a3b8"))
        if self.idx < 0:
            self._draw_instructions(p)
            return
        if self.idx >= len(CALIB_GRID):
            if not self._failed:
                p.setPen(QColor(self.result_color))
                p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.result_text)
            return
        fx, fy = CALIB_GRID[self.idx]
        cx, cy = int(fx * self.width()), int(fy * self.height())
        p.setBrush(QColor("#22d3ee"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - 18, cy - 18, 36, 36)
        p.setBrush(QColor("#0b1220"))
        p.drawEllipse(cx - 5, cy - 5, 10, 10)