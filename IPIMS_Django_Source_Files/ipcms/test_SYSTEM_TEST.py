from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test.client import Client as client
from ipcms.models import TempPatientData, Doctor, Patient, PatientHealthConditions, PatientAppt, Alert, PermissionsRole, EMedication, LabReport, LabTech, AddMedicalHistory
from pprint import pprint
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import AnonymousUser, User
import time
from ipcms.views import PatientPortalView, HealthConditionsView, SuccessTestView
from django.views import generic

#Function to output color codes of the efficiency of the response time for each of the features in the IPIMS
def calculateResponseEfficiency(output_time):
	if (output_time < .006):
		return '\033[1;32mVERY GOOD\033[0m'
	elif (output_time < .01):
		return '\033[1;32mGOOD\033[0m'

def separator():
	print '\t\t---------------------------------------------------------'

class Test_SystemComplianceTest(TestCase):


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
			income = "$0-$10,000",
			gender = "other"
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



	def test_PatientFeature(self):
		TOTAL_PATIENT_FEATURE_TIME = 0

		print '\033[1;45m\n----------------------------------------------------------\n (1) SYSTEM TEST FOR REGISTRATION FEATURE\n-----------------------------------------------------------\033[0m\n'

		print '\t\t- \033[1;33mFeature Name:\033[0m %s'%("Patient Registration")

		#Run the registration code here
		#Build the user in the system

		response_time_begin = time.time()

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

		#Load the patient portal
		request = self.factory.get(reverse_lazy('SuccessTestView'))

		#Set the current user request object
		request.user = self.patient_user

		#Store the view response
		response = SuccessTestView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Now load the actual portal view after registration
		response_time = time.time() - response_time_begin

		TOTAL_PATIENT_FEATURE_TIME += response_time

		print '\t\t- \033[1;33mResponse Time:\033[0m %.3f seconds'%(response_time)
		print '\t\t- \033[1;33mReliability Rating:\033[0m %s'%(calculateResponseEfficiency(response_time))
		separator()
		print '\t\t- \033[1;33mFeature Name:\033[0m %s'%("Updating Medical History")

		#Upload an associated medical report for the patient

		response_time_begin = time.time()

		patient_medical_history_upload = AddMedicalHistory.objects.create(
			allergies="Dogs, Flees",
			medical_conditions="Heart Pain",
			patient=self.patient_object
			)
		patient_medical_history_upload.save()

		#Load the patient portal
		request = self.factory.get(reverse_lazy('SuccessTestView'))

		#Set the current user request object
		request.user = self.patient_user

		#Store the view response
		response = SuccessTestView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Now load the actual portal view after registration
		response_time = time.time() - response_time_begin

		TOTAL_PATIENT_FEATURE_TIME += response_time
		print '\t\t- \033[1;33mResponse Time:\033[0m %.3f seconds'%(response_time)
		print '\t\t- \033[1;33mReliability Rating:\033[0m %s'%(calculateResponseEfficiency(response_time))
		separator()
		print '\t\t- \033[1;33mFeature Name:\033[0m %s'%("Uploading and Storing Medical Records")
		response_time_begin = time.time()

		#Build the user in the system

		#Upload an associated medical report for the patient
		patient_medical_history_upload = AddMedicalHistory.objects.create(
			allergies="Dogs, Flees",
			medical_conditions="Heart Pain, Back Pain, Shoulder",
			patient=self.patient_object
			)
		patient_medical_history_upload.save()

		#Update and store medical data
		patient_medical_history_upload.medical_conditions = patient_medical_history_upload.medical_conditions + ", head pain"

		patient_medical_history_upload.save()

		#Load the patient portal
		request = self.factory.get(reverse_lazy('SuccessTestView'))

		#Set the current user request object
		request.user = self.patient_user

		#Store the view response
		response = SuccessTestView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Now load the actual portal view after registration
		response_time = time.time() - response_time_begin

		TOTAL_PATIENT_FEATURE_TIME += response_time
		print '\t\t- \033[1;33mResponse Time:\033[0m %.3f seconds'%(response_time)
		print '\t\t- \033[1;33mReliability Rating:\033[0m %s'%(calculateResponseEfficiency(response_time))
		separator()
		print '\t\t- \033[1;33mFeature Name:\033[0m %s'%("Approving Patient Application Request")

		#Now load the actual portal view after registration
		response_time = time.time() - response_time_begin

		self.patient_object.approved = 1
		self.patient_object.save()

		#Load the patient portal
		request = self.factory.get(reverse_lazy('SuccessTestView'))

		#Set the current user request object
		request.user = self.patient_user

		#Store the view response
		response = SuccessTestView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Now load the actual portal view after registration
		response_time = time.time() - response_time_begin
		TOTAL_PATIENT_FEATURE_TIME += response_time
		print '\t\t- \033[1;33mResponse Time:\033[0m %.3f seconds'%(response_time)
		print '\t\t- \033[1;33mReliability Rating:\033[0m %s'%(calculateResponseEfficiency(response_time))

		print '\033\n[44mTOTAL TIME: %.5f seconds\033[0m'%(TOTAL_PATIENT_FEATURE_TIME)

	def test_ScheduleApptFeature(self):

		print '\033[1;45m\n----------------------------------------------------------\n (2) SYSTEM TEST FOR SCHEDULE FEATURE\n-----------------------------------------------------------\033[0m\n'

		print '\t\t- \033[1;33mFeature Name:\033[0m %s'%("Schedule Appt. Request")

		#Build the user in the system
		response_time_begin = time.time()

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

		#Load the patient portal
		request = self.factory.get(reverse_lazy('SuccessTestView'))

		#Set the current user request object
		request.user = self.patient_user

		#Store the view response
		response = SuccessTestView(request)

		#Test valid response code
		self.assertEqual(response.status_code, 200)

		#Now load the actual portal view after registration
		response_time = time.time() - response_time_begin
		print '\t\t- \033[1;33mResponse Time:\033[0m %.3f seconds'%(response_time)
		print '\t\t- \033[1;33mReliability Rating:\033[0m %s'%(calculateResponseEfficiency(response_time))

