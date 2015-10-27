from __future__ import absolute_import
from django.views import generic
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from .forms import RegistrationForm, LoginForm, PatientForm, PatientHealthConditionsForm, TempPatientDataForm, EMedicationForm
from django.template import RequestContext
from django.views.generic import ListView
from .models import PermissionsRole, Patient, PatientHealthConditions, TempPatientData, Alert,PatientAppt, Doctor, EMedication
from django.shortcuts import render_to_response
from .forms import PatientApptForm
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


STAFF_APPROVAL_ROLES = ('admin', 'doctor', 'staff', 'nurse', 'lab')



def AlertSender(request):
	#This method should be responsible for sending an alert to the doctor and HSP staff when the patient requests and alert to be sent

	print 'inside alert sender'
	patient_model = Patient.objects.get(user__username=request.user.username)
	health_conditions_model = PatientHealthConditions.objects.get(user=patient_model)
	patient_data_information = TempPatientData.objects.get(user__username=request.user.username)

	total_health_condition_level =  (health_conditions_model.nausea_level +
									health_conditions_model.hunger_level +
									health_conditions_model.anxiety_level+
									health_conditions_model.stomach_level+
									health_conditions_model.body_ache_level+
									health_conditions_model.chest_pain_level)

	# print 'The current user that is being evaluated is ' + patient_data_information.user.username
	# print 'The level of the health conditison for total is ' + str(total_health_condition_level)

	#If this is a post method requested by the user, then execute the following logic
	if request.method == 'POST':

		desc = request.POST.get('desc')

		if desc is None:
			desc = "NO DESCRIPTION"

		#instantiate an alert model for the user
		alert_model = Alert(alert_patient = patient_model, alert_description = desc, alert_level = total_health_condition_level)
		patient_model.alertSent = 1
		patient_model.save()
		alert_model.save()

	# return render(request, '/accounts/portal/')
	return redirect(reverse('Portal'))

'''
Homepage to display the main control panel or HomePage based on user authentication
'''

def HomePageView(request):



	#Model Definitions & Declarations
	permissionModel = PermissionsRole
	patientModel = Patient

	#temp data for the user has been found
	tempDataFound = 0

	#Assign default permission role
	permissionRoleForUser = 'pending'

	#Assign a default approval rating
	approval = 0

	#Assign a default authentication boolean
	authenticated = False

	# approvalSwitch = 0

	#Check to see if the user has logged into the system or not
	if request.user.is_authenticated():

		#Boolean to ensure valid request authentication
		authenticated = True

		#Attempt a DB query on the request object
		if permissionModel.objects.filter(user__username=request.user.username)[:1].exists():

			#If request object from query exists, create a variable assignment on that object
			permissionRoleForUser = permissionModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the logged in person is a patient, grab request object, make a query and grab the approval integer
			if patientModel.objects.filter(user__username=request.user.username)[:1].exists():

				#Get an integer declaraction for the approval of the user
				approvalSwitch = patientModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the person is a hospital member, then they will automatically be considered approved
			if (permissionRoleForUser.role in STAFF_APPROVAL_ROLES):
				approval = 1
			else:
				if patientModel.objects.filter(user__username=request.user.username)[:1].exists():
					approval = approvalSwitch.approved
				else:
					approval = 0

	#Under the instance that the user is not authenticated
	else:
		permissionRoleForUser = ""



	return render( request, 'index.html', {'permissionModel': permissionModel, 'user': request.user, 'roles': permissionRoleForUser, 'approval': approval, 'authenticated': authenticated})


'''''''''''''''''''''''''''''''''''''''''''''''''''
Basic success page response rendering for the user
'''''''''''''''''''''''''''''''''''''''''''''''''''

class SuccessPageView(generic.TemplateView):
	template_name = 'accounts/success.html'

'''''''''''''''''''''''''''''''''''''''''''''''''''
Sign up view used to register a user into the system
'''''''''''''''''''''''''''''''''''''''''''''''''''

class SignUpView(generic.CreateView):

	form_class = RegistrationForm
	model = User
	template_name = 'register.html'
	success_url = reverse_lazy('Success')


'''''''''''''''''''''''''''''''''''''''''''''''''''
Login view for the user to redirect into the patient/admin portal
'''''''''''''''''''''''''''''''''''''''''''''''''''

