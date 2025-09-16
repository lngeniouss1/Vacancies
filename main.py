from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
import sys
from company_vacancies import VacancyManager


class VacancyDialog(QDialog):
    def __init__(self, parent=None, data=None, mode="add"):
        super().__init__(parent)
        uic.loadUi("vacancy_dialog.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.mode = mode
        self.data = data

        if mode == "edit" and data:
            self.lineEditCompany.setText(data[0])
            self.lineEditPhone.setText(data[1])
            self.lineEditPosition.setText(data[2])
            self.lineEditEducation.setText(data[3])
            self.lineEditExperience.setText(data[4])
            self.setWindowTitle("Edit Vacancy")
        elif mode == "add":
            self.setWindowTitle("Add Vacancy")
        elif mode == "delete":
            self.lineEditCompany.setText(data[0])
            self.lineEditPhone.setText(data[1])
            self.lineEditPosition.setText(data[2])
            self.lineEditEducation.setText(data[3])
            self.lineEditExperience.setText(data[4])
            self.lineEditCompany.setReadOnly(True)
            self.lineEditPhone.setReadOnly(True)
            self.lineEditPosition.setReadOnly(True)
            self.lineEditEducation.setReadOnly(True)
            self.lineEditExperience.setReadOnly(True)
            self.btnSave.setText("Delete")
            self.setWindowTitle("Delete Vacancy")

        self.btnSave.clicked.connect(self.accept)

    def get_data(self):
        return [
            self.lineEditCompany.text(),
            self.lineEditPhone.text(),
            self.lineEditPosition.text(),
            self.lineEditEducation.text(),
            self.lineEditExperience.text()
        ]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vacancies.ui", self)
        self.manager = VacancyManager()
        self.manager.load_data()

        self.btnLoad.clicked.connect(self.load_table)
        self.btnClear.clicked.connect(self.clear_table)
        self.btnSort.clicked.connect(self.load_sorted_table)
        self.btnAdd.clicked.connect(self.add_vacancy)
        self.btnDelete.clicked.connect(self.delete_vacancy)
        self.btnEdit.clicked.connect(self.edit_vacancy)
        self.btnSearch.clicked.connect(self.search_vacancies)

        self.tableVacancies.itemClicked.connect(self.on_table_item_clicked)
        self.load_table()

    def on_table_item_clicked(self):
        row = self.tableVacancies.currentRow()
        if row >= 0:
            self.current_row_data = [self.tableVacancies.item(row, i).text() for i in range(5)]

    def load_table(self):
        self._load_vacancies(self.manager.get_all_vacancies())

    def load_sorted_table(self):
        self._load_vacancies(self.manager.get_vacancies_sorted_by_company())

    def _load_vacancies(self, vacancies):
        self.tableVacancies.setRowCount(len(vacancies))
        self.tableVacancies.setColumnCount(5)
        self.tableVacancies.setHorizontalHeaderLabels([
            "Компания", "Телефон", "Должность", "Образование", "Стаж"
        ])

        for row, v in enumerate(vacancies):
            self.tableVacancies.setItem(row, 0, QTableWidgetItem(v.company_name))
            self.tableVacancies.setItem(row, 1, QTableWidgetItem(v.phone))
            self.tableVacancies.setItem(row, 2, QTableWidgetItem(v.position))
            self.tableVacancies.setItem(row, 3, QTableWidgetItem(v.education))
            exp_item = QTableWidgetItem(str(v.experience))
            exp_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.tableVacancies.setItem(row, 4, exp_item)

        self.tableVacancies.setColumnWidth(0, 200)
        self.tableVacancies.setColumnWidth(1, 120)
        self.tableVacancies.setColumnWidth(2, 150)
        self.tableVacancies.setColumnWidth(3, 150)
        self.tableVacancies.setColumnWidth(4, 80)

    def clear_table(self):
        self.tableVacancies.setRowCount(0)
        self.tableVacancies.clearContents()

    def add_vacancy(self):
        dialog = VacancyDialog(self, mode="add")
        if dialog.exec_():
            data = dialog.get_data()
            if all(data):
                self.manager.add(data)
                self.manager.save_data()
                self.load_table()

    def delete_vacancy(self):
        if hasattr(self, 'current_row_data'):
            dialog = VacancyDialog(self, data=self.current_row_data, mode="delete")
            if dialog.exec_():
                self.manager.delete(self.current_row_data)
                self.manager.save_data()
                self.load_table()

    def edit_vacancy(self):
        if hasattr(self, 'current_row_data'):
            dialog = VacancyDialog(self, data=self.current_row_data, mode="edit")
            if dialog.exec_():
                new_data = dialog.get_data()
                if all(new_data):
                    key = self.manager.find_key(self.current_row_data)
                    if key != -1:
                        self.manager.edit(key, new_data)
                        self.manager.save_data()
                        self.load_table()

    def search_vacancies(self):
        query = self.lineEditSearch.text()
        if query:
            vacancies = self.manager.filter_by_position(query)
        else:
            vacancies = self.manager.get_all_vacancies()
        self._load_vacancies(vacancies)


app = QtWidgets.QApplication([])
window = MainWindow()
window.setStyleSheet(open("style.qss", "r").read())
window.show()
sys.exit(app.exec())