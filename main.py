
import sys
import os
import json
import threading
import time
from datetime import datetime
from functools import partial

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit,
    QScrollArea, QFrame, QSizePolicy, QCheckBox,
    QTabWidget, QDialog, QButtonGroup, QRadioButton,
    QMessageBox, QSpacerItem, QGroupBox, QAbstractScrollArea,
)
from PyQt6.QtCore import (
    Qt, QSize, QTimer, pyqtSignal, QObject, QThread,
    QPropertyAnimation, QPoint,
)
from PyQt6.QtGui import (
    QPixmap, QFont, QColor, QPalette, QPainter,
    QLinearGradient, QBrush, QFontDatabase, QCursor, QIcon,
)

sys.path.insert(0, os.path.dirname(__file__))
from database import (
    init_db, validate_user, register_user,
    get_all_plants, get_plants_by_filter,
    add_to_cart, get_cart, remove_from_cart, clear_cart,
    toggle_wishlist, get_wishlist,
    place_order, get_orders,
    save_note, get_note,
    get_stats,
)
from planner import (
    get_recommendation, get_seasonal_plants,
    get_budget_suggestions, get_purpose_suggestions,
    get_all_purposes, get_all_budget_tiers, get_difficulty_tip,
)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# ─────────────────────────────────────────────────────────────────────────────
#  COLOUR PALETTES
# ─────────────────────────────────────────────────────────────────────────────

PALETTES = {
    "Forest Dark": {
        "bg":       "#080E0C",
        "panel":    "#0E1814",
        "card":     "#14221C",
        "accent":   "#39D353",
        "accent2":  "#00B4D8",
        "text":     "#DCF0E4",
        "dim":      "#78A082",
        "danger":   "#F85149",
        "warning":  "#E3B341",
        "border":   "#284637",
        "tag_a":    "#14592D",
        "tag_b":    "#003C5A",
        "tag_c":    "#501400",
    },
    "Deep Ocean": {
        "bg":       "#050A14",
        "panel":    "#0A1226",
        "card":     "#101C37",
        "accent":   "#00B4D8",
        "accent2":  "#39D353",
        "text":     "#D2E4F8",
        "dim":      "#648CB4",
        "danger":   "#FF5050",
        "warning":  "#FFC83C",
        "border":   "#1E3764",
        "tag_a":    "#004664",
        "tag_b":    "#145A28",
        "tag_c":    "#641E00",
    },
    "Midnight Purple": {
        "bg":       "#0A0614",
        "panel":    "#120C24",
        "card":     "#1C1437",
        "accent":   "#A064FF",
        "accent2":  "#39D353",
        "text":     "#E1D7F8",
        "dim":      "#826EAA",
        "danger":   "#FF5050",
        "warning":  "#FFC83C",
        "border":   "#37285A",
        "tag_a":    "#50288C",
        "tag_b":    "#145A28",
        "tag_c":    "#781E00",
    },
    "Light Garden": {
        "bg":       "#F0F8F0",
        "panel":    "#DCEEDF",
        "card":     "#FFFFFF",
        "accent":   "#1E823C",
        "accent2":  "#0078B4",
        "text":     "#14281C",
        "dim":      "#5A7862",
        "danger":   "#C80000",
        "warning":  "#B47800",
        "border":   "#B4D2B9",
        "tag_a":    "#1E823C",
        "tag_b":    "#0064A0",
        "tag_c":    "#A05000",
    },
}

_theme_name = ["Light Garden"]

def C(key):
    return PALETTES[_theme_name[0]][key]


PLANT_EMOJI_MAP = {
    "Snake Plant":"🐍","Money Plant":"💰","Aloe Vera":"🌵","Spider Plant":"🕷",
    "Rose":"🌹","ZZ Plant":"🌱","Peace Lily":"🌸","Cactus":"🌵",
    "Marigold":"🌼","Sunflower":"🌻","Krishnachura":"🔥","Shapla":"💧",
    "Neem":"🍀","Tulsi":"🌿","Mehendi":"🍃","Kadam":"🌳","Bamboo":"🎋",
    "Curry Leaf":"🍛","Aparajita":"💙","Brahmi":"🧠","Areca Palm":"🌴",
    "Paan":"🫚","Lemon Grass":"🍋","Jasmine (Beli)":"⚪","Gandharaj":"🌟",
    "Joba (Hibiscus)":"🌺","Mint":"🫐","Drumstick (Moringa)":"🥢",
    "Bamboo Palm":"🌴","Duranta":"🟣",
}

# ─────────────────────────────────────────────────────────────────────────────
#  STYLESHEET GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def build_stylesheet():
    c = PALETTES[_theme_name[0]]
    return f"""
QWidget {{
    background-color: {c['bg']};
    color: {c['text']};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}}
QMainWindow, QDialog {{ background-color: {c['bg']}; }}

/* ── Scrollbars ── */
QScrollBar:vertical {{
    background: {c['panel']}; width: 8px; border-radius: 4px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {c['border']}; border-radius: 4px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {c['accent']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {c['panel']}; height: 8px; border-radius: 4px; margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {c['border']}; border-radius: 4px; min-width: 24px;
}}
QScrollBar::handle:horizontal:hover {{ background: {c['accent']}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ── Buttons ── */
QPushButton {{
    background-color: {c['border']};
    color: {c['text']};
    border: none; border-radius: 7px;
    padding: 8px 16px; font-weight: 600; font-size: 13px;
}}
QPushButton:hover {{ background-color: {c['accent']}; color: #000000; }}
QPushButton:pressed {{ background-color: {c['accent2']}; color: #000000; }}
QPushButton:disabled {{ background-color: {c['panel']}; color: {c['dim']}; }}

QPushButton[btntype="accent"] {{
    background-color: {c['accent']}; color: #0A0A0A;
}}
QPushButton[btntype="accent"]:hover {{ background-color: {c['accent2']}; color: #0A0A0A; }}

QPushButton[btntype="ghost"] {{
    background-color: transparent; border: 1px solid {c['border']}; color: {c['dim']};
}}
QPushButton[btntype="ghost"]:hover {{
    background-color: {c['panel']}; border-color: {c['accent']}; color: {c['text']};
}}

QPushButton[btntype="danger"] {{
    background-color: transparent; border: 1px solid {c['danger']}; color: {c['danger']};
}}
QPushButton[btntype="danger"]:hover {{ background-color: {c['danger']}; color: white; }}

QPushButton[btntype="warning"] {{
    background-color: {c['warning']}; color: #0A0A0A;
}}
QPushButton[btntype="warning"]:hover {{ background-color: {c['accent2']}; color: #0A0A0A; }}

QPushButton[btntype="nav"] {{
    background-color: transparent; color: {c['dim']};
    border: none; border-radius: 8px; text-align: left;
    padding: 9px 14px; font-size: 13px;
}}
QPushButton[btntype="nav"]:hover {{ background-color: {c['panel']}; color: {c['text']}; }}
QPushButton[btntype="nav"][active="true"] {{
    background-color: {c['panel']}; color: {c['accent']};
    border-left: 3px solid {c['accent']};
}}

/* ── Inputs ── */
QLineEdit, QTextEdit, QComboBox {{
    background-color: {c['panel']}; border: 1px solid {c['border']};
    border-radius: 7px; padding: 8px 12px; color: {c['text']}; font-size: 13px;
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border-color: {c['accent']}; background-color: {c['card']};
}}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox::down-arrow {{ width: 10px; height: 10px; }}
QComboBox QAbstractItemView {{
    background-color: {c['card']}; border: 1px solid {c['border']};
    color: {c['text']}; selection-background-color: {c['border']};
    border-radius: 6px; padding: 2px;
}}

/* ── Tabs ── */
QTabWidget::pane {{
    border: 1px solid {c['border']}; border-radius: 8px;
    background-color: {c['panel']}; top: -1px;
}}
QTabBar::tab {{
    background-color: {c['bg']}; color: {c['dim']};
    padding: 8px 18px; border-top-left-radius: 7px; border-top-right-radius: 7px;
    border: 1px solid {c['border']}; border-bottom: none; margin-right: 2px;
}}
QTabBar::tab:selected {{ background-color: {c['panel']}; color: {c['accent']}; }}
QTabBar::tab:hover {{ background-color: {c['card']}; color: {c['text']}; }}

/* ── Frames ── */
QFrame[frameclass="card"] {{
    background-color: {c['card']}; border: 1px solid {c['border']}; border-radius: 10px;
}}
QFrame[frameclass="separator"] {{
    background-color: {c['border']}; max-height: 1px;
}}

/* ── CheckBox ── */
QCheckBox {{ color: {c['dim']}; spacing: 6px; }}
QCheckBox:hover {{ color: {c['text']}; }}
QCheckBox::indicator {{
    width: 15px; height: 15px; border-radius: 4px;
    border: 1px solid {c['border']}; background: {c['panel']};
}}
QCheckBox::indicator:checked {{
    background-color: {c['accent']}; border-color: {c['accent']};
}}

/* ── RadioButton ── */
QRadioButton {{ color: {c['dim']}; spacing: 6px; }}
QRadioButton:hover {{ color: {c['text']}; }}
QRadioButton::indicator {{
    width: 14px; height: 14px; border-radius: 7px;
    border: 1px solid {c['border']}; background: {c['panel']};
}}
QRadioButton::indicator:checked {{
    background-color: {c['accent']}; border-color: {c['accent']};
}}

/* ── ScrollArea ── */
QScrollArea {{ border: none; background-color: transparent; }}
QScrollArea > QWidget > QWidget {{ background-color: transparent; }}

/* ── Labels ── */
QLabel {{ background-color: transparent; }}
"""


