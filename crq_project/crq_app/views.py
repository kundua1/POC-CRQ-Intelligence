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
    wintel_inventory_table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))
    
    unique_business_units_sql_query = f"""SELECT DISTINCT
                                                Business_Unit
                                            FROM
                                                {wintel_inventory_table_name}
                                            ORDER BY
                                                Business_Unit;
                                            """
    
    business_unit = "T&D"
    
    sql_query = f"""SELECT
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
                        
    mapping_data = db.get_data(sql_query=sql_query)
    
    context = {
        'mapping_data': mapping_data        
    }    
    
    return render(request, "crq_app/app_server_mapping.html", context=context)


@login_required
def project_team_view(request):
    from . import db
    wintel_inventory_table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))
    
    wintel_unique_app_names_sql_query = f"""SELECT DISTINCT
                                                Application_Name
                                            FROM
                                                {wintel_inventory_table_name}
                                            ORDER BY
                                                Application_Name;
                                            """
    wintel_unique_apps_data = db.get_data(sql_query=wintel_unique_app_names_sql_query)
    
    context = {
        'wintel_unique_apps_data': wintel_unique_apps_data
    }
    
    return render(request, "crq_app/project_team_view.html", context)


@login_required
def app_owner_view(request):
    from . import db
    
    upcoming_crq_table_name = str(os.getenv('UPCOMING_CRQ_TABLE_NAME'))    
    fetch_all_upcoming_crq_details_query = f"""select * from {upcoming_crq_table_name} order by id desc;"""    
    past_crq_all_data = db.get_data(sql_query=fetch_all_upcoming_crq_details_query)
    
    context = {
        'past_crq_all_data': past_crq_all_data
    }
    return render(request, "crq_app/app_owner_view.html", context= context)