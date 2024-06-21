from django.shortcuts import render, redirect
from django.http import HttpResponse
from dotenv import load_dotenv
import os

# Login Imports Below
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

from django.contrib import messages

load_dotenv()


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,
                            password=loginpassword)

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, "Invalid Credentials! \n Please check your Username & Password or Contact Administrator")
            return redirect('/')

    return HttpResponse('404 - Not Found')


def handleLogout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    

def index(request):
    return render(request, "crq_app/index.html")


@login_required
def home(request):
    from . import db
    # Ongoing
    
    # Upcoming
    
    # Past
    past_crq_table_name = str(os.getenv('PREVIOUS_CRQ_TABLE_NAME'))    
    fetch_all_past_crq_details_query = f"""select * from {past_crq_table_name} order by id desc;"""    
    past_crq_all_data = db.get_data(sql_query=fetch_all_past_crq_details_query)
    print(past_crq_all_data)
    
    context = {
        'past_crq_all_data': past_crq_all_data
    }
    return render(request, "crq_app/home.html", context=context)


@login_required
def app_server_mapping(request):
    from . import db
    
    filter_mapping_data = []
    wintel_inventory_table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))
    
    unique_application_sql_query = f"""SELECT DISTINCT Application_Name FROM {wintel_inventory_table_name} ORDER BY Application_Name;"""
    unique_application_data = db.get_data(sql_query=unique_application_sql_query)
    
    unique_application_owner_sql_query = f"""SELECT DISTINCT Application_Owner FROM {wintel_inventory_table_name} ORDER BY Application_Owner;"""
    unique_application_owner_data = db.get_data(sql_query=unique_application_owner_sql_query)
    
    unique_business_unit_sql_query = f"""SELECT DISTINCT Business_Unit FROM {wintel_inventory_table_name} ORDER BY Business_Unit;"""
    unique_business_unit_data = db.get_data(sql_query=unique_business_unit_sql_query)
    
    if request.method == 'POST':
        application_name = request.POST['application_name']
        application_owner = request.POST['application_owner']
        business_unit = request.POST['business_unit']
        
        if application_name != "select" and application_owner == "select" and business_unit == "select":
            filter_mapping_sql_query = f"""SELECT * FROM {wintel_inventory_table_name} WHERE Application_Name = '{application_name}' ORDER BY Application_Name;"""
            filter_mapping_data = db.get_data(sql_query=filter_mapping_sql_query)
            
        elif application_name == "select" and application_owner != "select" and business_unit == "select":
            filter_mapping_sql_query = f"""SELECT * FROM {wintel_inventory_table_name} WHERE Application_Owner = '{application_owner}' ORDER BY Application_Owner;"""
            filter_mapping_data = db.get_data(sql_query=filter_mapping_sql_query)
            
        elif application_name == "select" and application_owner == "select" and business_unit != "select":
            filter_mapping_sql_query = f"""SELECT * FROM {wintel_inventory_table_name} WHERE Business_Unit = '{business_unit}' ORDER BY Business_Unit;"""
            filter_mapping_data = db.get_data(sql_query=filter_mapping_sql_query)
    
    business_unit = "T&D"
    
    mapping_data_sql_query = f"""SELECT
                        Application_Name,
                        Application_Owner,
                        FQDN
                    FROM
                        {wintel_inventory_table_name}
                    WHERE
                        Business_Unit = '{business_unit}'
                    ORDER BY
                        Application_Name,
                        Application_Owner;"""
                        
    mapping_data = db.get_data(sql_query=mapping_data_sql_query)
    
    
    
    context = {
        'unique_application_data': unique_application_data,
        'unique_application_owner_data': unique_application_owner_data,
        'unique_business_unit_data': unique_business_unit_data,
        'filter_mapping_data': filter_mapping_data,
        'mapping_data': mapping_data        
    }    
    
    return render(request, "crq_app/app_server_mapping.html", context=context)


@login_required
def project_team_view(request):
    from . import db
    
    application_name = ""
    project_required_days = ""
    server_dependency_data = []
    upcoming_crq_data = []
    
    wintel_inventory_table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))
    
    wintel_unique_app_names_sql_query = f"""SELECT DISTINCT
                                                Application_Name
                                            FROM
                                                {wintel_inventory_table_name}
                                            ORDER BY
                                                Application_Name;
                                            """
    wintel_unique_apps_data = db.get_data(sql_query=wintel_unique_app_names_sql_query)
    
    if request.method == 'POST':
        application_name = request.POST['application_name']
        project_required_days = request.POST['required_days']
        
        if application_name != "select":
            server_dependency_query = f"""SELECT DISTINCT FQDN FROM {wintel_inventory_table_name} WHERE Application_Name = '{application_name}';""" 
            server_dependency_data = db.get_data(sql_query=server_dependency_query)
            
            upcoming_crq_table_name = str(os.getenv('UPCOMING_CRQ_TABLE_NAME'))
            upcoming_crq_query = f"""select * from {upcoming_crq_table_name}"""
            upcoming_crq_data = db.get_data(sql_query=upcoming_crq_query)    
    
    context = {
        'wintel_unique_apps_data': wintel_unique_apps_data,
        'application_name': application_name,
        'project_required_days': project_required_days,
        'server_dependency_data': server_dependency_data,
        'upcoming_crq_data': upcoming_crq_data
    }
    
    return render(request, "crq_app/project_team_view.html", context)


@login_required
def app_owner_view(request):
    from . import db
    
    upcoming_crq_table_name = str(os.getenv('UPCOMING_CRQ_TABLE_NAME'))    
    fetch_all_upcoming_crq_details_query = f"""select * from {upcoming_crq_table_name} order by id desc;"""    
    upcoming_crq_all_data = db.get_data(sql_query=fetch_all_upcoming_crq_details_query)
    
    if request.method == 'POST':
        action_taken = request.POST['crq_number']
        print(action_taken)
    
    conflict_counter = 2
    
    context = {
        'upcoming_crq_all_data': upcoming_crq_all_data,
        'conflict_counter': conflict_counter
    }
    return render(request, "crq_app/app_owner_view.html", context= context)