class LoginView(generic.FormView):
	form_class = LoginForm
	success_url = reverse_lazy('Portal')
	template_name = 'login.html'

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)

		if user is not None and user.is_active:
			login(self.request, user)
			return super(LoginView, self).form_valid(form)
		else:
			return self.invalid(form)

def PatientPortalView(request):
	# template_name = 'home.html'
	#Model Definitions & Declarations
	permissionModel = PermissionsRole
	patientModel = Patient
	userModel = User
	tempModel = TempPatientData
	conditions_complete = False
	patient_model = Patient
	conditions_model = PatientHealthConditions
	alert_model = Alert

	approvalSwitch = 0

	#Assign default permission role
	permissionRoleForUser = 'pending'

	#Assign a default approval rating
	approval = 0

	#Assign a default authentication boolean
	authenticated = False

	patient = -1

	total_health_condition_level = 0


	#If user has already sent an alert request
	alert_sent = 0

	#Check to see if the user has logged into the system or not
	if request.user.is_authenticated():

		if patient_model.objects.filter(user__username=request.user.username)[:1].exists():
			patient = patient_model.objects.filter(user__username=request.user.username)[:1].get()
			print 'about to set alert sent'
			if Alert.objects.filter(alert_patient=patient)[:1].exists():
				alert_sent = 1
				patient.alertSent = 1
				patient.save()
			else:
				alert_sent = patient.alertSent

		if conditions_model.objects.filter(user=patient)[:1].exists():
			conditions_complete = True
			patient_conditions = conditions_model.objects.filter(user=patient)[:1].get()

			total_health_condition_level =  (patient_conditions.nausea_level +
											patient_conditions.hunger_level +
											patient_conditions.anxiety_level+
											patient_conditions.stomach_level+
											patient_conditions.body_ache_level+
											patient_conditions.chest_pain_level)


			if (total_health_condition_level >= 40 and alert_sent == 0 and not Alert.objects.filter(alert_patient=patient)[:1].exists()):
				patient.alertSent = 1
				alert_sent = 1
				alert_model = Alert(alert_patient = patient, alert_description = 'SENT BY HOSPITAL SYSTEM', alert_level = total_health_condition_level)
				alert_model.save()
				patient.save()

			if (total_health_condition_level < 40 and alert_sent == 0):
				if Alert.objects.filter(alert_patient=patient)[:1].exists():
					alert_model = Alert.objects.filter(alert_patient=patient)[:1].get()
					alert_model.delete()

			#If there is no alert for the user, set the status to 0
			if not Alert.objects.filter(alert_patient=patient)[:1].exists() and patient_model.objects.filter(user__username=request.user.username)[:1].exists():
				patient.alertSent = 0
				patient.save()

			#If there health conditions are
			if (total_health_condition_level < 40 and alert_sent == 1):
				if Alert.objects.filter(alert_patient=patient)[:1].exists():
					alert_model = Alert.objects.filter(alert_patient=patient)[:1].get()
					if alert_model.alert_description == 'SENT BY HOSPITAL SYSTEM':
						# alert_model = alert_model.objects.filter(alert_patient=patient)[:1].get()
						alert_model.delete()
						patient.alertSent = 0
						patient.save()

			#If there health conditions are
			if (total_health_condition_level > 40 and alert_sent == 1 and not Alert.objects.filter(alert_patient=patient)[:1].exists()):
				if Alert.objects.filter(alert_patient=patient)[:1].exists():
					patient.alertSent = 1
					alert_sent = 1
					alert_model = Alert(alert_patient = patient, alert_description = 'SENT BY HOSPITAL SYSTEM', alert_level = total_health_condition_level)
					alert_model.save()
					patient.save()



		#Boolean to ensure valid request authentication
		authenticated = True

		#Attempt a DB query on the request object
		if permissionModel.objects.filter(user__username=request.user.username)[:1].exists():

			#If request object from query exists, create a variable assignment on that object
			permissionRoleForUser = permissionModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the logged in person is a patient, grab request object, make a query and grab the approval integer
			if patientModel.objects.filter(user__username=request.user.username)[:1].exists():

				#Get an integer declaraction for the approval of the user
				approvalSwitch = patientModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the person is a hospital member, then they will automatically be considered approved
			if (permissionRoleForUser.role in STAFF_APPROVAL_ROLES):
				approval = 1
			else:
				approval = approvalSwitch.approved

	#Under the instance that the user is not authenticated
	else:
		permissionRoleForUser = ""

	tempUserInformation = ""
	if tempModel.objects.filter(user=request.user)[:1].exists():
		tempUserInformation = tempModel.objects.filter(user=request.user)[:1].get()

	form = TempPatientDataForm()

	if request.method == "POST":

		form = TempPatientDataForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.data_sent = 1
			instance.email_address = request.user.username
			instance.save()
			return HttpResponseRedirect('formsuccess')

	#Get an array for allergies

	if not request.user.username == "admin" and approval == 1 and not permissionRoleForUser.role == 'doctor':

		if tempUserInformation.allergies is not None:
			allergens = tempUserInformation.allergies.split(",")

		if tempUserInformation.medications is not None:
			med_conditions = tempUserInformation.medications.split(",")
	else:
		allergens = ""
		med_conditions =""


	alerts_count = Alert.objects.all().count()

	doc_name = ''
	appts = ''
	if (not permissionRoleForUser == 'pending' and permissionRoleForUser.role == 'doctor'):

		doc_obj = Doctor.objects.filter(doctor_user=request.user).get()

		doc_name = doc_obj.doctor_first_name + ' ' + doc_obj.doctor_last_name

		appts = PatientAppt.objects.filter(doctor=doc_obj, resolved=0).count()

		if appts == 0:
			appts = 'No Appointments'

	current_patient = ''

	if (not tempUserInformation == ''):
		if (Patient.objects.filter(fill_from_application=tempUserInformation).exists()):
			current_patient = Patient.objects.filter(fill_from_application=tempUserInformation).get()

	context = {

		'form': form,
		'permissionModel': permissionModel,
		'user': request.user,
		'roles': permissionRoleForUser,
		'approval': approval,
		'authenticated': authenticated,
		'conditions_complete': conditions_complete,
		'temp_user_data': tempUserInformation,
		'allergens': allergens,
		'med_conditions':med_conditions,
		'alert_sent':alert_sent,
		'alerts_count':alerts_count,
		'doc_name' : doc_name,
		'appts' : appts,
		'current_patient' : current_patient
	}

	return render(request, 'portal.html', context)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
