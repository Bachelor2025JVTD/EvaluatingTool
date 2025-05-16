import threading as th, logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class FtpServer():
    def __init__(self,storePath:str, username:str=None,password:str=None)->"FtpServer":

        if type(storePath)!=str:
            raise ValueError("Error: Parameter 'storePath' must be of datatype string!")
        elif type(username)!=str and username is not None:
            raise ValueError("Error: Parameter 'username' must be of datatype string!")
        elif type(password)!=str and password is not None:
            raise ValueError("Error: Parameter 'password' must be of datatype string!")

        self.username=username
        self.password=password
        self.path=storePath
        self.instServer=None
        self.ServerRunning=False
        self.ServerThread=None

    def StartServer(self)->None:
        '''Start server on a different thread'''
        if not self.ServerRunning:
            self.ServerThread=th.Thread(target=self.__RunServer,daemon=True)
            self.ServerThread.start()
            print("FTP-server starter...")
    
    def StopServer(self)->None:
        '''Stops server'''
        if self.ServerRunning:
            try:
                print("Closing FTP-server")
                self.instServer.close_when_done()
                self.ServerThread.join(timeout=1)
            except:
                print("Information: Server is already stopped!")   
        self.instServer    

    def __RunServer(self)->None:
        '''Starting server'''
        #Adding authorization
        auth = DummyAuthorizer()

        if self.username is not None and self.password is not None:
            auth.add_user(self.username, self.password, self.path, perm="elradfmw")#Give full access to this user
        auth.add_anonymous(self.path, perm="elradfmw") #Adding anonymous login

        #Setup FTP-handler
        handler = SilenFtpHandler
        handler.authorizer = auth

        try:
            logging.getLogger("pyftpdlib").setLevel(logging.CRITICAL+1)
            logging.getLogger("pyftpdlib").propagate = False
            
            self.instServer = FTPServer(("0.0.0.0", 21), handler)
            self.ServerRunning=True
            self.instServer.serve_forever()
        except:
            self.ServerRunning=False
            self.instServer.close_when_done() #Close server if error occures
            raise RuntimeError("Error: Could not start FTP server!") 
        

class SilenFtpHandler(FTPHandler):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_login(self, username):
        pass

    def on_login_failed(self, username, password):
        pass