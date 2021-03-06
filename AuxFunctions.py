#########################################################################################

#Script Description:
# Auxillary functions used in main thread to setup Arduino & PC

#Author: Kyle Cook

#Last Updated: 4/24/2018

#########################################################################################



import os
import sys
import serial
import PyQt5.QtWidgets as qw
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def nav_to_directory(workingDirectory, outputFile):
    """Naviagtes to designated working directory. Creates said directory if need be"""

    #This block handles the creation of the specified working directory for compatibility between systems
    try:
        os.chdir(workingDirectory)
    except FileNotFoundError:
        os.mkdir(workingDirectory)
        os.chdir(workingDirectory)

    workingFile     = "dlhx0284F5.txt"
    filePath        = os.path.join(workingDirectory, workingFile)

    with open("Meet_Data.txt", 'w') as outputFile:
        outputFile.write("Meet Data\n")
        outputFile.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

def open_python_port():
    """Find connected Arduino and create serial object on connected port"""

    for port in list(serial.tools.list_ports.comports()):
        if 'Arduino' in port.description:
            return serial.Serial(port[0], 9600)

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def wait_for_arduino_ready(arduino):
    """Waits for Arduino to be ready to go, then allows program to proceed"""
    try:
        while arduino.inWaiting() <= 0:
            continue
        myData = bytes.decode(arduino.readline()) #Read Ready signal to clear it out
    except AttributeError:
        app = qw.QApplication(sys.argv)
        msg = qw.QMessageBox()
        msg.setWindowTitle("Receiver Error")
        msg.setText("No Receiving Module Detected.\nPlease insert Receiver and try again.")
        msg.exec_()
        sys.exit()