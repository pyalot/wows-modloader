import sys, os, traceback

## store original builtins ##
origExcept = sys.excepthook
origStdout = sys.stdout
origStderr = sys.stderr

## get path to here ##
mods = os.path.join(os.getcwd(), 'res_mods')
here = os.path.join(mods, os.listdir(mods)[0], 'scripts', 'client', 'mods')

## replace stdout ##
outfilename = os.path.join(here, 'mods.log')
outfile = open(outfilename, 'w')
sys.stdout = outfile
sys.stderr = outfile

try:
    print 'modloader.start'
    import new

    moduleCache = {}

    def modlog(*args):
        msg = ' '.join(str(arg) for arg in args) + '\n'
        outfile.write(msg)
        outfile.flush()

    class Require(object):
        def __init__(self, path):
            self.path = path
            self.directory = os.path.dirname(path)

        def __call__(self, path):
            path = os.path.join(self.directory, path + '.py')
            return Require.module(path)

        @staticmethod
        def module(path):
            module = moduleCache.get(path)
            if module is None:
                name = os.path.basename(path)[:-3]
                namespace = {
                    'require'   : Require(path),
                    '__file__'  : path, 
                    '__dir__'   : os.path.dirname(path),
                    'modlog'    : modlog,
                }
                execfile(path, namespace, namespace)
                module = moduleCache[path] = new.module(name)
                module.__dict__.update(namespace)
            return module

    packages = os.path.join(here, 'packages')
    for package in os.listdir(packages):
        packagePath = os.path.join(packages, package)
        initPath = os.path.join(packagePath, '__init__.py')
        if os.path.isdir(packagePath) and os.path.isfile(initPath):
            print 'modloader.load:', packagePath
            try:
                package = Require.module(initPath)
            except:
                print 'modloader.error'
                traceback.print_exc()
    print 'modloader.end'
except:
    traceback.print_exc()

outfile.flush()

## restore original builtins ##
sys.stdout = origStdout
sys.stderr = origStderr
