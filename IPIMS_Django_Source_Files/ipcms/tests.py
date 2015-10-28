from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from ipcms.models import TempPatientData, Doctor, Patient, PatientHealthConditions, PatientAppt, Alert
from pprint import pprint

#This will be used to prepare the creation of the users within the system
# class TestingDifferentUserCreations(TestCase):

# 	#Globally references patient object
# 	def testSubmitApplicationToHSPStaff(self):
# 		temp_patient_object = TempPatientData.objects.create()
# 		#Create the user to append into the model
# 		temp_patient_object.user = User.objects.create(username="johnson", email="johnson@johnson.com", password="johnson")
# 		print 'Temporary Patient Created Successfully!'

# 		#Assign the attributes that are associated with the user
# 		temp_patient_object.first_name = "Ryan"
# 		temp_patient_object.last_name = "Schachte"
# 		temp_patient_object.DOB = "2201995"
# 		temp_patient_object.ssn = "600489139"
# 		temp_patient_object.allergies = "NONE"
# 		temp_patient_object.address = "2463 E. Mallory Dr. Tempe, AZ 85281"
# 		temp_patient_object.medications = "NONE"
# 		temp_patient_object.insurance_provider = "Allstate"
# 		temp_patient_object.insurance_policy_number = "19938343434"
# 		temp_patient_object.email_address = "johnson@johnson.com"
# 		temp_patient_object.data_sent = "1"

# 		#Save user into the test database
# 		temp_patient_object.save()

# 		self.assertEqual(temp_patient_object.first_name, "Ryan")
# 		self.assertEqual(temp_patient_object.last_name, "Schachte")
# 		self.assertEqual(temp_patient_object.DOB, "2201995")
# 		self.assertEqual(temp_patient_object.ssn, "600489139")
# 		self.assertEqual(temp_patient_object.allergies, "NONE")
# 		self.assertEqual(temp_patient_object.address, "2463 E. Mallory Dr. Tempe, AZ 85281")
# 		self.assertEqual(temp_patient_object.medications, "NONE")
# 		self.assertEqual(temp_patient_object.insurance_provider, "Allstate")
# 		self.assertEqual(temp_patient_object.insurance_policy_number, "19938343434")
# 		self.assertEqual(temp_patient_object.email_address, "johnson@johnson.com")
# 		self.assertEqual(temp_patient_object.data_sent, "1")

# 		# pprint (vars(temp_patient_object))