View that is responsible for rendering the patient scheduling system for the user
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def ScheduleView(request):

	title = "Appointment Schedule"
	form = PatientApptForm(request.POST or None)
	patient_model = Patient

	patient = patient_model.objects.filter(user__username=request.user.username)[:1].get()

	conditions_complete = False

	conditions_model = PatientHealthConditions
	if (conditions_model.objects.filter(user=patient)[:1].exists()):
		conditions_complete = True
		patient_conditions = conditions_model.objects.filter(user=patient)[:1].get()

	if form.is_valid():
		instance = form.save(commit=False)
		instance.patient = patient
		instance.user = patient
		instance.current_health_conditions = patient_conditions
		instance.save()
		return HttpResponseRedirect('formsuccess')

	context = {
		"form": form,
		"template_title": title,
		"conditions_complete": conditions_complete
	}
	return render(request, 'schedule.html', context)

def HealthConditionsView(request):

	title = "Health Conditions"
	form = PatientHealthConditionsForm(request.POST or None)

	conditions_model = PatientHealthConditions
	patient_model = Patient

	data_exists = False

	#Check if the health conditions already exist within the database
	if patient_model.objects.filter(user__username=request.user.username)[:1].exists():
		patient = patient_model.objects.filter(user__username=request.user.username)[:1].get()

		if conditions_model.objects.filter(user=patient)[:1].exists():
			instance = conditions_model.objects.filter(user=patient)[:1].get()
			form = PatientHealthConditionsForm(instance=instance)
			data_exists = True

	if request.method == "POST":

		if conditions_model.objects.filter(user=patient)[:1].exists():
			instance = conditions_model.objects.filter(user=patient)[:1].get()
			form = PatientHealthConditionsForm(request.POST, instance=instance)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = patient
			instance.save()
			return HttpResponseRedirect('formsuccess')


	context = {
		"form": form,
		"template_title": title
	}

	return render(request, 'healthconditions.html', context)

