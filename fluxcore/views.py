from django.shortcuts import render, redirect, get_object_or_404
from . forms import CreateUserForm, LoginForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import auth
from .models import File
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from datetime import datetime
import uuid
import zipfile
import shutil
from django.urls import reverse
import json
from datetime import datetime, timedelta
import time
import psutil # type: ignore


from .Part_1.driver import driver_part1
from .Part_2.driver import driver_part2
from .Part_3.driver import driver_part3

def homepage(request):
    #if the media folder is not there, create it
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'storage', 'user')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'storage', 'user'))
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'storage', 'user', 'Generated_Templates'))
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'storage', 'user', 'Branch_Calculation'))
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'storage', 'user', 'Batch_Calculation'))
    return render(request, 'index.html')

def read_config():
    config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user', 'config.json')
    with open(config_file, 'r') as f:
        return json.load(f)
    
def configure_outcomes(request):
    config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user', 'config.json')
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            #dump null json
            json.dump({}, f)

    if request.method == 'POST':
        num_pos = request.POST['num_pos']
        num_psos = request.POST['num_psos']
        with open(config_file, 'r') as f:
            config = json.load(f)

        config['PO'] = int(num_pos)
        config['PSO'] = int(num_psos)

        with open(config_file, 'w') as f:
            json.dump(config, f)

        return redirect('dashboard')
        
    config = read_config()
    return render(request, 'configure_outcomes.html', {'config': config})


def expiration(request):
    if request.method == 'POST':
        config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user',  'config.json')
        with open(config_file, 'r') as f:
            config = json.load(f)

        days = request.POST['days']
        doe = config['DOE']
        doe = datetime.strptime(doe, "%d-%m-%y")
        doe = doe + timedelta(days=int(days))
        doe = doe.strftime("%d-%m-%y")
        config['DOE'] = doe
        print("days", days)

        with open(config_file, 'w') as f:
            json.dump(config, f)

        return redirect('dashboard')
    return render(request, 'expiration.html')


def dashboard(request):
    config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user',  'config.json')
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            #dump null json and 'dod' as today's date in ddmmyy format
            json.dump({'DOD': datetime.now().strftime("%d-%m-%y"), 'DOE': (datetime.now() + timedelta(days=120)).strftime("%d-%m-%y")}, f)

        with open(config_file, 'r') as f:
            config = json.load(f)

        return render(request, 'configure_outcomes.html', {'config': config})
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    #if doe is >= today's date, then redirect to expiration page
    doe = datetime.strptime(config['DOE'], "%d-%m-%y")
    today = datetime.now()
    if doe < today:
        return redirect('expiration')



    # display_name = request.user.username.split('@')[0]
    display_name = 'user'
    user_directory = os.path.join(settings.MEDIA_ROOT, 'storage', display_name)
    Generated_Templates_dir = os.path.join(user_directory, 'Generated_Templates')

    #Template Generation
    Generated_Templates = os.listdir(Generated_Templates_dir)
    file_time_stamp = []
    for file in Generated_Templates:
        file_time_stamp.append(os.path.getmtime(os.path.join(Generated_Templates_dir, file)))
    file_time_stamp = [datetime.fromtimestamp(i).strftime("%d-%m-%Y %H:%M") for i in file_time_stamp]
    Generated_Templates = dict(zip(Generated_Templates, file_time_stamp))
    # End of Template Generation
    #=======================================================================================================
    #Branch Calculation
    Branch_Calculation_dir = os.path.join(user_directory, 'Branch_Calculation')
    Branch_Calculation = os.listdir(Branch_Calculation_dir)
    file_time_stamp = []
    files=[]
    for folder in Branch_Calculation:
        file_time_stamp.append(os.path.getmtime(os.path.join(Branch_Calculation_dir, folder)))
        files.append(os.listdir(os.path.join(Branch_Calculation_dir, folder)))
    file_time_stamp = [datetime.fromtimestamp(i).strftime("%d-%m-%Y %H:%M") for i in file_time_stamp]

    #dictionary as {folder_name: [[file_name,file_name],file_time_stamp]}
    Branch_Calculation = dict(zip(Branch_Calculation, zip(files,file_time_stamp)))

    # End of Branch Calculation
    #=======================================================================================================
    #Batch Calculation
    Batch_Calculation_dir = os.path.join(user_directory, 'Batch_Calculation')
    Batch_Calculation = os.listdir(Batch_Calculation_dir)
    file_time_stamp = []
    files=[]
    for folder in Batch_Calculation:
        file_time_stamp.append(os.path.getmtime(os.path.join(Batch_Calculation_dir, folder)))
        files.append(os.listdir(os.path.join(Batch_Calculation_dir, folder)))
    file_time_stamp = [datetime.fromtimestamp(i).strftime("%d-%m-%Y %H:%M") for i in file_time_stamp]

    #dictionary as {folder_name: [[file_name,file_name],file_time_stamp]}
    Batch_Calculation = dict(zip(Batch_Calculation, zip(files,file_time_stamp)))
            
    # End of Batch Calculation


    return render(request, 'dashboard.html', {'Generated_Templates': Generated_Templates, 
                                                'Branch_Calculation': Branch_Calculation,
                                                'Batch_Calculation': Batch_Calculation})

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')