def style_btn(btn, btntype="ghost"):
    btn.setProperty("btntype", btntype)
    btn.style().unpolish(btn)
    btn.style().polish(btn)
    return btn


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def lbl(text, color=None, bold=False, size=None, wrap=False):
    l = QLabel(text)
    l.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    style = "background: transparent;"
    if color: style += f" color: {color};"
    if bold:  style += " font-weight: bold;"
    if size:  style += f" font-size: {size}px;"
    l.setStyleSheet(style)
    if wrap:  l.setWordWrap(True)
    return l


def hsep():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setProperty("frameclass", "separator")
    f.setStyleSheet(f"background-color: {C('border')}; max-height: 1px; border: none;")
    return f


def hspace(w=10):
    sp = QWidget()
    sp.setFixedWidth(w)
    sp.setStyleSheet("background: transparent;")
    return sp


def vspace(h=10):
    sp = QWidget()
    sp.setFixedHeight(h)
    sp.setStyleSheet("background: transparent;")
    return sp


def card_frame():
    f = QFrame()
    f.setProperty("frameclass", "card")
    f.setStyleSheet(f"""
        QFrame[frameclass="card"] {{
            background-color: {C('card')};
            border: 1px solid {C('border')};
            border-radius: 10px;
        }}
    """)
    return f


def load_pixmap(image_path, w=None, h=None):
    if not image_path:
        return None
    full = os.path.join(ASSETS_DIR, os.path.basename(image_path)) \
        if not os.path.isabs(image_path) else image_path
    if not os.path.exists(full):
        return None
    px = QPixmap(full)
    if px.isNull():
        return None
    if w and h:
        px = px.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                       Qt.TransformationMode.SmoothTransformation)
        # centre-crop
        if px.width() > w or px.height() > h:
            x = (px.width()  - w) // 2
            y = (px.height() - h) // 2
            px = px.copy(x, y, w, h)
    return px


def plant_image_label(image_path, w=140, h=130):
    lb = QLabel()
    lb.setFixedSize(w, h)
    lb.setStyleSheet(f"border-radius: 6px; background-color: {C('panel')}; border: none;")
    lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    px = load_pixmap(image_path, w, h)
    if px:
        lb.setPixmap(px)
    else:
        name = os.path.splitext(os.path.basename(image_path or ""))[0]
        emoji = PLANT_EMOJI_MAP.get(name.replace("_", " ").title(), "🌿")
        lb.setText(emoji)
        lb.setStyleSheet(lb.styleSheet() + " font-size: 40px;")
    return lb


# ─────────────────────────────────────────────────────────────────────────────
#  TOAST WIDGET
# ─────────────────────────────────────────────────────────────────────────────

