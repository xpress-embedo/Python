import os
import codecs
import pickle
import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtGui, QtWidgets

global server_info
global led_state
led_state = False

filename = 'settings.txt'

def save_file():
    with open(filename, "wb") as myFile:
        pickle.dump(server_info, myFile)

if os.path.exists(filename):
    # Read Dictionary from this file
    with open(filename, "rb") as myFile:
        server_info = pickle.load(myFile)
else:
    # Create Dictionary Using Default parameters
    server_info = { "Server_Address":"hairdresser.cloudmqtt.com", \
                    "Server_Port":"17259", \
                    "Username": "pyptiouq", \
                    "Password":"aQp113ENJeO9"}
    save_file()


# Callback Function on Connection with MQTT Server
def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    if rc == 0:
        # Subscribe Topic from here
        client.subscribe("home/#")
        # Enable Disconnect Button and Enable Others
        ui.connect_btn.setDisabled(True)
        # ui.server_add.setEnabled(False) Don't use this
        ui.server_add.setDisabled(True)
        ui.server_port.setDisabled(True)
        ui.username.setDisabled(True)
        ui.password.setDisabled(True)
        ui.disconnect_btn.setEnabled(True)
        ui.led_btn.setEnabled(True)
        ui.statusBar.setStatusTip("Connected")

# Callback Function on Receiving the Subscribed Topic/Message
def on_message( client, userdata, msg):
    # print the message received from the subscribed topic
    #print ( str(msg.payload) )
    #print ( str(len(msg.payload) ))
    if len(msg.payload) == 5:
        message = msg.payload
        message = message.decode()      # default decoding utf-8
        temp, humidity = message.split(',')
        ui.temp.setText(temp)
        ui.humidity.setText(humidity)
    

def save_server_add():
    global server_info
    server_info["Server_Address"] = ui.server_add.text()
    save_file()

def save_server_port():
    server_info["Server_Port"] = ui.server_port.text()
    save_file()

def save_username():
    server_info["Username"] = ui.username.text()
    save_file()

def save_password():
    server_info["Password"] = ui.password.text()
    save_file()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def connect_with_server():
    global server_info
    client.username_pw_set(server_info["Username"], server_info["Password"])
    client.connect(server_info["Server_Address"], int(server_info["Server_Port"]), 60)
    client.loop_start()


def disconnect_with_server():
    client.loop_stop()
    client.disconnect()
    # Enable Connect Button and Disable Others
    ui.connect_btn.setEnabled(True)
    ui.server_add.setEnabled(True)
    ui.server_port.setEnabled(True)
    ui.username.setEnabled(True)
    ui.password.setEnabled(True)
    ui.disconnect_btn.setDisabled(True)
    ui.led_btn.setDisabled(True)
    ui.statusBar.setStatusTip("Not Connected")

