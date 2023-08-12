from gui import *
import formulas as f

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        '''
        Initializes logic of GUI; Generates cache, hides graphic modules that should not be present at startup, and links buttons to py methods.
        '''
        super().__init__()
        self.setupUi(self)

        self.__lastOperator = self.group_operator.checkedButton() # None

        # Cache
        self.__cache = {
            self.radio_add:         [ "", "", "", False ],
            self.radio_divide:      [ "", "", "", False ],
            self.radio_multiply:    [ "", "", "", False ],
            self.radio_modulo:      [ "", "", "", False ],
            self.radio_subtract:    [ "", "", "", False ],
            self.radio_root:        [ "", "", "", False ],
            None:                   [ "", "", "", False]
        }
        self.__operator_display_settings = {
            self.radio_add:         [ "Value 1"   , "Value 2"  ,  True ],
            self.radio_divide:      [ "Numerator" , "Divisor"  ,  True ],
            self.radio_multiply:    [ "Value 1"   , "Value 2"  ,  True ],
            self.radio_modulo:      [ "Base"      , "Divisor"  ,  False ],
            self.radio_subtract:    [ "Value 1"   , "Value 2"  ,  True ],
            self.radio_root:        [ "Base"      , "Exponent" ,  False ],
            None:                   [ "Value 1"   , "Value 2"  ,  True ]
        }

        # Initial Hiding
        self.refresh_all_ui_elements()


        # Control Mappings
        self.check_extra_values.clicked.connect(lambda: self.click_check_extra_values())
        self.button_calculate.clicked.connect(lambda: self.click_calculate())
        self.group_operator.buttonClicked.connect(lambda: self.click_operation())
        self.button_clear_cache.clicked.connect(lambda: self.cache_clear())

    def click_check_extra_values(self) -> None:
        '''
        Master action on Click of check_extra_values checkbox; Updates cache and updates module visibility.
        '''
        self.update_cache(self.group_operator.checkedButton())
        self.refresh_all_ui_elements()

    def update_module_visibility(self) -> None:
        '''
        Updates all of the graphic modules' visibily based on various parameters: state of cache, active selected operation, last selected operation, etc
        '''
        def vis_extra_value(status: bool) -> None: 
            '''
            Set the visibility of the inversely-related frames of extra values and default 2-value data entry.

            :param status: Visibility status of extra values frame; Visibility not status of two value frame 
            '''
            if status:
                self.frame_two_values.hide()
                self.frame_extra_values.show()
            else:
                self.frame_extra_values.hide()
                self.frame_two_values.show()
        def vis_answer(status: bool) -> None:
            '''
            Set the visibility of the frame containing all answer-related display modules.

            :param status: Visibility status of frame containing answer-related display modules
            '''
            if status:
                self.group_answer.show()
            else:
                self.group_answer.hide()
        def vis_all_value(status: bool) -> None:
            '''
            Set the visibility of the frame containing all value-related display modules.

            :param status: Visibility status of the frame containing all value-related display modules.
            '''
            if status:
                self.group_value.show()
            else:
                self.group_value.hide()

        if self.__lastOperator == None and self.group_operator.checkedButton() == None:
            vis_answer(False)
            vis_extra_value(False)
            vis_all_value(False)
            return
        else: 
            vis_all_value(True)
            vis_answer(True)

        self.line_value_1.setText(self.__cache[self.group_operator.checkedButton()][0])
        self.line_value_2.setText(self.__cache[self.group_operator.checkedButton()][1])
        self.text_values.setText(self.__cache[self.group_operator.checkedButton()][2])

        vis_extra_value(self.__cache[self.group_operator.checkedButton()][3])

    def set_operation_dependent_display_settings(self) -> None:
        '''
        Method grabs display settings to set the availability of extra value input when using some operations.
        '''
        def enable_check_extra_values(option: bool) -> None:
            '''
            Toggles the availability of check_extra_values
            :param option: True/False Availability of check_extra_values
            '''
            self.check_extra_values.setEnabled(option)
            if option:
                self.check_extra_values.setToolTip("")
            else:
                self.check_extra_values.setToolTip("This option has been disabled.")

        operation = self.group_operator.checkedButton()
        self.label_value_1.setText(self.__operator_display_settings[operation][0])
        self.label_value_2.setText(self.__operator_display_settings[operation][1])
        enable_check_extra_values(self.__operator_display_settings[operation][2])
     
    def click_calculate(self) -> None:
        '''
        Method is called when calculate button is clicked; Handles calculation and setting answer text.
        '''
        def get_decimal_fraction(text: str) -> float:
            '''
            Gets the decimal fraction of string input that can become float
            :param text: Input string with optional numerator/denominator to be calculated
            :return: Float value of the calculated and transformed input string
            '''
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

        def get_extra_values() -> list[float]:
            '''
            Gets a list of all the float values of the input in extra values input box
            :return: list[float] of the values in the extra values input box
            '''
            raw = self.text_values.toPlainText().strip()
            if raw == '':
                raise IndexError
            else:
                raw = raw.split(',')
            
            values = []
            for value in raw:
                values.append(get_decimal_fraction(value))
            return values

        def get_two_values() -> list[float]:
            '''
            Gets a list of all the float values of the input in two values input box
            :return: list[float] of the values in the two values input box
            '''
            if self.line_value_1.text().strip() == "" or self.line_value_2.text().strip() == "":
                raise TypeError

            value_1 = get_decimal_fraction(self.line_value_1.text())
            value_2 = get_decimal_fraction(self.line_value_2.text())
            
            return [ value_1, value_2 ]

        # Get user input from selected option
        list[float]: values
        try:
            if self.check_extra_values.isChecked():
                values = get_extra_values()
            else:
                values = get_two_values()
        except ValueError:
            self.set_answer_text("Input must contain only numbers!")
            return
        except TypeError:
            self.set_answer_text("All input boxes must contain a number!")
            return
        except IndexError:
            self.set_answer_text("The input box must contain a number!")
            return
        
        # Run operation
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
                try:
                    answer = f.divide(values)
                except ZeroDivisionError:
                    answer = "Cannot Divide by Zero"
            case self.radio_modulo:
                try:
                    answer = f.modulo(values)
                except ZeroDivisionError:
                    answer = "Cannot Divide by Zero"
            case self.radio_root:
                answer = f.exponent(values)
            case None:
                self.set_answer_text("Select an operation!")
                return
            case _:
                self.set_answer_text("Unknown Error - Contact Developer")
                return

        self.set_answer_text(str(answer))

    def click_operation(self) -> None:
        '''
        Main method when an operation checkbox is clicked.
        '''
        self.update_cache(self.__lastOperator)

        self.refresh_all_ui_elements()

        self.__lastOperator = self.group_operator.checkedButton()

    def refresh_all_ui_elements(self) -> None:
        '''
        Main refresh for all UI elements
        '''
        self.check_extra_values.setChecked(self.__cache[self.group_operator.checkedButton()][3])
        self.set_answer_text("")
        self.update_module_visibility()
        self.set_operation_dependent_display_settings()

    def update_cache(self, button: QRadioButton) -> None:
        '''
        Stores UI element data to the cache of the button
        :param button: Operation option that assumes responsibility for UI elements
        '''
        self.__cache[button] = [ self.line_value_1.text(), self.line_value_2.text(), self.text_values.toPlainText(), self.check_extra_values.isChecked() ]

    def cache_clear(self) -> None:
        '''
        Resets cache to default; Sets UI to reflect cache entries
        '''
        # Cache
        self.__cache = {
            self.radio_add:         [ "", "", "", False ],
            self.radio_divide:      [ "", "", "", False ],
            self.radio_multiply:    [ "", "", "", False ],
            self.radio_modulo:      [ "", "", "", False ],
            self.radio_subtract:    [ "", "", "", False ],
            self.radio_root:        [ "", "", "", False ],
            None:                   [ "", "", "", False]
        }

        self.refresh_all_ui_elements()

    def set_answer_text(self, text: str) -> None:
        '''
        Sets the answer text box with proper formating.
        :param text: Text to be displayed on the answer spot.
        '''
        self.label_answer.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">" + text + "<br/></span></p></body></html>", None))

if __name__ == "__main__":
    import main
    main.main()