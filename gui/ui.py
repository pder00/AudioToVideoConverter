'''enter deepspeech training files at line 354'''
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, time, subprocess


class Constants():
    SC_WIDTH, SC_HEIGHT = 600, 450
    SC_X, SC_Y = 250, 150
    LBL_WIDTH, LBL_HEIGHT = 550, 10
    BTN_WIDTH, BTN_HEIGHT = 80, 25
    
    def color_blue_light(self):
        return  "color: rgb(197, 255, 254);\n"
    def color_blue_dark(self):
        return "color: rgb(94, 130, 180);\n"
    def color_white(self):
        return "color: rgb(255, 255, 255);\n"
    def color_gray_light(self):
        return "color: rgb(230, 230, 230);\n"
    def color_black(self):
        return "color: rgb(0, 0, 0);\n"
    def color_red(self):
        return "color: rgb(230,30,30);\n"

def set_model(train_dir):
    from deepspeech import Model
    model_file_path=train_dir+'deepspeech-0.7.4-models.pbmm'
    lm_file_path=train_dir+'deepspeech-0.7.4-models.scorer'
    beam_width, lm_alpha, lm_beta = 100, 0.75, 1.85
    model = Model(model_file_path)
    model.enableExternalScorer(lm_file_path)
    model.setScorerAlphaBeta(lm_alpha, lm_beta)
    model.setBeamWidth(beam_width)
    return model

def new_file(file,type):
    f,i=file,1
    while True:
        if os.path.exists(f+type):
            f = '{}({})'.format(file, i)
            i+=1
        else:
            return f+type

class Ui_Welcome_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Welcome_MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setGeometry(Constants().SC_X,Constants().SC_Y,Constants().SC_WIDTH,Constants().SC_HEIGHT)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-"+Constants().color_blue_light())
        self.file_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__))+ os.sep + os.pardir)
        icon_path = "sprites/icon.png"
        file_path = os.path.join(self.file_dir, icon_path)
        self.setWindowIcon(QtGui.QIcon(file_path))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.ui_dir = Ui_Directories_MainWindow()
        self.setupUi()
        

    def setupUi(self):
        '''image label'''
        self.lbl_img = QtWidgets.QLabel(self.centralwidget)
        self.lbl_img.setGeometry(QtCore.QRect(20, 70, 281, 401))
        self.lbl_img.setText("") 
        rel_path = "sprites/welcome_transparent.png"
        abs_file_path = os.path.join(self.file_dir, rel_path)
        pixmap = QtGui.QPixmap(abs_file_path)
        self.lbl_img.setPixmap(pixmap)
        self.lbl_img.setObjectName("lbl_img_welcome")
        self.lbl_img.resize(pixmap.width(),pixmap.height())
        '''start button'''
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(370, 150, 151, 141))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btn_start.setFont(font)
        self.btn_start.setStyleSheet("background-"+Constants().color_blue_dark()+Constants().color_blue_light())
        self.btn_start.setObjectName("btn_start")
        self.btn_start.clicked.connect(self.click_start)
        '''welcome label'''
        self.lbl_welcome = QtWidgets.QLabel(self.centralwidget)
        self.lbl_welcome.setGeometry(QtCore.QRect(25, 35, 281, 25))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lbl_welcome.setFont(font)
        self.lbl_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_welcome.setObjectName("lbl_welcome")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AudioToVideo", "AudioToVideo"))
        self.btn_start.setText(_translate("MainWindow", "START"))
        self.lbl_welcome.setText(_translate("MainWindow", "Welcome!"))

    def click_start(self):
        self.ui_dir.show()
        self.close()
