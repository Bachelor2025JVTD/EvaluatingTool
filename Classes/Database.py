import pyodbc as db
#Database klasse
class Database:
    """
    Database class to execute queries with MSSQL-databases. Defoult connection is already configured!
    """
    def __init__(self, serverName:str="LAPTOP\SQLEXPRESS", databaseName:str="BCHLR2025", username:str="plsadmin", password:str="123456")->"Database":
        '''Creates an class of Database'''
        self.servername=serverName
        self.databasename=databaseName
        self.username=username
        self.password=password
        self.conn=None
        self.connectionOk=False
    
    def __enter__(self)->"Database":
         return self
    
    def __exit__(self, exc_type, exc_val, exc_tb)->None:
         self.CloseConnection()
         if exc_type:
            print(f"Error with class 'Image': {exc_type.__name__} - {exc_val}")
         return False  #Stops program if fault
        
  
    def Connect(self)->None:
        '''Creates connection with database'''
        try:
              self.conn = db.connect(
                f"DRIVER={{SQL Server}};"
                f"SERVER={self.servername};"
                f"DATABASE={self.databasename};"
                f"UID={self.username};"
                f"PWD={self.password};")
              self.connectionOk=True
        except:
            raise ConnectionError("Error: Control connection with database!")
        
    def CloseConnection(self)->bool:
        '''Terminates connection with database'''
        if self.connectionOk:
            try:
                self.conn.close()
                self.connectionOk=False
                return True
            except:
                 self.connectionOk=False
                 return False
        
    def Query(self, query:str,params:tuple=None,returnValue:bool=False, commit:bool=True)->tuple:
                '''Executes query to database, parameters can be added by using "?" and the values as an array or list in the input argument "params"'''
                data=None
                try:
                    self.Connect()
                    cursor=self.conn.cursor()

                    if params is None:
                        cursor.execute(query)
                    else:
                         cursor.execute(query,params)
                    
                    if returnValue:
                        data=cursor.fetchall()

                    if commit:
                        self.conn.commit()
                         
                except Exception as err:
                     print(f"ERROR DB: {err}")
                     if self.connectionOk:
                        raise ValueError("Error: An error with query!")
                     else:
                        raise ConnectionRefusedError("Error: An error occured during execution of query!")
                finally:
                     self.CloseConnection()
                     return data


