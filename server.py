from flask import Flask 
from flask import render_template
from forms import SignUpForm
from flask import request

app = Flask (__name__)
app.config['SECRET_KEY'] = 'abcdefg'
# create a wrarp of localhost
@app.route('/')
def home():
	return 'Hello world'

@app.route('/about')
def about():
	return 'The about page'
@app.route('/blog')
def blog():
	posts = [{'title':'Title 1', 'author': 'author 1'},{'title': 'Title 2', 'author':'author 2'}]
	return render_template('blog.html', author = 'catafest', sunny=True, posts = posts)
# creaza a regula variabila ( variable rules) 
@app.route('/blog/<blog_id>')
def blogpost(blog_id):
	return 'This is the post '+str(blog_id)

@app.route('/signup', methods = ['GET','POST'])
def signup():
	form = SignUpForm()
	if form.is_submitted():
		result = request.form
		return render_template('user.html', result = result)
	return render_template('signup.html', form = form)

# the default name main 
if __name__ == '__main__':
	app.run()
