import os, hou

hou.appendSessionModuleSource('''hou.hscript("autosave on")''')

path_data = os.environ['PRJ'] 
hou.hscript('set -g "%s"="%s"' % ('PRJ', path_data.replace('\\','/')))

path_data = os.environ['SHOT'] 
hou.hscript('set -g "%s"="%s"' % ('SHOT', path_data.replace('\\','/')))

path_data = os.environ['ANIMATION'] 
hou.hscript('set -g "%s"="%s"' % ('ANIMATION', path_data.replace('\\','/')))

path_data = os.environ['ASSETS'] 
hou.hscript('set -g "%s"="%s"' % ('ASSET', path_data.replace('\\','/')))

path_data = os.environ['DATA'] 
hou.hscript('set -g "%s"="%s"' % ('DATA', path_data.replace('\\','/')))

path_data = os.environ['CACHE'] 
hou.hscript('set -g "%s"="%s"' % ('CACHE', path_data.replace('\\','/')))

path_data = os.environ['OUT']
hou.hscript('set -g "%s"="%s"' % ('OUT', path_data.replace('\\','/')))

path_data = os.environ['SRC'] 
hou.hscript('set -g "%s"="%s"' % ('SRC', path_data.replace('\\','/')))

path_data = os.environ['RENDER'] 
hou.hscript('set -g "%s"="%s"' % ('RENDER', path_data.replace('\\','/')))

path_data = os.environ['OTL'] 
hou.hscript('set -g "%s"="%s"' % ('OTL', path_data.replace('\\','/')))

path_data = os.environ['LAYOUT'] 
hou.hscript('set -g "%s"="%s"' % ('LAYOUT', path_data.replace('\\','/')))

path_data = os.environ['TRACKING'] 
hou.hscript('set -g "%s"="%s"' % ('TRACKING', path_data.replace('\\','/')))

path_data = os.environ['SHOTNAME'] 
hou.hscript('set -g "%s"="%s"' % ('SHOTNAME', path_data.replace('\\','/')))
