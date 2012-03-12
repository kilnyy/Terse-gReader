#!/home2/kilnyyco/python/bin/python
#coding=utf-8

import web
import htmlmaker

web.config.debug = False

usecgi = True

if usecgi:
    import cgitb
    cgitb.enable()
    import sys
    import os
    os.environ['REAL_SCRIPT_NAME'] = "/greader"


urls = (
    '/', 'index',
    '/login', 'login'
)

app = web.application(urls, globals())
render = web.template.render('templates')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'email': '', 'password': ''})

class index:

    def GET(self):
        if session.email and session.password:
            maker = htmlmaker.Htmlmaker(session.email, session.password)
            return render.index(maker.run())
        else:
            session.kill()
            raise web.seeother('/login')

class login:

    def GET(self):
        if session.email and session.password:
            raise web.redirect('/')
        else:
            return render.login()

    def POST(self):
        data = web.input()
        session.email = data.email
        session.password = data.password
        if session.email and session.password:
            raise web.redirect('/')
        else:
            return 'LoginFailed'

    

if __name__ == "__main__" :
    app.run()

if usecgi:
    def cgidebugerror():
        _wrappedstdout = sys.stdout

        sys.stdout = web._oldstdout
        cgitb.handler()

        sys.stdout = _wrappedstdout

    web.internalerror = cgidebugerror
