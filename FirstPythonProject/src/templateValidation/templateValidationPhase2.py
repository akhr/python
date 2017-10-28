import json
from builtins import str
from _ast import Str

class SaaSTemplate:
    def __init__(self, dict):
        self.__dict__ = dict


def readAndValidateTemplates(configTemplatesFile):
    """
    This function reads configuration templates from configTemplatesFile ....
    :param configTemplatesFile:
    :return:
    """
    with open(configTemplatesFile) as file:
        templatesArray = json.loads(file.read(), object_hook=SaaSTemplate)
        for templateObj in templatesArray:
#             print(templateObj.__dict__)
#             print(templateObj.ssoConfig.__dict__)
            validate(templateObj)
    return


def validate(templateObj):
    if validateSubstitution(templateObj):
        print('Successful substitution for %s template'%(templateObj.templateName))
    else:    
        print('Error in substitution for %s template'%(templateObj.templateName))
    
    if not validateSubjectType(templateObj):
        print('Missing subjectType for %s template'%(templateObj.templateName))
    

def validateSubstitution(tempObj):
    for varObj in tempObj.templatePropertyMetadata.variables:

        varName = varObj.name
        spConn = tempObj.spConnector
        ssoConf = tempObj.ssoConfig

        print("Subs for %s in spConn %s"%(varName, getSubsCount(spConn, varName)))
        print("Subs for %s in ssoConf %s"%(varName, getSubsCount(ssoConf, varName)))
        
        subsCount = getSubsCount(spConn, varName) + getSubsCount(ssoConf, varName)
        targetPropsCount = len(varObj.targetProperties)
        
        if(subsCount != targetPropsCount):
            return False
    
    return True

def getSubsCount(obj, variableName):
    subsCount = 0
    
    if type(obj) == str:
        return  1 if (('$'+variableName+'$') in obj) else 0
    elif not is_primitive(obj):
        for k, v in obj.__dict__.items():
            if type(v) == str:
                if (('$'+variableName+'$') in obj.__dict__.get(k)):
                    subsCount += 1
            elif type(v) == list:
                for subObj in v:
                    subsCount += getSubsCount(subObj, variableName)
        
        return subsCount              
    else:
        return 0


def is_primitive(var):
    primitive = (int, str, bool)
    return isinstance(var, primitive)

def validateSubjectType(templateObj):
    
    return False

    
def main():
    fileName = "saas-templates.json"
    readAndValidateTemplates(fileName)
    
main()        
        


