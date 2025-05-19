import threading as th,os
from Classes import Lightbulb as lb, Database as db, configReader as cr

cnfg=cr.ConfigReader(r"C:\Users\vetle\Desktop\BCHLR JCDT25\Utilities\config.json")

EXIT_PROGRAM= TESTID_ALREADY_EXISTS= UNVALID_TESTID=False
CONTINUE_PROGRAM=True
RETURN_NO_ID=-1
POS_PERCENTAGE=LOW_LIMIT_TESTID=0
POS_COLORTEMP=1
TESTID_OK=2
KEY_DELETE='y'
KEY_ENTER_NEW_TESTID='n'

DB_ADDR=cnfg.Read("CONNECTIONSTRING")
DB_DTBS=cnfg.Read("DBNAME")
DB_USRNM=cnfg.Read("USRNM")
DB_PSWRD=cnfg.Read("PSWRD")
UDP_DELETETESTID=cnfg.Read("DLT_TESTID")
UDP_CHECKTESTID=cnfg.Read("CHCK_TESTID")

def Log(message:str,level="USER"):
    levels={"INFO": "[INFO]",
        "WARNING": "[WARNING]",
        "ERROR": "[ERROR]",
        "DEBUG": "[DEBUG]",
        "USER":"[USER]",
        "MSG":"[MESSAGE]"}
    print(f"{levels[level]} {message}")

def EnterTestId()->tuple[int,bool]:
    while True:
        Log("ENTER TESTID...")
        Log("Press 'q' to exit!")
        id=__TryConvertInt(input())
        match id:
            case x if isinstance(x,int) and x>LOW_LIMIT_TESTID:
                #Check if testId is valid
                if __CheckTestId(id)==TESTID_OK:
                    os.system("cls")
                    return id,CONTINUE_PROGRAM
                    
                else:
                    Log("TestId is already in use, do you want to delete? [y/n]")
                    key=input().lower()
                    if key==KEY_DELETE:
                        __DeleteTestId(id)
                        os.system("cls")
                        return id, CONTINUE_PROGRAM
                    else:
                        continue
                
            case x if isinstance(x,str) and x.lower()=='q':
                return RETURN_NO_ID,EXIT_PROGRAM
            
            case _:
                Log("You must enter a valid ID!")
                continue 

def SetLighting(lightjob:int, testId:int, lightId:int):
    '''Changes lightsettings'''
    bulb1=lb.LightBulb(cnfg.Read("BLB1_ADDR"))
    bulb2=lb.LightBulb(cnfg.Read("BLB2_ADDR"))

    taskBulb1=th.Thread(target=bulb1.SetLight, args=(lightjob[POS_PERCENTAGE],lightjob[POS_COLORTEMP]))
    taskBulb2=th.Thread(target=bulb2.SetLight, args=(lightjob[POS_PERCENTAGE],lightjob[POS_COLORTEMP]))

    taskBulb1.start()
    taskBulb2.start()

    taskBulb1.join()
    taskBulb2.join()

def __DeleteTestId(testId:int):
    query = f"""
    EXEC {UDP_DELETETESTID} @testId={testId};
    """
    with db.Database(DB_ADDR,DB_DTBS,DB_USRNM,DB_PSWRD) as inst:
        data=inst.Query(query)

def __CheckTestId(testId:int)->int:
    '''Executes udpCheckTestId in MSSQL database'''
    query = f"""
    DECLARE @status INT;
    EXEC {UDP_CHECKTESTID} @testId = ?, @status = @status OUTPUT;
    SELECT @status AS status;
    """
    with db.Database(DB_ADDR,DB_DTBS,DB_USRNM,DB_PSWRD) as inst:
        data=inst.Query(query,testId,True,False)
        return data[0][0]

def __TryConvertInt(number:str):
    try:
        return int(number)
    except:
        return number

def StartThread(thread:th.Thread, waitThread:bool=False):
    while waitThread and thread.is_alive():
        pass
    
    if not thread.is_alive():
        thread.start()




