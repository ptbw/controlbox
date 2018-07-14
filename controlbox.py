#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import web
import time
import threading

onPi = False
running = True

try:
	import automationhat
	print("On a Pi")
	onPi = True
except RuntimeError:
	print("Not on a Pi")
	onPi = False
	 
def make_text(string):
    return string
    

def tick():	
	global speed
	global onPi		
	global running
	while running:
		if speed > 0:
			interval = 3600.0 / speed
			print("Interval " + str(interval) )	
			if onPi and automationhat.is_automation_hat():
				automationhat.output.one.on()
				time.sleep(0.01)
				automationhat.output.one.off()
			time.sleep( interval )
	
	print("Exiting")
	os._exit(0)	
	
						
	
speed = -1.0
threading.Timer(1, tick).start()

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
		global speed	
		global onPi	
		global running		
		form = my_form()
		form.validates()
		
		greenBtn = form.value['green']
		print( "Green Button: " + greenBtn )
		if onPi and automationhat.is_automation_hat() and greenBtn == 'down':
			print("Relay One On");			
			automationhat.relay.one.on();
		if onPi and automationhat.is_automation_hat() and greenBtn == 'up':
			print("Relay One Off");			
			automationhat.relay.one.off();
			
		
		redBtn = form.value['red']
		print( "Red Button: " + redBtn )
		if onPi and automationhat.is_automation_hat() and redBtn == 'down':
			print("Relay Two On");			
			automationhat.relay.one.on();
		if onPi and automationhat.is_automation_hat() and redBtn == 'up':
			print("Relay Two Off");			
			automationhat.relay.one.off();
		
		whiteBtn = form.value['white']
		print( "White Button: " + whiteBtn )
		if onPi and automationhat.is_automation_hat() and whiteBtn == 'down':
			print("Relay Three On");			
			automationhat.relay.one.on();
		if onPi and automationhat.is_automation_hat() and whiteBtn == 'up':
			print("Relay Three Off");			
			automationhat.relay.one.off();
				
		s = form.value['textfield']
		if s == 'STOP':
			running = False
			# Wait for tick thread to stop
			time.sleep(10)		
			# exit application????
			os._exit(0)
			
		if s.isdigit():
			speed = int(s) * 1000
			print("Speed " + str(speed) )		
				
		return make_text(speed)
 
if __name__ == '__main__':			
	app.run()
	

