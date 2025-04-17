from PySide6.QtWidgets import QApplication
from Ui import Project

if __name__ == '__main__':
    app = QApplication([])

    with open("src/style.qss", "r") as arquivo:
        app.setStyleSheet(arquivo.read())
    
    projeto = Project()
    projeto.show()
    app.exec()