# 		print '\n\n\nALERT FOR THE USER HAS BEEN SUCCESSFULLY CREATED!\n\n\n'

	# #Create a doctor object that will be used for the patient to schedule an appt. within the system
	# def testDoctorCreation(self):

	# 	#Create the doctor object
	# 	temp_doctor_object = Doctor.objects.create()
	# 	print 'The doctor object has been successfully created'

	# 	#Assign the attributes to the doctor object 
	# 	temp_doctor_object.doctor_first_name = "Katelyn"
	# 	temp_doctor_object.doctor_last_name = "Duffy"
	# 	temp_doctor_object.doctor_type = "Gynecologist"

	# 	pprint (vars(temp_doctor_object))

	# 	print '\n\n\nDOCTOR HAS BEEN CREATED AND SENT SUCCESSFULLY\n\n\n'

	# 	return temp_doctor_object

	#Test the creation of a patient
	# def testPatientCreation(self):

	# 	temp_patient_object = TempPatientData.objects.create()

	# 	#Create the user to append into the model
	# 	temp_patient_object.user = User.objects.create(username="johnson", email="johnson@johnson.com", password="johnson")
	# 	print 'Temporary Patient Created Successfully!'

	# 	#Assign the attributes that are associated with the user
	# 	temp_patient_object.first_name = "Ryan"
	# 	temp_patient_object.last_name = "Schachte"
	# 	temp_patient_object.DOB = "2201995"
	# 	temp_patient_object.ssn = "600489139"
	# 	temp_patient_object.allergies = "NONE"
	# 	temp_patient_object.address = "2463 E. Mallory Dr. Tempe, AZ 85281"
	# 	temp_patient_object.medications = "NONE"
	# 	temp_patient_object.insurance_provider = "Allstate"
	# 	temp_patient_object.insurance_policy_number = "19938343434"
	# 	temp_patient_object.email_address = "johnson@johnson.com"
	# 	temp_patient_object.data_sent = "1"

	# 	#Save user into the test database
	# 	temp_patient_object.save()

	# 	print 'Application Submitted, now testing creation of an approved patient by HSP staff'

	# 	approved_patient = Patient.objects.create()
	# 	approved_patient.user = temp_patient_object.user
	# 	approved_patient.fill_from_application = temp_patient_object
	# 	approved_patient.approved = 1
	# 	approval = approved_patient.approved

	# 	#Testing to ensure the object data from temp patient filtered down into the approved patient
	# 	self.assertEqual(approved_patient.user.username, temp_patient_object.user.username)
	# 	self.assertEqual(approved_patient.fill_from_application.DOB, "2201995")
	# 	self.assertEqual(approval, 1)

	# 	approved_patient.save()

	# 	print '\n\n\nThe patient has been approved succesfully!\n\n\n'


	# # #Test the update of health condition
	# def testUpdateHealthConditions(self):


		# temp_patient_object = TempPatientData.objects.create()

		# #Create the user to append into the model
		# temp_patient_object.user = User.objects.create(username="johnson1", email="johnson1@johnson.com", password="johnson1")
		# print 'Temporary Patient Created Successfully!'

		# #Assign the attributes that are associated with the user
		# temp_patient_object.first_name = "Ryewfan"
		# temp_patient_object.last_name = "Schawefchte"
		# temp_patient_object.DOB = "220195"
		# temp_patient_object.ssn = "6009139"
		# temp_patient_object.allergies = "fNONE"
		# temp_patient_object.address = "24f63 E. Mallory Dr. Tempe, AZ 85281"
		# temp_patient_object.medications = "NONE"
		# temp_patient_object.insurance_provider = "Allstaefte"
		# temp_patient_object.insurance_policy_number = "19938343434"
		# temp_patient_object.email_address = "johnsofn@johnsown.com"
		# temp_patient_object.data_sent = "1"

		# # #Save user into the test database
		# temp_patient_object.save()

		# print 'Application Submitted, now testing creation of an approved patient by HSP staff'

		# approved_patient = Patient.objects.create()
		# approved_patient.user = temp_patient_object.user
		# approved_patient.fill_from_application = temp_patient_object
		# approved_patient.approved = 1
		# approval = approved_patient.approved

		# #Testing to ensure the object data from temp patient filtered down into the approved patient
		# self.assertEqual(approved_patient.user.username, temp_patient_object.user.username)
		# self.assertEqual(approved_patient.fill_from_application.DOB, "220195")
		# self.assertEqual(approval, 1)
		# approved_patient.save()

		

		#user is now created, we want to update the health conditions of the patient
		# patient_health_conditions = PatientHealthConditions.objects.create()
		# patient_health_conditions.nausea_level = 5
		# patient_health_conditions.hunger_level = 7
		# patient_health_conditions.anxiety_level = 3
		# patient_health_conditions.stomach_level = 1
		# patient_health_conditions.body_ache_level = 4
		# patient_health_conditions.chest_pain_level = 9

		# self.assertEqual(patient_health_conditions.nausea_level, 5)
		# self.assertEqual(patient_health_conditions.hunger_level, 7)
		# self.assertEqual(patient_health_conditions.anxiety_level, 3)
		# self.assertEqual(patient_health_conditions.stomach_level, 1)
		# self.assertEqual(patient_health_conditions.body_ache_level, 4)
		# self.assertEqual(patient_health_conditions.body_ache_level, 4)
		# self.assertEqual(patient_health_conditions.chest_pain_level, 9)

		# print '\n\n\nAPPT. SCHEDULED SUCCESSFULLY!!!\n\n\n'


	# # #Test the creation of a an appointment
	# def testPatientAppoitmentSchedule(self):
	# 	appt_obj = PatientAppt.objects.create()

	# 	# appt_obj.doctor = Doctor_Obj()
	# 	appt_obj.pain_level = 5
	# 	appt_obj.medical_conditions = "None"
	# 	# appt_obj.user = patient_user()
	# 	appt_obj.allergies = "None"
	# 	# appt_obj.current_health_conditions = health_conditions()

	# 	# self.assertEqual(appt_obj.doctor.name, Doctor_Obj.name)
	# 	self.assertEqual(appt_obj.pain_level, 5)
	# 	self.assertEqual(appt_obj.medical_conditions, "None")

	# 	print 'Appt. Created Successfully!'



	# date = models.CharField(max_length=1000, unique=True)
	# doctor = models.ForeignKey(Doctor, unique=False, blank=False, default=-1)
	# pain_level = models.IntegerField(validators=[MinValueValidator(0),
 #                                       MaxValueValidator(10)], default=0)
	# medical_conditions = models.CharField(max_length=1000, default="None")
	# allergies = models.CharField(max_length=1000, default="None")
	# user = models.ForeignKey(Patient, unique=False, blank=True, default="")
	# current_health_conditions = models.ForeignKey(PatientHealthConditions, unique=False, blank=True, default="", null=True)


