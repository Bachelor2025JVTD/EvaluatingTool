import queue,numpy as np, threading as th,os,cv2
from Classes import Image, MatrixReader as qr, configReader as cr, Database
databaseQueue=queue.Queue()
writeQueue=queue.Queue()
imageQueue=queue.Queue()
cnfg=cr.ConfigReader(r"C:\Users\vetle\Desktop\BCHLR25_V3\Utilities\config.json")
__image=Image.Image()
roi=None

IMAGE_NOT_FILTERED=POS_IMAGE=POS_DATA=IMAGE_NOT_ROIED=0
IMAGE_FILTERED=POS_LIGHTID=SET_IMAGE_ROIED=1
POS_TESTID=2
POS_CAMERAID=3
POS_JOBID=4
TIMEOUT_5S=POS_PICTUREID=5
POS_FILTERED_STATE=6
POS_INDUSTRIAL_CAMERA_RESULT=7
POS_USED_TRESHOLD=8
POS_ROI=9
POS_STATUS_ROI=10

stopEvent=th.Event()

__lockAnalyze=th.Lock()
__lockDecodePyzbarAndCv2=th.Lock()
__lockDecodeQReader=th.Lock()
__lockDecodedPylib=th.Lock()

__threadAnalyze=None
__threadDecodePyzbarAndCv2=None
__threadDecodeQReader=None
__threadDecodePylib=None

__queryAnalyze=None
__queryDecodePyzbarAndCv2=None
__queryDecodedQReader=None
__queryDecodePylib=None

def __WriteImages():
    while True:
        queue=writeQueue.get()
        if queue is None and stopEvent.isSet():
            break
        elif queue is None:
            continue


        #PROGRAM: ADD FOLDER STRUCTURE FOR FILTERED/NOT FILTERED
        if queue[POS_FILTERED_STATE]:
            path=os.path.join(cnfg.Read("STR_BSE_PATH"),"Filtered")
        else:
            path=os.path.join(cnfg.Read("STR_BSE_PATH"),"NonFilter")

        #PROGRAM: ADD FOLDER STRUCTURE FOR WEBCAMERA/INDUSTRIAL CAMERA
        if cnfg.Read("WEB_CMR_ID")==queue[POS_CAMERAID]:
            path=os.path.join(path,"WebCamera")
        elif cnfg.Read("IND_CMR_ID")==queue[POS_CAMERAID]:
            path=os.path.join(path,"IndustrialCamera")
        else:
            raise ValueError("Error: CameraId is not configuration in config file!")
        
        #PROGRAM: ADD FOLDER STRUCTURE FOR ORIGINAL IMAGES
        if queue[POS_STATUS_ROI] == IMAGE_NOT_ROIED:
            path=os.path.join(path,"Original")
        
        #CONTROL FILEPATH
        if not os.path.exists(path):
            raise FileExistsError("Error: Constructed filepath does not exists!")
        
        #CONSTRUCT FILENAME
        fileName=f"""{str(queue[POS_TESTID]).zfill(3)}_{Convert(queue[POS_JOBID])}_{Convert(queue[POS_INDUSTRIAL_CAMERA_RESULT])}_{Convert(queue[POS_LIGHTID])}_{Convert(queue[POS_PICTUREID])}_{Convert(queue[POS_CAMERAID])}.bmp"""
        cv2.imwrite(os.path.join(path,fileName),queue[POS_IMAGE])

def DatabaseThread():
    with Database.Database(cnfg.Read("CONNECTIONSTRING"),cnfg.Read("DBNAME"),cnfg.Read("USRNM"),cnfg.Read("PSWRD")) as db:
        while True:
            query=databaseQueue.get()
            if query is None and stopEvent.isSet():
                break
            elif query is None:
                continue

            db.Query(query)

__threadDatabase=th.Thread(target=DatabaseThread, daemon=True, name="Database thread")
__threadWrite=th.Thread(target=__WriteImages, daemon=True, name="Writer thread")

