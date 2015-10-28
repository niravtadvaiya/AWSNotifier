from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.template import RequestContext, loader
from django.template.context_processors import csrf
from django.core.files import File
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from urllib import urlencode
import os 
import urllib2
import nexmo
import json
import ConfigParser 

FILE_NAME = settings.BASE_DIR + '/monitor.conf'

@csrf_exempt
def index(request):
	if request.method != 'POST':
		return redirect('/login')

	data_dict = json.loads(request.body)
	if data_dict['Type']=='SubscriptionConfirmation':
		raw_url = data_dict['SubscribeURL']
		print urllib2.urlopen(raw_url).read()

	if data_dict['Type'] == 'Notification':
		nexmo_conf =  nexmo_config()
		FROM = dequote(nexmo_conf['NUser'])
		TO = dequote(nexmo_conf['NRecv'])
		EnableSMS = nexmo_conf['EnableSMS'].lower()
		data = json.loads(data_dict['Message'])
		msg = "ALRM:",data['AlarmName'],":",data['NewStateReason']
		msg = ''.join(msg)
		if EnableSMS=='on':
			conn = nexmo.Client(key=str(nexmo_conf['NKey']),secret=str(nexmo_conf['NSecret']))
			conn.send_message({'from':FROM,'to':TO,'text':msg})
		
		return HttpResponse("200")



def settings(request):
	c = {}
	c.update(csrf(request))
	try:
		if 'logged_in' not in request.session:
			return redirect('/login')
	except:
		return redirect('/login')
		
	if request.method == 'GET':
		nexmo_conf = nexmo_config()
		return render_to_response('settings.htm',{'nxmo_conf':nexmo_conf},context_instance=RequestContext(request))
	
	if request.method == 'POST':
		nxmo_conf = nexmo_config()
		Error = False
		if trim(request.POST['NKey']) is None or trim(request.POST['NKey']) == '':
			Error = True
			messages.error(request,"Please enter the Nexmo API Key!")
			
		if trim(request.POST['NSecret']) is None or trim(request.POST['NSecret']) == '':
			Error = True
			messages.error(request,"Please enter the Nexmo Secret!")
			
		if trim(request.POST['NRecv']) is None or trim(request.POST['NRecv']) == '':
			Error = True
			messages.error(request,"Please enter the Phone Number!")
		if trim(request.POST['NRecv']):

			if not request.POST['NRecv'].isnumeric():
				Error = True
				messages.error(request,"Please enter the valid Phone Number!.")
				
			if len(trim(request.POST['NRecv']))<=10:
				Error = True
				messages.error(request,"Phone Number should combination with country code.")
				
		if trim(request.POST['UserName']) is None or trim(request.POST['UserName']) == '':
			Error = True
			messages.error(request,"Please enter the Username!")

		if trim(request.POST['password']) is None or trim(request.POST['password']) == '':
			Error = True
			messages.error(request,"Please enter the Password!")
			
		if Error == True:
			return render_to_response('settings.htm',{'nxmo_conf':nxmo_conf},context_instance=RequestContext(request))

		try:
			conn = nexmo.Client(key=str(request.POST['NKey']),secret=str(request.POST['NSecret']))
			json_number =  conn.get_account_numbers()
			from_number = json_number['numbers'][0]['msisdn']
		except:
			messages.error(request,"Please enter a valid Nexmo API Key and Secret!")
			return render_to_response('settings.htm',{'nxmo_conf':nxmo_conf},context_instance=RequestContext(request))
		
		myvar = ''
		myvar +='api_key='+request.POST['NKey']+"\n"
		myvar +='secret_key='+request.POST['NSecret']+"\n"
		myvar +='fromuser='+str(from_number)+"\n"
		myvar +='touser='+request.POST['NRecv']+"\n"
		if 'EnableSMS' in request.POST:
			myvar +='EnableSMS='+request.POST['EnableSMS']+"\n"
		else:
			myvar +='EnableSMS=0\n'
		myvar +='username='+request.POST['UserName']+"\n"
		myvar +='password='+request.POST['password']+"\n"
		
		with open(FILE_NAME, 'w') as f:
			my = File(f)
			my.write('[nexmo_monitor]\n')
			my.write(myvar)
			
		f.close()
		my.close()
		nxmo_conf = nexmo_config()
		messages.success(request,"Your data is saved successfully.")
		return render_to_response('settings.htm',{'nxmo_conf':nxmo_conf},context_instance=RequestContext(request))

def config_reader(key):
	try:
		if os.path.exists(FILE_NAME):
			config = ConfigParser.RawConfigParser()
			config.read(FILE_NAME)
			return config.get('nexmo_monitor', key).strip()
		else:
			print "Configuration file does not exist."
	except Exception as err:
		print str(err)

def nexmo_config():
	nxmo_conf={}
	nxmo_conf['NKey']=config_reader('api_key')
	nxmo_conf['NSecret']=config_reader('secret_key')
	nxmo_conf['NUser']=config_reader('fromuser')
	nxmo_conf['NRecv']=config_reader('touser')
	nxmo_conf['EnableSMS']=config_reader('EnableSMS')
	nxmo_conf['username']=config_reader('username')
	nxmo_conf['password']=config_reader('password')
	return nxmo_conf
	
def dequote(str):
	if str.startswith(("'", '"')):
		return str[1:-1]
	return str
	
def trim(strn):
		if strn:
			return strn.strip()
		return strn
		
def login(request):
	if request.method == 'GET':
		return render_to_response('login.htm',{},context_instance=RequestContext(request))
	if request.method == 'POST':
		if request.POST['NKey']==config_reader('username') and request.POST['NSecret']==config_reader('password'):
			request.session['logged_in']=True
			return redirect("/settings/")
		else:
			messages.error(request,"Invalid login credentials.")
			return render_to_response('login.htm',{},context_instance=RequestContext(request))
		
def logout(request):
	try:
		if request.session['logged_in']:
			del(request.session['logged_in'])
		return redirect('/login/')
	except:
		return redirect('/login/')
