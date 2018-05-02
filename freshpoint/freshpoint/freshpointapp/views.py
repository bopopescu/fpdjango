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
from django.conf import settings
import os
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
    user = request.user
    if not user.is_authenticated:
        return redirect('/')
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
    user = request.user
    if not user.is_authenticated:
        return redirect('/')
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
        fvt_list = [(19,'GREEN ONIONS',0,0,0,0,0,1,1,1,1,0,0,0,1017596),(12,'CHERRY TOMATOES',0,0,0,0,0,0,1,1,1,1,0,0,1106274),(50,'SPRITE MELONS',0,0,0,0,0,0,1,1,0,0,0,0,1197281),(7,'BROCCOLI',0,0,0,1,1,0,0,0,0,0,0,0,1201376),(24,'INDIA CORN ',0,0,0,0,0,0,0,0,1,1,1,0,1201958),(49,'SPINACH',1,1,1,1,1,0,0,0,0,1,1,1,1250955),(32,'OKRA',0,0,0,0,0,0,1,1,0,0,0,0,1295483),(54,'SWEET POTATOES',1,1,1,1,1,1,1,1,1,1,1,1,1583974),(45,'ROMAINE',0,0,0,1,1,0,0,0,0,1,1,0,1657272),(10,'CANTALOUPE',0,0,0,0,0,0,1,1,0,0,0,0,1695538),(42,'PUMPKINS',0,0,0,0,0,0,0,0,1,1,0,0,1840745),(31,'NECTARINE',0,0,0,0,0,0,1,1,0,0,0,0,1893549),(26,'LETTUCE',0,0,0,1,1,0,0,0,0,1,1,1,1910007),(16,'EGGPLANT',0,0,0,0,0,1,1,1,0,0,0,0,1921959),(44,'RASPBERRIES',0,0,0,0,0,1,0,0,1,1,0,0,1925689),(23,'HONEYDEW',0,0,0,0,0,0,1,1,0,0,0,0,2035329),(15,'CUCUMBER',0,0,0,0,0,1,1,1,1,1,1,0,2125830),(2,'ASPARAGUS',0,0,1,1,0,0,0,0,0,0,0,0,2289502),(39,'PERSIMMONS',0,0,0,0,0,0,0,0,1,1,0,0,2361346),(4,'BLACKBERRIES',0,0,0,0,0,1,1,0,1,0,0,0,2497648),(1,'APPLE',1,1,0,0,0,0,0,1,1,1,1,1,2557119),(21,'GREENS',0,0,1,1,1,1,1,1,1,1,1,1,2621525),(53,'SWEET CORN',0,0,0,0,0,1,1,1,1,0,0,0,2834656),(27,'MUSCADINE GRAPES',0,0,0,0,0,0,0,1,1,1,0,0,2845392),(43,'RADISH',0,0,0,1,1,1,0,0,0,1,1,0,2946537),(11,'CARROTS',1,0,0,0,0,1,1,0,0,0,0,1,2953655),(29,'MUSTARD GREENS',0,0,0,1,1,1,0,0,1,1,1,1,2971863),(57,'WATERMELON',0,0,0,0,0,0,1,1,0,0,0,0,2979790),(14,'COLLARDS',1,1,1,1,1,1,1,1,1,1,1,1,3002007),(55,'TOMATO',0,0,0,0,0,1,1,1,1,1,0,0,3013774),(34,'PEACH',0,0,0,0,0,1,1,1,1,0,0,0,3058103),(20,'GREENS PEAS',0,0,0,0,1,0,0,0,0,0,0,0,3304894),(5,'BLUEBERRY',0,0,0,0,1,1,1,0,0,0,0,0,3412757),(13,'CHRISTMAS TREES',0,0,0,0,0,0,0,0,0,0,1,1,3442780),(3,'BEETS',0,0,0,0,1,1,0,0,0,1,1,1,3509996),(46,'SNAP BEANS',0,0,0,0,0,1,1,1,1,0,0,0,3555013),(35,'PEANUTS',1,1,1,1,1,1,1,1,1,1,1,1,3658846),(25,'KALE',0,0,0,0,1,1,0,0,0,1,1,1,3676040),(30,'NAPA',0,0,0,0,1,1,0,0,0,1,1,0,3754851),(9,'CABBAGE',0,0,0,0,1,1,1,1,1,1,1,1,3805072),(6,'BOKCHOY',0,0,0,0,1,1,0,0,0,1,1,1,3810851),(56,'TURNIP',0,0,0,1,1,1,0,0,0,1,1,1,3838576),(51,'SQUASH-YELLOW',0,0,0,0,1,1,1,1,1,0,0,0,3852220),(8,'BUTTERBEANS',0,0,0,0,0,0,1,1,0,0,0,0,3882505),(41,'POTATO',0,0,0,0,0,1,1,0,0,0,0,0,3898135),(58,'ZUCCHINI',0,0,0,0,1,1,1,1,1,0,0,0,3981754),(59,'TOMATILLO',0,0,0,0,0,1,1,1,1,1,0,0,3981755),(28,'MUSHROOM',0,0,1,1,1,1,0,0,1,1,1,0,4067311),(37,'PECANS',0,0,0,0,0,0,0,0,0,0,1,1,4127838),(36,'PEARS',0,0,0,0,0,0,0,1,1,1,0,0,4236146),(17,'FIGS',0,0,0,0,0,0,1,1,1,1,1,1,4335992),(40,'PLUMS',0,0,0,0,0,1,1,1,0,0,0,0,4487531),(52,'STRAWBERRY',0,0,0,1,1,1,0,0,0,0,0,0,4494988),(48,'SNOW PEAS TIPS',0,0,0,1,1,0,0,0,0,1,1,0,4496223),(38,'PEPPER',0,0,0,0,0,1,1,1,0,0,0,0,4606080),(33,'ONION',0,0,0,0,0,1,1,0,0,0,0,0,4672570),(47,'SNOW PEAS',0,0,0,0,1,1,0,0,0,1,1,0,4852257),(22,'HERB',1,1,1,1,1,1,1,1,1,1,1,1,4902192),(18,'GARLIC',0,0,0,0,0,0,1,1,0,0,0,0,4921692)]
        fvt_list = sorted(fvt_list, key=lambda fvt: fvt[0])
        column_names = ("ID","Food","January","February","March","April","May","June","July","August","September","October","November","December","ProductID")
        month_names = ["Food","January","February","March","April","May","June","July","August","September","October","November","December"]
        fvt_dict = {}
        combo_dict = {}

        def setavailable(transFVT,avallist):
            if avallist == available:
                for fvtindex, fvtrow in transFVT.iterrows():
                    for product in fvtrow.index:
                        fvtProduct = product
                        fvtMonth = fvtindex
                        fvtAvailability = fvtrow[product]

                        outer = hmFVT2FP(fvtProduct,fvtMonth,fvtAvailability,fp_final_df,available)
                        if outer == 0 and fvtAvailability == 0.0:
                            available.append(0)

                        if outer == 0 and fvtAvailability == 1.0:
                            available.append(1)

            if avallist == localavailable:
                for fvtindex, fvtrow in transFVT.iterrows():
                    for product in fvtrow.index:
                        fvtProduct = product
                        fvtMonth = fvtindex
                        fvtAvailability = fvtrow[product]

                        outer = hmFVT2FP(fvtProduct,fvtMonth,fvtAvailability,fp_final_df,localavailable)
                        if outer == 0 and fvtAvailability == 0.0:
                            localavailable.append(0)
                        if outer == 0 and fvtAvailability == 1.0:
                            localavailable.append(1)

        def setAzonicHeatmap(available, transFVT):
            #print (available)
            #print (len(available))
            hm = pd.DataFrame(np.array(available).reshape(12,59), columns =list(transFVT.columns),index=list(transFVT.index))
            plt.figure(figsize=(20,7))

            plt.ylabel('y',rotation='vertical')
            hmFinish = sns.heatmap(hm,linecolor='black',cmap=ListedColormap(['None', 'yellow', 'green','red']),square=True,linewidth=.5)
            loc, labels = plt.xticks(fontsize=8, rotation=75)
            cbar = hmFinish.collections[0].colorbar
            cbar.set_ticks([.4,1.15,1.85,2.62])
            cbar.set_ticklabels(['Seasonally Unavailable, No Purchase','Seasonally Availalable, No Azonic Purchased','Seasonally Unavailable, Azonic Purchase','Seasonally Avaliable, Azonic Purchase'])
            plt.suptitle('Seasonal Opportunities', x=.45, fontsize=14)
            plt.title("""Comparing what you've done with what you could do, with regards to purchasing locally.""", fontsize=10)
            #print("before savefig")
            plt.savefig(os.path.join(settings.BASE_DIR, 'static/img/W_W_heatmap_fin.png'), dpi = 250)
            plt.close()

        def setLocalHeatmap(localavailable, transFVT):
            #print(localavailable)
            #print(len(localavailable))
            hm = pd.DataFrame(np.array(localavailable).reshape(12,59), columns =list(transFVT.columns),index=list(transFVT.index))
            plt.figure(figsize=(20,8))
            plt.ylabel('y',rotation='vertical')
            hmFinish = sns.heatmap(hm,linecolor='black',cmap=ListedColormap(['None', 'grey','green','pink']),square=True,linewidth=.5)
            loc, labels = plt.xticks(fontsize=8, rotation=75)    #hmFinish.xaxis.tick_top()
            cbar = hmFinish.collections[0].colorbar
            cbar.set_ticks([.4,1.15,1.85,2.62])
            cbar.set_ticklabels(['Seasonally Unavailable, No purchase','Seasonally Available, No Local Purchase','Seasonally Available, Local Purchase','Seasonally Unavailable, Azonic Purchase'])
            plt.suptitle('Seasonal Improvement Opportunities', fontsize=16, x=.45)
            plt.savefig(os.path.join(settings.BASE_DIR, 'static/img/W_W_goodmapv_fin.png'), dpi = 200)
            plt.tight_layout()
            plt.close()

        def hmFVT2FP(fvtProduct,fvtMonth,fvtAvailability,FreshPoint,mapType):
            inner=0
            global localCount
            if mapType == available:
                for fpindex, fprow in FreshPoint.iterrows():
                    fpMonth = fprow['CsvMonth']
                    fpCases = fprow['Cases']
                    fpProduct = fprow['FoodType']
                    fpLocal = fprow['Local']
                    #print ('fvtProduct: ', fvtProduct, ' fpProduct: ', fpProduct, '| fpMonth: ', fpMonth, ' fvtMonth: ',
                    #       fvtMonth, '| fpCases: ', fpCases, '| fvtAvailability: ', fvtAvailability,' AKA fvtrow[fvtProduct] : ', fvtrow[fvtProduct], '\n', file=f)

                    if fpMonth.lower() == fvtMonth.lower() and fpProduct.lower()==fvtProduct.lower():
                        inner+=1
                        if fpCases > 0.0:

                            if fvtAvailability == 0.0 and fpLocal == 0.0:
                                available.append(2)

                            elif fvtAvailability == 1.0 and fpLocal == 0.0:
                                available.append(3)
                                #keep track of how many are locally purchased may be better to perform act from sql?

                            elif fvtAvailability == 0.0 and fpLocal > 0.0:
                                available.append(2)

                            elif fvtAvailability == 1.0 and fpLocal > 0.0:
                                available.append(1)

                            else:
                                break

                        elif fvtAvailability == 1.0:
                            available.append(1)
                        else:
                            available.append(0)

                return inner

            if mapType == localavailable:
                for fpindex, fprow in FreshPoint.iterrows():
                    fpMonth = fprow['CsvMonth']
                    fpCases = fprow['Cases']
                    fpProduct = fprow['FoodType']
                    fpLocal = fprow['Local']
                    #print ('fvtProduct: ', fvtProduct, ' fpProduct: ', fpProduct, '| fpMonth: ', fpMonth, ' fvtMonth: ', fvtMonth, '| fpCases: ', fpCases, '\n')

                    if fpMonth.lower() == fvtMonth.lower() and fpProduct.lower()==fvtProduct.lower():
                        inner+=1
                        if fpCases > 0.0:

                            if fvtAvailability == 0.0 and fpLocal > 0:
                                localavailable.append(3)

                            elif fvtAvailability == 1.0 and fpLocal == 0:
                                localavailable.append(1)

                            elif fvtAvailability == 0.0 and fpLocal == 0:
                                localavailable.append(3)

                            elif fvtAvailability == 1.0 and fpLocal > 0:
                                localavailable.append(2)
                            else:
                                localavailable.append(0)
                                break


                        elif fvtAvailability == 1.0:
                            localavailable.append(1)

                        else:
                            localavailable.append(0)

                return inner
        def column(fvt_list, colnum):
            return ([row[colnum] for row in fvt_list])

        for y in range(len(column_names)):
            fvt_dict[column_names[y]] = column(fvt_list, y)

        for y in range(len(column_names)):
            if column_names[y] != "ID" and column_names[y] != "ProductID":
                combo_dict[column_names[y]] = column(fvt_list, y)


        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        data_dict = {"Description":[],"Cases":[],"Hunmiles":[],"Twohunmiles":[],"Fivhunmiles":[],"CsvMonth":[],"CsvYear":[],"Local":[],"FoodType":[]}

        #loop over the lines and add them to dataframe. If error , store as string and then display
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

        ######
        fp_data = pd.DataFrame.from_dict(data_dict)
        fp_data = fp_data.iloc[1:]
        fp_final_df = fp_data[['CsvMonth','Cases','FoodType', 'Local']]
        fp_final_df = fp_final_df.loc[fp_final_df['FoodType'] != '']
        fp_final_df = fp_final_df.reset_index(drop=True)
        fp_final_df = fp_final_df.groupby(["""CsvMonth""", """FoodType"""]).sum().reset_index()
        fp_final_df.to_csv('fp_final_df.txt', header=None, sep=' ', mode='w')
        """try:
                form = FoodClass(data_dict)
                if form.is_valid():
                    form.save()                    
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())                                                
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))                    
                pass"""

        sorted_combo_dict = OrderedDict(sorted(combo_dict.items(),key =lambda x:month_names.index(x[0])))
        FVT = pd.DataFrame(sorted_combo_dict)
        transFVT = FVT.set_index('Food').T
        available=[]
        localavailable=[]

        setavailable(transFVT,available)
        setavailable(transFVT,localavailable)
        setAzonicHeatmap(available, transFVT)
        setLocalHeatmap(localavailable, transFVT)


    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))


    return redirect('/index')


