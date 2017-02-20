import sys
import os
import base64
import re
import scipy
import zlib
import numpy
import gzip
import numpy as np
import copy

class Payload:

    def __init__(self, img=None, compressionLevel=-1, xml=None):
        if img == None and xml == None:
            raise ValueError("img and xml not provided")
        if(compressionLevel < -1 or compressionLevel > 9):
            raise ValueError("compressionLevel must be between 0 to 9")
        if img != None and type(img) is not numpy.ndarray :
            raise TypeError("Incorrect argument type")
        if xml != None and type(xml) is not str:
            raise TypeError("Incorrect argument type")
        if(xml):
            self.xml = xml
            self.img =  self.reconstruct_payload()
        else:
            self.img = img
            self.xml = self.generate_xml_string(compressionLevel)
            
    def reconstruct_payload(self):

        alllines = self.xml.split('\n')
        out = base64.b64decode(alllines[2])
        pattern_1 = r".*payload type=\"(\w+)\".*"
        pattern_2 = r".*size=\"(\d+),(\d+)\".*"
        pattern_3 = r".*compressed=\"True\".*"
        match_1 = re.match(pattern_1,alllines[1])
        match_2 = re.match(pattern_2,alllines[1])
        match_3 = re.match(pattern_3,alllines[1])
        if match_1:
            c_g = match_1.group(1)
        if match_2:
            col = int(match_2.group(2))
            row = int(match_2.group(1))
        if match_3:
            output = list(zlib.decompress(out))
        else:
            output = list(out)
        if(c_g == "Color"):

            red = []
            green = []
            blue = []
            final = []
            i = 0
            for i in range(len(output)):
                if(i < len(output)/3):
                    red.append(output[i])
                elif(i >= len(output)/3 and i < 2*len(output)/3 ):
                    green.append(output[i])
                else:
                    blue.append(output[i])
            i = 0
            for item in red:
                final.append(item)
                final.append(green[i])
                final.append(blue[i])
                i += 1
            aa = numpy.resize(final,(row,col,3))
        elif(c_g == "Gray"):
            aa = numpy.resize(output,(row,col))
        return aa

    def generate_xml_string(self,compressionLevel):

        A = self.img.shape
        dimension = len(A)
        if(dimension == 2):
            row = A[0]
            col = A[1]
            c_g = "Gray"
            img_arr = self.gray_image(row, col)
        elif(dimension == 3):
            row = A[0]
            col = A[1]
            c_g = "Color"
            img_arr = self.color_image(row,col)
        if(compressionLevel != -1):
            img_arra = zlib.compress(img_arr,compressionLevel)
        else:
            img_arra = img_arr
        img_array_1 = base64.b64encode(img_arra)
        img_array = str(img_array_1, encoding='UTF-8')
        xml_string = ""
        xml_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        if compressionLevel != -1:
            xml_string += "<payload type=\"" + c_g +"\" size=\"" + str(row) + "," + str(col) + "\" compressed=\"True\">\n"
        else:
            xml_string += "<payload type=\"" + c_g +"\" size=\"" + str(row) + "," + str(col) + "\" compressed=\"False\">\n"
        xml_string += img_array + "\n"
        xml_string += "</payload>"
        return xml_string

    def gray_image(self,row,col):
        image = self.img
        list_1 = []
        i = 0
        j = 0
        for i in range(row):
            for j in range(col):
                list_1.append(image[i,j])
        return numpy.asarray(list_1)

    def color_image(self,row,col):
        image = self.img
        list_1 = []
        for i in range(row):
            for j in range(col):
                list_1.append(image[i][j][0])
        for i in range(row):
            for j in range(col):
                list_1.append(image[i][j][1])
        for i in range(row):
            for j in range(col):
                list_1.append(image[i][j][2])
        return numpy.asarray(list_1)