#View that allows the admin user or employee to search for a patient
def PatientSearch(request):

	user_has_been_located = False

	patient_model = Patient #Perform queries on the database model that holds all the patient information

	search_data_list = ""

	patient_found = ''

	#Grab the post param information so that you can perform iteration logic through the database on the searchable customer
	if request.method == "POST":
		search_data = request.POST.get("search_data", "") #store the data of the user search information into a variable that you can parse
		db_search_type = request.POST.get("db_search_type", "")

		search_data_list = search_data.split(" ") #If there is more than one entry in the search bar, parse it as necessary

		#Check to see if the inputted email matches any of the patient emails in the databases
		if db_search_type == "email":
			if patient_model.objects.filter(fill_from_application__email_address__iexact=search_data_list[0]).exists():
				patient_found = patient_model.objects.filter(fill_from_application__email_address__iexact=search_data_list[0]).get()
				search_data_list.append(patient_found)
				user_has_been_located = True

		elif db_search_type == "firstlast":
			if patient_model.objects.filter(fill_from_application__first_name__iexact=search_data_list[0]).exists() and patient_model.objects.filter(fill_from_application__last_name__iexact=search_data_list[1]).exists():
				patient_found = patient_model.objects.filter(fill_from_application__first_name__iexact=search_data_list[0], fill_from_application__last_name__iexact=search_data_list[1]).all()
				search_data_list.append(patient_found)
				user_has_been_located = True

	if search_data_list == "":

		context = {

			'search_data': 'none',
			'located': user_has_been_located
		}

	elif user_has_been_located == True:


		context = {

			'search_data': search_data_list,
			'temp_user_data': patient_found,
			'located': user_has_been_located
		}

	else:

		context = {

			'search_data': search_data_list,
			'temp_user_data': patient_found,
			'located': user_has_been_located
		}

	return render(request, 'search.html', context)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
View that forces request object to log out of the system
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def DeleteUser(request):

	patient_model = Patient

	if request.method == "POST":
		pk_id = request.POST.get("pk", "")
		if patient_model.objects.filter(id=pk_id).exists():
			found_patient_object = patient_model.objects.filter(id=pk_id).get()
			found_patient_object.delete()

	context = {

		'pk_id': pk_id
	}

	return render(request, 'deleted.html', context)

def EmergencyAlerts(request):

	#Model Definitions & Declarations
	permissionModel = PermissionsRole
	patientModel = Patient
	userModel = User
	tempModel = TempPatientData
	conditions_complete = False
	patient_model = Patient
	conditions_model = PatientHealthConditions
	alert_model = Alert

	#Check to see if the user has logged into the system or not
	if request.user.is_authenticated():

		#Boolean to ensure valid request authentication
		authenticated = True

		#Attempt a DB query on the request object
		if permissionModel.objects.filter(user__username=request.user.username)[:1].exists():

			#If request object from query exists, create a variable assignment on that object
			permissionRoleForUser = permissionModel.objects.filter(user__username=request.user.username)[:1].get()

			#If the person is a hospital member, then they will automatically be considered approved
			if (permissionRoleForUser.role in STAFF_APPROVAL_ROLES):
				approval = 1
			else:
				approval = 0

	#Under the instance that the user is not authenticated
	else:
		permissionRoleForUser = ""

	alerts_count = Alert.objects.all().count()
	all_alerts = Alert.objects.all()

	context = {

		'roles': permissionRoleForUser,
		'alerts_count':alerts_count,
		'alerts': all_alerts
	}

	return render(request, 'view_alerts.html', context)


#This is the view that is going to be used to update the account information for the user
def UpdateAccountView(request):
	title = "Update Account Information"
	form = TempPatientDataForm(request.POST or None)
	patient_model = Patient


	patient = patient_model.objects.filter(user=request.user)[:1].get()

	if (TempPatientData.objects.filter(user=request.user)[:1].exists()):

		instance = TempPatientData.objects.filter(user=request.user)[:1].get()
		form = TempPatientDataForm(instance = instance)

	if request.method == "POST":

		TPD = TempPatientData.objects.filter(user=request.user)[:1].get()

		if (not TPD is None):
			instance = TempPatientData.objects.filter(user=request.user)[:1].get()

			# form = TempPatientDataForm(request.POST, instance = instance)

		form = TempPatientDataForm(request.POST, instance = TPD)
		if form.is_valid():

			form.save()
		else:
			print form.errors
		return HttpResponseRedirect('/accounts/portal/update_account/')


	context = {
		"form": form,
		"template_title": title
	}
	return render(request, 'update_account.html', context)

