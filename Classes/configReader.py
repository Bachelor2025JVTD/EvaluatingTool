import os,json

class ConfigReader:

    __path=None

    def __init__(self,path:str)->"ConfigReader":
        """Initalize ConfigReader with path to JSON file"""
        if not os.path.exists(path):
            raise FileExistsError(f"Error: Path: {path} do not exists!")
        
        self.__path=path

   
    def Read(self, property: str):
        """Find property from configured JSON file"""
        with open(self.__path, "r") as file:
            json_file = json.load(file)
            return self.__RecursiveSearch(json_file, property)

    @staticmethod
    def __RecursiveSearch(node, property: str):
        """Private helper for Read methode"""
        if isinstance(node, dict):
            for key, item in node.items():
                if key == property:
                    return item
                result = ConfigReader.__RecursiveSearch(item, property)
                if result is not None:
                    return result
        elif isinstance(node, list):
            for element in node:
                result = ConfigReader.__RecursiveSearch(element, property)
                if result is not None:
                    return result
        return None
            