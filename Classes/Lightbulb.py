import requests as r, ipaddress, time as t

class LightBulb():
    
    @staticmethod
    def __SendRequest(url:str)->bool:
        '''Sends API request and validates response. Retries 3 times if any faults'''
        for i in range(0,3):
            try:
                response = r.get(url)  
                if response.status_code != 200:
                    if i==2:
                        print(f"Error: {response.status_code}, {response.text}")
                    else:
                        print(f"Error: Connection estabelished with lightbulb, but recived response code: {response.statuse_code}!")
                        print("Retrying...")
                else:
                    return True

            except r.RequestException as e:
                if i==2:
                    print(f"Error with lightbulb: {e}")
                    return False
                else:
                    print("Error: No response from lightbulb, retrying...")
                    t.sleep(1)

    @staticmethod
    def SetLight(ipAddress:str, percentage:int=0, colorTemp:int=3000)->bool:
        '''Change settings on lightbulb'''
        LightBulb.__ControlSettings(percentage,colorTemp)
        LightBulb.__CheckIpAddress(ipAddress)

        url = f"http://{ipAddress}/light/0?turn=on&brightness={percentage}&temp={colorTemp}"
        return LightBulb.__SendRequest(url)

        
    @staticmethod
    def __ControlSettings(percentage:int,colorTemp:int)->None:
        """Checks thats parameter is inside the allowed limits"""
        if type(percentage)!=int or percentage<0 or percentage>100:
            raise ValueError("Error: Parameter 'percentage' must be of datatype int and equal or between 0 to 100!")
        elif type(colorTemp)!=int or colorTemp<2700 or colorTemp>6500:
            raise ValueError("Error: Parameter 'colorTemp' must be of datatype int and between 2700 and 6500.")
        
    @staticmethod
    def __CheckIpAddress(ipAddress:str)->None:
        """Chekc the property to be a valid IP-adress"""
        try:
            addr=ipaddress.ip_address(ipAddress)
        except:
            raise TypeError("Error: Parameter 'ipAddress' must be of datatype string!")

        