class ToastWidget(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            background-color: {C('card')};
            color: {C('accent')};
            border: 1px solid {C('accent')};
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
        """)
        self.hide()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_msg(self, msg, ms=2500):
        self.setText(msg)
        self.adjustSize()
        parent = self.parentWidget()
        if parent:
            pw, ph = parent.width(), parent.height()
            self.setFixedWidth(min(500, pw - 40))
            self.move((pw - self.width()) // 2, ph - 70)
        self.raise_()
        self.show()
        self._timer.start(ms)


# ─────────────────────────────────────────────────────────────────────────────
#  PLANT DETAIL DIALOG
# ─────────────────────────────────────────────────────────────────────────────

class PlantDetailDialog(QDialog):
    cart_updated   = pyqtSignal()
    wish_updated   = pyqtSignal()

    def __init__(self, row, username, wishlist_set, parent=None):
        super().__init__(parent)
        self.row         = row
        self.username    = username
        self.wishlist_set = wishlist_set
        self._setup_ui()

    def _r(self, i): return self.row[i]

    def _setup_ui(self):
        name = self._r(1)
        self.setWindowTitle(f"🌿  {name}")
        self.setMinimumSize(780, 600)
        self.setStyleSheet(build_stylesheet())

        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # ── Left: image + actions ─────────────────────────────────────────
        left = QVBoxLayout()
        left.setSpacing(8)

        img_lbl = plant_image_label(self._r(4), 240, 260)
        img_lbl.setFixedSize(240, 260)
        left.addWidget(img_lbl)

        left.addWidget(hsep())

        price_lbl = lbl(f"৳{self._r(2)}", C("accent"), bold=True, size=22)
        left.addWidget(price_lbl)
        left.addWidget(lbl("BDT", C("dim")))
        left.addSpacing(8)

        in_wish = self._r(1) in self.wishlist_set
        self.wish_btn = QPushButton("💚 In Wishlist" if in_wish else "🤍 Add to Wishlist")
        style_btn(self.wish_btn, "accent" if in_wish else "ghost")
        self.wish_btn.setMinimumHeight(34)
        self.wish_btn.clicked.connect(self._toggle_wish)
        left.addWidget(self.wish_btn)

        cart_btn = QPushButton("🛒  Add to Cart")
        style_btn(cart_btn, "accent")
        cart_btn.setMinimumHeight(40)
        cart_btn.clicked.connect(self._add_cart)
        left.addWidget(cart_btn)

        close_btn = QPushButton("Close")
        style_btn(close_btn, "ghost")
        close_btn.setMinimumHeight(34)
        close_btn.clicked.connect(self.accept)
        left.addWidget(close_btn)

        left.addStretch()
        left_w = QWidget()
        left_w.setLayout(left)
        left_w.setFixedWidth(256)
        root.addWidget(left_w)

        # ── Right: details ────────────────────────────────────────────────
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        right_w = QWidget()
        right = QVBoxLayout(right_w)
        right.setSpacing(6)
        right.setContentsMargins(0, 0, 8, 0)

        right.addWidget(lbl(self._r(1), C("text"), bold=True, size=20))
        right.addWidget(lbl(self._r(8), C("accent2"), size=15))   # bengali
        right.addWidget(lbl(self._r(3), C("dim")))                 # type
        right.addSpacing(8)

        # Badge row
        badge_row = QHBoxLayout()
        badge_row.setSpacing(6)
        for text, color in [
            (f"☀ {self._r(5)}", C("tag_a")),
            (f"📍 {self._r(6)}", C("tag_b")),
            (f"⭐ {self._r(11)}", C("accent") if self._r(11)=="Beginner"
                                  else C("warning") if self._r(11)=="Intermediate"
                                  else C("danger")),
        ]:
            b = lbl(text, color)
            b.setStyleSheet(b.styleSheet() +
                            f" background:{color}22; border-radius:5px; padding:3px 8px;")
            badge_row.addWidget(b)
        if self._r(12): badge_row.addWidget(_mini_badge("💨 Air", C("accent")))
        if self._r(13): badge_row.addWidget(_mini_badge("🍃 Edible", C("accent2")))
        if self._r(14): badge_row.addWidget(_mini_badge("🌸 Fragrant", C("warning")))
        badge_row.addStretch()
        right.addLayout(badge_row)

        right.addSpacing(8)
        right.addWidget(hsep())
        right.addSpacing(6)

        for label, value in [("Season", self._r(9)), ("Watering", self._r(10)),
                              ("Difficulty", self._r(11))]:
            row_w = QHBoxLayout()
            row_w.addWidget(lbl(f"{label}:", C("dim")))
            row_w.addWidget(lbl(value, C("text")))
            row_w.addStretch()
            right.addLayout(row_w)
        right.addSpacing(8)

        right.addWidget(lbl("About this plant", C("accent"), bold=True))
        desc = lbl(self._r(7), C("text"), wrap=True)
        right.addWidget(desc)

        right.addSpacing(8)
        right.addWidget(hsep())
        right.addSpacing(6)
        right.addWidget(lbl("Care Guide", C("accent2"), bold=True))
        care = lbl(self._r(15), C("dim"), wrap=True)
        right.addWidget(care)

        right.addSpacing(8)
        right.addWidget(hsep())
        right.addSpacing(6)
        right.addWidget(lbl("Your Notes", C("accent"), bold=True))
        self.note_edit = QTextEdit()
        self.note_edit.setFixedHeight(80)
        self.note_edit.setPlaceholderText("Write your personal notes here…")
        self.note_edit.setPlainText(get_note(self.username, self._r(1)))
        right.addWidget(self.note_edit)

        save_note_btn = QPushButton("Save Note")
        style_btn(save_note_btn, "ghost")
        save_note_btn.clicked.connect(self._save_note)
        right.addWidget(save_note_btn)
        right.addStretch()

        right_scroll.setWidget(right_w)
        root.addWidget(right_scroll, 1)

    def _add_cart(self):
        add_to_cart(self.username, self._r(1), self._r(2))
        self.cart_updated.emit()
        self.accept()

    def _toggle_wish(self):
        added = toggle_wishlist(self.username, self._r(1))
        if added:
            self.wishlist_set.add(self._r(1))
            self.wish_btn.setText("💚 In Wishlist")
            style_btn(self.wish_btn, "accent")
        else:
            self.wishlist_set.discard(self._r(1))
            self.wish_btn.setText("🤍 Add to Wishlist")
            style_btn(self.wish_btn, "ghost")
        self.wish_updated.emit()

    def _save_note(self):
        save_note(self.username, self._r(1), self.note_edit.toPlainText())


def _mini_badge(text, color):
    b = QLabel(text)
    b.setStyleSheet(f"color:{color}; background:{color}22; border-radius:5px;"
                    f" padding:3px 8px; font-size:12px;")
    return b


# ─────────────────────────────────────────────────────────────────────────────
#  PLANT CARD (used in Store + Planner)
# ─────────────────────────────────────────────────────────────────────────────

class PlantCard(QFrame):
    detail_requested = pyqtSignal(object)
    cart_requested   = pyqtSignal(object)
    wish_requested   = pyqtSignal(object)

    def __init__(self, row, wishlist_set, compact=False):
        super().__init__()
        self.row = row
        self.compact = compact
        self.wishlist_set = wishlist_set
        self._setup()

    def _setup(self):
        r = self.row
        self.setProperty("frameclass", "card")
        self.setStyleSheet(f"""
            QFrame[frameclass="card"] {{
                background-color: {C('card')};
                border: 1px solid {C('border')};
                border-radius: 10px;
            }}
            QFrame[frameclass="card"]:hover {{
                border-color: {C('accent')};
            }}
        """)
        h = 170 if self.compact else 180
        self.setFixedHeight(h)

        root = QHBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)

        # Thumbnail
        img_w = 90 if self.compact else 150
        img_h = h - 20
        img_lbl = plant_image_label(r[4], img_w, img_h)
        root.addWidget(img_lbl)

        # Middle info
        info = QVBoxLayout()
        info.setSpacing(3)
        info.addWidget(lbl(r[1], C("text"), bold=True, size=14))
        info.addWidget(lbl(r[8], C("accent2")))          # bengali
        info.addWidget(lbl(r[3], C("dim")))               # type
        info.addSpacing(2)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(6)
        badge_row.addWidget(lbl(f"☀ {r[5]}", C("tag_a")))
        badge_row.addWidget(lbl(f"📍 {r[6]}", C("tag_b")))
        diff_color = C("accent") if r[11]=="Beginner" else C("warning") if r[11]=="Intermediate" else C("danger")
        badge_row.addWidget(lbl(f"⭐ {r[11]}", diff_color))
        if r[12]: badge_row.addWidget(lbl("💨 Air", C("accent")))
        if r[13]: badge_row.addWidget(lbl("🍃 Edible", C("accent2")))
        if r[14]: badge_row.addWidget(lbl("🌸 Fragrant", C("warning")))
        badge_row.addStretch()
        info.addLayout(badge_row)

        if not self.compact:
            desc = r[7][:100] + ("…" if len(r[7]) > 100 else "")
            info.addWidget(lbl(desc, C("dim"), wrap=True))

        info.addStretch()
        root.addLayout(info, 1)

        # Right actions
        actions = QVBoxLayout()
        actions.setSpacing(4)
        actions.addWidget(lbl(f"৳{r[2]}", C("accent"), bold=True, size=15))
        actions.addWidget(lbl(r[9], C("dim")))   # season
        actions.addSpacing(4)

        detail_btn = QPushButton("View Details")
        style_btn(detail_btn, "ghost")
        detail_btn.setFixedWidth(160)
        detail_btn.setFixedHeight(30)
        detail_btn.clicked.connect(lambda: self.detail_requested.emit(self.row))
        actions.addWidget(detail_btn)

        cart_btn = QPushButton("🛒 Add to Cart")
        style_btn(cart_btn, "accent")
        cart_btn.setFixedWidth(160)
        cart_btn.setFixedHeight(32)
        cart_btn.clicked.connect(lambda: self.cart_requested.emit(self.row))
        actions.addWidget(cart_btn)

        in_wish = r[1] in self.wishlist_set
        self.wish_btn = QPushButton("💚 Wishlisted" if in_wish else "🤍 Wishlist")
        style_btn(self.wish_btn, "accent" if in_wish else "ghost")
        self.wish_btn.setFixedWidth(160)
        self.wish_btn.setFixedHeight(28)
        self.wish_btn.clicked.connect(lambda: self.wish_requested.emit(self.row))
        actions.addWidget(self.wish_btn)

        actions.addStretch()
        root.addLayout(actions)

    def update_wish_btn(self):
        in_wish = self.row[1] in self.wishlist_set
        self.wish_btn.setText("💚 Wishlisted" if in_wish else "🤍 Wishlist")
        style_btn(self.wish_btn, "accent" if in_wish else "ghost")


# ─────────────────────────────────────────────────────────────────────────────
#  SETTINGS DIALOG
# ─────────────────────────────────────────────────────────────────────────────

class SettingsDialog(QDialog):
    theme_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙  Settings")
        self.setFixedSize(500, 320)
        self.setStyleSheet(build_stylesheet())
        self._setup()

    def _setup(self):
        root = QVBoxLayout(self)
        root.setSpacing(12)

        root.addWidget(lbl("Colour Theme", C("accent"), bold=True, size=15))
        root.addWidget(hsep())
        root.addSpacing(4)

        grid = QGridLayout()
        grid.setSpacing(8)
        for i, name in enumerate(PALETTES):
            btn = QPushButton(f"{'●  ' if _theme_name[0]==name else '   '}{name}")
            style_btn(btn, "accent" if _theme_name[0]==name else "ghost")
            btn.setMinimumHeight(38)
            btn.clicked.connect(partial(self._apply_theme, name))
            grid.addWidget(btn, i // 2, i % 2)
        root.addLayout(grid)

        root.addSpacing(8)
        root.addWidget(hsep())
        root.addSpacing(4)
        root.addWidget(lbl("Window", C("accent"), bold=True))
        wrow = QHBoxLayout()
        for ltext, w, h in [("Maximise", 0, 0), ("1280×800", 1280, 800), ("1920×1200", 1920, 1200)]:
            b = QPushButton(ltext)
            style_btn(b, "ghost")
            b.setMinimumHeight(34)
            if w == 0:
                b.clicked.connect(lambda: self.parentWidget().showMaximized() if self.parentWidget() else None)
            else:
                b.clicked.connect(partial(self._resize_win, w, h))
            wrow.addWidget(b)
        root.addLayout(wrow)

        root.addStretch()
        close = QPushButton("Close")
        style_btn(close, "accent")
        close.setMinimumHeight(36)
        close.clicked.connect(self.accept)
        root.addWidget(close)

    def _apply_theme(self, name):
        _theme_name[0] = name
        app = QApplication.instance()
        if app:
            app.setStyleSheet(build_stylesheet())
        self.theme_changed.emit()
        self.accept()

    def _resize_win(self, w, h):
        p = self.parentWidget()
        if p:
            p.resize(w, h)


# ─────────────────────────────────────────────────────────────────────────────
#  NAVBAR WIDGET
# ─────────────────────────────────────────────────────────────────────────────

class NavBar(QWidget):
    nav_clicked = pyqtSignal(str)
    logout_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()

    def __init__(self, username, active, cart_count=0, wish_count=0):
        super().__init__()
        self.username = username
        self.active = active
        self.cart_count = cart_count
        self.wish_count = wish_count
        self._setup()

    def _setup(self):
        self.setStyleSheet(f"background-color: {C('panel')}; border-bottom: 1px solid {C('border')};")
        self.setFixedHeight(52)

        row = QHBoxLayout(self)
        row.setContentsMargins(16, 6, 16, 6)
        row.setSpacing(4)

        logo = lbl("🌿  GreenVibe", C("accent"), bold=True, size=16)
        row.addWidget(logo)
        row.addWidget(hspace(20))

        nav_items = [
            ("🏪  Store",   "store"),
            ("📅  Planner", "planner"),
            (f"🛒  Cart ({self.cart_count})", "cart"),
            ("📦  Orders",  "orders"),
            (f"💚  Wishlist ({self.wish_count})", "wishlist"),
        ]
        for label, screen in nav_items:
            btn = QPushButton(label)
            style_btn(btn, "nav")
            btn.setProperty("active", "true" if screen == self.active else "false")
            btn.setFixedHeight(36)
            btn.clicked.connect(partial(self.nav_clicked.emit, screen))
            row.addWidget(btn)

        row.addStretch()
        user_lbl = lbl(f"👤  {self.username}", C("dim"))
        row.addWidget(user_lbl)
        row.addWidget(hspace(8))

        settings_btn = QPushButton("⚙ Settings")
        style_btn(settings_btn, "ghost")
        settings_btn.setFixedHeight(32)
        settings_btn.clicked.connect(self.settings_clicked.emit)
        row.addWidget(settings_btn)

        row.addWidget(hspace(4))
        logout_btn = QPushButton("Logout")
        style_btn(logout_btn, "danger")
        logout_btn.setFixedHeight(32)
        logout_btn.clicked.connect(self.logout_clicked.emit)
        row.addWidget(logout_btn)


# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class LoginScreen(QWidget):
    login_success = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._setup()

    def _setup(self):
        # Force a bright white background for the whole login screen
        self.setStyleSheet("background-color: #F4FAF5;")

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Left hero ────────────────────────────────────────────────────
        hero = QWidget()
        hero.setFixedWidth(440)
        hero.setStyleSheet("background-color: #1E7A3C;")
        hv = QVBoxLayout(hero)
        hv.setContentsMargins(40, 60, 40, 40)
        hv.setSpacing(0)

        logo = QLabel("🌿")
        logo.setStyleSheet("font-size: 60px; background: transparent; color: white;")
        hv.addWidget(logo)
        hv.addSpacing(12)

        brand = QLabel("GreenVibe")
        brand.setStyleSheet("color: #FFFFFF; font-size: 32px; font-weight: 900; background: transparent;")
        hv.addWidget(brand)

        tagline = QLabel("Smart Plants  ·  Native Species  ·  Green Future")
        tagline.setStyleSheet("color: #A8DDB8; font-size: 12px; background: transparent;")
        hv.addWidget(tagline)
        hv.addSpacing(28)

        sep = QFrame()
        sep.setFixedHeight(2)
        sep.setStyleSheet("background: #A8DDB8; border: none;")
        hv.addWidget(sep)
        hv.addSpacing(24)

        features = [
            "🌱  Smart space planner",
            "🇧🇩  30 Bangladesh-native & suited plants",
            "📷  Photo-based plant store",
            "🛒  Cart with SQLite persistence",
            "💚  Wishlist & personal notes",
            "📦  Order history",
            "🌍  SDG 11 · 13 · 15 aligned",
        ]
        for f in features:
            fl = QLabel(f"  {f}")
            fl.setStyleSheet("color: #D4F0DC; font-size: 13px; background: transparent;")
            hv.addWidget(fl)
            hv.addSpacing(6)

        hv.addSpacing(28)
        stats = get_stats()

        stats_w = QWidget()
        stats_w.setStyleSheet("background: rgba(255,255,255,0.12); border-radius: 10px;")
        stats_h = QHBoxLayout(stats_w)
        stats_h.setContentsMargins(12, 10, 12, 10)
        stats_h.setSpacing(0)

        for icon, val, name in [("🌿", stats['plants'], "Plants"),
                                  ("👤", stats['users'], "Users"),
                                  ("📦", stats['orders'], "Orders")]:
            col = QVBoxLayout()
            col.setSpacing(2)
            v = QLabel(str(val))
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: 800; background: transparent;")
            n = QLabel(f"{icon} {name}")
            n.setAlignment(Qt.AlignmentFlag.AlignCenter)
            n.setStyleSheet("color: #A8DDB8; font-size: 11px; background: transparent;")
            col.addWidget(v)
            col.addWidget(n)
            stats_h.addLayout(col)
            if name != "Orders":
                dv = QFrame()
                dv.setFrameShape(QFrame.Shape.VLine)
                dv.setStyleSheet("background: #A8DDB8; max-width: 1px; border: none;")
                stats_h.addWidget(dv)

        hv.addWidget(stats_w)
        hv.addStretch()
        root.addWidget(hero)

        # ── Right form ───────────────────────────────────────────────────
        right = QWidget()
        right.setStyleSheet("background-color: #F4FAF5;")
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.addStretch()

        card_outer = QHBoxLayout()
        card_outer.addStretch()

        card = QFrame()
        card.setStyleSheet("""
    QFrame {
        background-color: #FFFFFF;
        border: none;
        border-radius: 14px;
    }
""")
        card.setFixedWidth(440)
        cv = QVBoxLayout(card)
        cv.setContentsMargins(32, 28, 32, 28)
        cv.setSpacing(10)

        title = QLabel("Welcome 💚")
        title.setStyleSheet("color: #1A1A1A; font-size: 20px; font-weight: 800; background: transparent;")
        cv.addWidget(title)

        sub = QLabel("Sign in to your GreenVibe account")
        sub.setStyleSheet("color: #555555; font-size: 13px; background: transparent;")
        cv.addWidget(sub)
        cv.addSpacing(4)

        sep2 = QFrame()
        sep2.setFixedHeight(2)
        sep2.setStyleSheet("background: #1E7A3C; border: none; border-radius: 1px;")
        cv.addWidget(sep2)
        cv.addSpacing(4)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #C8E6C9;
                border-radius: 10px;
                background: #F9FFF9;
                top: -1px;
            }
            QTabBar::tab {
                background: #E8F5E9;
                color: #444444;
                padding: 9px 28px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #C8E6C9;
                border-bottom: none;
                margin-right: 3px;
                font-weight: 600;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                color: #1E7A3C;
                border-bottom: 2px solid #1E7A3C;
            }
            QTabBar::tab:hover {
                background: #FFFFFF;
                color: #1A1A1A;
            }
        """)

        def make_input(placeholder, password=False):
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setFixedHeight(40)
            if password:
                inp.setEchoMode(QLineEdit.EchoMode.Password)
            inp.setStyleSheet("""
                QLineEdit {
                    background: #FFFFFF;
                    border: 1.5px solid #C8E6C9;
                    border-radius: 8px;
                    padding: 8px 14px;
                    color: #1A1A1A;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border-color: #1E7A3C;
                }
            """)
            return inp

        def field_label(text):
            l = QLabel(text)
            l.setStyleSheet("color: #333333; font-weight: 700; font-size: 12px; background: transparent;")
            return l

        # ── Login tab ────────────────────────────────────────────────────
        login_tab = QWidget()
        login_tab.setStyleSheet("background: #F9FFF9; border-radius: 10px;")
        lt = QVBoxLayout(login_tab)
        lt.setSpacing(8)
        lt.setContentsMargins(12, 16, 12, 12)

        lt.addWidget(field_label("Username"))
        self.login_user = make_input("e.g. Annafee")
        lt.addWidget(self.login_user)

        lt.addWidget(field_label("Password"))
        self.login_pass = make_input("••••••", password=True)
        self.login_pass.returnPressed.connect(self._do_login)
        lt.addWidget(self.login_pass)

        self.login_msg = QLabel("")
        self.login_msg.setStyleSheet("color: #C62828; font-size: 12px; font-weight: 600; background: transparent;")
        lt.addWidget(self.login_msg)

        login_btn = QPushButton("Sign In  →")
        login_btn.setFixedHeight(44)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E7A3C;
                color: #FFFFFF;
                border: none;
                border-radius: 9px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #25964A; }
            QPushButton:pressed { background-color: #175C2D; }
        """)
        login_btn.clicked.connect(self._do_login)
        lt.addWidget(login_btn)

        hint = QLabel("") #Default credentials:  admin / 1234
        hint.setStyleSheet("color: #777777; font-size: 11px; background: transparent;")
        lt.addWidget(hint)
        lt.addStretch()

        tabs.addTab(login_tab, "  Login  ")

        # ── Register tab ─────────────────────────────────────────────────
        reg_tab = QWidget()
        reg_tab.setStyleSheet("background: #F9FFF9; border-radius: 10px;")
        rt = QVBoxLayout(reg_tab)
        rt.setSpacing(8)
        rt.setContentsMargins(12, 16, 12, 12)

        rt.addWidget(field_label("New Username"))
        self.reg_user = make_input("Choose a username")
        rt.addWidget(self.reg_user)

        rt.addWidget(field_label("Password"))
        self.reg_pass = make_input("Min. 4 characters", password=True)
        rt.addWidget(self.reg_pass)

        rt.addWidget(field_label("Confirm Password"))
        self.reg_pass2 = make_input("Repeat password", password=True)
        rt.addWidget(self.reg_pass2)

        self.reg_msg = QLabel("")
        self.reg_msg.setStyleSheet("color: #C62828; font-size: 12px; font-weight: 600; background: transparent;")
        rt.addWidget(self.reg_msg)

        reg_btn = QPushButton("Create Account  →")
        reg_btn.setFixedHeight(44)
        reg_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E7A3C;
                color: #FFFFFF;
                border: none;
                border-radius: 9px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #25964A; }
            QPushButton:pressed { background-color: #175C2D; }
        """)
        reg_btn.clicked.connect(self._do_register)
        rt.addWidget(reg_btn)
        rt.addStretch()

        tabs.addTab(reg_tab, "  Register  ")
        cv.addWidget(tabs)
        card_outer.addWidget(card)
        card_outer.addStretch()
        rv.addLayout(card_outer)
        rv.addStretch()
        root.addWidget(right, 1)

    def _do_login(self):
        u = self.login_user.text().strip()
        p = self.login_pass.text().strip()
        if not u or not p:
            self.login_msg.setText("⚠  Please fill in all fields."); return
        if validate_user(u, p):
            self.login_success.emit(u)
        else:
            self.login_msg.setText("✗  Invalid username or password.")

    def _do_register(self):
        u  = self.reg_user.text().strip()
        p  = self.reg_pass.text().strip()
        p2 = self.reg_pass2.text().strip()
        if not u or not p:
            self.reg_msg.setText("⚠  Fill all fields."); return
        if p != p2:
            self.reg_msg.setText("✗  Passwords don't match."); return
        if len(p) < 4:
            self.reg_msg.setText("✗  Password too short (min 4)."); return
        if register_user(u, p):
            self.reg_msg.setStyleSheet(f"color: {C('accent')};")
            self.reg_msg.setText("✓  Account created! Please log in.")
        else:
            self.reg_msg.setStyleSheet(f"color: {C('danger')};")
            self.reg_msg.setText("✗  Username already taken.")


