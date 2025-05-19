
# IMAGE EVALUATING TOOL

The Python script is used to evaluate the readability of a 2D-barcode in an image.







## Installation

Install EvaluatingTool with pip:

```bash
  git clone https://github.com/Bachelor2025JVTD/EvaluatingTool.git
  cd EvaluatingTool
```

Install requirements with pip:
```bash
  pip install -r requirements.txt
```
    
## Configuration

The hardware devices used:
- Pepperl + Fuchs VOS2000-F226R-8MM-S
- Logitech Carl Zeiss HD c930e 1080p
- 2pcs Shelly DUO smart Wi-Fi LED-Light

### Hardware configuration
#### Pepperl + Fuchs VOS2000-F226R-8MM-S
For detailed information about the camera configuration and jobs see [camera folder](https://github.com/Bachelor2025JVTD/EvaluatingTool/tree/main/Utilities/P%2BF%20Camera)
- Set IP-address.
- Create "solutions" and save to camera.
- Create script to save images to the FTP-server.

#### Logitech Carl Zeiss HD c930e 1080p

- Find correct cap-index for the camera.

#### Shelly DUO smart Wi-Fi LED-Light
Connect to the local web-API to configure the lightbulbs.
- Set IP-address through GUI available at 192.168.33.1.

![DUO smart Wi-Fi LED light confiuration.png](https://github.com/Bachelor2025JVTD/EvaluatingTool/blob/main/Utilities/Images/ShellyDueConfiguration.png)



### Software configuration
#### Folderstructure
The give folderstructure must be implemented with correct syntax to be able to save the images.

```bash

        Images/
            ├── Filtered/
            │   ├── WebCamera/
            │   └── IndustrialCamera/
            └── NonFilter/
            ├── WebCamera/
            │   └── Original/
            └── IndustrialCamera/
                └── Original/
```

#### Configuration file
All settings to be changed are set in config.json file.

- Set "STR_BSE_PATH" to the folder "Images".
- Set "IND_CMR_ADDR" to the IP-adress to Pepperl + Fuchs VOS2000-F226R-8MM-S.
- Set "CAP_INDX" to the cap index of Logitech Carl Zeiss HD c930e 1080p.
- Set "BASE_PATH_FTP" to an empty folder. 
- Set "BLB1_ADDR" and "BLB2_ADDR" to the IP-adresses of the configured lightbulbs.

#### Database
Link to the database structure: [Database structure.sql](https://github.com/Bachelor2025JVTD/EvaluatingTool/blob/main/Utilities/Database/DatabaseStructure.sql)


