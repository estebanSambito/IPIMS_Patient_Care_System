from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test.client import Client as client
from ipcms.models import TempPatientData, Doctor, Patient, PatientHealthConditions, PatientAppt, Alert, PermissionsRole, EMedication, LabReport, LabTech, AddMedicalHistory
from pprint import pprint
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import AnonymousUser, User
import time
from ipcms.views import PatientPortalView


class TestIntegration(TestCase):

	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.hsp_user = User.objects.create(username="hsp_user_1", 
			password="hsp_user_1_password")

		self.patient_user = User.objects.create(username="patient_user_1", 
			password="patient_user_1")


		self.hsp_permission_role = PermissionsRole.objects.create(

			role = "staff",
			user = self.hsp_user

			)

		self.patient_permission = PermissionsRole.objects.create(

			role = "patient",
			user = self.patient_user

			)

		self.temp_patient_user_data = TempPatientData.objects.create(
		#Assign the attributes that are associated with the user
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

		self.patient_object = Patient.objects.create(

			fill_from_application = self.temp_patient_user_data,
			user = self.patient_user,
			approved = 0
			)

		self.hsp_user.save()
		self.patient_user.save()
		self.temp_patient_user_data.save()
		self.patient_object.save()
		self.hsp_permission_role.save()
		self.patient_permission.save()

	def testHSPPortal(self):

		print 'PORTAL TEST FUNCTIONAL'

		request = self.factory.get(reverse_lazy('Portal'))
		# request.start_time = time.time()
		begin_time = time.time()
		print '\033[1;36;41m\n\n\n\nTESTING PORTAL LOAD FOR HSP\n\n\n\033[0m\n'
		request.user = self.hsp_user
		response = PatientPortalView(request)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'HSP Staff Control Panel')
		self.assertContains(response, 'Application Approvals')
		self.assertContains(response, 'View Patient Data')
		self.assertContains(response, 'Generate Stats Report')

		# print '\033[1;36;41m\n\n\n\nPORTAL LOAD TOOK %.5f seconds\n\n\n\033[0m\n' %(time.time() - request.start_time)

		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user
		response = PatientPortalView(request)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'We Are Still Reviewing Your Application')
		self.patient_object.approved = 1
		self.patient_object.save()


		request = self.factory.get(reverse_lazy('Portal'))
		request.user = self.patient_user
		response = PatientPortalView(request)

		self.assertContains(response, 'Before Continuing Further, please <a href="/health_conditions">add your health conditions..')

		# duration = time.time() - request.start_time
