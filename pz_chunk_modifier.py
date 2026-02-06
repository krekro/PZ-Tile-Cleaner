from ftplib import FTP
import re
import configparser
import os



class configs:
    def __init__(self, username:str, password:str, hostname:str, path:str, mapbin:str, x1:str, x2:str, y1:str, y2:str):
        # This is an instance variable, unique to each object
        self.username = username
        self.password = password
        self.hostname = hostname
        self.path = path
        self.mapbin = mapbin
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        


def main():
    print("Starting...")
    config_1 = loadConfig()
    valid = re.compile(config_1.mapbin)
    try:
        ftpClient = FTP(config_1.hostname)
        ftpClient.login(config_1.username,config_1.password)
        ftpClient.cwd(config_1.path)
        print("loading file list....")
        entries = ftpClient.nlst()
        
        cx1 = int(config_1.x1) 
        cx2 = int(config_1.x2)
        cy1 = int(config_1.y1)
        cy2 = int(config_1.y2)
        files = []
        for file in entries:
            if displaymatch(valid.match(file)):
                filewoext = file.replace(".bin", "")
                fx = int(filewoext.split("_")[1])
                fy = int(filewoext.split("_")[2])
                if fx >= cx1 and fx <=cx2 and fy >= cy1 and fy <= cy2:
                    files.append(file)
                    fullpath = config_1.path + file
                    try:
                        ftp_response = ftpClient.delete(fullpath)
                        print(f"File '{fullpath}' deleted successfully. Server response: {ftp_response}")
                    except Exception as e:
                        print(f"An error occurred when deleting file: {file}")
                        print(f"Error Message: {e}")

            
        ftpClient.close()            
        print(files)
        print(f"files deleted -> {len(files)}")       
    except ConnectionRefusedError:
        print("Connection Refused")
        
def displaymatch(match):
    if match is None:
        return False
    return True

def loadConfig(): 
    print("loading config")  
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config = configparser.ConfigParser()
    try: 
        config.read(config_path)
        username = config.get("ftp", "username")
        password = config.get("ftp", "password")
        hostname = config.get("ftp", "hostname")
        path = config.get ("ftp", "path")
        #print(config.items("ftp"))
        
        mapbin = config.get ("regex", "mapbin")
        #print(config.items("regex"))
        
        x1 = config.get("range", "x1")
        x2 = config.get("range", "x2")
        y1 = config.get("range", "y1")
        y2 = config.get("range", "y2")
        
        return configs(username, password, hostname, path, mapbin, x1, x2 ,y1, y2)
    except configparser.Error as e:
        print(f"Error reading config file: {e}")
    except FileNotFoundError:
        print(f"Configuration file '{config_path}' not found.")

main()