def CreateEmployeeView(request):

	#Grab the post parameters for the following data

	if request.method == "POST":
		user_name = request.POST.get('username')
		password = request.POST.get('password')
		staff_type = request.POST.get('staff_type')
		role = request.POST.get('role')

	user_model = User

#This view is responsible for quering all the currently existent appts for a user in the database and displaying the data to the page
def ApptView(request):

	current_appts_list = []

	#First you need to get the current patient to associate the patient with the appts
	current_patient = Patient.objects.filter(user=request.user)[:1].get()

	#Now you need to find all the appts that are associated with the current user who is logged in
	if (PatientAppt.objects.filter(user=current_patient)[:1].exists()):
		current_appts = PatientAppt.objects.filter(user=current_patient).all()
		for appts in current_appts:
			current_appts_list.append(appts)

	context = {

		'current_appts_list': current_appts_list,
		'current_patient': current_patient
	}

	return render(request, 'view_appts.html', context)

def GenerateStatsView(request):


	roles = PermissionsRole.objects.filter(user__username=request.user.username)[:1].get()

	#GENDER
	total_patients = TempPatientData.objects.filter().count()

	num_males = (float(TempPatientData.objects.filter(gender='male').count())/float(total_patients))*100
	num_females = (float(TempPatientData.objects.filter(gender='female').count())/float(total_patients))*100
	num_other = (float(TempPatientData.objects.filter(gender='other').count())/float(total_patients))*100
	num_PNTS = (float(TempPatientData.objects.filter(gender='prefer not to say').count())/float(total_patients))*100
	num_males = format(num_males, '.2f')
	num_females = format(num_females, '.2f')
	num_other = format(num_other, '.2f')
	num_PNTS = format(num_PNTS, '.2f')

	#RACE
	num_white = (float(TempPatientData.objects.filter(race='white').count())/float(total_patients))*100
	num_white = format(num_white, '.2f')
	num_indian = (float(TempPatientData.objects.filter(race='american_indian_alaskan_native').count())/float(total_patients))*100
	num_indian = format(num_indian, '.2f')
	num_hawaiian = (float(TempPatientData.objects.filter(race='hawaiian').count())/float(total_patients))*100
	num_hawaiian = format(num_hawaiian, '.2f')
	num_black = (float(TempPatientData.objects.filter(race='black').count())/float(total_patients))*100
	num_black = format(num_black, '.2f')
	num_asian = (float(TempPatientData.objects.filter(race='asian').count())/float(total_patients))*100
	num_asian = format(num_asian, '.2f')
	num_other_race = (float(TempPatientData.objects.filter(race='other').count())/float(total_patients))*100
	num_other_race = format(num_other_race, '.2f')


	#INCOME
	num_1 = (float(TempPatientData.objects.filter(income='$0-$10,000').count())/float(total_patients))*100
	num_1 = format(num_1, '.2f')
	num_2 = (float(TempPatientData.objects.filter(income='$10,001-$30,000').count())/float(total_patients))*100
	num_2 = format(num_2, '.2f')
	num_3 = (float(TempPatientData.objects.filter(income='$30,001-$60,000').count())/float(total_patients))*100
	num_3 = format(num_3, '.2f')
	num_4 = (float(TempPatientData.objects.filter(income='$60,001-$85,000').count())/float(total_patients))*100
	num_4 = format(num_4, '.2f')
	num_5 = (float(TempPatientData.objects.filter(income='$85,001-$110,000').count())/float(total_patients))*100
	num_5 = format(num_5, '.2f')
	num_6 = (float(TempPatientData.objects.filter(income='$110,001+').count())/float(total_patients))*100
	num_6 = format(num_6, '.2f')
	num_7 = (float(TempPatientData.objects.filter(income='Prefer Not To Say').count())/float(total_patients))*100
	num_7 = format(num_7, '.2f')

	#AGE
	age_1 = (float(TempPatientData.objects.filter(age__range=(0,19)).count())/float(total_patients))*100
	age_1 = format(age_1, '.2f')

	age_2 = (float(TempPatientData.objects.filter(age__range=(19,45)).count())/float(total_patients))*100
	age_2 = format(age_2, '.2f')

	age_3 = (float(TempPatientData.objects.filter(age__range=(45,61)).count())/float(total_patients))*100
	age_3 = format(age_3, '.2f')

	age_4 = (float(TempPatientData.objects.filter(age__range=(61,130)).count())/float(total_patients))*100
	age_4 = format(age_4, '.2f')

	#HOSPITAL CASES RESOLVED
	total_cases = PatientAppt.objects.filter().count()

	if (not total_cases == 0):

		resolved_cases = (float(PatientAppt.objects.filter(resolved=1).count())/float(total_cases))*100
		resolved_cases = format(resolved_cases, '.2f')

		unresolved_cases = (float(PatientAppt.objects.filter(resolved=0).count())/float(total_cases))*100
		unresolved_cases = format(unresolved_cases, '.2f')
	else:
		resolved_cases = 0
		unresolved_cases = 0

	context = {

		'roles' : roles,
		'num_males' : num_males,
		'num_females' : num_females,
		'num_other' : num_other,
		'num_PNTS' : num_PNTS,
		'total_patients' : total_patients,
		'num_white' : num_white,
		'num_indian' : num_indian,
		'num_hawaiian' : num_hawaiian,
		'num_black' : num_black,
		'num_asian' : num_asian,
		'num_other_race' : num_other_race,
		'num_1' : num_1,
		'num_2' : num_2,
		'num_3' : num_3,
		'num_4' : num_4,
		'num_5' : num_5,
		'num_6' : num_6,
		'num_7' : num_7,
		'age_1' : age_1,
		'age_2' : age_2,
		'age_3' : age_3,
		'age_4' : age_4,
		'unresolved_cases' : unresolved_cases,
		'resolved_cases' : resolved_cases
	}

	return render(request, 'stats.html', context)

