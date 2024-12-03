import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import qrcode
import cv2
import webbrowser
import time
import pyautogui

# img = qrcode.make('https://oa.zalo.me/home')
qr_image = cv2.imread("QR.png")

WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(600, 300, 640, 480)
        
        self.VBL = QVBoxLayout()
        self.HelloLabel = QLabel()
        self.VBL.addWidget(self.HelloLabel)
        
        self.HelloBTN = QPushButton("Welcome to QT5")
        self.HelloBTN.clicked.connect(self.setHelloLabel)
        self.VBL.addWidget(self.HelloBTN)
        
        self.Worker1 = Worker1()
        self.Worker1.start()
       
        self.setLayout(self.VBL)
        
    def setHelloLabel(self):
        self.HelloLabel.setText("Welcome to PYQT5")

class Worker1(QThread):
    # ImageUpdate = pyqtSignal(QImage)
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.START_TIME = 0
        # self.OPEN_FORM = False
        
    def face_data(self, image):
        face_width = 0
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
        for (x, y, h, w) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
            face_width = w
        return face_width
                        
    def run(self):
        OPEN_FORM = False
        start_time = time.time()
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        print("Run Worker1")
        while self.ThreadActive:
            _, frame = Capture.read()
            face_width_in_frame = self.face_data(frame)
            if (face_width_in_frame != 0):
                start_time = time.time()
                # SHOW WEBROWSER OPEN FORM
                if (OPEN_FORM == False):
                    print("Open tab")
                    webbrowser.open_new("https://oa.zalo.me/home")
                    OPEN_FORM = True
                # SHOW QR CODE
                # print("open QR code")
                # cv2.imshow("QR Code", qr_image)
            else:
                # CLOSE AFTRER 10S
                delay_time = time.time() - start_time
                print("Delay_time: ", delay_time) 
                if( delay_time >= 10): 
                    # CLOSE WEBROWSER OPEN FORM
                    if (OPEN_FORM):
                        pyautogui.hotkey('ctrl', 'w')
                        print("Close tab")
                        OPEN_FORM = False

                    
                    # CLOSE QR CODE
                    # cv2.destroyAllWindows()
            if cv2.waitKey(1) == ord("q"):
                break
        Capture.released()
        cv2.destroyAllWindows()
        
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())