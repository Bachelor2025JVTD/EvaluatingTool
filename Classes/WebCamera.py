from Classes import Camera as c
import cv2, numpy as np, time as t


class WebCamera(c.Camera):
    def __init__(self, portIndex:int=0)->"WebCamera":
        '''Creates an instance of class "WebCamera"'''
        if type(portIndex)!=int or portIndex<0:
            raise TypeError("Error: Parameter 'portIndex' must be of datatype int and greater than 0.")
        
        self.index=portIndex 
        self.cap=None
        self.focusTimeout=3
        self.focusStableTime=1

    def __enter__(self)->"WebCamera":
        return self
    
    def __exit__(self, exc_type, exc_val, traceback):
        self.__CloseCap()

        if exc_type:
            print(f"Error with class 'Image': {exc_type.__name__} - {exc_val}")
        return False  #Stops program if fault
    
    def CaptureImage(self,sharpnessReference:int=0,maxRetrys:int=3)->np.ndarray:
        "Take an image and returns an image"
        bestImage=None
        bestSharpness=0.0

        for take in range(0,maxRetrys):
            if self.__OpenCap():
                image,sharpness,imageFail=self.__Focus(self.focusTimeout,self.focusStableTime,sharpnessReference)

                if imageFail:
                    if sharpness>bestSharpness:
                        bestImage=image
                    continue
                else:
                    bestImage=image
                    break
        return bestImage

    def CalibrateImage(self)->np.ndarray:
        "Take picture and then ROI, returns ROIed image"
        if self.__OpenCap():
            print("Press 'n' to reopen camera or any other key to countinou...")
            while True:
                capOk,img=self.cap.read()

                if not capOk:
                    continue
                else:
                    cv2.imshow("Live view webcamera",c.Camera._AddCrossToImage(img))
                    key=cv2.waitKey(1)

                    if key==ord('n'):
                        print("Reopening camera...")
                        self.__CloseCap()
                        t.sleep(1)
                        self.__OpenCap()
                        print("Press 'n' to reopen camera or any other key to countinou...")
                    elif key!=-1:
                        self.__CloseCap()
                        cv2.destroyAllWindows()
                        return img

    def __Focus(self,timeout:int, focusOkTime:int, focusLimit:float=100.0)->tuple[np.ndarray,float,bool]:
        '''Waits for camerea to focus, returns best image, sharpness and True if error'''
        if not(type(timeout)==int or type(timeout)==float) or timeout<=0:
            raise ValueError("Error: Parameter 'timeout' must be of datatype int or float and greater than 0!")
        elif  not (type(focusOkTime)==int or type(focusOkTime)==float) or focusOkTime<=0:
            raise ValueError("Error: Parameter 'focusOkTime' must be of datatype int or float and greater than 0!")
        
        ERROR=True
        sharpnessOk=PASS=False
        startTime=t.time()
        focusLimit=focusLimit*1
        bestSharpness=0
        bestImage=None

        while True: 
            capOk, img=self.cap.read() #Read picture from camera

            if capOk and img is not None: #Controls image is good to prevent program to crash
                sharpness=np.var(cv2.Laplacian(self.__GrayScaleImage(img),cv2.CV_64F))

            if sharpness>=focusLimit and not sharpnessOk: #Raising edge on good sharpness
                sharpnessOk=True
                sharpnessOkTime=t.time()

            #Store best image
            if sharpness>bestSharpness:
                bestSharpness=sharpness
                bestImage=img

            elif sharpnessOk and ((t.time()-sharpnessOkTime)>focusOkTime): #Picture is valid
                self.__CloseCap()
                return bestImage,bestSharpness, PASS
            elif sharpness<focusLimit and sharpnessOk: #Negative edge of camera
                sharpnessOk=False     
            elif (t.time()-startTime)>timeout: #Timeout
                self.__CloseCap()
                return bestImage,bestSharpness, ERROR
            
    @staticmethod
    def __GrayScaleImage(image:np.ndarray)->np.ndarray:
        """Grayscal image"""
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    def __OpenCap(self)->bool:
        '''Open cap'''
        for i in range(3):
            self.cap=cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1920)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080)
            if self.cap.isOpened():
                return True
            else:
                print("Warning: Could not open camera, retrying...")
                self.cap=None
                t.sleep(0.5)
        raise IndexError("Error: Could not open communication with web-camera!")

    def __CloseCap(self)->bool:
        '''Closes cap'''
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
                
        self.cap=None
        return True
            
   
                            
                        

                        
                    
                