# ─────────────────────────────────────────────────────────────────────────────
#  STORE SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class StoreScreen(QWidget):
    nav_to = pyqtSignal(str)
    toast  = pyqtSignal(str)

    def __init__(self, username, wishlist_set):
        super().__init__()
        self.username = username
        self.wishlist_set = wishlist_set
        self._cards = []
        self._setup()
        self._render(get_all_plants())

    def _setup(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 10, 16, 10)
        root.setSpacing(8)

        # ── Filter bar ────────────────────────────────────────────────────
        fbar = QHBoxLayout()
        fbar.setSpacing(8)

        fbar.addWidget(lbl("🔍", C("dim")))
        self.search = QLineEdit()
        self.search.setPlaceholderText("Plant name or Bengali…")
        self.search.setFixedHeight(32)
        self.search.setFixedWidth(200)
        self.search.textChanged.connect(self._apply_filter)
        fbar.addWidget(self.search)

        fbar.addWidget(lbl("Light:", C("dim")))
        self.f_light = QComboBox()
        self.f_light.addItems(["All", "Low", "Medium", "High"])
        self.f_light.setFixedWidth(100)
        self.f_light.setFixedHeight(32)
        self.f_light.currentIndexChanged.connect(self._apply_filter)
        fbar.addWidget(self.f_light)

        fbar.addWidget(lbl("Space:", C("dim")))
        self.f_space = QComboBox()
        self.f_space.addItems(["All", "Room", "Balcony", "Rooftop"])
        self.f_space.setFixedWidth(100)
        self.f_space.setFixedHeight(32)
        self.f_space.currentIndexChanged.connect(self._apply_filter)
        fbar.addWidget(self.f_space)

        fbar.addWidget(lbl("Difficulty:", C("dim")))
        self.f_diff = QComboBox()
        self.f_diff.addItems(["All", "Beginner", "Intermediate", "Expert"])
        self.f_diff.setFixedWidth(120)
        self.f_diff.setFixedHeight(32)
        self.f_diff.currentIndexChanged.connect(self._apply_filter)
        fbar.addWidget(self.f_diff)

        self.f_air  = QCheckBox("Air Purifier")
        self.f_edible  = QCheckBox("Edible")
        self.f_fragrant = QCheckBox("Fragrant")
        for cb in [self.f_air, self.f_edible, self.f_fragrant]:
            cb.stateChanged.connect(self._apply_filter)
            fbar.addWidget(cb)

        reset_btn = QPushButton("Reset")
        style_btn(reset_btn, "ghost")
        reset_btn.setFixedHeight(32)
        reset_btn.clicked.connect(self._reset_filter)
        fbar.addWidget(reset_btn)
        fbar.addStretch()

        root.addLayout(fbar)
        root.addWidget(hsep())

        self.count_lbl = lbl("", C("dim"))
        root.addWidget(self.count_lbl)

        # ── Scroll area for cards ─────────────────────────────────────────
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(8)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.cards_container)
        root.addWidget(self.scroll, 1)

    def _apply_filter(self):
        rows = get_plants_by_filter(
            light      = None if self.f_light.currentText()=="All" else self.f_light.currentText(),
            space      = None if self.f_space.currentText()=="All" else self.f_space.currentText(),
            difficulty = None if self.f_diff.currentText()=="All" else self.f_diff.currentText(),
            air_purifier = True if self.f_air.isChecked() else None,
            edible       = True if self.f_edible.isChecked() else None,
            fragrant     = True if self.f_fragrant.isChecked() else None,
            search       = self.search.text().strip() or None,
        )
        self._render(rows)

    def _reset_filter(self):
        self.search.clear()
        self.f_light.setCurrentIndex(0)
        self.f_space.setCurrentIndex(0)
        self.f_diff.setCurrentIndex(0)
        self.f_air.setChecked(False)
        self.f_edible.setChecked(False)
        self.f_fragrant.setChecked(False)
        self._render(get_all_plants())

    def _render(self, rows):
        # Clear old cards
        for c in self._cards:
            self.cards_layout.removeWidget(c)
            c.deleteLater()
        self._cards.clear()

        self.count_lbl.setText(f"Showing {len(rows)} plant{'s' if len(rows)!=1 else ''}")

        if not rows:
            emp = lbl("No plants match this filter.", C("dim"))
            self.cards_layout.insertWidget(0, emp)
            self._cards.append(emp)
            return

        for row in rows:
            card = PlantCard(row, self.wishlist_set)
            card.detail_requested.connect(self._open_detail)
            card.cart_requested.connect(self._add_cart)
            card.wish_requested.connect(self._toggle_wish)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
            self._cards.append(card)

    def _open_detail(self, row):
        dlg = PlantDetailDialog(row, self.username, self.wishlist_set, self)
        dlg.cart_updated.connect(lambda: self.nav_to.emit("_cart_refresh"))
        dlg.wish_updated.connect(self._wish_updated)
        dlg.exec()

    def _add_cart(self, row):
        add_to_cart(self.username, row[1], row[2])
        self.toast.emit(f"✓  {row[1]} added to cart!")
        self.nav_to.emit("_cart_refresh")

    def _toggle_wish(self, row):
        added = toggle_wishlist(self.username, row[1])
        if added:
            self.wishlist_set.add(row[1])
            self.toast.emit(f"💚  {row[1]} added to wishlist!")
        else:
            self.wishlist_set.discard(row[1])
            self.toast.emit(f"🤍  {row[1]} removed from wishlist.")
        self._update_wish_btns()

    def _wish_updated(self):
        self._update_wish_btns()

    def _update_wish_btns(self):
        for c in self._cards:
            if isinstance(c, PlantCard):
                c.update_wish_btn()


