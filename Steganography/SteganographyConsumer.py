import sys
from functools import partial
from os.path import splitext
from SteganographyGUI import *
from PySide.QtCore import *
from PySide.QtGui import *
import scipy.misc
import Steganography



class SteganographyConsumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(SteganographyConsumer, self).__init__(parent)
        self.setupUi(self)

        self.compression = -1
        self.flag_carrier = 0
        self.flag_payload = 0
        self.size_payload = 0
        self.size_carrier = 0
        self.carrier_array = 0
        self.payload_array = 0
        self.carrier2_array = 0


        self.chkApplyCompression.setDisabled(True)


        self.chkApplyCompression.stateChanged.connect(lambda: self.compression_1())
        self.chkOverride.stateChanged.connect(lambda: self.random())
        self.btnSave.clicked.connect(lambda: self.embed())
        self.btnExtract.clicked.connect(lambda :self.extract())
        self.btnClean.clicked.connect(lambda: self.clean())

        # Get the views that are required to have the drag-and-drop enabled.
        views = [self.viewPayload1, self.viewCarrier1, self.viewCarrier2]
        accept = lambda e: e.accept()

        for view in views:
            # We need to accept the drag event to be able to accept the drop.
            view.dragEnterEvent = accept
            view.dragMoveEvent = accept
            view.dragLeaveEvent = accept

            # Assign an event handler (a method,) to be invoked when a drop is performed.
            view.dropEvent = partial(self.processDrop, view)








        # NOTE: The line above links "all" views to the same function, and passes the view as a parameter in the
        # function. You could pass more than one widget to the function by adding more parameters to the signature,
        # in case you want to bind more than one widget together. you can even pass in another function, as a parameter,
        # which might significantly reduce the size of your code. Finally, if you prefer to have a separate function
        # for each view, where the view name is, say, "someView", you will need to:
        # 1- Create a function with a definition similar: funcName(self, e)
        # 2- Assign the function to be invoked as the event handler:
        #   self.someView.dropEvent = self.funcName

    def processDrop(self, view, e):
        """
        Process a drop event when it occurs on the views.
        """
        mime = e.mimeData()

        # Guard against types of drops that are not pertinent to this app.
        if not mime.hasUrls():
            return

        # Obtain the file path using the OS format.
        filePath = mime.urls()[0].toLocalFile()
        _, ext = splitext(filePath)

        if not ext == ".png":
            return

        # Now the file path is ready to be processed.
        #
        # TODO: Remove the print statement and continue the implementation using the filePath.
        #

        self.filePath = filePath
        if view == self.viewPayload1:
            self.filePath_pay = filePath
            self.flag = 0
        self.set_diplays(view,filePath)


        if self.flag_carrier == 1 and self.flag_payload == 1:


            aa = Steganography.Carrier(self.carrier_array)
            if aa.payloadExists() and self.chkOverride.isChecked() and (self.size_carrier > self.size_payload):
                self.btnSave.setEnabled(True)

            elif (not(aa.payloadExists())) and (self.size_carrier > self.size_payload):
                self.btnSave.setEnabled(True)

            else:
                self.btnSave.setEnabled(False)


    def set_diplays(self, view, filePath):

        if view == self.viewPayload1:
            if self.flag == 0:
                self.displayImage(view, filePath)
                self.chkApplyCompression.setChecked(False)
                self.slideCompression.setSliderPosition(0)
                self.slideCompression.setEnabled(False)

                img_array = scipy.misc.imread(filePath)
                a = Steganography.Payload(img = img_array)
                size = len(a.xml)
                size_1 = str(size)
                self.txtPayloadSize.setText(size_1)
                self.chkApplyCompression.setDisabled(False)
                self.flag = 1
                self.flag_payload = 1
                self.size_payload = size
                self.payload_array = img_array

            else:
                img_array = scipy.misc.imread(filePath)
                a = Steganography.Payload(img = img_array, compressionLevel= self.compression)
                size = len(a.xml)
                size_1 = str(size)
                self.payload_array = img_array
                self.size_payload = size
                self.txtPayloadSize.setText(size_1)

        elif view == self.viewCarrier1:

            self.displayImage(view,filePath)
            img_array = scipy.misc.imread(filePath)

            size = img_array.size/8
            size_1 = str(size)
            self.txtCarrierSize.setText(size_1)

            aa = Steganography.Carrier(img_array)
            if aa.payloadExists():
                self.lblPayloadFound.setText(">>>>Payload Found <<<<")
                self.chkOverride.setEnabled(True)
            else:
                self.lblPayloadFound.setText("")
                self.chkOverride.setEnabled(False)

            self.flag_carrier = 1
            self.size_carrier = size
            self.carrier_array = img_array

        elif view == self.viewCarrier2:

            self.displayImage(view,filePath)
            img_array = scipy.misc.imread(filePath)
            self.carrier2_array = img_array

            a = Steganography.Carrier(img_array)

            if not(a.payloadExists()):
                self.lblCarrierEmpty.setText(">>>>Carrier Empty<<<<")
                self.btnExtract.setEnabled(False)
                self.btnClean.setEnabled(False)
            else:
                self.lblCarrierEmpty.setText("")
                self.btnExtract.setEnabled(True)
                self.btnClean.setEnabled(True)


    def displayImage(self, view, filePath):

        a = QGraphicsScene()
        image = QPixmap(filePath)
        image_2 = image.scaled(355,275, Qt.KeepAspectRatio)
        a.addPixmap(image_2)
        view.setScene(a)
        view.show()

    def compression_1(self):

        if self.chkApplyCompression.isChecked():
            self.slideCompression.setEnabled(True)
            self.compression = self.slideCompression.value()
            if self.flag == 1:
                self.set_diplays(self.viewPayload1, self.filePath_pay)

                if self.flag_carrier == 1 and self.flag_payload == 1:
                    aa = Steganography.Carrier(self.carrier_array)
                    if aa.payloadExists() and self.chkOverride.isChecked() and (self.size_carrier > self.size_payload):
                        self.btnSave.setEnabled(True)

                    elif (not(aa.payloadExists())) and (self.size_carrier > self.size_payload):
                        self.btnSave.setEnabled(True)

                    else:
                        self.btnSave.setEnabled(False)









            self.slideCompression.valueChanged.connect(lambda: self.set_value_compression() )


        else:
            self.slideCompression.setEnabled(False)
            self.compression = -1
            if self.flag == 1:
                self.set_diplays(self.viewPayload1, self.filePath_pay)

                if self.flag_carrier == 1 and self.flag_payload == 1:
                    aa = Steganography.Carrier(self.carrier_array)
                    if aa.payloadExists() and self.chkOverride.isChecked() and (self.size_carrier > self.size_payload):
                        self.btnSave.setEnabled(True)

                    elif (not(aa.payloadExists())) and (self.size_carrier > self.size_payload):
                        self.btnSave.setEnabled(True)

                    else:
                        self.btnSave.setEnabled(False)




    def set_value_compression(self):

        self.compression = self.slideCompression.value()
        if self.flag == 1:
            self.set_diplays(self.viewPayload1, self.filePath_pay)

            if self.flag_carrier == 1 and self.flag_payload == 1:


                aa = Steganography.Carrier(self.carrier_array)
                if aa.payloadExists() and self.chkOverride.isChecked() and (self.size_carrier > self.size_payload):
                    self.btnSave.setEnabled(True)

                elif (not(aa.payloadExists())) and (self.size_carrier > self.size_payload):
                    self.btnSave.setEnabled(True)

                else:
                    self.btnSave.setEnabled(False)

        a = str(self.compression)
        self.txtCompression.setText(a)

    def random(self):
       if self.flag_carrier == 1 and self.flag_payload == 1:


            aa = Steganography.Carrier(self.carrier_array)
            if aa.payloadExists() and self.chkOverride.isChecked() and (self.size_carrier > self.size_payload):
                self.btnSave.setEnabled(True)
            elif (not(aa.payloadExists())) and (self.size_carrier > self.size_payload):
                self.btnSave.setEnabled(True)
            else:
                self.btnSave.setEnabled(False)

    def embed(self):

        aa = Steganography.Carrier(self.carrier_array)
        bb = Steganography.Payload(self.payload_array,compressionLevel=self.compression)
        final_img = aa.embedPayload(bb,override=True)


        filePath, _ = QFileDialog.getSaveFileName(self, caption='Save Image ...', filter="PNG files (*.png)")

        if not filePath:
            return

        scipy.misc.imsave(filePath+'.png',final_img)

    def extract(self):

        a = Steganography.Carrier(self.carrier2_array)
        b = a.extractPayload()
        filePath = "/home/yara/ee364/ee364b02/Lab11/new.png"
        scipy.misc.imsave(filePath,b.img)
        self.displayImage(self.viewPayload2,filePath)





    def clean(self):

        a = Steganography.Carrier(self.carrier2_array)
        b = a.clean()

        scipy.misc.imsave(self.filePath,b)
        self.lblCarrierEmpty.setText(">>>>Carrier Empty<<<<")
        self.btnExtract.setEnabled(False)
        self.btnClean.setEnabled(False)



if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = SteganographyConsumer()
    currentForm.show()
    currentApp.exec_()
