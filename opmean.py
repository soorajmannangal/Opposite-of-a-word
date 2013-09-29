from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import urllib2
import re
import sets
import sys
import cookielib
import datetime


from urllib import urlencode
import cgi
import urllib
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users

class  Registration(db.Model):
  code = db.StringProperty()
  name = db.StringProperty()
  mobno = db.StringProperty()
  pwd = db.StringProperty()
  pro = db.StringProperty()
  #count = db.StringProperty()
class Code(db.Model):
  current = db.StringProperty()
  
def registration_key():
  return db.Key.from_path('RegistrationTable', 'registration_record')

def code_key():
  return db.Key.from_path('CodeTable', 'lastcode')

name = None  #user name
mobno = None #user mobile no
pro = None  #provider eg 160by2,site2sms
pswd = None #provider password
key = None  # send s or regiser r
code = None  #user registerd unique code
msg = None
urltosend = None
tono = None
TOTAL = 260

CONNECTION_ERROR = -1
SUCCESS = 1
class MainPage(webapp.RequestHandler): 
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    message=self.request.get_all('message' or '00')
    self.response.out.write("<html><body>")  
    if message is None:
      sys.exit(1)    
    data=[]
    data=message[-1].split(' ') 
    a =1
    if a == 1 :
      uid =data[0]
      psw = data[1]
      cj = cookielib.CookieJar()
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      opener.addheaders = [('User-Agent','Mozilla/5.0 (Ubuntu; X11; Linux x86_64; rv:8.0) Gecko/20100101 Firefox/8.0')]
      url = 'www.google.com'
      url_data = urlencode({'userid':uid,'password':psw,'Submit':'Submit'})
      try:
	usock = opener.open(url, url_data) 
	   
      except IOError:      
	self.response.out.write("User name or password incorrect")  
	self.response.out.write("</body></html>")
	sys.exit(1)
      url = 'http://117.211.100.44:8080/index.php'
      url_data = urlencode({'module':'com_views','task':'student_attendance_view'})
      atand = opener.open(url, url_data)
      page=atand.read()
      line=page.split('\n')
      new=set([])
      for i in range (len(line)) :    
	mat2=re.match(r'.*Logged in as.*',line[i],re.M)
	if mat2: 
	  i = i+2
	  nam=re.match(r'.*<td>(.*?)</td>.*',line[i])
	  if nam:
	    str0= nam.group(1)
	    self.response.out.write("Name : "+str0)
	mat1=re.match(r'.*Attendance till date :.*',line[i],re.M)
	if mat1:	
	  self.response.out.write("</br>"+line[i])       
   
    self.response.out.write("</body></html>")
	    
	    	    
application = webapp.WSGIApplication(
    [('/', MainPage)],
    debug=True)

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
	main()		                       
                        
