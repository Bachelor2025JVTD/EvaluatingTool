from abc import abstractmethod
import numpy as np,cv2

class Camera():

    @staticmethod
    def _AddCrossToImage(image:np.ndarray)->np.ndarray:
        '''Adds cross in the center of image'''
        imgTemp=image.copy()
        h,w=imgTemp.shape[:2]
        center= (w // 2, h // 2)

        cv2.line(imgTemp, (0, center[1]), (w, center[1]), (0, 0, 255), thickness=1)
        cv2.line(imgTemp, (center[0], 0), (center[0], h), (0, 0, 255), thickness=1)
        return imgTemp

    @abstractmethod
    def CaptureImage(self,sharpnessReference:int=0)->np.ndarray:
        '''Capturing images'''
        pass

    @abstractmethod
    def CalibrateImage(self)->np.ndarray:
        '''Methode to adjust parts before starting test'''
        pass

    
    
    

