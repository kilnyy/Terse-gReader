import cgitb
    cgitb.enable()
    import sys

def cgidebugerror():
        _wrappedstdout = sys.stdout

        sys.stdout = web._oldstdout
        cgitb.handler()

        sys.stdout = _wrappedstdout

    web.internalerror = cgidebugerror
