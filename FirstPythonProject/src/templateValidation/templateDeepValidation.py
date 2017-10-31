import json

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
    with open(configTemplatesFile) as file:
        templatesArray = json.loads(file.read(), object_hook=SaaSTemplate)
        for templateObj in templatesArray:
#             print(templateObj.__dict__)
#             print(templateObj.ssoConfig.__dict__)
            validate(templateObj)
    return


def validate(templateObj):
    """
    This function calls various validate functions
    :param templateObj
    :return: none
    """
    #print('Validating %s template : '%(templateObj.templateName))
    if validateSubstitution(templateObj):
#         print('\t Substitution - OK')
        pass
    else:    
        print('Validating %s template : '%(templateObj.templateName))
        print('\t ** Error in Substitution')
    
    if validateSubjectType(templateObj):
        pass
        #print('\t SubjectType - OK')
    else:    
        print('Validating %s template : '%(templateObj.templateName))
        print('\t ** Error Missing subjectType')
    

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
    #         print("Subs for %s in spConn %s"%(varName, getSubsCount(spConn, varName)))
    #         print("Subs for %s in ssoConf %s"%(varName, getSubsCount(ssoConf, varName)))
            subsCount = getSubsCount(spConn, varName) + getSubsCount(ssoConf, varName)
            targetPropsCount = 0
            
            if hasattr(varObj, 'targetProperties'):
                targetPropsCount = len(varObj.targetProperties)
            elif hasattr(varObj, 'values') and hasattr(varObj.values, 'staging') and hasattr(varObj.values.staging, 'targetProperties'):
                targetPropsCountStaging = len(varObj.values.staging.targetProperties)
                targetPropsCountProd = len(varObj.values.production.targetProperties)
                targetPropsCount = max(targetPropsCountProd, targetPropsCountStaging)
            else:
                print("\t ** Error in %s Template - Missing TargetProperties" % (tempObj.templateName))
                return False    
                
            if(subsCount != targetPropsCount):
                print('\t ** Error in %s Template- substitution count doesn\'t match' % (tempObj.templateName))
                return False
    return True


def getSubsCount(obj, variableName):
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
                    subsCount += getSubsCount(subObj, variableName)
        
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
    return True

    
def main():
    """
    Main function
    :param templates fileName
    :return: none
    """
#     fileName = "saas-templates.json"
    fileName = "saas-templates2.json"
#     fileName = "saasTemp_3.json"
    readAndValidateTemplates(fileName)
    
main()        
        


