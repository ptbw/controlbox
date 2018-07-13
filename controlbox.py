import web
 
def make_text(string):
    return string
 
urls = ('/', 'dashboard')
render = web.template.render('templates/')
 
app = web.application(urls, globals())
 
my_form = web.form.Form(
                web.form.Textbox('', class_='textfield', id='textfield'),
                )
 
class dashboard:
    def GET(self):
        form = my_form()
        return render.dashboard(form, "0")
         
    def POST(self):
		form = my_form()
		form.validates()
		
		greenBtn = form.value['green']
		print( "Green Button: " + greenBtn )
		
		redBtn = form.value['red']
		print( "Red Button: " + redBtn )
		
		whiteBtn = form.value['white']
		print( "White Button: " + whiteBtn )
		
		s = form.value['textfield']
		i = 0
		if( s.isdigit() ) :
			i = int(s) * 1000
		
		return make_text(i)
 
if __name__ == '__main__':
    app.run()

