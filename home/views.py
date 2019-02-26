# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse
from .forms import PublishForm
from accounts.models import Call
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

def get_call_view(request):
    call_id = request.GET.get('call_id', '')
    call_obj = Call.objects.filter(pk=call_id).values()
    context = {'call_obj':call_obj}
    return render(request, 'home/call_view.html', context)

def get_my_calls(request):
    call_id = request.GET.get('call_id', '')
    my_call_table_data = Call.objects.filter(funder_id=call_id).values()
    context = {'my_call_table_data':my_call_table_data}
    return render(request, 'home/my_calls.html', context)

def pub (request):
    l = []
    connection = None
    edit_toggle = False
    edit_info = []
    now = datetime.datetime.now()
    date_string = "%s-%s-%s"%(now.month,now.day,now.year)
    print(date_string)

    if request.method == "POST":
       now = datetime.datetime.now()
       date_string = "%s-%s-%s"%(now.month,now.day,now.year)

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

       editing_mode = request.POST.get("editing_mode") != None
       call_id = request.POST.get("call_id")

       for key in request.FILES:
           file = request.FILES[key]
           # with open("%s/%s"%(userFileDir,file.name),"wb+") as saveFile:
           #     print("OPENING FILE AND WRITING TO IT")
           #     for line in file:
           #         saveFile.write(line)
           #     print("File has been saved")
           filename = file.name
       print("___________________------------__________________",editing_mode,call_id)

       db_query = """

           INSERT INTO calls (target, created, funder_id, title, description, deadline,funds, file_location)
           VALUES ('%s','%s','%s','%s','%s','%s',%d,'%s');

       """ %(eligibility,date_string,funder_id,title,description,deadline,int(grant),filename)

       print("$"*50)

       if editing_mode:
          db_query = """

              UPDATE calls
              SET target='%s'
                  date_string='%s'
                  funder_id='%s',
                  title='%s',
                  description='%s',
                  deadline='%s',
                  funds=%d,
              WHERE call_id = '%s'

          """ %(eligibility,date_string,funder_id,title,description,deadline,int(grant),call_id)

       else:
          print("creating a new call man")

       print("$"*50)


       userFileDir = "/home/users/nadehh/django-uploads/%s"%(user.split("@")[0])
       # if os.path.isdir(userFileDir):
       #     print("exists")
       # else:
       #     os.makedirs(userFileDir)

       try:                        #success page if given to db
           connection = _db.connect(host=host_name,
                            user=user_name,
                            passwd=password,
                            db=db_name)

           print("#"*64 + "\n")
           print("%-25s %32s" % ("Connected to database POST:",db_info_string))
           print("%-25s %32s\n" % ("Established cursor POST:",db_info_string))
           print("#"*64)
           result = "success"
           cursor = connection.cursor()

           print("ABOUT TO EXECUTE QUERY")

           # stri=("""
           #
           #     INSERT INTO calls (target, title, description, deadline,funds, file_location)
           #     VALUES ('%s','%s','%s','%s',%d,'%s');
           #
           #
           # """ %(eligibility,title,description,deadline,int(grant),filename))

           print("________________________________________________________")
           print(db_query)
           print("________________________________________________________")


           cursor.execute(db_query)

           connection.commit()

           print("SUCCESSFULLY UPDATED TABLE WAHOOOO LETS GO BOYS")

           # for row in cursor.fetchall():
           #     print(row)

       except _db.Error as e:
           print("Error connecting to the database.. check credentials!")
           print(e)

       finally:
           connection.close()



        #print(request.POST.items())
            # for key in request.FILES:
            #     file = request.FILES[key]
            #     with open("/home/users/nadehh/django-uploads/%s"%(file.name),"wb+") as saveFile:
            #         for line in file:
            #             saveFile.write(line)
            #         print("File has been saved")


    if request.method == 'GET':
        #print(request.GET.items())
        #use this to check if all the form items have been given
        #then you can update the db
        #if request.GET.get('ok') != None: #this is just a test to make sure we can give proper
        try:                        #success page if given to db
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

            l =[]
            for row in cursor.fetchall():
                l.append(row[0])
            print(l)

            call_id = request.GET.get("call_id")
            if call_id is not None:
                edit_toggle = True

                cursor.execute("""

                    SELECT target,title, description, deadline, funds, file_location From calls WHERE id = %s;

                """%(call_id))

                for row in cursor.fetchall():
                    for data in row:
                        edit_info.append(data)
                print(edit_info)
                edit_info[3] = str(edit_info[3])

                print(edit_info)

                print(str(edit_info[3]))

                edit_info.append(call_id)

            # for row in cursor.fetchall():
            #     print(row)

        except _db.Error as e:
            print("Error connecting to the database.. check credentials!")
            print(e)

        finally:
            connection.close()


    form = PublishForm()
    return render(request, 'home/publish_call.html',{'form':form,'db':l, 'edit_info':edit_info, 'edit':edit_toggle})
    #return HttpResponse("publish calls")


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