# ─────────────────────────────────────────────────────────────────────────────
#  PLANNER SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class PlannerScreen(QWidget):
    nav_to = pyqtSignal(str)
    toast  = pyqtSignal(str)

    def __init__(self, username, wishlist_set):
        super().__init__()
        self.username = username
        self.wishlist_set = wishlist_set
        self._result_cards = []
        self._setup()

    def _setup(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 10, 16, 10)
        root.setSpacing(8)

        root.addWidget(lbl("📅  Smart Space Planner", C("accent"), bold=True, size=16))
        root.addWidget(lbl("Find the right plants for your space, season, budget & purpose.", C("dim")))
        root.addWidget(hsep())

        body = QHBoxLayout()
        body.setSpacing(12)

        # ── Left control panel ────────────────────────────────────────────
        ctrl = QWidget()
        ctrl.setFixedWidth(300)
        ctrl.setStyleSheet(f"background-color: {C('panel')}; border: 1px solid {C('border')}; border-radius: 10px;")
        cv = QVBoxLayout(ctrl)
        cv.setContentsMargins(12, 12, 12, 12)
        cv.setSpacing(0)

        tabs = QTabWidget()

        # ── Tab: Space ────────────────────────────────────────────────────
        t_space = QWidget()
        sv = QVBoxLayout(t_space)
        sv.setSpacing(8)
        sv.setContentsMargins(8, 12, 8, 8)
        sv.addWidget(lbl("☀  Sunlight Level", C("dim")))
        self.plan_light = QButtonGroup(self)
        for i, opt in enumerate(["Low", "Medium", "High"]):
            rb = QRadioButton(opt)
            if opt == "Medium": rb.setChecked(True)
            self.plan_light.addButton(rb, i)
            sv.addWidget(rb)
        sv.addSpacing(10)
        sv.addWidget(lbl("📍  Space Type", C("dim")))
        self.plan_space = QButtonGroup(self)
        for i, opt in enumerate(["Room", "Balcony", "Rooftop"]):
            rb = QRadioButton(opt)
            if opt == "Balcony": rb.setChecked(True)
            self.plan_space.addButton(rb, i)
            sv.addWidget(rb)
        sv.addSpacing(12)
        gen_btn = QPushButton("✦  Generate Recommendations")
        style_btn(gen_btn, "accent")
        gen_btn.setMinimumHeight(44)
        gen_btn.clicked.connect(self._run_space)
        sv.addWidget(gen_btn)
        sv.addSpacing(10)
        sv.addWidget(hsep())
        sv.addSpacing(6)
        sv.addWidget(lbl("🌍  SDG Alignment", C("accent2"), bold=True))
        for s in ["SDG 11 · Sustainable Cities","SDG 13 · Climate Action",
                  "SDG 15 · Life on Land","SDG 2  · Zero Hunger",
                  "SDG 3  · Good Health"]:
            sv.addWidget(lbl(f"  ✓  {s}", C("dim")))
        sv.addStretch()
        tabs.addTab(t_space, "Space")

        # ── Tab: Season ───────────────────────────────────────────────────
        t_season = QWidget()
        ssv = QVBoxLayout(t_season)
        ssv.setSpacing(8)
        ssv.setContentsMargins(8, 12, 8, 8)
        ssv.addWidget(lbl("Current Month", C("dim")))
        self.plan_month = QComboBox()
        self.plan_month.addItems(["Jan","Feb","Mar","Apr","May","Jun",
                                   "Jul","Aug","Sep","Oct","Nov","Dec"])
        self.plan_month.setCurrentText(datetime.now().strftime("%b"))
        ssv.addWidget(self.plan_month)
        ssv.addSpacing(12)
        s_btn = QPushButton("🌸  Show Seasonal Plants")
        style_btn(s_btn, "accent")
        s_btn.setMinimumHeight(44)
        s_btn.clicked.connect(self._run_season)
        ssv.addWidget(s_btn)
        ssv.addStretch()
        tabs.addTab(t_season, "Season")

        # ── Tab: Budget ───────────────────────────────────────────────────
        t_budget = QWidget()
        bv = QVBoxLayout(t_budget)
        bv.setSpacing(8)
        bv.setContentsMargins(8, 12, 8, 8)
        bv.addWidget(lbl("Your Budget", C("dim")))
        self.plan_budget = QComboBox()
        self.plan_budget.addItems(get_all_budget_tiers())
        bv.addWidget(self.plan_budget)
        bv.addSpacing(12)
        b_btn = QPushButton("💰  Show Plants in Budget")
        style_btn(b_btn, "accent")
        b_btn.setMinimumHeight(44)
        b_btn.clicked.connect(self._run_budget)
        bv.addWidget(b_btn)
        bv.addStretch()
        tabs.addTab(t_budget, "Budget")

        # ── Tab: Purpose ──────────────────────────────────────────────────
        t_purpose = QWidget()
        pv = QVBoxLayout(t_purpose)
        pv.setSpacing(8)
        pv.setContentsMargins(8, 12, 8, 8)
        pv.addWidget(lbl("What do you want?", C("dim")))
        self.plan_purpose = QComboBox()
        self.plan_purpose.addItems(get_all_purposes())
        pv.addWidget(self.plan_purpose)
        pv.addSpacing(12)
        p_btn = QPushButton("🎯  Show Purpose Plants")
        style_btn(p_btn, "accent")
        p_btn.setMinimumHeight(44)
        p_btn.clicked.connect(self._run_purpose)
        pv.addWidget(p_btn)
        pv.addStretch()
        tabs.addTab(t_purpose, "Purpose")

        # ── Tab: Skill ────────────────────────────────────────────────────
        t_skill = QWidget()
        skv = QVBoxLayout(t_skill)
        skv.setSpacing(8)
        skv.setContentsMargins(8, 12, 8, 8)
        skv.addWidget(lbl("Your Gardening Experience", C("dim")))
        self.plan_skill = QButtonGroup(self)
        for i, opt in enumerate(["Beginner", "Intermediate", "Expert"]):
            rb = QRadioButton(opt)
            if opt == "Beginner": rb.setChecked(True)
            self.plan_skill.addButton(rb, i)
            skv.addWidget(rb)
        skv.addSpacing(12)
        sk_btn = QPushButton("🌱  Show Plants for My Level")
        style_btn(sk_btn, "accent")
        sk_btn.setMinimumHeight(44)
        sk_btn.clicked.connect(self._run_skill)
        skv.addWidget(sk_btn)
        skv.addStretch()
        tabs.addTab(t_skill, "Skill")

        cv.addWidget(tabs, 1)
        body.addWidget(ctrl)

        # ── Right result panel ────────────────────────────────────────────
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(6)

        self.tip_frame = QFrame()
        self.tip_frame.setProperty("frameclass", "card")
        self.tip_frame.setStyleSheet(f"background:{C('card')}; border:1px solid {C('border')}; border-radius:8px;")
        tf = QVBoxLayout(self.tip_frame)
        tf.setContentsMargins(12, 10, 12, 10)
        self.tip_lbl  = lbl("", C("dim"), wrap=True)
        self.tip_lbl.hide()
        tf.addWidget(lbl("💡  Tip", C("accent"), bold=True))
        tf.addWidget(self.tip_lbl)
        self.tip_frame.hide()
        rv.addWidget(self.tip_frame)

        self.result_lbl = lbl("Select an option on the left and press Generate.", C("dim"))
        rv.addWidget(self.result_lbl)

        self.result_scroll = QScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.result_container = QWidget()
        self.result_vbox = QVBoxLayout(self.result_container)
        self.result_vbox.setContentsMargins(0, 0, 0, 0)
        self.result_vbox.setSpacing(8)
        self.result_vbox.addStretch()
        self.result_scroll.setWidget(self.result_container)
        rv.addWidget(self.result_scroll, 1)

        body.addWidget(right, 1)
        root.addLayout(body, 1)

    def _get_light(self):
        btn = self.plan_light.checkedButton()
        return btn.text() if btn else "Medium"

    def _get_space(self):
        btn = self.plan_space.checkedButton()
        return btn.text() if btn else "Balcony"

    def _get_skill(self):
        btn = self.plan_skill.checkedButton()
        return btn.text() if btn else "Beginner"

    def _show_results(self, plant_names, tip="", extra=""):
        for c in self._result_cards:
            self.result_vbox.removeWidget(c)
            c.deleteLater()
        self._result_cards.clear()

        if tip:
            self.tip_lbl.setText(tip + (f"\n\n{extra}" if extra else ""))
            self.tip_lbl.show()
            self.tip_frame.show()
        else:
            self.tip_frame.hide()

        self.result_lbl.setText(f"Recommended Plants  ({len(plant_names)})")

        lookup = {r[1]: r for r in get_all_plants()}
        for name in plant_names:
            row = lookup.get(name)
            if row:
                card = PlantCard(row, self.wishlist_set, compact=True)
                card.detail_requested.connect(self._open_detail)
                card.cart_requested.connect(self._add_cart)
                card.wish_requested.connect(self._toggle_wish)
                self.result_vbox.insertWidget(self.result_vbox.count()-1, card)
                self._result_cards.append(card)
            else:
                l = lbl(f"  {name}  (not in store yet)", C("dim"))
                self.result_vbox.insertWidget(self.result_vbox.count()-1, l)
                self._result_cards.append(l)

    def _open_detail(self, row):
        dlg = PlantDetailDialog(row, self.username, self.wishlist_set, self)
        dlg.cart_updated.connect(lambda: self.nav_to.emit("_cart_refresh"))
        dlg.exec()

    def _add_cart(self, row):
        add_to_cart(self.username, row[1], row[2])
        self.toast.emit(f"✓  {row[1]} added to cart!")
        self.nav_to.emit("_cart_refresh")

    def _toggle_wish(self, row):
        added = toggle_wishlist(self.username, row[1])
        if added:
            self.wishlist_set.add(row[1])
            self.toast.emit(f"💚  {row[1]} added to wishlist!")
        else:
            self.wishlist_set.discard(row[1])
            self.toast.emit(f"🤍  {row[1]} removed from wishlist.")

    def _run_space(self):
        names_csv, care, seasonal, sdg = get_recommendation(self._get_light(), self._get_space())
        names = [n.strip() for n in names_csv.split(",")]
        self._show_results(names, care, seasonal)

    def _run_season(self):
        month = self.plan_month.currentText()
        names = get_seasonal_plants(month)
        self._show_results(names, f"These plants are in peak season during {month} in Bangladesh.")

    def _run_budget(self):
        tier = self.plan_budget.currentText()
        names = get_budget_suggestions(tier)
        self._show_results(names, f"Great plants within the {tier} budget range.")

    def _run_purpose(self):
        purpose = self.plan_purpose.currentText()
        names = get_purpose_suggestions(purpose)
        self._show_results(names, f"Selected for: {purpose}")

    def _run_skill(self):
        skill = self._get_skill()
        tip = get_difficulty_tip(skill)
        rows = get_plants_by_filter(difficulty=skill)
        names = [r[1] for r in rows]
        self._show_results(names, tip)


