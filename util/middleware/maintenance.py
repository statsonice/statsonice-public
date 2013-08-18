"""
This Middleware checks if maintenance.txt exists in the
repository root directory.  If it does, load a maintenance
page instead of normal
"""
import os
from django.shortcuts import render

from django.http import HttpResponse

class MaintenanceMiddleware(object):
    def process_request(self, request):
        maintenance_file_path = os.path.dirname(os.path.realpath(__file__))+'/../../maintenance.txt'
        if os.path.exists(maintenance_file_path):
            return render(request, 'maintenance.dj')
        return None
