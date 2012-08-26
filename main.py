import webapp2
import os
import jinja2
from google.appengine.ext import db
from google.appengine.api import images

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Post(db.Model):
	title = db.StringProperty(required = True)
	image = db.BlobProperty(required = True)
	description = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	#valid_till = db.DateTimeProperty() Figure out how to add a calendar input

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):   
    def get(self):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
		self.render("posts.html", posts=posts)

class UploadHandler(Handler):
	def get(self):
		self.render("upload.html")
		
	def post(self):
		title = self.request.get("title")
		image = self.request.get("image")
		description = self.request.get("description")
		password = self.request.get("pass")
		if title and image and password==key:
			p = Post(title=title, image=db.Blob(image), description=description)
			p.put()
		else:
			self.render("404.html")
		
class ImageHandler(Handler):
	def get(self):
		p = Post.get_by_id(int(self.request.get('img_id')))
		full = int(self.request.get('full')) 
		if p.image:
			img = images.Image(p.image)
			if full==1:
				self.response.headers['Content-Type'] = 'image/JPEG'
				self.write(p.image)	
			else:
				img.resize(width=300, height=240)
				im = img.execute_transforms(output_encoding=images.JPEG)
				self.response.headers['Content-Type'] = 'image/JPEG'
				self.write(im)
		else:
			self.render("404.html")

class PosterHandler(Handler):
	def get(self, post_id):
		p = Post.get_by_id(int(post_id))
		if p:
			self.render("poster.html", p=p)
		else:
			self.render("404.html")
			
app = webapp2.WSGIApplication([('/', MainPage),
								('/upload', UploadHandler),
								('/img', ImageHandler),
								('/poster/([0-9]+)', PosterHandler)],
                              debug=True)

key = "booger"