# ─────────────────────────────────────────────────────────────────────────────
#  CART SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class CartScreen(QWidget):
    nav_to = pyqtSignal(str)
    toast  = pyqtSignal(str)
    cart_updated = pyqtSignal()

    def __init__(self, username):
        super().__init__()
        self.username = username
        self._setup()

    def _setup(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 10, 16, 10)
        root.setSpacing(8)
        root.addWidget(lbl("🛒  My Cart", C("warning"), bold=True, size=16))
        root.addWidget(hsep())
        self._body = QVBoxLayout()
        root.addLayout(self._body, 1)
        self.refresh()

    def refresh(self):
        # Clear body
        while self._body.count():
            item = self._body.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        items = get_cart(self.username)
        if not items:
            self._body.addWidget(lbl("Your cart is empty.", C("dim")))
            self._body.addSpacing(10)
            browse_btn = QPushButton("Browse Plants →")
            style_btn(browse_btn, "accent")
            browse_btn.setFixedWidth(200)
            browse_btn.setFixedHeight(40)
            browse_btn.clicked.connect(lambda: self.nav_to.emit("store"))
            self._body.addWidget(browse_btn)
            self._body.addStretch()
            return

        # Header row
        hdr = QHBoxLayout()
        hdr.addWidget(lbl("Plant", C("dim")))
        hdr.addStretch()
        hdr.addWidget(lbl("Price", C("dim")))
        hdr.addWidget(hspace(80))
        hdr.addWidget(lbl("Added", C("dim")))
        self._body.addLayout(hdr)
        self._body.addWidget(hsep())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sw = QWidget()
        sv = QVBoxLayout(sw)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.setSpacing(6)

        total = 0
        for plant, price, qty, added_at in items:
            emoji = PLANT_EMOJI_MAP.get(plant, "🌿")
            row_w = QHBoxLayout()
            row_w.addWidget(lbl(f"{emoji}  {plant}", C("text")))
            row_w.addStretch()
            row_w.addWidget(lbl(f"৳{price}", C("accent")))
            row_w.addWidget(hspace(60))
            row_w.addWidget(lbl(str(added_at)[:16], C("dim")))
            sv.addLayout(row_w)
            total += price

        sv.addStretch()
        scroll.setWidget(sw)
        self._body.addWidget(scroll, 1)

        self._body.addWidget(hsep())

        totrow = QHBoxLayout()
        totrow.addWidget(lbl(f"Total: ৳{total} BDT", C("accent"), bold=True, size=16))
        totrow.addWidget(lbl(f"({len(items)} items)", C("dim")))
        totrow.addStretch()
        self._body.addLayout(totrow)

        self._body.addSpacing(8)
        btnrow = QHBoxLayout()
        checkout_btn = QPushButton("✓  Place Order")
        style_btn(checkout_btn, "warning")
        checkout_btn.setFixedSize(200, 44)
        checkout_btn.clicked.connect(lambda: self._do_checkout(items, total))
        btnrow.addWidget(checkout_btn)
        btnrow.addWidget(hspace(12))
        clear_btn = QPushButton("Clear Cart")
        style_btn(clear_btn, "danger")
        clear_btn.setFixedSize(140, 44)
        clear_btn.clicked.connect(self._do_clear)
        btnrow.addWidget(clear_btn)
        btnrow.addStretch()
        self._body.addLayout(btnrow)

    def _do_checkout(self, items, total):
        if not items:
            return
        item_list = [{"plant": p, "price": pr, "qty": q} for p, pr, q, _ in items]
        place_order(self.username, item_list, total)
        self.toast.emit(f"✓  Order placed! ৳{total} BDT  ·  {len(items)} items. Happy gardening! 🌱")
        self.cart_updated.emit()
        self.refresh()

    def _do_clear(self):
        clear_cart(self.username)
        self.cart_updated.emit()
        self.refresh()


