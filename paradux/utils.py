import pkgutil

def findSubmodules(packageName) :
    ret = []
    for importer, modname, ispkg in pkgutil.iter_modules(packageName.__path__):
        ret.append(modname)
    return ret

