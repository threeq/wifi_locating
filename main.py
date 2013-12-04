# -*- coding: utf-8 -*-
import web;
import locatingserver;
#from mylog import Log;

render = web.template.render("templates/");
urls = (
	#'/(.*)/', 'redirect',
    '/locating', locatingserver.app_locating
	
)
app = web.application(urls, globals())

def my_processor(handler):
	#print 'before handling'
	result = handler();
	#print 'after handling'
	
	# jsonp调用处理
	jsonp_callback = None;
	inputs = web.input(jsonp_callback=None)
	jsonp_callback = inputs['jsonp_callback'];
	if jsonp_callback!=None:
		result = jsonp_callback+"("+result+")";
		web.header('Content-type', "text/javascript; charset=utf-8")
		
	return result

def my_loadhook():
	print 'my load hook'
	web.header('Content-type', "text/html; charset=utf-8")

def my_unloadhook():
	print 'my unload hook'

app.add_processor(my_processor);
# app.add_processor(web.loadhook(my_loadhook));
# app.add_processor(web.unloadhook(my_unloadhook));

# 404
def notfound():
	return web.notfound("404 error.")

    # You can use template result like below, either is ok:
    #return web.notfound(render.notfound())
    #return web.notfound(str(render.notfound()))
app.notfound = notfound;
# 500
def internalerror():
    return web.internalerror("500 error.")
app.internalerror = internalerror

class index:
	#----------------------------------------------------------------------
	def GET(self):
		""""""
		return render.index();
		
class redirect:
	def GET(self, path):
		web.seeother('/'+path);

web.webapi.internalerror = web.debugerror
if __name__ == "__main__":
    #app.run(Log)
	app.run()