# ─────────────────────────────────────────────────────────────────────────────
#  ORDERS SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class OrdersScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self._setup()

    def _setup(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 10, 16, 10)
        root.setSpacing(8)
        root.addWidget(lbl("📦  Order History", C("accent"), bold=True, size=16))
        root.addWidget(hsep())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        sw = QWidget()
        sv = QVBoxLayout(sw)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.setSpacing(8)

        orders = get_orders(self.username)
        if not orders:
            sv.addWidget(lbl("No orders yet.", C("dim")))
        else:
            for oid, items, total, placed_at in orders:
                card = card_frame()
                card.setFixedHeight(100)
                cv = QVBoxLayout(card)
                cv.setContentsMargins(12, 10, 12, 10)
                top = QHBoxLayout()
                top.addWidget(lbl(f"Order #{oid}", C("text"), bold=True))
                top.addWidget(lbl(str(placed_at)[:16], C("dim")))
                top.addStretch()
                cv.addLayout(top)
                cv.addWidget(lbl(f"Total: ৳{total}", C("accent")))
                plants_str = ", ".join([f"{i['plant']} (৳{i['price']})" for i in items])
                pl = lbl(plants_str, C("dim"), wrap=True)
                cv.addWidget(pl)
                sv.addWidget(card)

        sv.addStretch()
        scroll.setWidget(sw)
        root.addWidget(scroll, 1)