def __StarterThread():
    while True:
        #Get image from queue
        queue=imageQueue.get()

        #Check for stop stignal on thread
        if queue is None and stopEvent.is_set():
            databaseQueue.put(None)
            writeQueue.put(None)
            __threadDatabase.join()
            __threadAnalyze.join()
            __threadWrite.join()
            break
        elif queue is None:
            continue

        #PROGRAM: ADD IMAGE TO WRITE QUEUE
        
        writeQueue.put(queue.copy())
        CheckThread(__threadWrite)

        #ROI image
        if queue[POS_STATUS_ROI]==IMAGE_NOT_ROIED:
            queue[POS_IMAGE]=Image.Image.RoiImage(queue[POS_IMAGE],*queue[POS_ROI])
            queue[POS_STATUS_ROI]=SET_IMAGE_ROIED
            writeQueue.put(queue)

        #CREATE/UPDATE THREADS
        __threadAnalyze=th.Thread(target=__AnalyzeThread,args=(queue,), daemon=True, name="Analyzing of image")
        __threadDecodePyzbarAndCv2=th.Thread(target=__DecodePyzbarAndCv2,args=(queue[POS_IMAGE],), daemon=True, name="Decoding with Pyzbar and Cv2")
        __threadDecodeQReader=th.Thread(target=__DecodeQReader,args=(queue[POS_IMAGE],), daemon=True, name="Decoded with QReader")
        __threadDecodePylib=th.Thread(target=__DecodePylib,args=(queue[POS_IMAGE],), daemon=True, name="Decoded with Pylib")

        #START THREADS
        __threadAnalyze.start()
        __threadDecodePyzbarAndCv2.start()
        __threadDecodeQReader.start()
        __threadDecodePylib.start()

        #PROGRAM: ADD FILTERED IMAGE TO QUEU
        if bool(queue[POS_FILTERED_STATE])==IMAGE_NOT_FILTERED:
            temp=queue.copy()
            temp[POS_FILTERED_STATE]=IMAGE_FILTERED
            temp[POS_IMAGE],temp[POS_USED_TRESHOLD]=__image.Filtrate(queue[POS_IMAGE])
            imageQueue.put(temp)

        #WAIT THREADS DONE
        __threadAnalyze.join()
        __threadDecodePyzbarAndCv2.join()
        __threadDecodeQReader.join()
        __threadDecodePylib.join()

        #COMBINE QUERIES  
        query=f"""INSERT INTO {cnfg.Read("DB_TABLE_NAME")} VALUES(
                                {__queryAnalyze},{__queryDecodePyzbarAndCv2},{__queryDecodePylib},{__queryDecodedQReader},{queue[POS_INDUSTRIAL_CAMERA_RESULT]})"""
        databaseQueue.put(query)
        CheckThread(__threadDatabase)

def __DecodePyzbarAndCv2(image:np.ndarray):
    global __queryDecodePyzbarAndCv2
    stateCv2,textCv2,timeCv2=qr.MatrixReader.DecodeWithCv2QrReader(image)
    statePyzbar,textPyzbar,timePyzbar=qr.MatrixReader.DecodeWithPyzbar(image)

    with __lockDecodePyzbarAndCv2:
        __queryDecodePyzbarAndCv2=f"{textPyzbar},{textCv2}"

def __DecodePylib(image:np.ndarray):
    global __queryDecodePylib
    statePylib,textPylib,timePylib=qr.MatrixReader.DecodeWithPylibdmtx(image)
    with __lockDecodedPylib:
        __queryDecodePylib=f"{textPylib}"

def __DecodeQReader(image:np.ndarray):
    global __queryDecodedQReader
    stateQReader,textQReader,timeQReader=qr.MatrixReader.DecodeWithQReader(image)
    with __lockDecodeQReader:
        __queryDecodedQReader=f"{textQReader}"

def __AnalyzeThread(queue):
    global __queryAnalyze
    image=queue[POS_IMAGE]
    with __lockAnalyze:
        __queryAnalyze=f"""{queue[POS_TESTID]},{queue[POS_JOBID]},{queue[POS_LIGHTID]},{queue[POS_PICTUREID]},{queue[POS_CAMERAID]},{queue[POS_FILTERED_STATE]},
                            {__image.AvgBrightness(image)},{__image.BrightnessVarians(image)},{__image.Contrast(image)},{__image.NormalizedSharpness(image)}"""

def CheckThread(thread:th.Thread):
    if thread is None:
        raise ValueError("Error: Thread is None!")
    elif thread.is_alive():
        return
    thread.start()

def Convert(value:str)->str:
    if value=="NULL":
        return "0"
    else:
        return value

threads=th.Thread(target=__StarterThread, daemon=True, name="Controller thread")

