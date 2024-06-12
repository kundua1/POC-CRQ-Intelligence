from django.shortcuts import render
from dotenv import load_dotenv
import os

load_dotenv()


def index(request):
    return render(request, "crq_app/index.html")


def home(request):
    return render(request, "crq_app/home.html")


def app_server_mapping(request):
    from . import db
    unique_business_units_sql_query = f"""SELECT DISTINCT
                                                Business_Unit
                                            FROM
                                                Wintel_Inventory
                                            ORDER BY
                                                Business_Unit;
                                            """
    wintel_inventory_table_name = str(os.getenv('WINTEL_INVENTORY_TABLE_NAME'))
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
    print(mapping_data)
    
    context = {
        'mapping_data': mapping_data        
    }    
    
    return render(request, "crq_app/app_server_mapping.html", context=context)


def project_manager_view(request):
    return render(request, "crq_app/project_manager_view.html")