#class TestingPatientAlertSystem(TestCase):

	#Globally references patient object
	#def testAlertSystem(self):
	#	temp_patient_object = TempPatientData.objects.create()
	#	#Create the user to append into the model
	#	temp_patient_object.user = User.objects.create(username="johnson", email="johnson@johnson.com", password="johnson")
	#	print 'Temporary Patient Created Successfully!'

	#	#Assign the attributes that are associated with the user
	#	temp_patient_object.first_name = "Ryan"
	#	temp_patient_object.last_name = "Schachte"
	#	temp_patient_object.DOB = "2201995"
	#	temp_patient_object.ssn = "600489139"
	#	temp_patient_object.allergies = "NONE"
	#	temp_patient_object.address = "2463 E. Mallory Dr. Tempe, AZ 85281"
	#	temp_patient_object.medications = "NONE"
	#	temp_patient_object.insurance_provider = "Allstate"
	#	temp_patient_object.insurance_policy_number = "19938343434"
	#	temp_patient_object.email_address = "johnson@johnson.com"
	#	temp_patient_object.data_sent = "1"

	#	#Save user into the test database
	#	temp_patient_object.save()

	#	self.assertEqual(temp_patient_object.first_name, "Ryan")
	#	self.assertEqual(temp_patient_object.last_name, "Schachte")
	#	self.assertEqual(temp_patient_object.DOB, "2201995")
	#	self.assertEqual(temp_patient_object.ssn, "600489139")
	#	self.assertEqual(temp_patient_object.allergies, "NONE")
	#	self.assertEqual(temp_patient_object.address, "2463 E. Mallory Dr. Tempe, AZ 85281")
	#	self.assertEqual(temp_patient_object.medications, "NONE")
	#	self.assertEqual(temp_patient_object.insurance_provider, "Allstate")
	#	self.assertEqual(temp_patient_object.insurance_policy_number, "19938343434")
	#	self.assertEqual(temp_patient_object.email_address, "johnson@johnson.com")
	#	self.assertEqual(temp_patient_object.data_sent, "1")

	#	patient_object = Patient.objects.create()

	#	patient_object.fill_from_application = temp_patient_object
	#	patient_object.user = temp_patient_object.user
	#	patient_object.approved = 1
	#	patient_object.alertSent = 1

	#	self.assertEqual(patient_object.alertSent,1)
	#	self.assertEqual(patient_object.approved, 1)
	#	self.assertEqual(patient_object.user.username, 'johnson')

	#	patient_object.save()
		
	#	alert_object = Alert.objects.create()
	#	alert_object.alert_level = 40
	#	alert_object.alert_patient = patient_object
	#	alert_object.alert_description = 'Hello, this is the description for alerts'
	#	alert_object.save()

	#	self.assertEqual(alert_object.alert_level, 40)
	#	self.assertEqual(alert_object.alert_patient, patient_object)
	#	alert_object.alert_description, 'Hello, this is the description for alerts'

	#	pprint(alert_object)

	#	print '\n\n\nALERT FOR THE USER HAS BEEN SUCCESSFULLY CREATED!\n\n\n'

