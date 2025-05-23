--DATABASE
USE master
GO
CREATE DATABASE BCHLR25
GO
USE BCHLR25
GO

CREATE TABLE CAMERA(
CameraId int,
CameraName varchar(30),
CONSTRAINT PK_CAMERA PRIMARY KEY (CameraId))
GO

CREATE TABLE LIGHT_CONFIGURATION(
LightId int ,
Brightness int,
Temperature int,
CONSTRAINT PK_LIGHT_CONFIGURATION PRIMARY KEY (LightId)
)
GO

CREATE TABLE TEST_DATA(
TestId int ,
MatrixType varchar(20) ,
MarkingType varchar(20) ,
SurfaceArea varchar(20) ,
MatrixText varchar(50), 
CONSTRAINT PK_TEST_DATA PRIMARY KEY (TestId),
)
GO


CREATE TABLE DOTPEEN_CONFIGURATION(
LayoutId int,
Depth int,
[Format] varchar(15),
Angle int,
DblRef varchar(5),
Spacing int,
CONSTRAINT PK_DOTPEEN_CONFIGURATION PRIMARY KEY(LayoutId)
)
GO

CREATE TABLE DOTPEEN_SETTING(
TestId int,
LayoutId int,
X int,
Y int,
W int,
H int,
CONSTRAINT PK_DOTPEEN PRIMARY KEY (TestId),
CONSTRAINT FK_DOTPEENSETTING_DOTPEENCONFIGURATION FOREIGN KEY (LayoutId) REFERENCES DOTPEEN_CONFIGURATION (LayoutId),
CONSTRAINT FK_DOTPEENSETTING_TESTDATA FOREIGN KEY(TestId) REFERENCES TEST_DATA(TestId)
)
GO

CREATE TABLE IMAGE_DATA(
TestId int,
JobId int,
LightId int,
PictureId int,
CameraId int,
ImageFiltered bit,
AveragePixelBrightness float,
PixelBrightnessVarians float,
Contrast float,
NormalizedSharpness float,
PyzbarText varchar(255) ,
Cv2Text varchar(255) ,
PylibText varchar(255) ,
QrText varchar(255) ,
IndustrialCameraResult int,
CONSTRAINT PK_IMAGE_DATA PRIMARY KEY (TestId,LightId,PictureId,CameraId,ImageFiltered),
CONSTRAINT FK_IMAGEDATA_CAMERA FOREIGN KEY (CameraId) REFERENCES CAMERA (CameraId),
CONSTRAINT FK_IMAGEDATA_LIGHTCONFIGURATION FOREIGN KEY (LightId) REFERENCES LIGHT_CONFIGURATION (LightId),
CONSTRAINT FK_IMAGEDATA_TESTDATA FOREIGN KEY (TestId) REFERENCES TEST_DATA (TestId)
)
GO


CREATE TABLE LASER_LOGO_BLOCK(
ProfileId int ,
Height int ,
[Compression] int,
Filling varchar(50) ,
AddingContour bit,
CONSTRAINT PK_LASER_LOGO_BLOCK PRIMARY KEY (ProfileId)
)
GO

CREATE TABLE LASER_MARKING_PROFILE(
ProfileId int ,
MarkingSpeed int,
MarkingFrequency int,
MarkingPower int,
NumberOfPasses int,
CONSTRAINT PK_LASER_MARKING_PROFILE PRIMARY KEY (ProfileId)
)
GO

CREATE TABLE LASER_QR_CODE_BLOCK(
ProfileId int ,
ErrorCorrectionLevel varchar(1) ,
Height int,
[Version] varchar(15),
Correction int,
ShapeOfElementaryCell varchar(15) ,
DisplayMode varchar(15) ,
QuietZone int,
CONSTRAINT PK_LASER_QR_CODE_BLOCK PRIMARY KEY (ProfileId)
)
GO

CREATE TABLE LASER_MARKING_PARAM(
TestId int ,
PreLasingMirrorStabilisationDelay int,
ActualLasingDelay int,
DelayBetweenTwoContigousVectors int,
EndVectorMirrorStablisationDelay int,
ActualEndLasingDelay int,
ProfileId int,
LogoBlockId int,
LogoBlockMarkingProfile int,
QrBlockId int,
QrBlockMarkingProfile int,
CONSTRAINT PK_LASER_MARKING_PARAM PRIMARY KEY (TestId),
CONSTRAINT FK_LASERMARKINGPARAM_LASERLOGOBLOCK FOREIGN KEY (LogoBlockId) REFERENCES LASER_LOGO_BLOCK(ProfileId),
CONSTRAINT FK_LASERMARKINGPARAM_LASERQRCODEBLOCK FOREIGN KEY (QrBlockId) REFERENCES LASER_QR_CODE_BLOCK(ProfileId),
CONSTRAINT FK_LASERMARKINGPARAM_LASERMARKINGPROFILE FOREIGN KEY (ProfileId) REFERENCES LASER_MARKING_PROFILE(ProfileId),
CONSTRAINT FK_LASERMARKINGPARAM_LASERMARKINGPROFILE_QRBLOCK FOREIGN KEY (QrBlockMarkingProfile) REFERENCES LASER_MARKING_PROFILE(ProfileId),
CONSTRAINT FK_LASERMARKINGPARAM_LASERMARKINGPROFILE_LOGOBLOCK FOREIGN KEY (LogoBlockMarkingProfile) REFERENCES LASER_MARKING_PROFILE(ProfileId),
CONSTRAINT FK_LASERMARKINGPARAM_TESTDATA FOREIGN KEY(TestId) REFERENCES TEST_DATA (testId)
)
GO

CREATE PROCEDURE udpDeleteRecord @testId int AS 
BEGIN
	IF (@testId>=0) AND EXISTS(SELECT * FROM IMAGE_DATA WHERE TestId=@testId) BEGIN	
		--DELETE FROM TABLE
		DELETE FROM IMAGE_DATA WHERE TestId=@testId
	END	
END
GO


--CHECK IF TEST ID ALREADY EXISTS IN DATABASE
CREATE PROCEDURE udpCheckTestId @testId int, @status int OUT AS BEGIN

	IF @testId<0 or NOT EXISTS (SELECT TOP(1)* FROM TEST_DATA WHERE TestId=@testId) BEGIN
		--TEST ID NOT ALLOWED
		SET	@status=3
	END 
	ELSE IF EXISTS (SELECT TOP(1)* FROM IMAGE_DATA WHERE TestId=@testId) 
	BEGIN
		--TEST ID ALREADY EXISTS
		SET @status=1
	END
	ELSE
	BEGIN 
	--TEST ID OK!
		SET @status=2
	END 
END
GO



