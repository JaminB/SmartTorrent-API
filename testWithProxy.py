#!/usr/bin/python
from proxywrap import Proxy
proxy = Proxy()
print proxy.run('"' +"./RunSearch " + "test" + " " + "other"+'"')
