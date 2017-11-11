import json
from shutil import copyfile
import os

class SaaSTemplate:
    def __init__(self, dictionary):
        self.__dict__ = dictionary
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)    
     
    
        
def addMissingSubjectType(dirName):
    print('Calling sample() from fixSubjectType.py')
    path = dirName+'/template.json'
    with open(path, "r") as json_file:
            data = json.loads(json_file.read(), object_hook=SaaSTemplate)
            ssoConfig = data.ssoConfig
            if not hasattr(ssoConfig, 'subjectType'):
                subType = 'email-address' if isSubjectValueIsMail(ssoConfig) else 'unspecified'
                print('Adding subjectType - %s'% subType)
                data.ssoConfig.subjectType = subType
                writeToFile(path, data)
#                 print(json.dumps(ssoConfig, indent=4, sort_keys=True))

def writeToFile(filePath, jsonData):
    tempFilePath = filePath+'.bakup'
    
    os.remove(tempFilePath)
    open(tempFilePath, 'w')
    copyfile(filePath, tempFilePath)
    
    with open(tempFilePath, "w") as temp_json_file:
        try:
            temp_json_file.write(jsonData.toJSON())
            with open(filePath, "w") as json_file:
                json_file.write(jsonData.toJSON())
#                 copyfile(tempFilePath, filePath)
#             os.remove(tempFilePath)
        except:
            print("Something went wrong while writing to %s template file"% filePath.split(":")[1])
#             os.remove(tempFilePath)

def isSubjectValueIsMail(ssoConfig):
    valueArr = ['%{session.ad.last.attr.mail}', '%{session.ldap.last.attr.mail}', '%{session.radius.last.attr.mail}']
    for value in valueArr:
        if ssoConfig.subjectValue == value:
            return True
    return False            