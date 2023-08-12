from gui import *
import formulas as f

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.__lastOperator = None

        # Hide
        self.hide_ev_inputs()
        self.group_value.hide()
        self.hide_answer()

        # Cache
        self.__cache = {
            self.radio_add:         [ "", "", "", False ],
            self.radio_divide:      [ "", "", "", False ],
            self.radio_multiply:    [ "", "", "", False ],
            self.radio_modulo:      [ "", "", "", False ],
            self.radio_subtract:    [ "", "", "", False ],
            self.radio_root:        [ "", "", "", False ],
            None:                   ["","","", False]
        }

        # Control Mappings
        self.check_extra_values.clicked.connect(lambda: self.click_ev_button())
        self.button_calculate.clicked.connect(lambda: self.calculate())
        self.group_operator.buttonClicked.connect(lambda: self.click_operator_buttons())
        self.button_clear_cache.clicked.connect(lambda: self.cache_clear())

    def click_operator_buttons(self):
        self.cache_main()
        self.set_operation_dependent_display_settings()
        self.set_answer_text('')        

    def set_operation_dependent_display_settings(self):
        def enable_check_extra_values(option):
            self.check_extra_values.setEnabled(option)
            if option:
                self.check_extra_values.setToolTip("")
            else:
                self.check_extra_values.setToolTip("This has been disabled due to it not making sense with the selected operation.")

        operation = self.group_operator.checkedButton()
        match operation:
            case self.radio_add:
                enable_check_extra_values(True)
                self.label_value_1.setText('Value 1')
                self.label_value_2.setText('Value 2')
            case self.radio_subtract:
                enable_check_extra_values(True)
                self.label_value_1.setText('Value 1')
                self.label_value_2.setText('Value 2')
            case self.radio_multiply:                
                enable_check_extra_values(True)
                self.label_value_1.setText('Value 1')
                self.label_value_2.setText('Value 2')
            case self.radio_divide:
                enable_check_extra_values(False)
                self.label_value_1.setText('Numerator')
                self.label_value_2.setText('Divisor')
            case self.radio_modulo:
                enable_check_extra_values(False)
                self.label_value_1.setText('Numerator')
                self.label_value_2.setText('Divisor')
            case self.radio_root:
                enable_check_extra_values(False)
                self.label_value_1.setText('Base')
                self.label_value_2.setText('Exponent')
            case None:
                enable_check_extra_values(True)
                self.label_value_1.setText('Value 1')
                self.label_value_2.setText('Value 2')
                return
            case _:
                enable_check_extra_values(True)
                self.label_value_1.setText('Value 1')
                self.label_value_2.setText('Value 2')
                return

    def set_multi_focus(self, soonOperator: QRadioButton):
        self.check_extra_values.setChecked(self.__cache[soonOperator][3])
        self.click_ev_button()    

    def cache_main(self):
        soonOperator = self.group_operator.checkedButton()

        self.__cache[self.__lastOperator] = [ self.line_value_1.text(), self.line_value_2.text(), self.text_values.toPlainText(), self.check_extra_values.isChecked() ]
        
        if self.__lastOperator == None:
            self.__cache[soonOperator][3] = self.check_extra_values.isChecked()
            self.show_answer()
            self.group_value.show()
        else:
            self.line_value_1.setText(self.__cache[soonOperator][0])
            self.line_value_2.setText(self.__cache[soonOperator][1])
            self.text_values.setText(self.__cache[soonOperator][2])

        self.__lastOperator = self.group_operator.checkedButton()


        self.set_multi_focus(soonOperator)

    def cache_clear(self):
        self.__cache = {
            self.radio_add:        [ "", "", "", False ],
            self.radio_divide:     [ "", "", "", False ],
            self.radio_multiply:   [ "", "", "", False ],
            self.radio_modulo:     [ "", "", "", False ],
            self.radio_subtract:   [ "", "", "", False ],
            self.radio_root:       [ "", "", "", False ],
            None: ["","","", False ]
        }
        
        self.line_value_1.setText('')
        self.line_value_2.setText('')
        self.text_values.setText('')

        self.set_multi_focus(self.group_operator.checkedButton())
        self.set_answer_text('')

    def calculate(self):
        self.set_answer_text('')

        values = []
        try:
            if self.check_extra_values.isChecked():
                values = self.get_ev()
            else:
                values = self.get_general_values()
        except ValueError:
            self.set_answer_text("Input must only contain numbers!")
            return
        except TypeError:
            self.set_answer_text("All input boxes must contain a value!")
            return

        answer = None
        operation = self.group_operator.checkedButton()
        match operation:
            case self.radio_add:
                answer = f.add(values)
            case self.radio_subtract:
                answer = f.subtract(values)
            case self.radio_multiply:
                answer = f.multiply(values)
            case self.radio_divide:
                answer = f.divide(values)
            case self.radio_modulo:
                answer = f.modulo(values)
            case self.radio_root:
                answer = f.root(values)
            case None:
                self.set_answer_text("Select an operation!")
                return
            case _:
                self.set_answer_text("Unknown Error - Contact Developer")
                return
        self.set_answer_text(answer)

        return

    def get_ev(self):
        raw = self.text_values.toPlainText()

        values = []
        if '/' in raw:
            rawList = [ value.strip() for value in raw.split(',') if value.strip() ]
            for val in rawList:
                if '/' in val:
                    numer, denom = val.split('/')
                    val = (float(numer) / float(denom))
                
                values.append(float(val))
        else:
            values = [ float(value.strip()) for value in raw.split(',') if value.strip() ]
        return values

    def click_ev_button(self):
        if self.check_extra_values.isChecked():
            self.show_ev_inputs()
        else:
            self.hide_ev_inputs()

    def get_general_values(self):
        def get_decimal_fraction(text):
            text = str(text).strip()
            if '/' in text:
                textList = text.split('/')
                
                numer = textList[0]
                denoms = textList[1:len(textList)]
                
                total = float(numer)
                for denom in denoms:
                    total = float(total) / float(denom)
                return total
            else:
                return float(text)

        if self.line_value_1.text().strip() == "" or self.line_value_2.text().strip() == "":
            raise TypeError

        text_1 = self.line_value_1.text().strip()
        text_2 = self.line_value_2.text().strip()


        value_1 = get_decimal_fraction(text_1)
        value_2 = get_decimal_fraction(text_2)
        
        return [ value_1, value_2 ]

    def show_ev_inputs(self): 
        self.frame_two_values.hide()
        self.frame_extra_values.show()

    def hide_ev_inputs(self):
        self.frame_extra_values.hide()
        self.frame_two_values.show()

    def hide_answer(self):
        self.group_answer.hide()

    def show_answer(self):
        self.group_answer.show()

    def set_answer_text(self, text):
        self.label_answer.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">" + str(text) + "<br/></span></p></body></html>", None))
        return text

if __name__ == "__main__":
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()