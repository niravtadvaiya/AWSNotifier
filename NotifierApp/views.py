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
<<<<<<< HEAD
		FROM = dequote(nexmo_conf['NUser'])
=======
		FROM = dequote(nexmo_conf['NexmoFrom'])
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
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
<<<<<<< HEAD
		nxmo_conf = nexmo_config()
		Error = False
		if trim(request.POST['NKey']) is None or trim(request.POST['NKey']) == '':
			Error = True
			messages.error(request,"Please enter the Nexmo API Key!")
			
		if trim(request.POST['NSecret']) is None or trim(request.POST['NSecret']) == '':
			Error = True
			messages.error(request,"Please enter the Nexmo Secret!")
			
		if trim(request.POST['NSecret']) and trim(request.POST['NKey']):
			try:
				conn = nexmo.Client(key=str(request.POST['NKey']),secret=str(request.POST['NSecret']))
=======
	  try:
		nxmo_conf = nexmo_config()
		for k,v in nxmo_conf.iteritems():
			if v is '':
				nxmo_conf[k]=request.POST[k]

		Error = False
		recv = ''.join(request.POST['NRecv'].split())
		recv = recv.replace('+','')
		recv = recv.replace('-','')

		api_key = request.POST['NKey'].strip()
		api_secret = request.POST['NSecret'].strip()

		if trim(api_key) and trim(api_secret):
			try:
				conn = nexmo.Client(key=str(api_key),secret=str(api_secret))
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
				json_number =  conn.get_account_numbers()
				from_number = json_number['numbers'][0]['msisdn']
			except:
				messages.error(request,"Please enter a valid Nexmo API Key and Secret!")
				return render_to_response('settings.htm',{'nxmo_conf':nxmo_conf},context_instance=RequestContext(request))
<<<<<<< HEAD
		
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

=======

		from_number = request.POST['NexmoFrom']
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
		myvar = ''
		myvar +='api_key='+request.POST['NKey']+"\n"
		myvar +='secret_key='+request.POST['NSecret']+"\n"
		myvar +='fromuser='+str(from_number)+"\n"
<<<<<<< HEAD
		myvar +='touser='+request.POST['NRecv']+"\n"
=======
		myvar +='touser='+recv+"\n"
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
		if 'EnableSMS' in request.POST:
			myvar +='EnableSMS='+request.POST['EnableSMS']+"\n"
		else:
			myvar +='EnableSMS=0\n'
		myvar +='username='+request.POST['UserName']+"\n"
		myvar +='password='+request.POST['password']+"\n"
		
<<<<<<< HEAD
=======
		
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
		with open(FILE_NAME, 'w') as f:
			my = File(f)
			my.write('[nexmo_monitor]\n')
			my.write(myvar)
			
		f.close()
		my.close()
		nxmo_conf = nexmo_config()
		messages.success(request,"Your data is saved successfully.")
		return render_to_response('settings.htm',{'nxmo_conf':nxmo_conf},context_instance=RequestContext(request))
<<<<<<< HEAD
=======
	  except Exception as err:
		messages.error(request,"We find some errors." + str(err))
		return render_to_response('settings.htm',{'nxmo_conf':nxmo_conf},context_instance=RequestContext(request))
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c

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
<<<<<<< HEAD
	nxmo_conf['NUser']=config_reader('fromuser')
=======
	nxmo_conf['NexmoFrom']=config_reader('fromuser')
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
	nxmo_conf['NRecv']=config_reader('touser')
	nxmo_conf['EnableSMS']=config_reader('EnableSMS')
	nxmo_conf['username']=config_reader('username')
	nxmo_conf['password']=config_reader('password')
<<<<<<< HEAD
=======
	
	
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
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
<<<<<<< HEAD
=======
		username  = request.POST['NKey'].strip()
		password  = request.POST['NSecret'].strip()
		if username == '' and password == '':
			messages.error(request,"Please enter the Username and Password.")
			return render_to_response('login.htm',{},context_instance=RequestContext(request))
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
		if request.POST['NKey']==config_reader('username') and request.POST['NSecret']==config_reader('password'):
			request.session['logged_in']=True
			return redirect("/settings/")
		else:
<<<<<<< HEAD
			messages.error(request,"Invalid login credentials.")
=======
			messages.error(request,"Please enter valid Username and Password.")
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
			return render_to_response('login.htm',{},context_instance=RequestContext(request))
		
def logout(request):
	try:
		if request.session['logged_in']:
			del(request.session['logged_in'])
		return redirect('/login/')
	except:
		return redirect('/login/')

@csrf_exempt	
def ajax_validator(request):
	if 'logged_in' not in request.session:
		return HttpResponse("you are not logged in")
	
<<<<<<< HEAD
	api_key = request.POST['NKey']
	api_secret = request.POST['NSecret'] 
	django_html = []
	get_num  = None
	if not api_key and  not api_secret:
		return HttpResponse("Please enter a valid Nexmo API Key and Secret!")
	if not api_key:
		return HttpResponse("Please enter a valid Nexmo API Key!")
	if not api_secret:
		return HttpResponse("Please enter a valid Nexmo Secret!")
	try:
		conn = nexmo.Client(key=str(api_key),secret=str(api_secret))
		json_number =  conn.get_account_numbers()
		from_number = json_number['numbers']
		for from_number in json_number['numbers']:
			get_num += '<input type="radio" name="from_number" value="%s"/>' %from_number['msisdn']
		django_html.append({'error':'false','html':get_num})
		return HttpResponse(from_number)
	except Exception as err:
		return HttpResponse(str(err))
=======
	api_key = request.POST['NKey'].strip()
	api_secret = request.POST['NSecret'].strip()
	django_html = []
	get_num  = None
	if api_secret is not '' and api_key is not '':
		try:
			conn = nexmo.Client(key=str(api_key),secret=str(api_secret))
			json_number =  conn.get_account_numbers()
			from_number = json_number['numbers']
			get_num = []
			for from_number in json_number['numbers']:
				if from_number['msisdn'].strip() is not None:
					get_num.append(from_number['msisdn'])
			
			msisdn = ','.join(get_num)
			django_html = {'error':'false','html':msisdn}
			return HttpResponse(json.dumps(django_html))
		except nexmo.AuthenticationError as err:
			django_html = {'error':'true','html':"Please enter valid Nexmo Key and Secret."}
			return HttpResponse(json.dumps(django_html))
		except Exception as err:
			django_html = {'error':'true','html':str(err)}
			return HttpResponse(json.dumps(django_html))
>>>>>>> c3b3e3206355290b64bbd291f76241588ebdcd0c
