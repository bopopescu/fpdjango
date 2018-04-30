from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.views import login, logout
from django.contrib.auth import authenticate
from django.views.generic import View
from .forms import UserForm, FoodClass
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from matplotlib.colors import ListedColormap
from django.contrib import messages
from collections import OrderedDict
import logging
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from django.contrib.auth.models import User


class UserFormView(View):
    form_class = UserForm
    template_name = 'freshpointapp/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request)
                    return redirect('/success')

        # if user didn't login, redirect to login
        return render(request, self.template_name, {'form': form})


def clean_password1(self):
    password = self.cleaned_data.get(User.password)
    if len(password) < 8:
        messages.info(self, 'Your password needs to be at least 8 characters long')
    return super(UserFormView, self).clean_password1()


def intro(request):
    introduce = loader.get_template('freshpointapp/intro.html')
    context = {

    }
    return HttpResponse(introduce.render(context, request))


def about(request):
    about = loader.get_template('freshpointapp/about.html')
    context = {

    }
    return HttpResponse(about.render(context, request))


def index(request):
    mainpage = loader.get_template('freshpointapp/index.html')
    context = {

    }
    user = request.user
    if not user.is_authenticated:
        return redirect('/')
    return HttpResponse(mainpage.render(context, request))


def login(request):
    login = loader.get_template('freshpointapp/login.html')
    context = {

    }
    return HttpResponse(login.render(context, request))


def logout_view(request):
    logOut = loader.get_template('freshpointapp/logout.html')
    context = {

    }

    logout(request)
    return redirect(logOut)


def success(request):
    success = loader.get_template('freshpointapp/success.html')
    context = {

    }
    return HttpResponse(success.render(context, request))