class TestingHealthConditions(TestCase):

	def testHealthConditions(self):
		temp_patient_object = TempPatientData.objects.create()
		#Create the user to append into the model
		temp_patient_object.user = User.objects.create(username="johnson", email="johnson@johnson.com", password="johnson")
		print 'Temporary Patient Created Successfully!'

		#Assign the attributes that are associated with the user
		temp_patient_object.first_name = "Ryan"
		temp_patient_object.last_name = "Schachte"
		temp_patient_object.DOB = "2201995"
		temp_patient_object.ssn = "600489139"
		temp_patient_object.allergies = "NONE"
		temp_patient_object.address = "2463 E. Mallory Dr. Tempe, AZ 85281"
		temp_patient_object.medications = "NONE"
		temp_patient_object.insurance_provider = "Allstate"
		temp_patient_object.insurance_policy_number = "19938343434"
		temp_patient_object.email_address = "johnson@johnson.com"
		temp_patient_object.data_sent = "1"

		#Save user into the test database
		temp_patient_object.save()

		self.assertEqual(temp_patient_object.first_name, "Ryan")
		self.assertEqual(temp_patient_object.last_name, "Schachte")
		self.assertEqual(temp_patient_object.DOB, "2201995")
		self.assertEqual(temp_patient_object.ssn, "600489139")
		self.assertEqual(temp_patient_object.allergies, "NONE")
		self.assertEqual(temp_patient_object.address, "2463 E. Mallory Dr. Tempe, AZ 85281")
		self.assertEqual(temp_patient_object.medications, "NONE")
		self.assertEqual(temp_patient_object.insurance_provider, "Allstate")
		self.assertEqual(temp_patient_object.insurance_policy_number, "19938343434")
		self.assertEqual(temp_patient_object.email_address, "johnson@johnson.com")
		self.assertEqual(temp_patient_object.data_sent, "1")

		patient_object = Patient.objects.create()

		patient_health_conditions = PatientHealthConditions.objects.create()
		patient_health_conditions.nausea_level = 5
		patient_health_conditions.hunger_level = 7
		patient_health_conditions.anxiety_level = 3
		patient_health_conditions.stomach_level = 1
		patient_health_conditions.body_ache_level = 4
		patient_health_conditions.chest_pain_level = 9

		self.assertEqual(patient_health_conditions.nausea_level, 5)
		self.assertEqual(patient_health_conditions.hunger_level, 7)
		self.assertEqual(patient_health_conditions.anxiety_level, 3)
		self.assertEqual(patient_health_conditions.stomach_level, 1)
		self.assertEqual(patient_health_conditions.body_ache_level, 4)
		self.assertEqual(patient_health_conditions.body_ache_level, 4)
		self.assertEqual(patient_health_conditions.chest_pain_level, 9)

		print '\n\n\nHEALTH CONDITIONS UPDATED SUCCESSFULLY!!!\n\n\n'

class TestingPatient(TestCase):

	def testPatientCreation(self):
		temp_patient_object = TempPatientData.objects.create()

		# 	#Create the user to append into the model
		temp_patient_object.user = User.objects.create(username="johnson", email="johnson@johnson.com", password="johnson")
		print 'Temporary Patient Created Successfully!'

		# 	#Assign the attributes that are associated with the user
		temp_patient_object.first_name = "Ryan"
		temp_patient_object.last_name = "Schachte"
		temp_patient_object.DOB = "2201995"
		temp_patient_object.ssn = "600489139"
		temp_patient_object.allergies = "NONE"
		temp_patient_object.address = "2463 E. Mallory Dr. Tempe, AZ 85281"
		temp_patient_object.medications = "NONE"
		temp_patient_object.insurance_provider = "Allstate"
		temp_patient_object.insurance_policy_number = "19938343434"
		temp_patient_object.email_address = "johnson@johnson.com"
		temp_patient_object.data_sent = "1"

		# 	#Save user into the test database
		temp_patient_object.save()

		print 'Application Submitted, now testing creation of an approved patient by HSP staff'

		approved_patient = Patient.objects.create()
		approved_patient.user = temp_patient_object.user
		approved_patient.fill_from_application = temp_patient_object
		approved_patient.approved = 1
		approval = approved_patient.approved

		# 	#Testing to ensure the object data from temp patient filtered down into the approved patient
		self.assertEqual(approved_patient.user.username, temp_patient_object.user.username)
		self.assertEqual(approved_patient.fill_from_application.DOB, "2201995")
		self.assertEqual(approval, 1)

		approved_patient.save()

		print '\n\n\nThe patient has been approved succesfully!\n\n\n'