#=======================================================================================================
#=======================================================================================================
#============================Template Generation========================================================
@csrf_exempt
def submit(request):
    config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user',  'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)

    if request.method == 'POST':
        data = {
            "Teacher": str(request.POST.get('teacher')),
            "Academic_year": str(request.POST.get('academicYearStart')) + "-" + str(request.POST.get('academicYearEnd')),
            "Semester": str(request.POST.get('semester')),
            "Branch": str(request.POST.get('branch')),
            "Batch": int(request.POST.get('batch')),
            "Section": str(request.POST.get('section')),
            "Subject_Code": str(request.POST.get('subjectCode')),
            "Subject_Name": str(request.POST.get('subjectName')),
            "Number_of_Students": int(request.POST.get('numberOfStudents')),
            "Number_of_COs": int(request.POST.get('numberOfCOs')),
        }


        num_components = int(request.POST.get('numberOfComponents'))
        Component_Details = {}
        for i in range(1, num_components+1):
            component_name_key = 'componentName' + str(i)
            component_value_key = 'componentValue' + str(i)
            component_type_key = 'componentType' + str(i)
            
            component_name = request.POST.get(component_name_key)
            component_value = request.POST.get(component_value_key)
            component_type = request.POST.get(component_type_key)

            full_component_name = f"{component_name}-{component_type[0]}".upper()
            Component_Details[full_component_name] = int(component_value)

        print(Component_Details)
        # Directory for generated templates
        # display_name = request.user.username.split('@')[0]
        display_name = 'user'

        Generated_Templates_dir = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Generated_Templates')

        # Generate file name for the Excel file
        excel_file_path = os.path.join(Generated_Templates_dir)

        # Call main1 function with the necessary data and file path
        generated_file_name = driver_part1(data, Component_Details,config, excel_file_path)
        file_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Generated_Templates', generated_file_name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=generated_file_name)
            return response
        return redirect('/dashboard/?show=template')
    # If the request method is not POST, handle accordingly (redirect to a form, etc.)
    return redirect('/dashboard/?show=template')

#=======================================================================================================
def download_file_generated(request, file_name):
    # Paths to the different folders
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'

    Generated_Templates_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Generated_Templates')
    # Check which folder contains the file
    if os.path.isfile(os.path.join(Generated_Templates_path, file_name)):
        file_path = os.path.join(Generated_Templates_path, file_name)
    else:
        raise Http404("File not found")

    # If the file exists, serve it
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response

    # If the file does not exist
    raise Http404("File not found")

#=======================================================================================================
def delete_file_generated(request, file_name):
    # Paths to the different folders
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'

    Generated_Templates_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Generated_Templates')

    # Check which folder contains the file
    if os.path.isfile(os.path.join(Generated_Templates_path, file_name)):
        file_path = os.path.join(Generated_Templates_path, file_name)

    # If the file exists, delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect('/dashboard/?show=template')

#=======================================================================================================
#=======================================================================================================
#============================Branch Calculation========================================================

def delete_folder(unique_folder_path):
    if os.path.exists(unique_folder_path):
        shutil.rmtree(unique_folder_path)
        return

@csrf_exempt
def upload_multiple_files_branch(request):
    config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user',  'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('BranchExcelFiles')
        num_files = len(uploaded_files)
        # display_name = request.user.username.split('@')[0]
        display_name = 'user'

        user_directory = os.path.join(settings.MEDIA_ROOT, 'storage', display_name)
        branch_directory = os.path.join(user_directory, 'Branch_Calculation')
        
        unique_id = str(uuid.uuid4()).split('-')[0]
        unique_folder_name = f"{num_files}Files_BranchCalculation_{unique_id}"
        unique_folder_path = os.path.join(branch_directory, unique_folder_name)
        os.makedirs(unique_folder_path, exist_ok=True)
        fs = FileSystemStorage(location=unique_folder_path)
        
        for uploaded_file in uploaded_files:
            with fs.open(uploaded_file.name, 'wb+') as destination:
                destination.write(uploaded_file.read())
                destination.close()

        message = driver_part2(unique_folder_path, unique_folder_path, config)
        message=message[0]
        time.sleep(2)
        if "success" in message:
            messages.success(request, message)
        else:
            messages.error(request, message)
            # Optionally, delete the folder
            if os.path.exists(unique_folder_path):
                shutil.rmtree(unique_folder_path)

        return redirect('/dashboard/?show=branch')  # This assumes you want to redirect to a new request where the message will be displayed
    else:
        # If it's not a POST request, handle accordingly
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