def PatientDataView(request):

	#get permissions of current user
	roles = PermissionsRole.objects.filter(user=request.user)[:1].get()
	patients = ''

	if roles.role == 'doctor':
		current_doctor = Doctor.objects.filter(doctor_user=request.user)
		patients = PatientAppt.objects.filter(doctor=current_doctor).all()
		if PatientAppt.objects.filter(doctor=current_doctor).count() == 0:
			patients = 0
		else:
			print patients

	context = {

		'roles' : roles,
		'patients' : patients

	}

	return render(request, 'view_patients.html', context)

def ScheduledDoctorAppointments(request):

	current_doctor = ''
	relevant_appts = ''
	roles 		   = ''

	if (Doctor.objects.filter(doctor_user = request.user).exists()):
		current_doctor = Doctor.objects.filter(doctor_user = request.user).get()
		relevant_appts = PatientAppt.objects.filter(doctor = current_doctor)
		roles = PermissionsRole.objects.filter(user__username=request.user.username)[:1].get()


	context = {

		'current_doctor' : current_doctor,
		'relevant_appts' : relevant_appts,
		'roles'          : roles
	}

	return render(request, 'doctor_scheduled_appointments.html', context)

def ResolvedPatientAjaxView(request):

	current_appt_num = ''
	current_appt = ''

	if request.is_ajax() or request.method == 'POST':

		primary_key_val = request.POST.get('appt_id')
		print primary_key_val

		if PatientAppt.objects.filter(pk=primary_key_val).exists():
			current_appt = PatientAppt.objects.filter(pk=primary_key_val).get()

			if (current_appt.resolved == 0):
				current_appt.resolved = 1
				current_appt.save()
				current_appt_num = current_appt.resolved

			elif (current_appt.resolved == 1):
				current_appt.resolved = 0
				current_appt.save()
				current_appt_num = current_appt.resolved

	current_doctor = ''
	relevant_appts = ''
	roles 		   = ''

	if (Doctor.objects.filter(doctor_user = request.user).exists()):
		current_doctor = Doctor.objects.filter(doctor_user = request.user).get()
		relevant_appts = PatientAppt.objects.filter(doctor = current_doctor)
		roles = PermissionsRole.objects.filter(user__username=request.user.username)[:1].get()

	context = {

		'current_doctor' : current_doctor,
		'relevant_appts' : relevant_appts,
		'roles'          : roles,
		'current_appt'   : current_appt,
		'current_appt_num' : current_appt_num
	}

	return HttpResponseRedirect(reverse("ScheduledDoctorAppointments"))

