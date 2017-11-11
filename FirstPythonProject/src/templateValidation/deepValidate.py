import json
import os
import re
from fixSubjectType import addMissingSubjectType

class SaaSTemplate:
    def __init__(self, dictionary):
        self.__dict__ = dictionary


def readAndValidateTemplates(configTemplatesFile):
    """
    This function reads configuration templates from configTemplatesFile 
    and performs deep validation
    :param configTemplatesFile:
    :return: none
    """
    if os.path.getsize(configTemplatesFile) < 0:
        print("Template file empty")
        return
    
    errorCount = 0;
    with open(configTemplatesFile) as file:
        templatesArray = json.loads(file.read(), object_hook=SaaSTemplate)
        if len(templatesArray) <= 0:
            print("Array empty - No template objects to validate")
            return
        for templateObj in templatesArray:
            print('Validating %s template '%(templateObj.templateName))
            errorCount += validate(templateObj)
    
    if errorCount != 0 :
        print("%d templates in error state"%errorCount)        
    return


def validate(templateObj):
    """
    This function calls various validate functions
    :param templateObj
    :return: none
    """
    isSubstitutionValid = validateSubstitution(templateObj)
    isSubjectTypeValid = validateSubjectType(templateObj)
        
    return (int) (not isSubstitutionValid or not isSubjectTypeValid)    
    

def validateSubstitution(tempObj):
    """
    This function validates the template object for variable substituion
    :param templateObj
    :return: boolean
    """
    if not hasattr(tempObj, 'templatePropertyMetadata'):
        print('\t ** Error in %s Template- Missing templatePropertyMetadata' % (tempObj.templateName))
        return False
    
    if not hasattr(tempObj.templatePropertyMetadata, 'variables'):
        print('\t ** Error in %s Template- Missing Variables' % (tempObj.templateName))
        return False
    
    if len(tempObj.templatePropertyMetadata.variables) > 0:
        for varObj in tempObj.templatePropertyMetadata.variables:
            varName = varObj.name
            spConn = tempObj.spConnector
            ssoConf = tempObj.ssoConfig
            subsCount = getSubstitutionCount(spConn, varName) + getSubstitutionCount(ssoConf, varName)
            targetPropsCount = 0
            
            if hasattr(varObj, 'type') and (varObj.type == 'inputText' or varObj.type == 'inputtext'):
                if hasattr(varObj, 'targetProperties'):
                    targetPropsCount = len(varObj.targetProperties)

                    for targetProperty in varObj.targetProperties:                         
                        if not hasAttribute(varName, tempObj, targetProperty):
                            print('\t ** Error in %s Template- Invalid targetProperty %s for variable %s'% (tempObj.templateName, targetProperty, varName))
                            return False

                    if(subsCount != targetPropsCount):
                        print('\t ** Error in %s Template- substitution count doesn\'t match' % (tempObj.templateName))
                        return False
                    
                else:
                    print("\t ** Error in %s Template - Missing TargetProperties Section" % (tempObj.templateName))
                    return False    
            else:
                print("\t Skipping substitutionValidation for %s Template since variable type is NOT inputText" % (tempObj.templateName))    
                return True
            
    return True


def hasAttribute(varName, obj, keyString):
    if '.' in keyString:
        currKey = keyString[0:keyString.index('.')]
        
        if isArray(currKey):
            keyWithIndex = extractKeyWithIndex(keyString)
            items = obj.__dict__.get(keyWithIndex[0])
            item = items[keyWithIndex[1]]
            return hasAttribute(varName, item, keyString[keyString.index('.')+1:len(keyString)])  
        elif hasattr(obj, currKey):
            return hasAttribute(varName, obj.__dict__.get(currKey), keyString[keyString.index('.')+1:len(keyString)])
        else:
            return False            
    else:
        if isArray(keyString):
            keyWithIndex = extractKeyWithIndex(keyString)
            items = obj.__dict__.get(keyWithIndex[0])
            return (len(items) > keyWithIndex[1]) and ('$'+varName+'$') in items[keyWithIndex[1]]
        else:    
            return hasattr(obj, keyString) and (('$'+varName+'$') in obj.__dict__.get(keyString))
    

def isArray(keyString):
    return '[' in keyString
    
        
def extractKeyWithIndex(keyString):
    match = re.search('(.*?)\[(\d)\]', keyString, re.IGNORECASE)
    if match is not None:
        propName = match.group(1)
        index = match.group(2)
        return [propName, int(index)]
    return None


def getSubstitutionCount(obj, variableName):
    """
    This function counts the number of occurrences of a variable in the template object
    :param templateObj, variableName
    :return: integer
    """
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
                    subsCount += getSubstitutionCount(subObj, variableName)
        
        return subsCount              
    else:
        return 0


def is_primitive(var):
    primitive = (int, str, bool)
    return isinstance(var, primitive)


def validateSubjectType(templateObj):
    """
    This function validates the template object for missing subjectType attribute
    :param templateObj
    :return: none
    """
    ssoConf = templateObj.ssoConfig
    if hasattr(ssoConf, 'subjectValue'):
        if hasattr(ssoConf, 'subjectType'):
            if (templateObj.ssoConfig.subjectType == 'email-address') and not isSubjectValueIsMail(ssoConf):
                print('\t ** Error in %s Template - Incorrect subjectType %s for subjectValue %s' % (templateObj.templateName, ssoConf.subjectType, ssoConf.subjectValue))
                return False
        else:
            print('\t ** Error in %s Template - Missing mandatory subjectType field' % (templateObj.templateName))
            return False
        
    else:
        print('\t ** Error in %s Template - Missing mandatory subjectValue field' % (templateObj.templateName))
        return False
           
    return True


def isSubjectValueIsMail(ssoConfig):
    valueArr = ['%{session.ad.last.attr.mail}', '%{session.ldap.last.attr.mail}', '%{session.radius.last.attr.mail}']
    for value in valueArr:
        if ssoConfig.subjectValue == value:
            return True
    return False

    
def main():
    """
    Main function
    :param templates fileNameYes...
    :return: none
    """
    fileName = "saas-templates2.json"
#     readAndValidateTemplates(fileName)
    addMissingSubjectType('arcgis')
    
main()     