def led_state_loggle():
    global led_state
    if led_state ==  True:
        client.publish("led", bytes([0x00]))
        led_state = False
        ui.led_btn.setText("OFF")
    else:
        client.publish("led", bytes([0x01]))
        led_state = True
        ui.led_btn.setText("ON")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(306, 199)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setGeometry(QtCore.QRect(220, 10, 75, 31))
        self.connect_btn.setObjectName("connect_btn")
        self.disconnect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_btn.setEnabled(False)
        self.disconnect_btn.setGeometry(QtCore.QRect(220, 70, 75, 31))
        self.disconnect_btn.setObjectName("disconnect_btn")
        self.temp_lbl = QtWidgets.QLabel(self.centralwidget)
        self.temp_lbl.setGeometry(QtCore.QRect(10, 120, 69, 18))
        self.temp_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.temp_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_lbl.setObjectName("temp_lbl")
        self.humid_lbl = QtWidgets.QLabel(self.centralwidget)
        self.humid_lbl.setGeometry(QtCore.QRect(110, 120, 69, 18))
        self.humid_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.humid_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.humid_lbl.setObjectName("humid_lbl")
        self.temp = QtWidgets.QLabel(self.centralwidget)
        self.temp.setGeometry(QtCore.QRect(10, 140, 31, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.temp.setFont(font)
        self.temp.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.temp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.temp.setObjectName("temp")
        self.c_lbl = QtWidgets.QLabel(self.centralwidget)
        self.c_lbl.setGeometry(QtCore.QRect(50, 140, 21, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.c_lbl.setFont(font)
        self.c_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.c_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.c_lbl.setObjectName("c_lbl")
        self.humidity = QtWidgets.QLabel(self.centralwidget)
        self.humidity.setGeometry(QtCore.QRect(110, 140, 31, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.humidity.setFont(font)
        self.humidity.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.humidity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.humidity.setObjectName("humidity")
        self.percent_lbl = QtWidgets.QLabel(self.centralwidget)
        self.percent_lbl.setGeometry(QtCore.QRect(150, 140, 21, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.percent_lbl.setFont(font)
        self.percent_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.percent_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.percent_lbl.setObjectName("percent_lbl")
        self.led_btn = QtWidgets.QPushButton(self.centralwidget)
        self.led_btn.setGeometry(QtCore.QRect(220, 110, 71, 51))
        self.led_btn.setObjectName("led_btn")
        self.led_btn.setEnabled(False)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 71, 91))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.server_add_lbl = QtWidgets.QLabel(self.widget)
        self.server_add_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.server_add_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.server_add_lbl.setObjectName("server_add_lbl")
        self.verticalLayout.addWidget(self.server_add_lbl)
        self.server_port_lbl = QtWidgets.QLabel(self.widget)
        self.server_port_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.server_port_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.server_port_lbl.setObjectName("server_port_lbl")
        self.verticalLayout.addWidget(self.server_port_lbl)
        self.username_lbl = QtWidgets.QLabel(self.widget)
        self.username_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.username_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.username_lbl.setObjectName("username_lbl")
        self.verticalLayout.addWidget(self.username_lbl)
        self.password_lbl = QtWidgets.QLabel(self.widget)
        self.password_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.password_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.password_lbl.setObjectName("password_lbl")
        self.verticalLayout.addWidget(self.password_lbl)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(90, 10, 111, 91))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.server_add = QtWidgets.QLineEdit(self.widget1)
        self.server_add.setMaxLength(30)
        self.server_add.setObjectName("server_add")
        self.verticalLayout_2.addWidget(self.server_add)
        self.server_port = QtWidgets.QLineEdit(self.widget1)
        self.server_port.setMaxLength(30)
        self.server_port.setObjectName("server_port")
        self.verticalLayout_2.addWidget(self.server_port)
        self.username = QtWidgets.QLineEdit(self.widget1)
        self.username.setMaxLength(30)
        self.username.setObjectName("username")
        self.verticalLayout_2.addWidget(self.username)
        self.password = QtWidgets.QLineEdit(self.widget1)
        self.password.setMaxLength(30)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.verticalLayout_2.addWidget(self.password)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Weather Monitor"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
        self.disconnect_btn.setText(_translate("MainWindow", "Disconnect"))
        self.temp_lbl.setText(_translate("MainWindow", "Temperature"))
        self.humid_lbl.setText(_translate("MainWindow", "Humidity"))
        self.temp.setText(_translate("MainWindow", "0"))
        self.c_lbl.setText(_translate("MainWindow", "C"))
        self.humidity.setText(_translate("MainWindow", "0"))
        self.percent_lbl.setText(_translate("MainWindow", "%"))
        self.led_btn.setText(_translate("MainWindow", "OFF"))
        self.server_add_lbl.setText(_translate("MainWindow", "Server Add :"))
        self.server_port_lbl.setText(_translate("MainWindow", "Server Port :"))
        self.username_lbl.setText(_translate("MainWindow", "Username :"))
        self.password_lbl.setText(_translate("MainWindow", "Password :"))
        # Main Program Starts from Here
        self.statusBar.setStatusTip("Not Connected")
        # Update Server Information
        global server_info
        self.server_add.setText(server_info["Server_Address"])
        self.server_port.setText(server_info["Server_Port"])
        self.username.setText(server_info["Username"])
        self.password.setText(server_info["Password"])
        # Button Press Events
        self.connect_btn.clicked.connect( connect_with_server )
        self.disconnect_btn.clicked.connect( disconnect_with_server )
        self.led_btn.clicked.connect( led_state_loggle )
        self.server_add.editingFinished.connect( save_server_add )
        self.server_port.editingFinished.connect( save_server_port )
        self.username.editingFinished.connect( save_username )
        self.password.editingFinished.connect( save_password )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
