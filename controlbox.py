#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import web
import time
import threading
import json

import automationhat

import board
import busio
#import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


DEVICE_BUS = 1
DEVICE_ADDR_BOT = 0x13
DEVICE_ADDR_TOP = 0x10

running = True


	 
def make_text(s1,s2):	
	dic = { 
		"speed1": str(s1), 
		"speed2": str(s2)
		}
	
	return json.dumps(dic)
    

def tick():	
	global speed1
	global onPi		
	global running
	while running:
		if speed1 > 0:
			interval = (3600.0 / speed1) -0.01
			#print("Interval 1" + str(interval) )				
			write_byte_data(DEVICE_ADDR_TOP, 4, 0xFF)
			automationhat.output.one.on()			
			time.sleep(0.01)
			write_byte_data(DEVICE_ADDR_TOP, 4, 0x00)			
			automationhat.output.one.off()
			time.sleep( interval )
		else :
			time.sleep( 1 )	
	
	time.sleep(2)
	print("Exiting 1")
	os._exit(0)			

			
		
def tick2():	
	global speed2
	global onPi		
	global running
	while running:
		if speed2 > 0:
			interval = (3600.0 / speed2) -0.01
			#print("Interval 2" + str(interval) )				
			write_byte_data(DEVICE_ADDR_TOP, 3, 0xFF)
			automationhat.output.two.on();
			time.sleep(0.01)
			write_byte_data(DEVICE_ADDR_TOP, 3, 0x00)
			automationhat.output.two.off();
			time.sleep( interval )
		else :
			time.sleep( 1 )

	time.sleep(20)	
	print("Exiting 2")
	os._exit(0)			
	
	
def tick3():	
	global speed1
	global onPi		
	global running
	while running:
		if speed1 > 0:
			interval = (3600.0 / speed1) -0.01
			#print("Interval 2" + str(interval) )				
			write_byte_data(DEVICE_ADDR_TOP, 2, 0xFF)
			automationhat.output.one.on();			
			time.sleep(0.01)
			write_byte_data(DEVICE_ADDR_TOP, 2, 0x00)
			automationhat.output.one.off();
			time.sleep( interval )
		else :
			time.sleep( 1 )

	time.sleep(20)	
	print("Exiting 3")
	os._exit(0)			
			
	
def tick4():	
	global speed2
	global onPi		
	global running
	while running:
		if speed2 > 0:
			interval = (3600.0 / speed2) -0.01
			#print("Interval 2" + str(interval) )				
			write_byte_data(DEVICE_ADDR_TOP, 1, 0xFF)
			automationhat.output.two.on();
			time.sleep(0.01)
			write_byte_data(DEVICE_ADDR_TOP, 1, 0x00)
			automationhat.output.two.off();
			time.sleep( interval )
		else :
			time.sleep( 1 )
		
	time.sleep(20)	
	print("Exiting 4")
	os._exit(0)			

	
	
def write_byte_data( address, reg, data):
	global i2c			
	while not i2c.try_lock():
		pass
	try:
		buf = bytearray(2)
		buf[0] = reg
		buf[1] = data	
		i2c.writeto(address, buf)
	finally:
		i2c.unlock()
	return None		
						

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

speed1 = -1.0
threading.Timer(1, tick).start()
# Uses same speed as tick1
threading.Timer(1, tick3).start()
speed2 = -1.0
threading.Timer(1, tick2).start()
# Uses same spped as tick2
threading.Timer(1, tick4).start()

# Modify this if you have a different sized Character LCD
#lcd_columns = 16
#lcd_rows = 2
 

 
# Initialise the lcd class
#lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows, 32)

#lcd.color = [0,0,0]
#lcd.display = True 
#lcd.clear()
#lcd.text_direction = lcd.LEFT_TO_RIGHT
#lcd.cursor = False
#lcd.message = "* Running *"


urls = ('/', 'dashboard')
render = web.template.render('templates/')
 
app = web.application(urls, globals())
 
my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'), )                              
 
class dashboard:
	def GET(self):		
		form = my_form()
		return render.dashboard(form, "0")
		 
	def POST(self):
		global speed1
		global speed2
		global onPi	
		global running	
		
		prev_msg = ""	
		msg1 = ""
		msg2 = ""
		form = my_form()
		form.validates()
				
		greenBtn = form.value['green']
		print( "Green Button: " + greenBtn )
		if greenBtn == 'down':
			print("Relay One On")		
			write_byte_data(DEVICE_ADDR_BOT, 1, 0xFF)
			automationhat.relay.one.on();
		if greenBtn == 'up':
			time.sleep(0.5)
			print("Relay One Off")
			write_byte_data(DEVICE_ADDR_BOT, 1, 0x00)
			automationhat.relay.one.off();
			

		redBtn = form.value['red']
		print( "Red Button: " + redBtn )
		if redBtn == 'down':
			print("Relay Two On")			
			write_byte_data(DEVICE_ADDR_BOT, 2, 0xFF)
			automationhat.relay.two.on();
		if redBtn == 'up':
			time.sleep(0.5)
			print("Relay Two Off")
			write_byte_data(DEVICE_ADDR_BOT, 2, 0x00)
			automationhat.relay.two.off();

		whiteBtn = form.value['white']
		print( "White Button: " + whiteBtn )
		if whiteBtn == 'down':
			print("Relay Three On")
			automationhat.relay.three.on();
			write_byte_data(DEVICE_ADDR_BOT, 3, 0xFF)
		if whiteBtn == 'up':
			time.sleep(0.5)
			print("Relay Three Off")
			write_byte_data(DEVICE_ADDR_BOT, 3, 0x00)
			automationhat.relay.three.off();
				
		s = form.value['speed1']
		if s == 'STOP':
			running = False
			# Wait for tick threads to stop
			time.sleep(30)					
			os._exit(0)
			
		if s.isdigit():
			speed1 = int(s) * 100			
			print("Speed 1 " + str(speed1))
		
		s = form.value['speed2']
		if s.isdigit():
			speed2 = int(s) * 100
			print("Speed 2 " + str(speed2))
						
		return make_text(speed1,speed2)
 
if __name__ == '__main__':			
	app.run()