class Carrier:

    def __init__(self,img):
        if type(img) is not numpy.ndarray:
            raise TypeError("Incorrect type of img")
        self.img = img

    def payloadExists(self):
        image = self.img
        A = self.img.shape
        dimension = len(A)
        row = A[0]
        col = A[1]
        k = 0
        counter = 0
        list_1 = []
        if dimension == 3:
            for i in range(row):
                if counter == 16:
                    break
                for j in range(col):
                    if counter == 16:
                        break
                    for k in range(1):
                        if((image[i][j][k] % 2) == 1 ):
                            list_1.append(1)
                        else:
                            list_1.append(0)
                        counter += 1
                        if counter == 16:
                            break

        elif(dimension == 2):
            for i in range(row):
                if counter == 16:
                    break
                for j in range(col):
                    if((image[i][j] % 2) == 1):
                        list_1.append(1)
                    else:
                        list_1.append(0)
                    counter += 1
                    if counter == 16:
                        break
        i = 0
        a = ""
        b = ""
        for i in range(16):
            if i < 8:
                a += str(list_1[i])
            else:
                b += str(list_1[i])
        test_1 = int(a,2)
        test_2 = int(b,2)
        if test_1 == 60 and test_2 == 63:
            return True
        else:
            return False

    def clean(self):
        image = copy.deepcopy(self.img)
        A = self.img.shape
        dimension = len(A)
        row = A[0]
        col = A[1]
        k = 0
        if dimension == 3:
            for i in range(row):
                for j in range(col):
                    for k in range(3):
                        if((image[i][j][k] % 2) == 1 ):
                            image[i][j][k] -= 1
        elif(dimension == 2):
            for i in range(row):
                for j in range(col):
                    if((image[i][j] % 2) == 1):
                        image[i][j] -= 1
        return image

    def embedPayload(self, payload, override=False):
        if type(payload) is not Payload:
            raise TypeError("Incorrect payload type")
        if override == False and self.payloadExists():
            raise Exception
        image = self.img
        A = self.img.shape
        dimension = len(A)
        row = A[0]
        col = A[1]
        k = 0
        list_1 = []
        if dimension == 3:
            if len(payload.xml)*8 > len(self.img)*len(self.img[0])*3:
                raise ValueError("Payload is larger than Carrier Image")
        elif(dimension == 2):
            if len(payload.xml)*8 > len(self.img)*len(self.img[0]) :
                raise ValueError("Payload is larger than Carrier Image")
        if dimension == 3:
            for i in range(row):
                for j in range(col):
                    list_1.append(self.img[i][j][0])
            for i in range(row):
                for j in range(col):
                    list_1.append(self.img[i][j][1])
            for i in range(row):
                for j in range(col):
                    list_1.append(self.img[i][j][2])
            i = 0
            for item in payload.xml:
                temp_ascii = ord(item)
                binary_rep = format(temp_ascii,'08b')
                for items in binary_rep:
                    if int(items) == 0:
                        if list_1[i] % 2 == 1:
                            list_1[i] -= 1
                            if list_1[i] < 0:
                                list_1[i] += 2
                    elif int(items) == 1:
                        if list_1[i] % 2 == 0:
                            list_1[i] += 1
                            if list_1[i] >= 256:
                                list_1 -= 2
                    i += 1
            red = []
            green = []
            blue = []
            final = []
            i = 0
            for i in range(len(list_1)):
                if(i < len(list_1)/3):
                    red.append(list_1[i])
                elif(i >= len(list_1)/3 and i < 2*len(list_1)/3 ):
                    green.append(list_1[i])
                else:
                    blue.append(list_1[i])
            i = 0
            for item in red:
                final.append(item)
                final.append(green[i])
                final.append(blue[i])
                i += 1
            aa = numpy.resize(final,(row,col,3))
        elif dimension == 2:
           for i in range(row):
                for j in range(col):
                    list_1.append(self.img[i][j])
           i = 0
           for item in payload.xml:
                temp_ascii = ord(item)
                binary_rep = format(temp_ascii,'08b')
                for items in binary_rep:
                    if int(items) == 0:
                        if list_1[i] % 2 == 1:
                            list_1[i] -= 1
                            if list_1[i] < 0:
                                list_1[i] += 2
                    elif int(items) == 1:
                        if list_1[i] % 2 == 0:
                            list_1[i] += 1
                            if list_1[i] >= 256:
                                list_1 -= 2
                    i += 1
           aa = numpy.resize(list_1,(row,col))
        return aa

    def extractPayload(self):
        if not(self.payloadExists()):
            raise Exception
        image = self.img
        A = self.img.shape
        dimension = len(A)
        row = A[0]
        col = A[1]
        k = 0
        list_1 = []
        if dimension == 3:
            for i in range(row):
                for j in range(col):
                    if((image[i][j][0] % 2) == 1 ):
                        list_1.append(1)
                    else:
                        list_1.append(0)
            for i in range(row):
                for j in range(col):
                    if((image[i][j][1] % 2) == 1 ):
                        list_1.append(1)
                    else:
                        list_1.append(0)

            for i in range(row):
                for j in range(col):
                    if((image[i][j][2] % 2) == 1 ):
                        list_1.append(1)
                    else:
                        list_1.append(0)
        elif(dimension == 2):
            for i in range(row):
                for j in range(col):
                    if((image[i][j] % 2) == 1):
                        list_1.append(1)
                    else:
                        list_1.append(0)
        a = ""
        final_str = ""
        b = ""
        i = 0
        b_str = ""
        for i in range(len(list_1)):
            if i % 8 == 0 and i != 0:
                aa = int(a,2)
                aaa = chr(aa)
                final_str += aaa
                a = ""
                if("</payload>" in final_str):
                    break
            a += str(list_1[i])

            b += str(list_1[i])
        print(final_str)
        result = Payload(xml = final_str)
        return result

if __name__ == "__main__":
    p = Payload()



