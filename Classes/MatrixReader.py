import cv2, numpy as np, time as t
from pylibdmtx.pylibdmtx import decode as decodeWithPylibdmtx
from qreader import QReader
from pyzbar.pyzbar import decode as decodeWithPyzbar
#from Utilities import util as u

class MatrixReader:

    @staticmethod
    def DecodeWithPyzbar(image:np.ndarray)->tuple[int,str,float]:
        '''Returns true if Pyzbar algorithm can find and decide matrix in image'''
        startTime=t.perf_counter()
        text=decodeWithPyzbar(MatrixReader.__ValidateImage(image))
        if text:
            return 1,f"'{''.join()}'",t.perf_counter()-startTime
        return 0,"NULL",t.perf_counter()-startTime
    
    @staticmethod
    def DecodeWithQReader(image:np.ndarray)->tuple[int,str,float]:
        '''Retursn True if QrReader algorithm can find and decode matrix in image'''
        startTime=t.perf_counter()
        text=QReader().detect_and_decode(MatrixReader.__ValidateImage(image))
        if text:
            return 1,f"'{text}'",t.perf_counter()-startTime
        return 0,"NULL",t.perf_counter()-startTime
    
    @staticmethod
    def DecodeWithCv2QrReader(image:np.ndarray)->tuple[int,str,float]:
        '''Returnrs True if cv2.QrCodeDetector can find and decode matrix in image'''
        startTime=t.perf_counter()
        try:
            data, points,_= cv2.QRCodeDetector().detectAndDecode(MatrixReader.__ValidateImage(image))
            if data and not data=='' :
                return 1, f"'{data}'",t.perf_counter()-startTime
            return 0, "NULL",t.perf_counter()-startTime
        except:
            return 0, "NULL",t.perf_counter()-startTime

    @staticmethod 
    def DecodeWithPylibdmtx(image:np.ndarray)->tuple[int,str,float]:
        '''Returns True if Pylibdmtx can find and decode matrix in image'''
        startTime=t.perf_counter()
        text=decodeWithPylibdmtx(MatrixReader.__ValidateImage(image))
        if text:
            return 1,f"'{''.join(text)}'",t.perf_counter()-startTime
        return 0,"NULL",t.perf_counter()-startTime

    @staticmethod
    def __ValidateImage(image:np.ndarray)->bool:
        """Returns image if of datatype numpy.ndarray"""
        if type(image)==np.ndarray:
            return image
        raise TypeError("Error: Parameter 'image' must be of datatype numpy.ndarray!")

    