#=======================================================================================================
def download_file_branch(request, file_name, folder_name):
    # Paths to the different folders
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'

    Branch_file_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Branch_Calculation', folder_name)
    # Check which folder contains the file
    if os.path.isfile(os.path.join(Branch_file_path, file_name)):
        file_path = os.path.join(Branch_file_path, file_name)
    else:
        raise Http404("File not found")

    # If the file exists, serve it
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response

    # If the file does not exist
    raise Http404("File not found")
#=======================================================================================================
def download_folder_branch(request, folder_name):
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'
    branch_calculation_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Branch_Calculation', folder_name)

    # Create a ZIP file in memory
    response = HttpResponse(content_type='application/zip')
    zip_filename = f"{folder_name}.zip"
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk(branch_calculation_path):
            for filename in filenames:
                # Create complete filepath of file in directory
                file_path = os.path.join(foldername, filename)
                # Add file to zip
                zip_file.write(file_path, os.path.relpath(file_path, branch_calculation_path))

    return response


#=======================================================================================================
def delete_folder_branch(request, folder_name):
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'
    branch_calculation_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Branch_Calculation')

    # Check if the directory exists
    if os.path.isdir(os.path.join(branch_calculation_path, folder_name)):
        branch_calculation_path = os.path.join(branch_calculation_path, folder_name)

    # Delete the folder and all its contents
    if os.path.exists(branch_calculation_path):
        shutil.rmtree(branch_calculation_path)

    # Redirect to the dashboard or appropriate page
    return redirect('/dashboard/?show=branch')


#=======================================================================================================
#=======================================================================================================
#============================Batch Calculation========================================================

@csrf_exempt
def upload_multiple_files_batch(request):
    config_file = os.path.join(settings.MEDIA_ROOT, 'storage', 'user',  'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('BatchExcelFiles')
        num_files = len(uploaded_files)
        # display_name = request.user.username.split('@')[0]
        display_name = 'user'
        user_directory = os.path.join(settings.MEDIA_ROOT, 'storage', display_name)
        batch_directory = os.path.join(user_directory, 'Batch_Calculation')
        
        unique_id = str(uuid.uuid4()).split('-')[0]
        unique_folder_name = f"{num_files}Files_BatchCalculation_{unique_id}"
        unique_folder_path = os.path.join(batch_directory, unique_folder_name)
        os.makedirs(unique_folder_path, exist_ok=True)
        fs = FileSystemStorage(location=unique_folder_path)
        
        for uploaded_file in uploaded_files:
            fs.save(uploaded_file.name, uploaded_file)
        message = driver_part3(unique_folder_path, unique_folder_path, config)
        message=message[0]
        if "success" in message:
            messages.success(request, message)
        else:
            messages.error(request, message)
            # Optionally, delete the folder
            if os.path.exists(unique_folder_path):
                shutil.rmtree(unique_folder_path)

        return redirect('/dashboard/?show=batch')  # This assumes you want to redirect to a new request where the message will be displayed
    else:
        # If it's not a POST request, handle accordingly
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

#=======================================================================================================
def download_file_batch(request, file_name, folder_name):
    # Paths to the different folders
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'
    Batch_file_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Batch_Calculation', folder_name)
    # Check which folder contains the file
    if os.path.isfile(os.path.join(Batch_file_path, file_name)):
        file_path = os.path.join(Batch_file_path, file_name)
    else:
        raise Http404("File not found")

    # If the file exists, serve it
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response

    # If the file does not exist
    raise Http404("File not found")

#=======================================================================================================
def download_folder_batch(request, folder_name):
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'
    batch_calculation_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Batch_Calculation', folder_name)

    # Create a ZIP file in memory
    response = HttpResponse(content_type='application/zip')
    zip_filename = f"{folder_name}.zip"
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk(batch_calculation_path):
            for filename in filenames:
                # Create complete filepath of file in directory
                file_path = os.path.join(foldername, filename)
                # Add file to zip
                zip_file.write(file_path, os.path.relpath(file_path, batch_calculation_path))

    return response
#=======================================================================================================
def delete_folder_batch(request, folder_name):
    # display_name = request.user.username.split('@')[0]
    display_name = 'user'
    branch_calculation_path = os.path.join(settings.MEDIA_ROOT, 'storage', display_name, 'Batch_Calculation')

    # Check if the directory exists
    if os.path.isdir(os.path.join(branch_calculation_path, folder_name)):
        branch_calculation_path = os.path.join(branch_calculation_path, folder_name)

    # Delete the folder and all its contents
    if os.path.exists(branch_calculation_path):
        shutil.rmtree(branch_calculation_path)

    # Redirect to the dashboard or appropriate page
    return redirect('/dashboard/?show=batch')








