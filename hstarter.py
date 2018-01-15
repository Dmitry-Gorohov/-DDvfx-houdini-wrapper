#!/usr/bin/python3
# ================= V007 ==========================================================================
import os, sys
import platform
import subprocess
import getpass
import sys
import json
from pprint import pprint

VERBOSE = 0

if VERBOSE:
    print (sys.version) 

print ('\nRun houdini from current folder\n')

def JsonVariables():
    jsonname = "config.json"
    jsonpath = os.path.join(GetSettringsDir(), jsonname)
    
    with open(jsonpath, 'r') as f:
        data = json.load(f)

    env_for_system = data["envvariables"]["oswariables"][platform.system()]

    loop = 0
    for item in env_for_system:
        #print("item is:", item)
        #print("item type:", type(item))
        name = list(item.keys())[0]
        print("name is:", name)
        path = env_for_system[loop][name]
        #pprint(path)
        
        os.environ[name] = path
        
        loop+=1


    print("LC_ALL is:", os.environ["LC_ALL"])
    print("LANG is:", os.environ["LANG"])
    print("CGRU_LOCATION is:", os.environ["CGRU_LOCATION"])


def GetSettringsDir():
    settingsDir = os.path.join(os.path.dirname(__file__), 'settings')
    return settingsDir

def GetConfigsPath():
    hfs_linuxInstallPath = '/opt/hfs/'
    hfs_windowsInstallPath = 'C:/Program Files/Side Effects Software/Houdini'

    opsystem = platform.system()

    if platform.system() == 'Linux':
        if  os.path.exists(hfs_linuxInstallPath):
            HOUDINI_INSTALL_PATH = hfs_linuxInstallPath
        else:
            print("Error - HoudiniEnv folder does not exists, terminating..")
            return

    if platform.system() == 'Windows':
        if  os.path.exists(hfs_windowsInstallPath):
            HOUDINI_INSTALL_PATH = hfs_windowsInstallPath
        else:
            print("Error - HoudiniEnv folder does not exists, terminating..")
            return

    return HOUDINI_INSTALL_PATH

def GetHFS():
    HOUDINI_MAJOR_RELEASE = '16'
    HOUDINI_MINOR_RELEASE = '0'
    HOUDINI_BUILD_VERSION = '736'
    HOUDINI_INSTALL_PATH = 'C:/Program Files/Side Effects Software/Houdini '

    HOUDINI_BUILD = '%s.%s.%s' % (
        HOUDINI_MAJOR_RELEASE,
        HOUDINI_MINOR_RELEASE,
        HOUDINI_BUILD_VERSION)

    HFS = "%s%s" % (
        HOUDINI_INSTALL_PATH,
        HOUDINI_BUILD)

def CreateHFS():

    print ('\n')
    HOUDINI_MAJOR_RELEASE = '16'
    HOUDINI_MINOR_RELEASE = '0'
    HOUDINI_BUILD_VERSION = '736'
    
    opsystem = platform.system()

    if platform.system() == 'Linux':

        hfsLocal = '/opt/hfs/'
        hfsNas   = '/software/hfs/'

        if  os.path.exists(hfsLocal):
            HOUDINI_INSTALL_PATH = hfsLocal
        else :
            HOUDINI_INSTALL_PATH = hfsNas

        print ("It's ok bro, that's Linux")

    elif platform.system() == 'Windows':
        HOUDINI_INSTALL_PATH = 'C:/Program Files/Side Effects Software/Houdini '
        print ("Holly shit, that's fucking Windows")
    else:
        print ("ERROR: Cant get install path directory")
        return

    print ('\n')

    HOUDINI_BUILD = '%s.%s.%s' % (
        HOUDINI_MAJOR_RELEASE,
        HOUDINI_MINOR_RELEASE,
        HOUDINI_BUILD_VERSION)

    HFS = "%s%s" % (
        HOUDINI_INSTALL_PATH,
        HOUDINI_BUILD)

    os.environ['HFS'] = HFS

    HFS = HFS.replace('/', os.sep)

    print ('HFS is:%s' % HFS)

    return HFS

