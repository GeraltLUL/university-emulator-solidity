from PyQt5 import QtWidgets
from run import Ui_MainWindow
from w3 import University
import sys


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.univ = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.enter_contract_address)
        self.ui.tabWidget.setTabText(0, "Contract verifying")
        self.ui.tabWidget.setTabText(1, "Log in")
        self.ui.tabWidget.setTabText(2, "Student's tab")
        self.ui.tabWidget.setTabText(3, "Professor's tab")
        self.ui.tabWidget.setTabText(4, "Admin panel")
        self.ui.tabWidget.setTabEnabled(0, True)
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.tabWidget.setTabEnabled(3, False)
        self.ui.tabWidget.setTabEnabled(4, False)
        self.ui.tabWidget_2.setTabText(0, "Login")
        self.ui.tabWidget_2.setTabText(1, "Student's register")
        self.ui.tabWidget_2.setTabText(2, "Professor's register")

        self.ui.pushButton_3.clicked.connect(self.student_register)
        self.ui.pushButton_2.clicked.connect(self.login_user)
        self.ui.pushButton_4.clicked.connect(self.professor_register)
        self.ui.pushButton_5.clicked.connect(self.add_grade_exam)
        self.ui.tabWidget.tabBarClicked.connect(self.render_professors_grades)

    def enter_contract_address(self):
        addr = self.ui.lineEdit.text()
        try:
            self.univ = University(addr)
            self.ui.label_3.setText("OK!")
            self.ui.label_5.setText(f"contract: {addr}")
            self.ui.tabWidget.setTabEnabled(1, True)
            # self.ui.verticalLayoutWidget.deleteLater()
            self.ui.tabWidget.removeTab(0)
        except Exception as e:
            self.ui.label_3.setText("Wrong address! Try again!")
            print(e)

    def student_register(self):
        try:
            id = self.univ.get_students_count()
            name = self.ui.lineEdit_6.text()
            password = self.ui.lineEdit_7.text()
            group = self.ui.lineEdit_5.text()
            addr = self.ui.lineEdit_4.text()
            if self.univ.add_student(addr, name, id, group, password) is not True:
                raise Exception("False")
            else:
                self.ui.label_8.setStyleSheet("color: green")
                self.ui.label_8.setText("OK!")
        except Exception as e:
            print(e)
            self.ui.label_8.setStyleSheet("color: red")
            self.ui.label_8.setText("Wrong data!")

    def professor_register(self):
        try:
            id = self.univ.get_professors_count()
            name = self.ui.lineEdit_8.text()
            password = self.ui.lineEdit_10.text()
            addr = self.ui.lineEdit_9.text()
            if self.univ.add_professor(addr, name, id, password) is not True:
                raise Exception("False")
            else:
                self.ui.label_9.setStyleSheet("color: green")
                self.ui.label_9.setText("OK!")
        except Exception as e:
            print(e)
            self.ui.label_9.setStyleSheet("color: red")
            self.ui.label_9.setText("Wrong data!")

    def add_grade_exam(self):
        try:
            name = self.ui.lineEdit_11.text()
            addr = self.ui.lineEdit_12.text()
            grade = int(self.ui.lineEdit_13.text())
            if self.univ.add_exam(grade, addr, name) is not True:
                raise Exception("False")
            else:
                self.ui.label_11.setStyleSheet("color: green")
                self.ui.label_11.setText("OK!")
        except Exception as e:
            print(e)
            self.ui.label_11.setStyleSheet("color: red")
            self.ui.label_11.setText("Wrong address!")

    def login_user(self):
        try:
            addr = self.ui.lineEdit_2.text()
            password = self.ui.lineEdit_3.text()
            res = self.univ.try_login(addr, password)

            if res is True:
                is_admin = self.univ.is_user_admin(addr)
                self.ui.tabWidget.removeTab(0)
                if self.univ.is_user_student(addr) is True:
                    type = "Student"
                    self.ui.tabWidget.setTabEnabled(0, True)
                    self.ui.tabWidget.setCurrentIndex(0)
                    self.render_student_grades(addr)
                else:
                    type = "Professor"
                    self.ui.tabWidget.setTabEnabled(1, True)
                    self.ui.tabWidget.setCurrentIndex(1)
                    self.render_professors_grades()

                self.ui.label_4.setText(f"user: {addr}, {type}")
                if is_admin is True:
                    print('admin')
                    self.ui.tabWidget.setTabEnabled(2, True)
                    self.ui.label_4.setText(f"{self.ui.label_4.text()} (Admin)")
            else:
                self.ui.label_7.setText("Wrong login or password!")
        except Exception as e:
            print(e)
            self.ui.label_7.setText("Wrong data!")

    def render_student_grades(self, student_addr):
        exams = self.univ.get_exams()
        my_exams = {}
        exams_names = []

        for e in exams:
            if e[1] == student_addr:
                my_exams[e[2]] = []

        cnt = 0
        for e in exams:
            if e[1] == student_addr:
                my_exams[e[2]].append(e[0])
                cnt = max(cnt, len(my_exams[e[2]]))

        for e in my_exams:
            if e not in exams_names:
                exams_names.append(e)

        print(exams)
        print(my_exams)

        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(cnt)
        self.ui.tableWidget.setColumnCount(len(my_exams))
        self.ui.tableWidget.setHorizontalHeaderLabels(exams_names)

        i = 0
        for arr in my_exams:
            j = 0
            for gr in my_exams[arr]:
                print(gr)
                self.ui.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(gr)))
                j += 1
            i += 1

    def render_professors_grades(self):
        exams = self.univ.get_exams()
        stud_exams = {}
        exams_names = []
        students_addrs = []

        flag_3 = self.ui.radioButton.isChecked()
        flag_4_5 = self.ui.radioButton_2.isChecked()
        flag_5 = self.ui.radioButton_3.isChecked()

        print(flag_3, flag_4_5, flag_5)

        for e in exams:
            stud_exams[e[2]] = []

        for e in exams:
            stud_exams[e[2]].append(e[0])

        for e in exams:
            if e[2] not in exams_names:
                exams_names.append(e[2])

        for e in exams:
            if (e[1]) not in students_addrs:
                students_addrs.append(e[1])

        for addr in students_addrs:
            for name in exams_names:
                res = False
                for exam in exams:
                    if exam[2] == name and exam[1] == addr:
                        res = True

                if res is False:
                    print('!', addr, name)
                    # exams.append(['-', addr, name])
                    stud_exams[name].append('-')

        students_addrs = [i[:6]+'...' for i in students_addrs]

        print(exams)
        print(stud_exams)
        print(exams_names)
        print(students_addrs)

        if not flag_3 and not flag_5 and not flag_4_5:
            self.ui.tableWidget_2.clear()
            self.ui.tableWidget_2.setRowCount(len(students_addrs))  # cnt
            self.ui.tableWidget_2.setColumnCount(len(exams_names))  # exams
            self.ui.tableWidget_2.setHorizontalHeaderLabels(exams_names)
            self.ui.tableWidget_2.setVerticalHeaderLabels(students_addrs)

            i = 0
            for arr in stud_exams:
                j = 0
                for gr in stud_exams[arr]:
                    print(gr)
                    self.ui.tableWidget_2.setItem(j, i, QtWidgets.QTableWidgetItem(str(gr)))
                    j += 1
                i += 1

        elif flag_5:
            self.ui.tableWidget_2.clear()
            self.ui.tableWidget_2.setRowCount(len(students_addrs))  # cnt
            self.ui.tableWidget_2.setColumnCount(len(exams_names))  # exams
            self.ui.tableWidget_2.setHorizontalHeaderLabels(exams_names)
            self.ui.tableWidget_2.setVerticalHeaderLabels(students_addrs)

            i = 0
            for arr in stud_exams:
                j = 0
                for gr in stud_exams[arr]:
                    if gr == 5:
                        self.ui.tableWidget_2.setItem(j, i, QtWidgets.QTableWidgetItem(str(gr)))
                        j += 1
                i += 1
        elif flag_4_5:
            self.ui.tableWidget_2.clear()
            self.ui.tableWidget_2.setRowCount(len(students_addrs))  # cnt
            self.ui.tableWidget_2.setColumnCount(len(exams_names))  # exams
            self.ui.tableWidget_2.setHorizontalHeaderLabels(exams_names)
            self.ui.tableWidget_2.setVerticalHeaderLabels(students_addrs)

            i = 0
            for arr in stud_exams:
                j = 0
                for gr in stud_exams[arr]:
                    if gr == 5 or gr == 3:
                        self.ui.tableWidget_2.setItem(j, i, QtWidgets.QTableWidgetItem(str(gr)))
                        j += 1
                i += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())