class Ui_Directories_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Directories_MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setGeometry(Constants().SC_X,Constants().SC_Y,Constants().SC_WIDTH,Constants().SC_HEIGHT)
        self.setStyleSheet("background-"+Constants().color_blue_light())
        self.file_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__))+ os.sep + os.pardir)
        icon_path = "sprites/icon.png"
        file_path = os.path.join(self.file_dir, icon_path)
        self.setWindowIcon(QtGui.QIcon(file_path))
        self.centralwidget = QtWidgets.QWidget(self)
        self.audio_dir=''
        self.output_dir=''
        self.script_dir=''
        self.has_script=False
        self.text=False
        self.centralwidget.setObjectName("centralwidget")
        self.setupUi()

    def setupUi(self):
        self.lbl_audio_dir = QtWidgets.QLabel(self.centralwidget)
        self.lbl_audio_dir.setGeometry(QtCore.QRect(10, 20, 180, 16))
        self.lbl_audio_dir.setObjectName("lbl_audio_dir")
        self.lbl_audio_found = QtWidgets.QLabel(self.centralwidget)
        self.lbl_audio_found.setGeometry(QtCore.QRect(180, 20, 571, 16))
        self.lbl_audio_found.setStyleSheet("QLabel { "+Constants().color_red()+"}")
        self.lbl_audio_found.setHidden(True)
        self.lbl_audio_format = QtWidgets.QLabel(self.centralwidget)
        self.lbl_audio_format.setGeometry(QtCore.QRect(180, 20, 571, 16))
        self.lbl_audio_format.setStyleSheet("QLabel { "+Constants().color_red()+"}")
        self.lbl_audio_format.setHidden(True)
        self.txt_output_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_output_dir.setGeometry(QtCore.QRect(10, 110, 571, 25))
        self.txt_output_dir.setStyleSheet("background-"+Constants().color_white())
        self.txt_output_dir.setText("")
        self.txt_audio_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_audio_dir.setGeometry(QtCore.QRect(10, 50, 571, 25))
        self.txt_audio_dir.setStyleSheet("background-"+Constants().color_white())
        self.txt_audio_dir.setText("")
        self.lbl_out_dir = QtWidgets.QLabel(self.centralwidget)
        self.lbl_out_dir.setGeometry(QtCore.QRect(10, 90, 180, 16))
        self.lbl_out_dir.setObjectName("lbl_out_dir")
        self.lbl_out_found = QtWidgets.QLabel(self.centralwidget)
        self.lbl_out_found.setGeometry(QtCore.QRect(180, 90, 571, 16))
        self.lbl_out_found.setStyleSheet("QLabel { "+Constants().color_red()+"}")
        self.lbl_out_found.setHidden(True)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 150, 571, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.check_b)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 180, 571, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.check_b2)
        self.lbl_script_dir = QtWidgets.QLabel(self.centralwidget)
        self.lbl_script_dir.setGeometry(QtCore.QRect(10, 210, 180, 16))
        self.lbl_script_dir.setObjectName("lbl_script_dir")
        self.lbl_script_dir.setHidden(True)
        self.lbl_script_found = QtWidgets.QLabel(self.centralwidget)
        self.lbl_script_found.setGeometry(QtCore.QRect(180, 210, 571, 16))
        self.lbl_script_found.setStyleSheet("QLabel { "+Constants().color_red()+"}")
        self.lbl_script_found.setHidden(True)
        self.lbl_script_format = QtWidgets.QLabel(self.centralwidget)
        self.lbl_script_format.setGeometry(QtCore.QRect(180, 210, 571, 16))
        self.lbl_script_format.setStyleSheet("QLabel { "+Constants().color_red()+"}")
        self.lbl_script_format.setHidden(True)
        self.txt_script_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_script_dir.setGeometry(QtCore.QRect(10, 240, 571, 25))
        self.txt_script_dir.setStyleSheet("background-"+Constants().color_white())
        self.txt_script_dir.setText("")
        self.txt_script_dir.setObjectName("txt_script_dir")
        self.txt_script_dir.setHidden(True)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 400, 75, 23))
        self.pushButton.setStyleSheet("background-"+Constants().color_blue_dark()+Constants().color_blue_light())
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 400, 75, 23))
        self.pushButton_2.setStyleSheet("background-"+Constants().color_blue_dark()+Constants().color_blue_light())
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.click_run)
        self.pushButton.clicked.connect(self.click_cancel)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AudioToVideo", "AudioToVideo"))
        self.lbl_audio_dir.setText(_translate("MainWindow", "Choose Audio File Directory:"))
        self.lbl_audio_found.setText(_translate("MainWindow", "Audio file not found"))
        self.lbl_audio_format.setText(_translate("MainWindow", "Check file format"))
        self.lbl_script_found.setText(_translate("MainWindow", "Script file not found"))
        self.lbl_out_found.setText(_translate("MainWindow", "folder not found"))
        self.lbl_script_format.setText(_translate("MainWindow", "Check file format"))
        self.lbl_out_dir.setText(_translate("MainWindow", "Choose Output Directory:"))
        self.checkBox.setText(_translate("MainWindow", "I just want the text file"))
        self.checkBox_2.setText(_translate("MainWindow", "I have the script"))
        self.lbl_script_dir.setText(_translate("MainWindow", "Choose Text File Directory:"))
        self.pushButton.setText(_translate("MainWindow", "CANCEL"))
        self.pushButton_2.setText(_translate("MainWindow", "NEXT"))
    def check_b(self):
        if self.checkBox.isChecked():
            self.text=True
            self.checkBox_2.setCheckable(False)
            self.checkBox_2.setStyleSheet("QCheckBox::indicator{ border: 1px solid black; background-"+Constants().color_gray_light()+"}\n")
        else:
            self.text=False
            self.checkBox_2.setCheckable(True)
            self.checkBox_2.setStyleSheet("")
        
    def check_b2(self):
        if self.checkBox_2.isChecked():
            self.checkBox.setCheckable(False)
            self.has_script=True
            self.checkBox.setStyleSheet("QCheckBox::indicator{ border: 1px solid black; background-"+Constants().color_gray_light()+"}\n")
            self.lbl_script_dir.setHidden(False)
            self.txt_script_dir.setHidden(False)
        else:
            self.script_dir =""
            self.has_script=False
            self.lbl_script_format.setHidden(True)
            self.lbl_script_found.setHidden(True)
            self.lbl_script_dir.setHidden(True)
            self.txt_script_dir.setHidden(True)
            self.checkBox.setCheckable(True)
            self.checkBox.setStyleSheet("")
    def cheak_format(self):
        audio_format=False
        script_format=False
        output_format=False
        if os.path.isfile(self.audio_dir):
            self.lbl_audio_found.setHidden(True)
            audio_extenions =['wav','mp3','flac']
            if self.audio_dir.endswith(tuple(audio_extenions)):
                self.lbl_audio_format.setHidden(True)
                audio_format=True
            else:
                self.lbl_audio_format.setHidden(False)
        else:
            self.lbl_audio_found.setHidden(False)
        if self.checkBox_2.isChecked():
            if os.path.isfile(self.script_dir):
                script_extenions =["txt"]
                if self.script_dir.endswith(tuple(script_extenions)):
                    self.lbl_script_found.setHidden(True)
                    script_format=True
                else:
                    self.lbl_script_format.setHidden(False)
            else:
                self.lbl_script_found.setHidden(False)
        else:
            self.lbl_script_format.setHidden(True)
            self.lbl_script_found.setHidden(True)
            script_format=True
        if os.path.isdir(self.output_dir):
            self.lbl_out_found.setHidden(True)
            output_format=True
        else:
            self.lbl_out_found.setHidden(False)
        if output_format==True and script_format==True and audio_format==True :
            return True
        else:
            return False
    def click_cancel(self):
        self.close()
    def click_run(self):
        self.audio_dir = self.txt_audio_dir.text()
        self.output_dir = self.txt_output_dir.text()
        self.script_dir = self.txt_script_dir.text() 
        if self.cheak_format():
            self.ui_convert = Ui_Converting_MainWindow(self.audio_dir,self.output_dir, self.script_dir,self.text,self.has_script)
            self.close()
            self.ui_convert.show()
