from Classes import IndustrialCamera as ic, WebCamera as wc, FtpServer as ftp, Image,Lightbulb as bulb
from Utilities import util as u
import os, analyzeThread as at, time as t

#Variabels
IMAGE_NOT_FILTERED=NO_JOBID=IMAGE_NOT_ROIED=0
START_PICTUREID=1
POS_LIGHTID='id'
NO_INDUSTRIAL_CAMERA_RESULT=NO_TRESHOLD="NULL"

os.system("cls")
u.Log("PROGRAM STARTING","INFO")
ftpInstanse=ftp.FtpServer(u.cnfg.Read("BASE_PATH_FTP"),u.cnfg.Read("USRNM_FTP"),u.cnfg.Read("PSWRD_FTP"))

while True:
    #PROGRAM UIF: ENTER TESTID OR EXIT PROGRAM
    testId, continueProgram=u.EnterTestId()

    #PROGRAM: EXIT
    if not continueProgram:
        u.Log("Stopping program...","INFO")
    
        if at.threads.is_alive():
            at.stopEvent.set()
            at.imageQueue.put(None)
            u.Log("Waiting on threads...","INFO")
            at.threads.join()
        u.Log("Program end...","INFO")
        break
    
    #PROGRAM: PEPPERL+FUCHS SEQUENCE IF ENABLED
    if u.cnfg.Read("ENBL_IND_CMR"):

        #PROGRAM: START SERVER
        if not ftpInstanse.ServerRunning:
            ftpInstanse.StartServer()
        
        with ic.IndustrialCamera(u.cnfg.Read("IND_CMR_ADDR"),u.cnfg.Read("IND_CMR_PRT_SND"),u.cnfg.Read("IND_CMR_PRT_RCV"),u.cnfg.Read("BASE_PATH_FTP"),u.cnfg.Read("IND_CMR_TIMEOUT")) as camera:
            ROI,sharpnessRefernce=Image.Image.SelectRoi(camera.CalibrateImage())

            for lightjob in u.cnfg.Read("LIGHT_JOBS"):
                #PROGRAM: CHANGE LIGHT SETTING
                bulb.LightBulb.SetLight(u.cnfg.Read("BLB1_ADDR"),lightjob['brightness'],lightjob['temperature'])
                #bulb.LightBulb.SetLight(u.cnfg.Read("BLB2_ADDR"),lightjob['brightness'],lightjob['temperature'])

                for take in range(START_PICTUREID,u.cnfg.Read("IND_CMR_REDUNTATNT_IMAGES")+1):
                    _=camera.ChangeJob(take)
                    t.sleep(1)
                    image,result=camera.CaptureImage()
                    image=Image.Image.Grayscale(image)
                    
                    at.imageQueue.put([image,lightjob[POS_LIGHTID],testId,u.cnfg.Read("IND_CMR_ID"),take,take,
                                       IMAGE_NOT_FILTERED,result,NO_TRESHOLD,ROI,IMAGE_NOT_ROIED])
                    u.StartThread(at.threads)
    
    #PROGRAM: WEBCAMERA SEQUENCE IF ENABLED
    if u.cnfg.Read("ENBL_WEB_CMR"):
        sharpnessRefernce=None
        for lightjob in u.cnfg.Read("LIGHT_JOBS"):
            #PROGRAM CHANGE SETTING
            bulb.LightBulb.SetLight(u.cnfg.Read("BLB1_ADDR"),lightjob['brightness'],lightjob['temperature'])
            #bulb.LightBulb.SetLight(u.cnfg.Read("BLB2_ADDR"),lightjob['brightness'],lightjob['temperature'])
        
            #PROGRAM: START CAPTURE IMAGE SEQUENCE
            with wc.WebCamera(u.cnfg.Read("CAP_INDX")) as camera:
                if sharpnessRefernce is None:
                    ROI, sharpnessRefernce=Image.Image.SelectRoi(Image.Image.Grayscale(camera.CalibrateImage()))
                for take in range(START_PICTUREID,u.cnfg.Read("WEB_CMR_REDUNTANT_IMAGES")+1):
                    image=Image.Image.Grayscale(camera.CaptureImage(sharpnessRefernce))
                    #Image,lightId,testId,cameraId,jobId,filtered, industrial camera result
                    at.imageQueue.put([image,lightjob[POS_LIGHTID],testId,u.cnfg.Read("WEB_CMR_ID"),NO_JOBID,take,
                                       IMAGE_NOT_FILTERED,NO_INDUSTRIAL_CAMERA_RESULT,NO_TRESHOLD,ROI,IMAGE_NOT_ROIED])
                    u.StartThread(at.threads)

                    
                    











        

        