# ─────────────────────────────────────────────────────────────────────────────
#  WISHLIST SCREEN
# ─────────────────────────────────────────────────────────────────────────────

class WishlistScreen(QWidget):
    nav_to = pyqtSignal(str)
    toast  = pyqtSignal(str)

    def __init__(self, username, wishlist_set):
        super().__init__()
        self.username = username
        self.wishlist_set = wishlist_set
        self._cards = []
        self._setup()

    def _setup(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 10, 16, 10)
        root.setSpacing(8)
        root.addWidget(lbl("💚  My Wishlist", C("accent"), bold=True, size=16))
        root.addWidget(hsep())

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(8)
        self.scroll.setWidget(self.container)
        root.addWidget(self.scroll, 1)
        self.refresh()

    def refresh(self):
        for c in self._cards:
            self.vbox.removeWidget(c)
            c.deleteLater()
        self._cards.clear()

        wish_names = list(self.wishlist_set)
        lookup = {r[1]: r for r in get_all_plants()}

        if not wish_names:
            emp = lbl("Your wishlist is empty.", C("dim"))
            self.vbox.addWidget(emp)
            self._cards.append(emp)
            browse_btn = QPushButton("Browse Plants →")
            style_btn(browse_btn, "accent")
            browse_btn.setFixedWidth(200)
            browse_btn.setFixedHeight(40)
            browse_btn.clicked.connect(lambda: self.nav_to.emit("store"))
            self.vbox.addWidget(browse_btn)
            self._cards.append(browse_btn)
        else:
            for name in wish_names:
                row = lookup.get(name)
                if row:
                    card = PlantCard(row, self.wishlist_set, compact=True)
                    card.detail_requested.connect(self._open_detail)
                    card.cart_requested.connect(self._add_cart)
                    card.wish_requested.connect(self._toggle_wish)
                    self.vbox.addWidget(card)
                    self._cards.append(card)

        self.vbox.addStretch()

    def _open_detail(self, row):
        dlg = PlantDetailDialog(row, self.username, self.wishlist_set, self)
        dlg.cart_updated.connect(lambda: self.nav_to.emit("_cart_refresh"))
        dlg.exec()

    def _add_cart(self, row):
        add_to_cart(self.username, row[1], row[2])
        self.toast.emit(f"✓  {row[1]} added to cart!")
        self.nav_to.emit("_cart_refresh")

    def _toggle_wish(self, row):
        added = toggle_wishlist(self.username, row[1])
        if added:
            self.wishlist_set.add(row[1])
        else:
            self.wishlist_set.discard(row[1])
            self.refresh()
        self.toast.emit(f"{'💚' if added else '🤍'}  {row[1]} {'added to' if added else 'removed from'} wishlist.")


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GreenVibe 🌿")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        self.username    = ""
        self.wishlist_set = set()

        self._root = QWidget()
        self.setCentralWidget(self._root)
        self._main_layout = QVBoxLayout(self._root)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # Toast
        self.toast = ToastWidget(self._root)
        self.toast.raise_()

        self._stack = QStackedWidget()
        self._main_layout.addWidget(self._stack)

        # Login screen
        self._login_screen = LoginScreen()
        self._login_screen.login_success.connect(self._on_login)
        self._stack.addWidget(self._login_screen)
        self._stack.setCurrentWidget(self._login_screen)

        # App container (shown after login)
        self._app_widget  = None
        self._navbar      = None
        self._content     = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.toast.raise_()
        self.toast.move((self.width() - self.toast.width()) // 2, self.height() - 70)

    def _on_login(self, username):
        self.username = username
        self.wishlist_set = set(get_wishlist(username))
        self._build_app_ui()

    def _build_app_ui(self):
        if self._app_widget:
            self._stack.removeWidget(self._app_widget)
            self._app_widget.deleteLater()

        self._app_widget = QWidget()
        av = QVBoxLayout(self._app_widget)
        av.setContentsMargins(0, 0, 0, 0)
        av.setSpacing(0)

        # Content area
        self._content = QStackedWidget()

        # Build screens
        self._screens = {}
        self._screens["store"]    = StoreScreen(self.username, self.wishlist_set)
        self._screens["planner"]  = PlannerScreen(self.username, self.wishlist_set)
        self._screens["cart"]     = CartScreen(self.username)
        self._screens["orders"]   = OrdersScreen(self.username)
        self._screens["wishlist"] = WishlistScreen(self.username, self.wishlist_set)

        for s in self._screens.values():
            self._content.addWidget(s)
            if hasattr(s, "nav_to"):
                s.nav_to.connect(self._nav_to)
            if hasattr(s, "toast"):
                s.toast.connect(self._show_toast)

        self._screens["cart"].cart_updated.connect(self._refresh_navbar)

        # Build navbar
        self._navbar = self._make_navbar("store")
        av.addWidget(self._navbar)
        av.addWidget(self._content, 1)

        self._stack.addWidget(self._app_widget)
        self._stack.setCurrentWidget(self._app_widget)
        self._content.setCurrentWidget(self._screens["store"])

    def _make_navbar(self, active):
        cart_count = len(get_cart(self.username))
        wish_count = len(self.wishlist_set)
        nb = NavBar(self.username, active, cart_count, wish_count)
        nb.nav_clicked.connect(self._nav_to)
        nb.logout_clicked.connect(self._logout)
        nb.settings_clicked.connect(self._open_settings)
        return nb

    def _refresh_navbar(self):
        active = self._current_active()
        old = self._navbar
        self._navbar = self._make_navbar(active)
        layout = self._app_widget.layout()
        layout.replaceWidget(old, self._navbar)
        old.deleteLater()

    def _current_active(self):
        cur = self._content.currentWidget()
        for name, w in self._screens.items():
            if w is cur:
                return name
        return "store"

    def _nav_to(self, screen):
        if screen == "_cart_refresh":
            self._screens["cart"].refresh()
            self._refresh_navbar()
            return
        if screen not in self._screens:
            return
        self._content.setCurrentWidget(self._screens[screen])
        self._refresh_navbar()
        # Refresh screens that need it
        if screen == "cart":
            self._screens["cart"].refresh()
        elif screen == "wishlist":
            self._screens["wishlist"].refresh()

    def _logout(self):
        self.username = ""
        self.wishlist_set.clear()
        if self._app_widget:
            self._stack.removeWidget(self._app_widget)
            self._app_widget.deleteLater()
            self._app_widget = None
        self._stack.setCurrentWidget(self._login_screen)
        self._login_screen.login_user.clear()
        self._login_screen.login_pass.clear()
        self._login_screen.login_msg.clear()

    def _open_settings(self):
        dlg = SettingsDialog(self)
        dlg.theme_changed.connect(self._on_theme_change)
        dlg.exec()

    def _on_theme_change(self):
        self.setStyleSheet(build_stylesheet())
        # Rebuild app UI to apply new theme everywhere
        if self._app_widget:
            active = self._current_active()
            self._build_app_ui()
            self._nav_to(active)

    def _show_toast(self, msg):
        self.toast.show_msg(msg)
        self.toast.raise_()


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 52)
    print("  GreenVibe ")
    print("  ")
    print("=" * 52)

    init_db()
    print(" [OK] Database initialised.")

    app = QApplication(sys.argv)
    app.setApplicationName("GreenVibe")
    app.setApplicationVersion("5.0")
    app.setStyleSheet(build_stylesheet())

    win = MainWindow()
    win.showMaximized()
    print(" [OK] Launching GreenVibe (PyQt6)…")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