class PathVariables:
    def __init__(self):

        if len(sys.argv)<=1:
            # is project start manually
            shotFolderPath = os.path.dirname(os.path.realpath(__file__))
        else:
            # is farm
            shotFolderPath = os.path.dirname(sys.argv[-2])
        count = 0
        done = 0

        task = 0
        shot = 0
        scene = 0
        project = 0

        while not done:
            if task == 0:
                self.taskName = os.path.split(shotFolderPath)[1]
                FolderPath = os.path.split(shotFolderPath)[0]

                if self.taskName == "work":
                    self.taskName = None
                    self.taskPath = None
                task = 1

            elif shot == 0 and task == 1:
                if os.path.split(FolderPath)[1] == "Work":
                    self.shotName = os.path.split(os.path.split(FolderPath)[0])[1]
                    self.shotPath = os.path.split(FolderPath)[0]
                    # print os.path.split(FolderPath)
                    FolderPath = os.path.split(self.shotPath)[0]
                    shot = 1

            elif scene == 0 and shot == 1 and task == 1:
                if os.path.split(FolderPath)[1] == "Episodes":
                    self.sceneName = None
                    self.scenePath = None
                    scene = 1
                elif os.path.split(FolderPath)[1] == "master":
                    self.sceneName = os.path.split(FolderPath)[1]
                    self.scenePath = os.path.join(os.path.split(FolderPath)[0], self.sceneName)
                    FolderPath = os.path.split(self.scenePath)[0]
                    scene = 1

                else :
                    self.sceneName = os.path.split(FolderPath)[1]
                    self.scenePath = os.path.join(os.path.split(FolderPath)[0], self.sceneName)
                    FolderPath = os.path.split(self.scenePath)[0]
                    scene = 1

            elif project == 0 and scene == 1 and shot == 1 and task == 1:
                self.projectPath = os.path.split(FolderPath)[0]
                self.projectName = os.path.split(self.projectPath)[1]

            count += 1
            if count > 10:
                done = 1
            if project == 1 and scene == 1 and shot == 1 and task == 1:
                done = 1

        if VERBOSE:
            print ()
            print ('taskName    : %s' % self.taskName)
            print ('shotName    : %s' % self.shotName)
            print ('shotPath    : %s' % self.shotPath)
            print ('sceneName    : %s' % self.sceneName)
            print ('scenePath    : %s' % self.scenePath)
            print ('projectName : %s' % self.projectName)
            print ('projectPath : %s' % self.projectPath)
            print ()

def gethpath():

    settingsDir = GetSettringsDir()

    opsystem = platform.system()
    baseConfing = '/prefs/houdini/FX_PREFS/'
    if opsystem == 'Windows':
        baseConfing = os.path.join("C:\\", "Users", getpass.getuser(), "YandexDisk", "HoudiniEnv")
        #baseConfing = r'C:\Users\ANATOLIY\YandexDisk\HoudiniEnv'
    else:
        baseConfing = r'/nas/HoudiniEnv'
    print ('Current platform is %s' % opsystem)

    'Current platform is %s' % opsystem

    # settingsDir = 'C:\Users\dD\YandexDisk\OVFX-Houdini_Procedurals\Education_part\3D\FX\SCENES\01-Car_assembly\settings'

    contdir = []
    configdir = []
    for i in os.walk(baseConfing):
        contdir.append(i)

    for i in contdir[0][1]:
        pathConfig = os.path.join(contdir[0][0], i)
        print ("path configs is: %s" % (pathConfig))
        configdir.append(pathConfig)


    configdir.append(settingsDir)
    configdir.append('&')

    print ("full path configs is: %s" % (configdir))

    result = os.path.pathsep.join(configdir)

    return result

#print '\n\n'

def getotlsscan(path):
    if VERBOSE:
        print ("starting otlsscan")
    directoris = path.split(os.path.pathsep)
    
    if VERBOSE:
        print (directoris)
    assetsdir = []

    for basedir in directoris :
        if os.path.exists(basedir):

            for path, dirs, files in os.walk(basedir):

                #print basedir

                for dir in dirs:
                    fullpath = os.path.join(path, dir)
                    #print 'fullpath is %s' % fullpath

                    if dir == 'otls' or dir == 'OTL':
                        fullotlspath = os.path.join(path, dir)

                        for otlspath, otlsdirs, otlsfiles in os.walk(fullotlspath):
                            for otlsdir in otlsdirs:
                                fullotlpath = os.path.join(otlspath, otlsdir)
                                assetsdir.append(fullotlpath)
                                #print "otl scan dir is: %s" % (fullotlpath)

                assetsdir.append(basedir)


    assetsdir.append('&')
    
    if VERBOSE:
        print ("full path assets is: %s" % (assetsdir))
    
    result = os.path.pathsep.join(assetsdir)
    return result

print ('\n')

def setVar(varName, value):
    value = value.replace('/', os.sep)
    os.environ[varName] = value

def setLocalVar(varName, projectPath, innerPath, createFolder):
    if VERBOSE:
        print ('varname: %s, projectPath: %s, innerPath: %s, createFolder: %s' % (
            varName, projectPath, innerPath, createFolder))
        print ("\n")

    if (innerPath!=""):
        resultPath = os.path.join(projectPath, innerPath)
    else:
        resultPath = projectPath

    setVar(varName, resultPath)

    if not os.path.exists(resultPath):

        # if createFolder == 'manual':
        #     inpt = input("$%s, path: %s does not exist, create folder? \n" % (varName, resultPath))

        #     if inpt == 'y' or inpt == 'yes' or inpt == '+':
        #         print ("$%s creating folder.. \n" % resultPath)

        #         os.makedirs(resultPath)o

        #     else:
        #         print ("skip folder creation \n")

        if createFolder == 'auto':
            print ("$%s, path: %s does not exist, creating folder.. \n" % (varName, resultPath))
            os.makedirs(resultPath)

