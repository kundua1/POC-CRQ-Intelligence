from django.shortcuts import render, redirect
from django.http import HttpResponse
from dotenv import load_dotenv
import os

# Login Imports Below
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth

from django.contrib import messages

import sys
sys.path.insert(1, 'crq_project\\crq_app\\misc_functions\\llm_functions')
# from . import get_llm_response

load_dotenv()


def handleLogin(request):
    if request.method == 'POST':
        login_username = request.POST['login_username']
        login_password = request.POST['login_password']

        user = authenticate(username=login_username,
                            password=login_password)

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
    return render(request, "crq_app/login_validation.html")


@login_required
def home(request):
    from . import db
    
    # Metrics Data
    unique_apps_servers_count_query = f"""SELECT 
                                        Business_Unit,
                                        COUNT(DISTINCT Application_Name) AS unique_applications_count,
                                        COUNT(DISTINCT FQDN) AS unique_servers_count
                                    FROM {str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))}
                                    GROUP BY Business_Unit;"""
    unique_apps_servers_count = db.get_data(sql_query=unique_apps_servers_count_query)
    
    # Ongoing
    
    # Upcoming
    
    # Past
    past_crq_table_name = str(os.getenv('PREVIOUS_CRQ_TABLE_NAME'))    
    fetch_all_past_crq_details_query = f"""select * from {past_crq_table_name} order by id desc;"""    
    past_crq_all_data = db.get_data(sql_query=fetch_all_past_crq_details_query)
    
    # Business Unit Data
    wintel_inventory_table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))    
    business_unit_count_query = f"""SELECT COUNT(DISTINCT Business_Unit) AS distinct_BU_count from {wintel_inventory_table_name};"""    
    business_unit_count = db.get_data(sql_query=business_unit_count_query)
    print(business_unit_count)
    
    context = {
        'past_crq_all_data': past_crq_all_data,
        'business_unit_count': business_unit_count,
        'unique_apps_servers_count': unique_apps_servers_count
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


@login_required
def smoo_view(request):
    from . import db
    
    upcoming_crq_query = f"""select * from {str(os.getenv('UPCOMING_CRQ_TABLE_NAME'))}"""
    upcoming_crq_all_data = db.get_data(sql_query=upcoming_crq_query)
    
    context = {
        'upcoming_crq_all_data': upcoming_crq_all_data
    }
    return render(request, "crq_app/smoo_manager_view.html", context=context)