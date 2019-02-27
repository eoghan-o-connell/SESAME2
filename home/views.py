# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .forms import PublishForm
from accounts.models import Call, Center, Proposal, Reviewer
from accounts.forms import CenterForm, ProposalForm
import MySQLdb as _db
import os
import datetime


host_name = "mysql.netsoc.co"
user_name = "nadehh"
password = "HjOEsz2C483h"
db_name = "nadehh_db_final"
db_info_string="< %s > @ < %s >"%(db_name,host_name)
result = "fail"

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        tableData = Call.objects.all()
        context = {'tableData':tableData}
        return render(request, self.template_name, context)

def view_center(request):
    center_obj = Center.objects.filter(admin_id=request.user.id).values()
    context = {'center_obj':center_obj}
    return render(request, 'home/view_center.html', context)

def create_center(request):
    if request.method == 'POST':
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save(admin=request.user)
            return redirect(reverse('home:view_center'))
    else:
        form = CenterForm()
    return render(request, 'home/create_center.html', {'form': form})

def get_call_view(request):
    call_id = request.GET.get('call_id', '')
    call_obj = Call.objects.get(pk=call_id)
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user, call_obj)
            return redirect(reverse('home:home'))

    else:
        form = ProposalForm()

    call_id = request.GET.get('call_id', '')
    call_obj = Call.objects.filter(pk=call_id).values()
    context = {'call_obj':call_obj}
    return render(request, 'home/call_view.html', {'form':form, 'call_obj':call_obj})

def get_my_calls(request):
    user = request.user

    funder = user.funder
    researcher = user.researcher
    reviewer = user.reviewer

    call_id = request.GET.get('call_id', '')

    if funder:
        my_call_table_data = Call.objects.filter(funder_id=call_id).values()
        context = {'my_call_table_data':my_call_table_data}
    elif researcher:
        my_call_table_data = Proposal.objects.filter(user_id=request.user_id).values()
        context = {'my_call_table_data':my_call_table_data}
    else:
        my_call_table_data = Call.objects.filter(reviewer_id=request.user_id).values()
        context = {'my_call_table_data':my_call_table_data}

    return render(request, 'home/my_calls.html', context)

def pub (request):
    categories = []
    edit_info = []
    connection = None
    edit_toggle = False
    funds = ["€10,000 - €25,000","€25,000 - €50,000","€50,000 - €100,000","€100,000 - €250,000","€250,000 - €500,000","€500,000 - €1,000,000","€1,000,000 - €2,000,000"]
    editing_mode = False
    now = datetime.datetime.now()
    date_string = "%s-%s-%s"%(now.year,now.month,now.day)

    if request.method == "POST":
       now = datetime.datetime.now()
       date_string = "%s-%s-%s"%(now.year,now.month,now.day)

       print(request.user)
       fname = request.POST.get("fname")
       sname = request.POST.get("sname")
       eligibility = request.POST.get("tag")
       title = request.POST.get("title")
       description = request.POST.get("description")
       deadline = request.POST.get("date")
       grant = request.POST.get("grant")
       funder_id = request.user.id


       user = str(request.user)

       value = request.POST.get("editing_mode")

       if value == "True":
           editing_mode = True

       _call_id = request.POST.get("_call_id")

       # if os.path.isdir(userFileDir):
       #     print("exists")
       # else:
       #     os.makedirs(userFileDir)

       #print(request.POST.items())
       # for key in request.FILES:
       #     file = request.FILES[key]
       #     with open("/home/users/nadehh/django-uploads/%s"%(file.name),"wb+") as saveFile:
       #         for line in file:
       #             saveFile.write(line)
       #         print("File has been saved")
       for key in request.FILES:
           file = request.FILES[key]
           # with open("%s/%s"%(userFileDir,file.name),"wb+") as saveFile:
           #     print("OPENING FILE AND WRITING TO IT")
           #     for line in file:
           #         saveFile.write(line)
           #     print("File has been saved")
           filename = file.name
       # print("======================",value,_call_id)



       db_query = """

           INSERT INTO calls (target, created, funder_id, title, description, deadline,funds, file_location)
           VALUES ("%s","%s","%s","%s","%s","%s","%s","%s");

       """ %(eligibility,date_string,funder_id,title,description,deadline,grant,filename)

       print("$"*50)

       if editing_mode:
          db_query = """

              UPDATE calls
              SET target="%s",
                  created="%s",
                  funder_id=%d,
                  title="%s",
                  description="%s",
                  deadline="%s",
                  funds="%s"
              WHERE id = %d;

          """ %(eligibility,date_string,int(funder_id),title,description,deadline,grant,int(_call_id))

       userFileDir = "/home/users/nadehh/django-uploads/%s"%(user.split("@")[0])
       try:                        #success page if given to db
           connection = _db.connect(host=host_name,
                            user=user_name,
                            passwd=password,
                            db=db_name)

           result = "success"
           cursor = connection.cursor()

           cursor.execute(db_query)
           connection.commit()

       except _db.Error as e:
           print("Error connecting to the database.. check credentials!")
           print(e)

       finally:
           connection.close()

    if request.method == 'GET':
        try:
            connection = _db.connect(host=host_name,
                             user=user_name,
                             passwd=password,
                             db=db_name)

            print("#"*64 + "\n")
            print("%-25s %32s" % ("Connected to database:",db_info_string))
            print("%-25s %32s\n" % ("Established cursor:",db_info_string))
            print("#"*64)
            result = "success"
            cursor = connection.cursor()
            cursor.execute("""

                SELECT category FROM categories;

            """)

            for row in cursor.fetchall():
                categories.append(row[0])

            call_id = request.GET.get("call_id")

            if call_id is not None:
                edit_toggle = True

                cursor.execute("""

                    SELECT target,title, description, deadline, funds, file_location From calls WHERE id = %s;

                """%(call_id))

                row = cursor.fetchall()
                if len(row)!=0:
                    for data in row[0]:
                        edit_info.append(data)
                    edit_info[3] = str(edit_info[3])

                fund = edit_info[4].decode('utf-8')

                print("FUNDS -- > ", fund)

                funds.remove(fund)

                categories.remove(str(edit_info[0]))
                edit_info.append(call_id)

        except _db.Error as e:
            print("Error connecting to the database.. check credentials!")
            print(e)

        finally:
            connection.close()

    form = PublishForm()
    return render(request, 'home/publish_call.html',{'form':form,'db':categories, 'edit_info':edit_info, 'edit':edit_toggle, 'funds':funds})


