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



class Test_SystemComplianceTest(TestCase):
	print 'TO BE DETERMINED'