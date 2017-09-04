import os, new, marshal, traceback, gettext, BigWorld

trans = gettext.GNUTranslations(open('../res/texts/%s/LC_MESSAGES/global.mo' % BigWorld.getCurrentLocale(), 'rb'))
here = os.path.dirname(os.path.realpath(__file__))
packages = os.path.join(here, 'scripts')
logfile = open(os.path.join(here, 'mods.log'), 'w')

cache = {}

class ModAPI(object):
    def __init__(self, package, path):
        self.package = package
        self.path = path
        self.directory = os.path.dirname(path)
        self.trans = trans

    def log(self, *msg):
        msg = ' '.join(str(item) for item in msg) + '\n'
        logfile.write(msg)
        logfile.flush()

    def log_exc(self):
        logfile.write(traceback.format_exc())
        logfile.flush()

    def require(self, name):
        path = name
        if path.startswith('/'):
            path = path.lstrip('/')
            origin = self.package
        else:
            origin = self.directory
        path = os.path.join(origin, path)

        if os.path.isdir(path):
            path = os.path.join(path, '__init__.py')
        else:
            path = path + '.py'

        if os.path.isfile(path):
            return getModule(self.package, path)
        else:
            path = path + 'c'
            if os.path.isfile(path):
                return getModule(self.package, path)
            else:
                raise Exception('Module not found: %s' % name)

def runPy(path, ns):
    execfile(path, ns, ns)

def runPyc(path, ns):
    infile = open(path, 'rb')
    infile.seek(8)
    code = marshal.load(infile)
    exec code in ns, ns

def getModule(package, path):
    module = cache.get(path)
    if module is None:
        name = os.path.splitext(os.path.basename(path))[0]
        module = cache[path] = new.module(name)
        module.mapi = ModAPI(package, path)
        module.__file__ = path
        if path.endswith('.py'):
            runPy(path, module.__dict__)
        elif path.endswith('.pyc'):
            runPyc(path, module.__dict__)
        
    return module

logfile.write('modloader.start\n')
for name in os.listdir(packages):
    try:
        logfile.write('modloader.loading package: %s\n' % name)
        package = os.path.join(packages, name)
        if os.path.isdir(package):
            module = os.path.join(package, '__init__.py')
            
            if not os.path.exists(module):
                module += 'c'
            
            if os.path.exists(module):
                getModule(package, module)
    except:
        logfile.write('modloader.error\n')
        logfile.write(traceback.format_exc())
logfile.write('modloader.end\n')
logfile.flush()