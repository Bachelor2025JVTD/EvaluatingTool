from Classes import Camera
import ipaddress, socket as s, numpy as np,os, cv2, time as t


class IndustrialCamera(Camera.Camera):

    def __init__(self, ipAdress:str, portSend:int, portListen:int,basePath:str, timeout=20)->"IndustrialCamera":
        '''Creates an instance of class "IndustrialCamera'"'''
        try:
            addr=ipaddress.ip_address(ipAdress)
            self.ip=ipAdress
        except:
            raise TypeError("Error: Parameter 'ipAddress' must be of datatype string!")
        
        if type(portSend)!=int and portSend<=0:
            raise TypeError("Error: Parameter 'portSend' must be of datatype int and higher than 0.")
        elif type(timeout)!=int and timeout<0:
            raise TypeError("Error: Parameter 'Timeout' must be of datatype int and higher or equal to 0.")
        elif not os.path.exists(basePath):
            raise FileExistsError(f"Error: Could not find path: {basePath}!")
        if type(portListen)!=int and portListen<=0:
            raise TypeError("Error: Parameter 'portListen' must be of datatype int and higher than 0.")
        
        self.basePath=basePath
        self.timeout=timeout
        self.portSend=portSend
        self.portListen=portListen

    def __enter__(self)->"IndustrialCamera":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb)->None:
        pass

    def ChangeJob(self, jobId:int)->bool:
        '''Changes solution on P+F camera. Returns True if solution change completed succesfully'''
        if type(jobId)!=str and type(jobId)!=int:
            raise ValueError("Error: Parameter 'jobId' must be of datatype int or string!")
        
        retryCounter=0
        while True:
            try:
                self.portSend=5021
                self.timeOut=30
                _=self.__TcpIpRequest(f"ss 0{str(jobId)}\n\r")
                return True
            except Exception as err:
                retryCounter+=1

                if retryCounter>3:
                    raise ConnectionError("Error: Could not change camera job!")
                    
    def CaptureImage(self)->tuple[np.ndarray, int]:
        """Trigger P+F camera with TCP/IP communication. Returns job result"""
        self.portSend=5024
        self.portListen=5025
        data=self.__TcpIpRequest("T2\n\r",reciveSize=1024)
        t.sleep(2)
        imageName=self.__GetLatestImageName()
        image=cv2.imread(imageName)
        os.remove(imageName)
        return image,data

    def CalibrateImage(self)->np.ndarray:
        '''Shows image to calibrate before starting tasks'''
        while True:
            image,_=self.CaptureImage()
            cv2.imshow("Industrial camera view",image)
            print("Press 'n' to retake image or any other key to countinue...")

            while True:
                key=cv2.waitKey(1)

                if key==ord('n'):
                    print("Reshoot image...")
                    cv2.destroyAllWindows()
                    break
                elif key!=-1:
                    cv2.destroyAllWindows()
                    return image
    
    def __TcpIpRequest(self, command:str,reciveSize:int=0)->str:
        '''Sends command over TCP/IP and returns response'''
        seqState="Connecting"

        if command is not None and command!="" and type(command)==str:
            #Create socket
            with s.socket(s.AF_INET,s.SOCK_STREAM) as inst:
                try:
                    self.__ConnectToPartner(inst,self.ip,self.portSend)
                        
                    inst.sendall(str(command).encode()) #Send command
                    seqState="Command OK"

                    if self.timeout>0:
                        inst.settimeout(self.timeout)

                    #Wait for result
                    if reciveSize>0 and self.portListen==self.portSend:
                        return inst.recv(reciveSize).decode().strip()
                    elif reciveSize>0 and self.portListen!=self.portSend:
                         return self.__ListenSocket(self.ip,self.portListen)
                except:
                    #Error hanling      
                    if seqState=="Command OK":
                        raise ValueError("Error: Could not decode recived data!")
                    raise ConnectionRefusedError("Error: Something wrong with command!")
        else:
            raise IndexError("Error: Parameter 'command' can`t be None and must be of datatype string!")
        
    def __GetLatestImageName(self)->str:
        '''Retunrs latest edited file from basepath'''
        files=os.listdir(self.basePath)
        filePaths=[os.path.join(self.basePath,file) for file in files]
        return max(filePaths, key=os.path.getmtime)
    
    @staticmethod
    def __ConnectToPartner(socket:s.socket,ip:int,port:int)->str:
        '''Connects to partner'''
        for retryCounter in range(5):
            try:
                socket.connect((ip,port))
                return None
            except:
                t.sleep(1)
        raise ConnectionError("Error: Error during connection to camera!")

    def __ListenSocket(self,ip:int, port:int,reciveBuffer:int=1024)->str:
        '''Listen to desired socket'''
        with s.socket(s.AF_INET,s.SOCK_STREAM) as listenSocket:
            try:
                listenSocket.connect((ip,port))
                listenSocket.settimeout(self.timeout)
                return listenSocket.recvfrom(reciveBuffer)[0].decode().strip()
            except Exception as err:
                print(err)














