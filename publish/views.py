from django.shortcuts import render, HttpResponse
from .forms import PublishForm
#from django.core.files.storage import FileSystemStorage


import MySQLdb as _db

host_name = "mysql.netsoc.co"
user_name = "nadehh"
password = "HjOEsz2C483h"
db_name = "nadehh_db_new"
db_info_string="< %s > @ < %s >"%(db_name,host_name)
result = "fail"


def pub (request):
    l = []

    if request.method == "POST":
        print(request.POST)

        print(request.FILES)
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

            # for row in cursor.fetchall():
            #     print(row)

        except _db.Error as e:
            print("Error connecting to the database.. check credentials!")

        finally:
            connection.close()


    form = PublishForm()
    return render(request, 'publish/publish.html',{'form':form,'db':l})
    #return HttpResponse("publish calls")
