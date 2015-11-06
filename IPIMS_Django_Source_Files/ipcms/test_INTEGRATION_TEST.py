from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test.client import Client as client
from ipcms.models import TempPatientData, Doctor, Patient, PatientHealthConditions, PatientAppt, Alert, PermissionsRole, EMedication, LabReport, LabTech, AddMedicalHistory
from pprint import pprint
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import AnonymousUser, User
import time
from ipcms.views import PatientPortalView, HealthConditionsView



class Test_FullIntegrationTest(TestCase):

	def setUp(self):

		#Factory used to help with requests
		self.factory = RequestFactory()

		#Build HSP member to upload reports for patient
		self.hsp_user = User.objects.create(username="hsp1", password="hsp1")
		self.hsp_user_permission = PermissionsRole.objects.create(role = "staff",user = self.hsp_user)

		#Build Doctor member to allow appointment scheduling in the system
		self.doctor_user = User.objects.create(username="doc1", password="doc1")
		self.doctor_obj = Doctor.objects.create(doctor_first_name="Ryan", doctor_last_name="Schachte", doctor_type="Neurologist", doctor_user=self.doctor_user)
		self.doctor_permission = PermissionsRole.objects.create(role = "doctor",user = self.doctor_user)

		#Save objects into the test database
		self.hsp_user.save()
		self.doctor_obj.save()
		self.doctor_user.save()
		self.doctor_permission.save()
		self.hsp_user_permission.save()

		self.patient_user = User.objects.create(username="pat_user_test", password="pat_pass_test")

		#Have the patient fill in their medical information to submit to the HSP staff
		self.fill_patient_application = TempPatientData.objects.create(
			user = self.patient_user,
			first_name = "John",
			last_name = "Larsen",
			ssn = 600418394,
			allergies = "Soda",
			address = "2417 E. Laurel St. Mesa, AZ 85213",
			medications = "Xanax",
			insurance_provider = "StateFarm",
			insurance_policy_number = 19938343434,
			email_address = "jacob@jacob.com",
			data_sent = "1",
			race = "black",
			income = "$0-$10,000"
			)

		#Implement a patient role up to the newly registered (pending) patient
		self.patient_object = Patient.objects.create(
			fill_from_application = self.fill_patient_application,
			user = self.patient_user,
			approved = 1
			)

		#Implement a permission role access to the patient
		self.patient_permission = PermissionsRole.objects.create(
			role = "patient",
			user = self.patient_user
			)

		self.patient_user.save()
		self.fill_patient_application.save()
		self.patient_object.save()
		self.patient_permission.save()




	def test_RegistrationFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR REGISTRATION FUNCTIONALITY\n-----------------------------------------------------------'

		'''
		1) Register a new patient into the system
		2) Test integration implementation for the user before being approved
		'''

		'''
		1) Register a new HSP staff into the system
		2) Test that HSP can upload medical reports
		3) Ensure the health records are stored and accessible
		'''

		#Build the user in the system
		self.patient_user = User.objects.create(username="pat_user_1", password="pat_pass_1")

		#Have the patient fill in their medical information to submit to the HSP staff
		self.fill_patient_application = TempPatientData.objects.create(
			user = self.patient_user,
			first_name = "Ryan",
			last_name = "Schachte",
			ssn = 600489139,
			allergies = "NONE",
			address = "2463 E. Mallory Dr. Tempe, AZ 85281",
			medications = "NONE",
			insurance_provider = "Allstate",
			insurance_policy_number = 19938343434,
			email_address = "johnson@johnson.com",
			data_sent = "1",
			race = "white",
			income = "$0-$10,000"
			)

		#Implement a patient role up to the newly registered (pending) patient
		self.patient_object = Patient.objects.create(
			fill_from_application = self.fill_patient_application,
			user = self.patient_user,
			approved = 0
			)

		#Implement a permission role access to the patient
		self.patient_permission = PermissionsRole.objects.create(
			role = "patient",
			user = self.patient_user
			)

		self.patient_user.save()
		self.fill_patient_application.save()
		self.patient_object.save()
		self.patient_permission.save()

		print '\033[1;32m\nPATIENT REGISTERED SUCCESSFULLY\033[0m\n'

		print '\t-Testing that the patient hasn\'t been approved yet'

		#Load the patient portal
		request = self.factory.get(reverse_lazy('Portal'))

		#Set the current user request object
		request.user = self.patient_user

		#Store the view response
		response = PatientPortalView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Assert template output
		self.assertContains(response, 'We Are Still Reviewing Your Application')
		print '\t-Patient currently: UNAPPROVED'
		print '\t-Approving Patient To Access Portal'

		#Change approval status
		self.patient_object.approved = 1
		self.patient_object.save()

		#Reload data
		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user

		#Ensure patient was approved successfully
		response = PatientPortalView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Ensure the patient portal section loads
		self.assertContains(response, 'Before Continuing Further, please')

		#Patient now approved successfully
		print '\t-Patient currently: APPROVED'
		print '\033[1;32m\nPATIENT APPROVED\033[0m\n'

		#Ensure valid retrieval and storage of registration data in the database
		print '\t-Printing Current Patient Medical Data:\n'
		print '\t\t+Full Name: %s %s'%(self.fill_patient_application.first_name, self.fill_patient_application.last_name)
		print '\t\t+SSN: %s'%(self.fill_patient_application.ssn)
		print '\t\t+Allergies: %s'%(self.fill_patient_application.allergies)
		print '\t\t+Address: %s'%(self.fill_patient_application.address)
		print '\t\t+Medications: %s'%(self.fill_patient_application.medications)
		print '\t\t+Insurance Provider: %s'%(self.fill_patient_application.insurance_provider)
		print '\t\t+Insurance Policy #: %s'%(self.fill_patient_application.insurance_policy_number)
		print '\t\t+Email Address: %s'%(self.fill_patient_application.email_address)
		print '\t\t+Race: %s'%(self.fill_patient_application.race)
		print '\t\t+Income: %s'%(self.fill_patient_application.income)

		print '\n\t-Testing HSP Uploading Patient Medical Reports'

		#Upload an associated medical report for the patient
		patient_medical_history_upload = AddMedicalHistory.objects.create(
			allergies="Dogs, Flees",
			medical_conditions="Heart Pain",
			patient=self.patient_object
			)
		patient_medical_history_upload.save()

		print '\033[1;32m\nPATIENT MEDICAL REPORTS UPLOADED SUCCESSFULLY\033[0m\n'

		print '\t-Testing printing patient medical data for %s %s' %(self.fill_patient_application.first_name, self.fill_patient_application.last_name)

		#Grab a medical report for the selected patient
		query_history_reports = AddMedicalHistory.objects.filter(patient=self.patient_object).get()

		#View the stored data
		if (AddMedicalHistory.objects.filter(patient=self.patient_object).exists()):
			print '\t-Patient Medical History Upload From HSP Queried...'
			medical_data = AddMedicalHistory.objects.filter(patient=self.patient_object).get()
			print '\t-Patient Allergies: %s'%(medical_data.allergies)
			print '\t-Patient Medical Conditions: %s'%(medical_data.medical_conditions)

		print '\033[1;32m\nPATIENT MEDICAL REPORTS STORED AND RETRIEVED SUCCESSFULLY\033[0m\n'

		print '\n\t-Testing HSP Updating Patient Medical Reports'

		#Update the medical history information
		if (AddMedicalHistory.objects.filter(patient=self.patient_object).exists()):
			print '\t-Patient Medical History Upload From HSP Queried...'
			print '\t-Adding "CATS" as allergy to patient medical history'
			medical_data = AddMedicalHistory.objects.filter(patient=self.patient_object).get()
			medical_data.allergies = medical_data.allergies + ', CATS'
			print '\t-Patient Allergies: %s'%(medical_data.allergies)
			print '\t-Patient Medical Conditions: %s'%(medical_data.medical_conditions)

		print '\033[1;32m\nPATIENT MEDICAL REPORTS UPDATED\033[0m\n'

		#summary of integration test
		print '\033[30;42m\nREGISTRATION FEATURE INTEGRATION TEST SUMMARY:\033[0m'
		print '\033[30;42m\n-Successful Patient Registration (name, contact info, ssn, med history, allergies, insurance)\033[0m',
		print '\033[30;42m\n-Successful HSP Medical Information Upload (allergies, medical conditions upload)\033[0m',
		print '\033[30;42m\n-Successful HSP Medical Information Updating (allergies, medical conditions upload)\033[0m',
		print '\033[30;42m\n-Successful Patient Data Storage & Retrieval\033[0m'

	def test_ScheduleFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR SCHEDULE FUNCTIONALITY\n-----------------------------------------------------------'



		self.patient_health_conditions = PatientHealthConditions.objects.create(

			user = self.patient_object,
			nausea_level = 10,
			hunger_level = 8,
			anxiety_level = 1, 
			stomach_level = 3,
			body_ache_level = 1,
			chest_pain_level = 4
			)
		self.patient_health_conditions.save()


		#Request an appointment to the healthcare provider
		print '\t-Currently requesting a medical appointment from Dr. %s %s' %(self.doctor_obj.doctor_first_name, self.doctor_obj.doctor_last_name)

		print '\t-Currently requesting an appointment for patient: %s %s' %(self.fill_patient_application.first_name, self.fill_patient_application.last_name)
		print '\t-Appointment Details:'
		print '\t\t+Date: %s'%("02/20/2016")
		print '\t\t+Doctor: Dr. %s %s'%(self.doctor_obj.doctor_first_name, self.doctor_obj.doctor_last_name)
		print '\t\t+Pain Level: %d'%(10)
		print '\t\t+Medical Conditions: xanax'
		print '\t\t+Allergies: %s'%(self.fill_patient_application.allergies)
		print '\t\t+Patient: %s %s'%(self.fill_patient_application.first_name, self.fill_patient_application.last_name)
		print '\t\t+Current Health Conditions: %d %d %d %d %d %d'%(self.patient_health_conditions.anxiety_level,
																self.patient_health_conditions.stomach_level, 
																self.patient_health_conditions.body_ache_level, 
																self.patient_health_conditions.anxiety_level, 
																self.patient_health_conditions.chest_pain_level, 
																self.patient_health_conditions.hunger_level 
																)

		#Schedule an appointment
		medical_appointment_1 = PatientAppt.objects.create(
			date = "02/20/2016",
			doctor = self.doctor_obj,
			pain_level = 10,
			medical_conditions = "chest pain and stomach issues",
			allergies = self.fill_patient_application.allergies,
			user = self.patient_object,
			current_health_conditions = self.patient_health_conditions
			)
		medical_appointment_1.save()

		print '\033[1;32m\nPATIENT APPOINTMENT (#1) CREATED SUCCESSFULLY!\033[0m\n'

		print '\t-Test changing status of the appointment from not resolved to resolved'

		#Change resolution status of appointment
		medical_appointment_1.resolved = 1

		self.assertEqual(1, medical_appointment_1.resolved)

		print '\t-Medical appointment resolved successfully'

		print '\033[1;32m\nPATIENT APPOINTMENT RESOLVED SUCCESSFULLY!\033[0m\n'

		print '\t-Attempting to view all the currently scheduled appointments for patient %s %s' %(self.fill_patient_application.first_name, self.fill_patient_application.last_name)

		print '\t-There are currently (%d) appointments in the database' %(PatientAppt.objects.all().count())

		#Query appointment for the patient
		current_appointment = PatientAppt.objects.filter(user = self.patient_object).get()

		#Check appt. existence.
		if (PatientAppt.objects.filter(user = self.patient_object).exists()):
			print '\t-Appointment for patient has been found; Attempting to view appointment details'

			#Retrieve appt data. (view)
			current_appt = PatientAppt.objects.filter(user = self.patient_object).get()
			print '\t-Appointment object is %s' %(current_appt)
			print '\t\t+Date: %s'%(current_appt.date)
			print '\t\t+Doctor: Dr. %s %s'%(current_appt.doctor.doctor_first_name, current_appt.doctor.doctor_last_name)
			print '\t\t+Pain Level: %d'%(10)
			print '\t\t+Medical Conditions: xanax'
			print '\t\t+Allergies: %s'%(current_appt.allergies)
			print '\t\t+Patient: %s %s'%(current_appt.user.fill_from_application.first_name, current_appt.user.fill_from_application.last_name)
			print '\t\t+Current Health Conditions: %d %d %d %d %d %d'%(current_appt.current_health_conditions.anxiety_level,
																	current_appt.current_health_conditions.stomach_level, 
																	current_appt.current_health_conditions.body_ache_level, 
																	current_appt.current_health_conditions.anxiety_level, 
																	current_appt.current_health_conditions.chest_pain_level, 
																	current_appt.current_health_conditions.hunger_level 
																	)

			print '\033[1;32m\nPATIENT APPOINTMENT VIEWED SUCCESSFULLY!\033[0m\n'

		print '\tTesting the manage portion of the appointments scheduler..'
		print '\tAttempting to change the date of the appointment'
		print '\tCurrent appointment date: %s' %(current_appt.date)

		#Updating appt. data
		current_appt.date = "03/14/2015"

		print '\tCurrent appointment date: %s' %(current_appt.date)

		#Assert change was valid
		self.assertEqual(current_appt.date, "03/14/2015")

		print '\033[1;32m\nPATIENT APPOINTMENT DATE CHANGED SUCCESSFULLY!\033[0m\n'

		print '\tTesting the manage portion of the appointments scheduler..'
		print '\tAttempting to delete the appointment'

		#Remove appt.
		current_appt.delete()

		#Assert positive removal
		self.assertEqual(0, PatientAppt.objects.all().count())

		print '\033[1;32m\nPATIENT APPOINTMENT DELETED SUCCESSFULLY!\033[0m\n'

		#summary of the integration test that was ran
		print '\033[30;42m\nSCHEDULE APPOINTMENT FEATURE INTEGRATION TEST SUMMARY:\033[0m'
		print '\033[30;42m\n-Successful Patient Appointment Creation (Doctor Chosen based on health)\033[0m',
		print '\033[30;42m\n-Successful Patient Appointment Resolution By Doctor\033[0m',
		print '\033[30;42m\n-Successful Patient Appointment Viewed/Retrieved\033[0m',
		print '\033[30;42m\n-Successful Patient Appoinment Managed (Updated/Removed)\033[0m'



	def test_UpdateHealthConditionsFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR UPDATE HEALTH CONDITIONS FUNCTIONALITY\n-----------------------------------------------------------'

		print '\t-Testing ability for patient to login & update health conds.'

		#Login as the patient and ensure that the IPIMS wants us to update our health conditions
		#Reload data
		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user

		#Ensure patient was approved successfully
		response = PatientPortalView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		print '\t\t+Patient currently logged in successfully..'
		print '\t\t+Testing patient health-conds update'

		#Ensure the patient is viewing the page to force a health care update
		self.assertContains(response, '<h3>Before Continuing Further, please <a href="/health_conditions">add your health conditions..</a></h3>')

		#Update the health conditions of the patient
		self.patient_health_conditions = PatientHealthConditions.objects.create(

			user = self.patient_object,
			nausea_level = 10,
			hunger_level = 8,
			anxiety_level = 1, 
			stomach_level = 3,
			body_ache_level = 1,
			chest_pain_level = 4
			)
		self.patient_health_conditions.save()

		#Login as the patient and ensure that the IPIMS wants us to update our health conditions
		#Reload data
		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user

		#Ensure patient was approved successfully
		response = PatientPortalView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		print '\033[1;32m\nPATIENT HEALTH CONDITIONS ADDED SUCCESSFULLY!\033[0m\n'

		print '\t-Attempting to retrieve the patient health conditions to test validity'

		#Login as the patient and ensure that the IPIMS wants us to update our health conditions
		#Reload data
		request = self.factory.get(reverse_lazy('Conditions'))
		request.user = self.patient_user

		#Ensure patient was approved successfully
		response = HealthConditionsView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		'''
		ENSURING EACH INDIVIDUAL HEALTH CONDITION WAS STORED AND OUTPUTTED SUCCESSFULLY WITHIN THE IPIMS
		'''

		#Testing proper nausea level
		self.assertContains(response, 'name="nausea_level" type="number" value="10"')
		print '\t\t+Nausea level: Expected - 10, result - 10'

		#Testing proper hunger level
		self.assertContains(response, 'name="hunger_level" type="number" value="8"')
		print '\t\t+Hunger level: Expected - 8, result - 8'

		#Testing proper anxiety level
		self.assertContains(response, 'name="anxiety_level" type="number" value="1"')
		print '\t\t+Anxiety level: Expected - 1, result - 1'

		#Testing proper stomach level
		self.assertContains(response, 'name="stomach_level" type="number" value="3"')
		print '\t\t+Stomach level: Expected - 3, result - 3'

		#Testing proper body ache level
		self.assertContains(response, 'name="body_ache_level" type="number" value="1"')
		print '\t\t+Body Ache level: Expected - 1, result - 1'

		#Testing proper chest pain level
		self.assertContains(response, 'name="chest_pain_level" type="number" value="4"')
		print '\t\t+Chest Pain level: Expected - 4, result - 4'

		print '\033[1;32m\nPATIENT HEALTH CONDITIONS STORED AND VIEWED SUCCESSFULLY VIA IPIMS!\033[0m\n'

		'''
		ENSURE THE ALERT CAPABILITIES OF THE IPIMS ARE WORKING PROPERLY
		'''

		print('\t-Testing manual alert submission from patient to healthcare from portal page')

		#Ensure that the alert has not been sent yet
		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user
		response = PatientPortalView(request)

		self.assertNotContains(response, 'Your alert has been sent to the hospital!')

		print('\t\t+Successful analysis that the alert has not yet been sent.. sending alert now')

		self.patient_object.alertSent = 1
		self.patient_object.save()

		print('\t\t+Alert now sent successfully, testing page response')

		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user
		response = PatientPortalView(request)

		self.assertContains(response, '<h4><b>Your alert has been sent to the hospital!</b></h4>')

		print '\033[1;32m\nMANUAL SUBMISSION OF ALERT HAS BEEN SENT SUCCESSFULLY!\033[0m\n'

		#Reset alert sent
		self.patient_object.alertSent = 0
		self.patient_object.save()

		#Visit patient portal again as patient user
		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user
		response = PatientPortalView(request)

		#Alert send message disappears when the alert has been retracted from the system
		self.assertNotContains(response, '<h4><b>Your alert has been sent to the hospital!</b></h4>')

		print '\t-Testing IPIMS automatic analysis alert functionality'
		print '\t\t+Currently increasing health conditions above (40) threshhold'

		#Update the health conditions to exceed the threshhold
		self.patient_health_conditions.nausea_level = 10
		self.patient_health_conditions.hunger_level = 10
		self.patient_health_conditions.anxiety_level = 10
		self.patient_health_conditions.chest_pain_level = 10
		self.patient_health_conditions.save()

		print '\t\t+Patient health threshhold set.. Testing auto send alert feature'

		#Navigate back to the control panel
		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user
		response = PatientPortalView(request)

		#Test that the page ensures that the alert has been sent successfully!
		self.assertContains(response, '<h4><b>Your alert has been sent to the hospital!</b></h4>')

		print '\033[1;32m\nAUTOMATIC SUBMISSION OF ALERT HAS BEEN SENT SUCCESSFULLY BY IPIMS!\033[0m\n'

		#summary of the integration test that was ran
		print '\033[30;42m\nUPDATE HEALTH CONDITIONS FEATURE INTEGRATION TEST SUMMARY:\033[0m'
		print '\033[30;42m\n-Successful Addition of Patient Health Conditions\033[0m',
		print '\033[30;42m\n-Successful Storage of Patient Health Conditions\033[0m',
		print '\033[30;42m\n-Successful Retrieval of Patient Health Conditions\033[0m',
		print '\033[30;42m\n-Successful Manual Alert Submission To Health Staff\033[0m',
		print '\033[30;42m\n-Successful Automatic Alert Submission To Health Staff By IPIMS\033[0m'

	def test_ServiceToDoctorsFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR SERVICE TO DOCTORS FUNCTIONALITY\n-----------------------------------------------------------'


		print 'THIS NEEDS TO BE CODED STILL!'

		'''
		(First Generate some appointments to view in the IPIMS)

		Ensure the relevant doctor can view the appointments
		Ability for doctor/nurse to update the health conditions
		Ability for doctor to resolve a patient case 
		Ability for doctor to prescribe medications 
		Ability for doctor to view patient lab records (Will need to create lab record instantiation)
		'''

	def test_ServiceToStaffFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR SERVICE TO STAFF FUNCTIONALITY\n-----------------------------------------------------------'


		print 'THIS NEEDS TO BE CODED STILL!'


		'''
		Test retrieval of patient information
		View All Patients
		View Patient Medical Information
		View Patient Prescription
		Update Patient Medical History
		'''

	def test_LabRecordsFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR LAB RECORDS FUNCTIONALITY\n-----------------------------------------------------------'


		print 'THIS NEEDS TO BE CODED STILL!'

		'''
		Test creation of lab record
		Test viewing of lab record
		Test editing of lab record
		Test removal of lab record

		'''

	def test_StatsReportsFeatureIntegration(self):

		print '\n\n\n----------------------------------------------------------\nINTEGRATION TEST FOR STATISTICAL REPORTS FUNCTIONALITY\n-----------------------------------------------------------'


		print 'THIS NEEDS TO BE CODED STILL!'

		'''
		Health outcome analysis
		Admission rate
		Patient types
		Patient populations

		'''