global HB
def createEnv():
    print("Create env starts")
    global HB
    VarDict = [
        dict(
            varName='PRJ',
            projectPath=PathVariables().projectPath,
        ),
        dict(
            varName='ANIMATION',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Result', "Animation"),
            createFolder='manual'
        ),
        dict(
            varName='SHOT',
            projectPath=PathVariables().shotPath,
            createFolder = 'manual'
        ),
        dict(
            varName='OUT',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Result', PathVariables().taskName),
            createFolder='manual'
        ),
        dict(
            varName='ASSETS',
            projectPath=PathVariables().projectPath,
            innerPath=os.path.join('Assets'),
            createFolder = 'manual'
        ),
        dict(
            varName='DATA',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Data', PathVariables().taskName),
            createFolder='manual'
        ),
        dict(
            varName='CACHE',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Result', PathVariables().taskName, "Cache"),
            createFolder='manual'
        ),

        dict(
            varName='SRC',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Materials'),
            createFolder='manual'
        ),

        dict(
            varName='RENDER',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Result', PathVariables().taskName, "Render"),
            createFolder='manual'
        ),

        dict(
            varName='TRACKING',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Result', 'Tracking'),
            createFolder='manual'
        ),

        dict(
            varName='LAYOUT',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Result', 'Layout'),
            createFolder='manual'

        ),
        dict(
            varName='OTL',
            projectPath=PathVariables().shotPath,
            innerPath=os.path.join('Otl'),
            createFolder='manual'      
        )
    ]

    hpath = gethpath()

    #print ('new HPATH is %s') % ('test')

    os.environ['HOUDINI_PATH'] = hpath
    #print ('HOUDINI_PATH is:%s' % os.environ['HOUDINI_PATH'])

    print ('\n\n')

    for curvar in VarDict:
        setLocalVar(
            curvar.get('varName', ''),
            curvar.get('projectPath', ''),
            curvar.get('innerPath', ''),
            curvar.get('createFolder', 'none'))


    hpath = os.path.pathsep.join([hpath, os.environ['OTL'], os.environ['ASSETS']])

    if VERBOSE:
        print ('\n\n')
        print ('hpath is %s' % hpath)
        print ('\n\n')

    os.environ['HOUDINI_OTLSCAN_PATH'] = getotlsscan(hpath)
    print ('\n\n')

    if VERBOSE:
        print ('HOUDINI_OTLSCAN_PATH is:%s' % os.environ['HOUDINI_OTLSCAN_PATH'])
        print ("PathVariables().sceneName is: %s" % PathVariables().sceneName)

    setVar('SHOTNAME', PathVariables().shotName)
    setVar('PRJNAME', PathVariables().projectName)

    HB = CreateHFS() + '/bin'

    os.environ['PATH'] = os.path.pathsep.join([HB, os.environ['PATH']])

    HB = HB.replace('/', os.sep)

    JsonVariables()

    os.environ['HOUDINI_OTLSCAN_PATH'] = os.path.pathsep.join([
                                                                "C:/cgru.2.2.2/plugins/houdini",
                                                                os.environ['OTL'],
                                                                os.path.join(os.environ['ASSETS'], "asOtl"),
                                                                os.path.join(os.environ['ASSETS'], "Otls"),
                                                                os.environ['HOUDINI_OTLSCAN_PATH']])

    os.environ['HOUDINI_CGRU_PATH']    = "C:/cgru.2.2.2/plugins/houdini"
    os.environ['CGRU_LOCATION']        = "C:/cgru.2.2.2"
    os.environ['PYTHONPATH']           = os.path.pathsep.join([
                                                                "C:/cgru.2.2.2/plugins/houdini",
                                                                "C:/cgru.2.2.2/lib/python",
                                                                "C:/cgru.2.2.2/afanasy/python",
                                                                "C:/cgru.2.2.2/lib"])


    os.environ['SPIRIT'] = os.environ['PRJ']
    os.environ['TEXCROWD'] = os.path.join(os.environ['ASSETS'], "asCrowd", "TEXTURES")
    os.environ['TEXPROPS'] = os.path.join(os.environ['ASSETS'], "asProps", "TEXTURES")
    os.environ['JOB'] = os.environ['PRJ']


    os.environ['LC_ALL'] = 'C'
    os.environ['LANG'] = 'en_EN.utf8'
    print("Create env ends")

if __name__ == '__main__':
    print('>>>', sys.argv)
    createEnv()
    startpath = ['%shoudinifx' % (HB + os.sep)]
    print ()
    print (startpath)
    #subprocess.Popen(startpath)