class Ui_Converting_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,audio_dir,output_dir,script_dir,text,has_script):
        super(Ui_Converting_MainWindow, self).__init__()
        self.audio_dir, self.output_dir, self.script_dir,self.text,self.has_script=audio_dir, output_dir,script_dir, text, has_script
        self.setObjectName("MainWindow")
        self.setGeometry(Constants().SC_X,Constants().SC_Y,Constants().SC_WIDTH,Constants().SC_HEIGHT)
        self.setStyleSheet("background-"+Constants().color_blue_light())
        self.file_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__))+ os.sep + os.pardir)
        icon_path = "sprites/icon.png"
        file_path = os.path.join(self.file_dir, icon_path)
        self.setWindowIcon(QtGui.QIcon(file_path))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.ui_dir = Ui_Directories_MainWindow()
        self.done=False
        self.setupUi()
    def setupUi(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 110, 531, 31))
        self.progressBar.setStyleSheet("QProgressBar::chunk { background-"+Constants().color_blue_dark()+"}\n")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 400, 75, 23))
        self.pushButton.setStyleSheet("background-"+Constants().color_blue_dark()+Constants().color_blue_light())
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 200, 151, 31))
        self.pushButton_2.setStyleSheet("background-"+Constants().color_blue_dark()+Constants().color_blue_light())
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setHidden(True)
        self.pushButton_2.clicked.connect(self.open_folder)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(440, 400, 75, 23))
        self.pushButton_3.setStyleSheet("background-"+Constants().color_blue_dark()+Constants().color_blue_light())
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.progressBar_method)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AudioToVideo", "AudioToVideo"))
        self.label.setText(_translate("MainWindow", " "))
        self.pushButton.setText(_translate("MainWindow", "Cancel"))
        self.pushButton_2.setText(_translate("MainWindow", "Open file directory"))
        self.pushButton_3.setText(_translate("MainWindow", "START"))
    def progressBar_method(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "converting..."))
        self.pushButton_3.setHidden(True)
        '''./files/ : directory for temp files'''
        files = os.path.normpath(os.path.dirname(os.path.realpath(__file__))+ os.sep + os.pardir+ os.sep)+'/files'
        subprocess.call(['mkdir', files])
        files+='/'
        audio_dir, audio_name = os.path.split(self.audio_dir)
        name = os.path.splitext(audio_name)[0]
        
        train_dir = '' #enter deepspeech training files here

        output_dir = self.output_dir+'/'+name
        script,video,timestamps,subtitles= new_file(output_dir,'.txt'),new_file(output_dir,'.mp4'),files+'transcript.json',files+'subtitles.srt'
        
        sys.path.insert(0,(sys.path[0]+'/..'))

        from source.tools import Tools
        tools = Tools()

        '''convert audio form input directory to .wav format and save in ./files'''
        audio = tools.get_wav_file(self.audio_dir,name, files)
        audio_tuned = tools.tune_audio(audio,files) #sr:16000, pa:11025

        if self.has_script :
            '''if user has a script, remove annotations and save script.txt in ./files'''
            script=files+'script.txt'
            tools.remove_annotations(self.script_dir,script)
        else:
            '''convert speech to text and save script.txt in ./files'''
            from source.speechrecognizer import SpeechRecognition
            model = set_model(train_dir)
            speechrecognition = SpeechRecognition(model)
            speechrecognition.convert_speech_to_text(audio_tuned,script)

        for i in range(0,21):
            time.sleep(0.01)
            self.progressBar.setValue(i)
        
        if not self.text:
            '''align audio and script and save timestamps.jason in ./files'''
            tools.align_phonemes(audio_tuned,script,timestamps)
            for i in range(21,31):
                time.sleep(0.01)
                self.progressBar.setValue(i)

            from source.videomaker import VideoCreator
            videocreator = VideoCreator()

            '''convert phonemes and return a list of words and their values'''
            videocreator.convert_phonemes(timestamps)
            
            for i in range(31,41):
                time.sleep(0.01)
                self.progressBar.setValue(i)

            videocreator.create_subtitles(subtitles)

            for i in range(41,51):
                time.sleep(0.01)
                self.progressBar.setValue(i)

            '''create the output video file'''
            videocreator.creat_video(audio, video, subtitles)
            
        for i in range(51,101):
            time.sleep(0.01)
            self.progressBar.setValue(i)

        subprocess.call(['rm', '-rf', files[:-1]])

        self.done=True
        self.pushButton_2.setHidden(False)
        self.label.setText(_translate("MainWindow", "Done"))
        self.pushButton.setText(_translate("MainWindow", "Again"))

    def open_folder(self):
        #webbrowser.open(self.output_dir)
        subprocess.call(['xdg-open', self.output_dir])

    def click(self):
        if self.done:
            self.ui_dir.show()
            self.close()
        else:
            self.close()
       

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Welcome_MainWindow()
    ui.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()