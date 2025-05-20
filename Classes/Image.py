import numpy as np, copy,cv2


class Image:
    @staticmethod
    def RoiImage(image:np.ndarray,startX:int,startY:int,width:int,height:int)->np.ndarray:
        '''Set ROI in image with parameters'''
        Image.Check(image)
        w,h=image.shape
        if startX<0 or startY<0 or width<0 or height<0:
            raise ValueError("Error: All input arguments must be greater than zero and insde the image limitation shape!")
        return copy.copy(image[startY:startY+height, startX:startX+width])
    
    @staticmethod
    def Check(image:np.ndarray)->Exception:
         '''Check that image is of type nump.ndarray and correct dimension'''
         if Image.__IsImage(image) or len(image.shape)>2:
            raise ValueError("Error: Image is not greyscaled!")
         
    @staticmethod
    def Grayscale(image:np.ndarray)->np.ndarray:
        if len(image.shape)>2:
            return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError("Error: Image is already greyscaled!") 
    
    @staticmethod
    def __IsImage(image:np.ndarray)->bool:
        '''Check if image is of type numpy.ndarray'''
        if type(image)!=np.ndarray:
            raise ValueError("Error: Image is not of datatype numpy.ndarray!")
        
    @staticmethod
    def Filtrate(image:np.ndarray,kernel:int=5)->tuple[np.ndarray,float]:
        """Generates filtered version of image"""
        Image.Check(image)
        w,h=image.shape
        if kernel<=0 or kernel>w or kernel>h:
            raise ValueError("Error: Parameter zoneWidth must be greater than zero and equal or less than the image size! ")

        img = cv2.GaussianBlur(image, (kernel, kernel), 0)  #Filtrate disturbance
        img = cv2.equalizeHist(img)  #Create better contrast
        usedTreshold, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Filtrate image to be black and white pixels only
        return img, usedTreshold
    
    @staticmethod
    def NormalizedSharpness(image:np.ndarray)->float:
        """Returns normalized sharpness"""
        Image.Check(image)
        sharpness=float(np.var(cv2.Laplacian(image,cv2.CV_64F)))
        return sharpness/image.size

    @staticmethod
    def Contrast(image:np.ndarray,kernelSize:float=0.02)->float:
        """Retunrs contrast"""
        if kernelSize<=0.0 or kernelSize>1.0:
            raise ValueError("Error: Kernel must be greater than zero and equal or less than one!")

        Image.Check(image)
        sortedImage=np.sort(image.flatten())
        nbrElements=int(np.round(sortedImage.size*kernelSize))
        #Arrays
        darkestPixels=sortedImage[:nbrElements]
        brightestPixels=sortedImage[-nbrElements:]
        return float(np.average(brightestPixels)-np.average(darkestPixels))
    
    @staticmethod
    def AvgBrightness(image:np.ndarray)->float:
        '''Returns average pixel value in image'''
        Image.Check(image)
        return np.average(image)

    @staticmethod
    def BrightnessVarians(image:np.ndarray)->float:
        '''Returns varians of image brightness'''
        Image.Check(image)
        return np.var(image)

    @staticmethod
    def SelectRoi(image:np.ndarray)->tuple[tuple[int,int,int,int],float]:
        '''Select ROI in image manually with GUI'''
        roi=cv2.selectROI("Select ROI", image)
        roiedSharpnessReference=np.var(cv2.Laplacian(image,cv2.CV_64F))
        cv2.destroyAllWindows()
        return roi, roiedSharpnessReference