def MedicalHistoryView(request):

	if request.method == "POST" and 'pk_patient' in request.POST:

		patient_primary_key = request.POST.get('pk_patient', '')

		patient_appts = PatientAppt.objects.filter(pk=patient_primary_key).all()

		patient_obj = patient_appts[0].user

		patient_appts = PatientAppt.objects.filter(user=patient_obj).all()

		allergies = patient_obj.fill_from_application.allergies
		medications = patient_obj.fill_from_application.medications

		allergies = allergies.split(',')
		medications = medications.split(',')

		context = {

			'appts' : patient_appts,
			'patient' : patient_obj,
			'temp_user_data' : patient_obj.fill_from_application,
			'allergies' : allergies,
			'medications' : medications
		}

	elif request.method == "POST" and 'pk_patient2' in request.POST:

		patient_primary_key = request.POST.get('pk_patient2', '')
		print patient_primary_key

		# current_patient = Patient.objects.filter(user_id=patient_primary_key).get()

		if (Patient.objects.filter(id=patient_primary_key).exists()):
			print 'EXISTS'
			current_patient = Patient.objects.filter(id=patient_primary_key).get()
			print 'assigned based on user key'
		elif (Patient.objects.filter(pk=patient_primary_key).exists()):
			current_patient = Patient.objects.filter(pk=patient_primary_key).get()
			print 'assigned based on primary key'

		patient_appts = PatientAppt.objects.filter(user=current_patient).all()

		patient_obj = current_patient

		patient_appts = PatientAppt.objects.filter(user=patient_obj).all()

		allergies = patient_obj.fill_from_application.allergies
		medications = patient_obj.fill_from_application.medications

		allergies = allergies.split(',')
		medications = medications.split(',')


		context = {

			'appts' : patient_appts,
			'patient' : patient_obj,
			'temp_user_data' : patient_obj.fill_from_application,
			'allergies' : allergies,
			'medications' : medications,
		}


	return render(request, 'med_history.html', context)

def PrescribeMedicationView(request):

	title = "E-Medication Prescribe Form"
	form = EMedicationForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)

		instance.save()
		return HttpResponseRedirect('formsuccess')



	context = {
		"form": form,
		"template_title": title,
	}
	return render(request, 'prescribe.html', context)


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse_lazy('Home'))


class SuccessFormPageView(generic.TemplateView):
	template_name = 'accounts/formsuccess.html'

def appt_delete(request, pk):
	appt = get_object_or_404(PatientAppt,pk=pk)
	if request.method=='POST':
		appt.delete()
	current_appts_list = []
	#First you need to get the current patient to associate the patient with the appts
	current_patient = Patient.objects.filter(user=request.user)[:1].get()

	#Now you need to find all the appts that are associated with the current user who is logged in
	if (PatientAppt.objects.filter(user=current_patient)[:1].exists()):
		current_appts = PatientAppt.objects.filter(user=current_patient).all()
		for appts in current_appts:
			current_appts_list.append(appts)

	context = {

		'current_appts_list': current_appts_list,
		'current_patient': current_patient
	}
	return render(request,'view_appts.html',context)

def doctor_appt_delete(request, pk):
    doctor_appt = get_object_or_404(PatientAppt,pk=pk)
    if request.method=='POST':
        doctor_appt.delete()
	#First you need to get the current doctor to associate the doctor with the appts
	current_doctor = Doctor.objects.filter(doctor_user=request.user)

	if (Doctor.objects.filter(doctor_user = request.user).exists()):
		current_doctor = Doctor.objects.filter(doctor_user = request.user).get()
		relevant_appts = PatientAppt.objects.filter(doctor = current_doctor)
		roles = PermissionsRole.objects.filter(user__username=request.user.username)[:1].get()


	'''context = {

		'current_doctor' : current_doctor,
		'relevant_appts' : relevant_appts,
		'roles'          : roles
	}'''
    return render(request,'doctor_scheduled_appointments.html')
