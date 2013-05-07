#!/usr/bin/env python
#coding=utf-8

import web
import controller

web.config.debug = False

import cgitb
cgitb.enable()
import sys
import os


urls = (
    '/', 'index',
    '/login', 'login',
    '/doread', 'doread'
)

app = web.application(urls, globals())
render = web.template.render('templates')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'email': '', 'password': ''})

class index:

    def GET(self):
        if session.email and session.password:
            ctrl = controller.Controller(session.email, session.password)
            return render.index(ctrl.get_data())
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

class doread:

    def POST(self):
        data = web.input()
        if session.email and session.password:
            ctrl = controller.Controller(session.email, session.password)
            ctrl.do_read(data.entryid)
            return ''
        else:
            session.kill()
            raise web.seeother('login')

if __name__ == "__main__" :
    app.run()

def cgidebugerror():
    _wrappedstdout = sys.stdout

    sys.stdout = web._oldstdout
    cgitb.handler()

    sys.stdout = _wrappedstdout

web.internalerror = cgidebugerror