# def home(request):
#     output = ""#strings initialised at start for later
#     sql_query = ""
#     if request.method == 'GET':
#         search_query = request.GET.get('search_box', '') #text entered by user
#         search_type = request.GET.get('search_type', None) #which table to query
#         searching = request.GET.get('searching', None) #what field to search in table
#         deadline_before = request.GET.get('deadline_before', None) #input fields for calls to filter by deadline
#         deadline_after = request.GET.get('deadline_after', None)
#         try:
#             connection = _db.connect(host=host_name, user=user_name, passwd=password, db=db_name)
#             cursor = connection.cursor(_db.cursors.DictCursor)
#             #this big massive if elif else statement is essentially just building an SQL query depending on the type of search the user is doing
#             if search_type == "calls_":
#                 sql_query = "SELECT eligibility, title, description, deadline FROM calls_ WHERE "
#                 if searching == 'title':
#                     sql_query += "title"
#                 else: #only allowing searching of title and description rn
#                     sql_query += "description"
#                 sql_query +=" LIKE '%"
#                 sql_query += search_query
#                 sql_query += "%' "
#                 if deadline_before:
#                     sql_query += "AND deadline < '%s' "%str(deadline_before)
#                 if deadline_after:
#                     sql_query += "AND deadline > '%s' "%str(deadline_after)
#                 sql_query += ";"
#             elif search_type == "centers": #only allowing to search for centres by name atm
#                 sql_query = "SELECT name FROM centers WHERE name LIKE '%"
#                 sql_query += search_query
#                 sql_query += "%';"
#             elif search_type == "papers":
#                 sql_query = "SELECT title, description, r.job_title, c.name FROM papers AS p, researchers AS r, centers AS c WHERE "
#                 if searching == "title":
#                     sql_query += "p.title "
#                 elif searching == "researcher":
#                     sql_query += "r.jobtitle "
#                 elif searching == "center":
#                     sql_query += "c.name "
#                 else:
#                     sql_query += "p.description "
#                 sql_query +=" LIKE '%" #LIKE allows for a blank search if user puts in no input but will display all results
#                 sql_query += search_query
#                 sql_query += "%' AND p.researcher=r.researcher AND c.center=p.center ;"
#             else:
#                 pass
#             cursor.execute(sql_query)
#             #building table from executed SQL statemet
#             output += "<table>"
#             for row in cursor.fetchall(): #currently does not display the column titles
#                 output += "<tr>"
#                 for column in row:
#                     output += "<td>"
#                     output += str(row[column])
#                     output += "</td>"
#                 output += "</tr>"
#             output += "</table>"
#         except Exception as e: #change later
#             output = "<p>"
#             output += str(e)
#             output +="</p>"
#             output +="<p>"
#             output += str(search_query)
#
#     return HttpResponse("""<head>
#                             <style>
#                             table, td, th { border: 1px solid black;}
#                             table {border-spacing: 50px 0;}
#                             th, td { padding:15px;}
#                             </style>
#                             </head>
#                             <body>
#                                 <h1> Searchbar
#                                 </h1>
#                                 <form type="get" action="." style="margin: 0">
#                                     <input  id="search_box" type="text" name="search_box"  placeholder="Search..." >
#                                     <select id='search_type' name="search_type" onchange="variableSelect()">
#                                         <option value="calls_">Calls</option>
#                                         <option value="centers">Centers</option>
#                                         <option value="papers">Papers</option>
#                                     </select>
#                                     <button id="search_submit" type="submit" >Submit</button>
#                                     <div id="filter_div"></div>
#                                 </form>
#                                 <p1>%s</p1>
#                                 <script>
#                                     function variableSelect(){
#                                         var search_var = document.getElementById("search_type").value;
#                                         if (search_var == "calls_"){
#                                             filter_div.innerHTML=" <input type='radio' name='searching' value='title'>Title<input type='radio' name='searching' value='description'>Description<br>Deadline Before: <input type='date' name='deadline_before'/><br>Deadline After: <input type='date' name='deadline_after'/> ";
#                                         }
#                                         else if (search_var == "centers") {
#                                             filter_div.innerHTML=""
#                                         }
#                                         else if (search_var == "papers"){
#                                             filter_div.innerHTML="<input type='radio' name='searching' value='title'>Title<input type='radio' name='searching' value='description'>Description<input type='radio' name='searching' value='researcher'>Researcher<input type='radio' name='searching' value='center'>Center";
#                                         }
#                                     }
#                                 </script>
#                             </body> """%output)