def upload(request):
    uploadpage = loader.get_template('freshpointapp/upload.html')
    context = {

    }
    return HttpResponse(uploadpage.render(context, request))


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "freshpointapp/upload.html", data)
    # if not GET, then proceed

    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("freshpointapp/upload.html"))

        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("freshpointapp/upload.html"))

        #Variable declaration for FVT
        Saleshist = []
        fvt_list = [(19,'GREEN ONIONS',0,0,0,0,0,1,1,1,1,0,0,0,1017596),(12,'CHERRY TOMATOES',0,0,0,0,0,0,1,1,1,1,0,0,1106274),(50,'SPRITE MELONS',0,0,0,0,0,0,1,1,0,0,0,0,1197281),(7,'BROCCOLI',0,0,0,1,1,0,0,0,0,0,0,0,1201376),(24,'INDIA CORN ',0,0,0,0,0,0,0,0,1,1,1,0,1201958),(49,'SPINACH',1,1,1,1,1,0,0,0,0,1,1,1,1250955),(32,'OKRA',0,0,0,0,0,0,1,1,0,0,0,0,1295483),(54,'SWEET POTATOES',1,1,1,1,1,1,1,1,1,1,1,1,1583974),(45,'ROMAINE',0,0,0,1,1,0,0,0,0,1,1,0,1657272),(10,'CANTALOUPES',0,0,0,0,0,0,1,1,0,0,0,0,1695538),(42,'PUMPKINS',0,0,0,0,0,0,0,0,1,1,0,0,1840745),(31,'NECTARINES',0,0,0,0,0,0,1,1,0,0,0,0,1893549),(26,'LETTUCE',0,0,0,1,1,0,0,0,0,1,1,1,1910007),(16,'EGGPLANT',0,0,0,0,0,1,1,1,0,0,0,0,1921959),(44,'RASPBERRIES',0,0,0,0,0,1,0,0,1,1,0,0,1925689),(23,'HONEYDEW MELONS',0,0,0,0,0,0,1,1,0,0,0,0,2035329),(15,'CUCUMBERS',0,0,0,0,0,1,1,1,1,1,1,0,2125830),(2,'ASPARAGUS',0,0,1,1,0,0,0,0,0,0,0,0,2289502),(39,'PERSIMMONS',0,0,0,0,0,0,0,0,1,1,0,0,2361346),(4,'BLACKBERRIES',0,0,0,0,0,1,1,0,1,0,0,0,2497648),(1,'APPLES ',1,1,0,0,0,0,0,1,1,1,1,1,2557119),(21,'GREENS',0,0,1,1,1,1,1,1,1,1,1,1,2621525),(53,'SWEET CORN',0,0,0,0,0,1,1,1,1,0,0,0,2834656),(27,'MUSCADINE GRAPES',0,0,0,0,0,0,0,1,1,1,0,0,2845392),(43,'RADISHES',0,0,0,1,1,1,0,0,0,1,1,0,2946537),(11,'CARROTS',1,0,0,0,0,1,1,0,0,0,0,1,2953655),(29,'MUSTARD GREENS',0,0,0,1,1,1,0,0,1,1,1,1,2971863),(57,'WATERMELON',0,0,0,0,0,0,1,1,0,0,0,0,2979790),(14,'COLLARDS',1,1,1,1,1,1,1,1,1,1,1,1,3002007),(55,'TOMATOES',0,0,0,0,0,1,1,1,1,1,0,0,3013774),(34,'PEACHES',0,0,0,0,0,1,1,1,1,0,0,0,3058103),(20,'GREENS PEAS',0,0,0,0,1,0,0,0,0,0,0,0,3304894),(5,'BLUEBERRIES',0,0,0,0,1,1,1,0,0,0,0,0,3412757),(13,'CHRISTMAS TREES',0,0,0,0,0,0,0,0,0,0,1,1,3442780),(3,'BEETS',0,0,0,0,1,1,0,0,0,1,1,1,3509996),(46,'SNAP BEANS',0,0,0,0,0,1,1,1,1,0,0,0,3555013),(35,'PEANUTS',1,1,1,1,1,1,1,1,1,1,1,1,3658846),(25,'KALE',0,0,0,0,1,1,0,0,0,1,1,1,3676040),(30,'NAPA',0,0,0,0,1,1,0,0,0,1,1,0,3754851),(9,'CABBAGE',0,0,0,0,1,1,1,1,1,1,1,1,3805072),(6,'BOKCHOY',0,0,0,0,1,1,0,0,0,1,1,1,3810851),(56,'TURNIPS',0,0,0,1,1,1,0,0,0,1,1,1,3838576),(51,'SQUASH-YELLOW',0,0,0,0,1,1,1,1,1,0,0,0,3852220),(8,'BUTTERBEANS',0,0,0,0,0,0,1,1,0,0,0,0,3882505),(41,'POTATOES',0,0,0,0,0,1,1,0,0,0,0,0,3898135),(58,'ZUCCHINI',0,0,0,0,1,1,1,1,1,0,0,0,3981754),(59,'TOMATILLO',0,0,0,0,0,1,1,1,1,1,0,0,3981755),(28,'MUSHROOMS',0,0,1,1,1,1,0,0,1,1,1,0,4067311),(37,'PECANS',0,0,0,0,0,0,0,0,0,0,1,1,4127838),(36,'PEARS',0,0,0,0,0,0,0,1,1,1,0,0,4236146),(17,'FIGS',0,0,0,0,0,0,1,1,1,1,1,1,4335992),(40,'PLUMS',0,0,0,0,0,1,1,1,0,0,0,0,4487531),(52,'STRAWBERRIES',0,0,0,1,1,1,0,0,0,0,0,0,4494988),(48,'SNOW PEAS TIPS',0,0,0,1,1,0,0,0,0,1,1,0,4496223),(38,'PEPPERS',0,0,0,0,0,1,1,1,0,0,0,0,4606080),(33,'ONIONS ',0,0,0,0,0,1,1,0,0,0,0,0,4672570),(47,'SNOW PEAS',0,0,0,0,1,1,0,0,0,1,1,0,4852257),(22,'HERBS',1,1,1,1,1,1,1,1,1,1,1,1,4902192),(18,'GARLIC',0,0,0,0,0,0,1,1,0,0,0,0,4921692)]
        fvt_list = sorted(fvt_list, key=lambda fvt: fvt[0])
        #print (fvt_list)
        column_names = ("ID","Food","January","February","March","April","May","June","July","August","September","October","November","December","ProductID")
        month_names = ["Food","January","February","March","April","May","June","July","August","September","October","November","December"]
        fvt_dict = {}
        combo_dict = {}

        def column(fvt_list, colnum):
            return ([row[colnum] for row in fvt_list])

        for y in range(len(column_names)):
            fvt_dict[column_names[y]] = column(fvt_list, y)

        for y in range(len(column_names)):
            if column_names[y] != "ID" and column_names[y] != "ProductID":
                #print (column_names[y])
                combo_dict[column_names[y]] = column(fvt_list, y)
        #print (fvt_dict)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        data_dict = {"Description":[],"Cases":[],"Hunmiles":[],"Twohunmiles":[],"Fivhunmiles":[],"CsvMonth":[],"CsvYear":[],"Local":[],"FoodType":[]}
        #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:

            fields = line.split(",")

            data_dict["Description"].append(fields[0])
            if fields[1].upper() == 'CASES':
                data_dict["Cases"].append(0.0)
            else:
                data_dict["Cases"].append(float(fields[1]))
            data_dict["Hunmiles"].append(fields[2])
            data_dict["Twohunmiles"].append(fields[3])
            data_dict["Fivhunmiles"].append(fields[4])
            data_dict["CsvMonth"].append(fields[5])
            data_dict["CsvYear"].append(fields[6])
            if 'LOCAL' in fields[7].upper():
                data_dict["Local"].append(0.0)
            else:
                re.sub('[^A-Za-z0-9]+', '', fields[7])
                data_dict["Local"].append(float(fields[7]))

            #data_dict = dict(map(str.strip,x) for x in data_dict.items())

        for x in data_dict["Description"]:
            alreadyappended = False
            counter =0
            for y in combo_dict["Food"]:
                counter+=1
                if y in x.upper():
                    alreadyappended = True
                    data_dict["FoodType"].append(y)
                    break
            if alreadyappended is False and counter == len(combo_dict["Food"]):
                #print (counter)
                data_dict["FoodType"].append('')

        #for x in data_dict["Description"], y in data_dict["FoodType"]:
        #    for z in x:
        #        print (z," \/ ",y, "\n")

        fp_data = pd.DataFrame.from_dict(data_dict)
        fp_data = fp_data.iloc[1:]
        fp_final_df = fp_data[['CsvMonth','Cases','FoodType']]
        #fp_final_df.to_numeric('Cases')
        #fp_final_df = fp_final_df.loc[fp_final_df['Local'] == 0]
        fp_final_df = fp_final_df.loc[fp_final_df['FoodType'] != '']
        fp_final_df = fp_final_df.reset_index(drop=True)
        fp_final_df = fp_final_df.groupby(["""CsvMonth""", """FoodType"""]).sum().reset_index()
        print (fp_final_df.keys())
        fp_final_df.to_csv('fp_final_df.txt', header=None, sep=' ', mode='w')
        print ("""still here""")
        #print (fp_final_df)
        """try:
                form = FoodClass(data_dict)
                if form.is_valid():
                    form.save()                    
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())                                                
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))                    
                pass"""

        #print(combo_dict)
        sorted_combo_dict = OrderedDict(sorted(combo_dict.items(),key =lambda x:month_names.index(x[0])))
        #print(sorted_combo_dict)
        FVT = pd.DataFrame(sorted_combo_dict)
        #print (FVT)


        def hmFVT2FP(fvtProduct,fvtMonth,fvtAvailability,FreshPoint):
            inner=0
            global localCount
            for fpindex, fprow in FreshPoint.iterrows():
                fpMonth = fprow['CsvMonth']
                fpCases = fprow['Cases']
                fpProduct = fprow['FoodType']
                #print ('fvtProduct: ', fvtProduct, ' fpProduct: ', fpProduct, '| fpMonth: ', fpMonth, ' fvtMonth: ',
                #       fvtMonth, '| fpCases: ', fpCases, '| fvtAvailability: ', fvtAvailability,' AKA fvtrow[fvtProduct] : ', fvtrow[fvtProduct], '\n', file=f)

                if fpMonth.lower() == fvtMonth.lower() and fpProduct.lower()==fvtProduct.lower():
                    inner+=1
                    if fpCases > 0.0:

                        if fvtAvailability == 0.0:
                            available.append(2)

                        elif fvtAvailability == 1.0:
                            available.append(3)
                            #localCount += 1 #keep track of how many are locally purchased may be better to perform act from sql
                        else:
                            break

                        #available.append(0)
                    elif fvtAvailability == 1.0:
                        #print (fprow)
                        available.append(1)
                    else:
                        available.append(0)
            #print available, '|'
            return inner



        available=[]
        fpMonth=''
        fpProduct=''
        fvtMonth=''
        fvtProduct=''

        transFVT = FVT.set_index('Food').T
        #print (transFVT)
        for fvtindex, fvtrow in transFVT.iterrows():
            for product in fvtrow.index:
                #print ('fvtindex: ',fvtindex,'|product: ', product,'|fvtrow[product]: ', fvtrow[product])
                fvtProduct = product
                fvtMonth = fvtindex
                fvtAvailability = fvtrow[product]
                #print (fvtProduct, ' / ', fvtMonth, ' / ', fvtAvailability, '\n')

                outer = hmFVT2FP(fvtProduct,fvtMonth,fvtAvailability,fp_final_df)
                if outer == 0 and fvtAvailability == 0.0:
                    available.append(0)
                if outer == 0 and fvtAvailability == 1.0:
                    available.append(1)

        print (available, '\n')
        print (len(available))

        #available = [1, 2, 2, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 1, 2, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 1, 0, 2, 0, 2, 0, 0, 0, 1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 3, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 1, 0, 2, 0, 2, 0, 1, 0, 1, 0, 0, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 3, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 1, 0, 2, 0, 2, 0, 1, 0, 1, 0, 0, 2, 3, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 3, 0, 0, 1, 3, 0, 0, 1, 0, 1, 0, 0, 1, 2, 2, 0, 0, 1, 0, 1, 1, 3, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 3, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 3, 0, 1, 1, 3, 0, 1, 1, 0, 1, 0, 0, 1, 0, 3, 0, 0, 3, 1, 1, 1, 2, 0, 1, 0, 1, 0, 0, 1, 1, 3, 0, 2, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 2, 1, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 2, 3, 0, 0, 2, 1, 1, 0, 2, 1, 3, 1, 1, 1, 0, 1, 1, 1, 1, 3, 1, 3, 0, 1, 1, 0, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0, 1, 1, 1, 1, 0, 3, 3, 1, 0, 0, 0, 0, 0, 2, 1, 3, 1, 0, 1, 0, 1, 1, 1, 1, 3, 1, 1, 0, 1, 1, 0, 2, 2, 1, 0, 0, 0, 1, 3, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0, 1, 1, 1, 1, 0, 3, 3, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 2, 1, 1, 0, 1, 0, 1, 2, 2, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 2, 1, 0, 0, 2, 0, 1, 0, 1, 1, 3, 1, 0, 0, 3, 1, 0, 1, 0, 0, 1, 2, 0, 3, 0, 0, 1, 0, 1, 1, 2, 1, 2, 0, 3, 0, 1, 0, 1, 3, 3, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 3, 0, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 2, 1, 0, 3, 0, 0, 1, 2, 0, 3, 0, 0, 0, 1, 1, 1, 2, 1, 2, 0, 3, 0, 1, 0, 1, 3, 3, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 1, 3, 0, 0, 0, 0, 1, 0, 0, 1, 2, 2, 1, 0, 1, 0, 0, 1, 2, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 2, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2]
        hm = pd.DataFrame(np.array(available).reshape(12,59), columns =list(transFVT.columns),index=list(transFVT.index))
        #print hm
        plt.figure(figsize=(20,7))
        #   plt.xticks("""fontsize=10, rotation=90""")
        plt.ylabel('y',rotation='vertical')
        hmFinish = sns.heatmap(hm,linecolor='black',cmap=ListedColormap(['None', 'yellow', 'green','red']),square=True,linewidth=.5)
        loc, labels = plt.xticks(fontsize=8, rotation=75)
        #hmFinish.set_yticklabels(labels[::-1], rotation=0)
        #hmFinish.xaxis.tick_top()
        cbar = hmFinish.collections[0].colorbar
        cbar.set_ticks([.4,1.15,1.85,2.62])
        cbar.set_ticklabels(['Seasonally Unavailable, No Purchase','Seasonally Availalable, No Azonic Purchased','Seasonally Unavailable, Azonic Purchase','Seasonally Avaliable, Azonic Purchase'])
        #cbar.cbar_kws={"shrink":.50}
        #hmFinish.set_title('Seasonal Opportunities')
        plt.suptitle('Seasonal Opportunities', x=.45, fontsize=14)
        plt.title("""Comparing what you've done with what you could do, with regards to purchasing locally.""", fontsize=10)
        plt.savefig("""/Users/Dasani/Freshpoint/freshpoint/freshpoint/static/img/W_W_heatmapv2.png""", dpi = 250)
        #return plt
        #plt.show()


    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))


    return redirect('/upload_csv')


