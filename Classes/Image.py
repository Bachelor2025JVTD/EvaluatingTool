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
    def IsGreyscaled(image:np.ndarray)->bool:
        '''Check if image is correct dimentional'''
        Image.Check(image)
        if len(image.shape)>2:
            return False
        return True
    
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
    def Sharpness(image:np.ndarray)->float:
        """Returns sharpness and normalized sharpness"""
        Image.Check(image)
        sharpness=float(np.var(cv2.Laplacian(image,cv2.CV_64F)))
        return sharpness
    
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
    def Brightness(image:np.ndarray)->tuple[float,float,float]:
        """Returns minimum brightness, maximum brightness and average brightness"""
        Image.Check(image)
        return Image.LoBrightness(image),Image.HiBrightness(image), Image.AvgBrightness(image)
    
    @staticmethod
    def LoBrightness(image:np.ndarray)->float:
        '''Returns lowest pixel value in image'''
        Image.Check(image)
        return np.min(image)
    @staticmethod
    def HiBrightness(image:np.ndarray)->float:
        '''Returns highest pixel value in iamge'''
        Image.Check(image)
        return np.max(image)
    
    @staticmethod
    def AvgBrightness(image:np.ndarray)->float:
        '''Returns average pixel value in image'''
        Image.Check(image)
        return np.average(image)

    @staticmethod
    def QuitZoneContrast(image:np.ndarray, zoneWidth:int=20)->float:
        '''Returns contrast of quitzone'''
        Image.Check(image)
        h,w=image.shape

        if zoneWidth<=0 or zoneWidth>w or zoneWidth>h:
            raise ValueError("Error: Parameter zoneWidth must be greater than zero and equal or less than the image size! ")
        return float(Image.Contrast(image[0:h,0:zoneWidth])+Image.Contrast(image[0:h,w-zoneWidth:w])+Image.Contrast(image[0:zoneWidth,0:w])+Image.Contrast(image[h-zoneWidth:h,0:w]))/4.0
    
    @staticmethod
    def QuitZoneBrightness(image:np.ndarray,zoneWidth:int=20)->float:
        '''Returns brightness of quetizone'''
        Image.Check(image)
        h,w=image.shape

        if zoneWidth<=0 or zoneWidth>w or zoneWidth>h:
            raise ValueError("Error: Parameter zoneWidth must be greater than zero and equal or less than the image size! ")

        return float(Image.AvgBrightness(image[0:h,0:zoneWidth])+Image.AvgBrightness(image[0:h,w-zoneWidth:w])
                +Image.AvgBrightness(image[0:zoneWidth,0:w])+Image.AvgBrightness(image[h-zoneWidth:h,0:w]))/4.0

    @staticmethod
    def RMS(image:np.ndarray)->float:
        '''Returns RMS-value of image'''
        Image.Check(image)
        return np.sqrt(np.mean(np.square(image)))
    
    @staticmethod
    def StandardDeviation(image:np.ndarray)->float:
        '''Returns standard deviation of image'''
        Image.Check(image)
        return np.std(image)

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

