import logic
import gui

def main():
    '''
    Main function; Calls logic and gui 
    '''
    application = gui.QApplication([])
    window = logic.Logic()
    window.show()
    application.exec()

if __name__ == "__main__":
    main()