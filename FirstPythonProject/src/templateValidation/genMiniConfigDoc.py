import sys
import getopt
import json
import fileinput



SAAS_APPLICATION_DOC_TEMPLATE = './saas-application-configGuide-template.rst'
IDP_CONNECTOR_DOC_TEMPLATE = "./idp-connector-configGuide-template.rst"
SAAS_APPLICATION_TEMPLATES_FILE = "./saas-templates.json"
IDP_CONNECTOR_TEMPLATE_FILE = "./idp-connector-templates"


def getAppSpecificProperties(template):
    """
    This function looks up specified template JSON and prepares documentation for template
    specific properties.
    :param template:
    :return: documentation fragment documenting template specific properties.
    """
    props = {}
    appSpecificContent = ''
    templateLabel = template.get('templateLabel')
    propMetadata = template.get('templatePropertyMetadata')
    if (propMetadata):
        variables = propMetadata.get('variables')
        if (variables):
            for v in variables:
                label = v.get('displayLabel')
                help = v.get('helpText')
                # print('label ' + label + 'help ' + help)
                props[label] = help
    if (len(props)):
        appSpecificContent = 'To configure ' + templateLabel + ' provide following inputs:\n'
        for k, v in props.items():
            appSpecificContent = appSpecificContent + '	- **' + k + '** : ' + v + '\n'
    else:
        appSpecificContent = templateLabel + ' does not require any user input.'
    return appSpecificContent.strip()


def readAndParseTemplates(docTemplateFile, configTemplatesFile):
    """
    This function reads configuration templates from configTemplatesFile specified and generates
    configuration guide using configGuide documentation template specified by docTemplateFile
    :param docTemplateFile:
    :param configTemplatesFile:
    :return:
    """
    with open(configTemplatesFile) as json_data:
        templatesJson = json.load(json_data)
        substParams = {}
        for template in templatesJson:
            templateName = template.get('templateName')
            templateLabel = template.get('templateLabel')
            appContent = getAppSpecificProperties(template)
            substParams['$TEMPLATE_LABEL$'] = templateLabel
            substParams['$APP_PROPERTIES$'] = appContent
            generateMiniGuide(docTemplateFile, templateName, substParams)
        # print('templateName ' + template["templateName"])
        # print(substParams)
    return


def generateMiniGuide(docTemplateFile, templateName, substParams):
    """
	This function generates a mini configuration guide and writes it in the file with a name templateName.rst
	Configuration Guide is created in docs directory.
	:param docTemplateFile configGuide template (rst) file
	:param templateName: used to name the configuration guide file
	:param substParams: dictionary (key : value ) of parameters to substitute
	:return:
	"""
    templateFileName = "./docs/" + templateName + ".rst"
    print('Generating configuration guide : ' + templateFileName)
    templateFile = open(templateFileName, 'w')
    for line in fileinput.input(docTemplateFile):
        line = line.strip()
        for key, value in substParams.items():
            line = line.replace(key, value)
        templateFile.write(line + '\n')
    templateFile.close()
    return


def testGen():
    filename = "abc"
    params = {'$TEMPLATE_LABEL$': 'appName', '$APP_PARAMS$': 'application params'}
    generateMiniGuide(filename, params)
    return


def testParse():
    readAndParseTemplates(SAAS_APPLICATION_DOC_TEMPLATE, SAAS_APPLICATION_TEMPLATES_FILE)
    return

def main(argv):
   docTemplateFile = ''
   configTemplatesFile = ''
   try:
      opts, args = getopt.getopt(argv,"hd:t:",["docFile=","templatesFile="])
   except getopt.GetoptError:
      print('python genMiniConfigDoc.py -d <docTemplateFile> -t <templatesFile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('python genMiniConfigDoc.py  -d <docTemplateFile> -t <templatesFile>')
         sys.exit()
      elif opt in ("-d", "--docFile"):
         docTemplateFile = arg
      elif opt in ("-t", "--templatesFile"):
         configTemplatesFile = arg
   print('docTemplate file is ', docTemplateFile)
   print('configTemplates file is ', configTemplatesFile)
   if (docTemplateFile == '' or configTemplatesFile == ''):
       print('Usage: python genMiniConfigDoc.py  -d <docTemplateFile> -t <templatesFile>')
       sys.exit(2)

   readAndParseTemplates(docTemplateFile, configTemplatesFile)

if __name__ == "__main__":
   main(sys.argv[1:])