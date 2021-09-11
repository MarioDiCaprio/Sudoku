import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from sudoku import Sudoku


class SudokuGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sudoku')
        self.setGeometry(20, 20, 600, 600)

        # center
        self.center = _Center()
        self.setCentralWidget(self.center)

        # menu bar
        bar = QMenuBar()
        self.setMenuBar(bar)

        # tools
        tools = QMenu('Tools')
        bar.addMenu(tools)

        # tools/generate
        generate = QAction('Generate', bar)
        generate.triggered.connect(lambda: self.center.sudoku.generate())
        tools.addAction(generate)

        # tools/solve
        solve = QAction('Solve', bar)
        solve.triggered.connect(lambda: self.center.sudoku.solve())
        tools.addAction(solve)

        # tools/clear
        clear = QAction('Clear', bar)
        clear.triggered.connect(lambda: self.center.sudoku.clear())
        tools.addAction(clear)


class _Center(QWidget):

    def __init__(self):
        super().__init__()

        # layouts
        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)

        # sudoku
        self.sudoku = _SudokuGUI()
        self.root_layout.addWidget(self.sudoku)


class _SudokuGUI(QWidget):

    def __init__(self):
        super().__init__()

        # attributes
        self.sudoku = Sudoku()

        # layout
        self.root_layout = QGridLayout()
        self.setLayout(self.root_layout)

        # initialize board layout
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(32 * 8, 32 * 8)
        for i in range(9):
            self.layout().setRowStretch(i, 1)
            self.layout().setColumnStretch(i, 1)
        for i in range(9):
            for j in range(9):
                self.layout().addWidget(_Square(), i, j)

        # initialize game
        self.generate()

    def reload(self):
        for i in range(9):
            for j in range(9):
                num = self.sudoku.matrix[i][j]
                if 0 < num < 10:
                    color = 'rgb(0, 0, 0)'
                else:
                    color = 'rgb(250, 0, 0)'
                widget = self.root_layout.itemAtPosition(i, j).widget()
                widget.label.setStyleSheet(f'color: {color};')
                widget.set_num(num)

    def generate(self):
        self.sudoku = Sudoku()
        self.reload()

    def solve(self):
        self.sudoku.solve()
        self.reload()

    def clear(self):
        self.sudoku.clear()
        self.reload()

    def resizeEvent(self, event: QResizeEvent):
        rect = self.layout().geometry()
        x = min(rect.width(), rect.height())
        self.setGeometry(0, 0, x, x)

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)
        pen = QPen(QBrush(), 3)
        pen.setColor(QColor(0, 0, 0))
        qp.setPen(pen)

        m = int(self.layout().geometry().width() / 3)
        for i in range(3):
            for j in range(3):
                qp.drawRect(i*m, j*m, m, m)


class _Square(QWidget):

    def __init__(self, num: int = 0):
        super().__init__()

        # attributes
        self.num = num
        self.background = QColor(220, 220, 220)

        # layouts
        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)

        # label
        self.label = QLineEdit(self.get_num())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.textChanged.connect(self.set_text)
        self.root_layout.addWidget(self.label)

    def set_text(self, txt: str):
        if txt.isnumeric():
            x = int(txt)
            if 0 < x < 10:
                self.label.setText(txt)
                return
        self.label.setText('')

    def set_num(self, num):
        self.num = int(num)
        self.label.setText(self.get_num())

    def get_num(self) -> str:
        return str(self.num) if (0 < self.num < 10) else ''

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)
        qp.drawRect(self.layout().geometry())

    def resizeEvent(self, event: QResizeEvent):
        rect = self.layout().geometry()
        r = 5
        u = rect.x() + r
        v = rect.width() - 2 * r
        self.label.setGeometry(u, u, v, v)

        font = self.label.font()
        font.setPointSize(v * 0.4)
        self.label.setFont(font)


if __name__ == '__main__':
    app = QApplication()
    window = SudokuGUI()
    window.show()
    sys.exit(app.exec())
