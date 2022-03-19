# load library

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from csv import writer
from datetime import datetime

#-------web scraping using beautifulsoup -------------#

today = datetime.today()
day = today.day
month = today.month
year = today.year
newdate= str(day)+'_'+str(month)+'_'+str(year)
# print(newdate)

# -------------   Create  CSV File -------------------------------------------- #
df = pd.DataFrame({'profile_name':[''], 'company_name':[''], 'location_name':[''],'Joining':[''],'Duration':[''],'stipend':[''],'Apply_by':[''],'Apply':[''],'company_link':['']}).to_csv(newdate+"Internshala_internships.csv",index=False)

count = 1

#--------------- OPEN CSV FILE ------------------------------------------------#
with open(newdate+"Internshala_internships.csv", 'a') as f_object:
    try:
        # -------------- URL ---------------------------------#
        siteUrl = "https://internshala.com/internships/data%20science-internship"
        responce = get(siteUrl)
        main_container = BeautifulSoup(responce.text , 'html.parser')
        sub_container = main_container.find('div',{'id':'list_container'})
        # print(sub_container)

        for j in range(1,10):
            try:
                if j == 1:
                    considerUrl = siteUrl
                elif j > 1:
                    considerUrl = siteUrl + '/page-{}'.format(j)
                print(considerUrl)

                responce = get(considerUrl)
                main_container = BeautifulSoup(responce.text, 'html.parser')
                sub_container = main_container.find('div', {'id': 'list_container'})

                for job_div in sub_container.find_all('div',class_='container-fluid individual_internship'):
                    try:
                        print('')
                        print("=================================================================================================================================")
                        print('')
                        profile_name_title = job_div.find('div', class_='heading_4_5 profile')
                        profile_name_title = profile_name_title.text
                        profile_name = profile_name_title.strip()
                        print(str(count) +")profile_name : ",profile_name)

                        company_name_title = job_div.find('div', class_='heading_6 company_name')
                        company_name_title = company_name_title.text
                        company_name = company_name_title.strip()
                        print('company_name  : ',company_name)

                        location_name_title = job_div.find('div',{'id':'location_names'})
                        location_name_title = location_name_title.text
                        location_name = location_name_title.strip()
                        print('location_name : ',location_name)

                        other_item_list = []
                        for other_detail_container in job_div.find_all('div',class_='other_detail_item_row'):
                            for other_detail in other_detail_container.find_all('div',class_='item_body'):
                                other_detail = other_detail.text
                                others = other_detail.strip()
                                other_item_list.append(others)
                                # print(others)
                        try:
                            Starts = other_item_list[0]
                            joining = Starts.replace('Starts immediatelyImmediately','Immediately')
                            print("Joining : ", joining)
                            print('Duration : ',other_item_list[1])
                            print('stipend : ' ,other_item_list[2])
                            print("Apply_by : ", other_item_list[3])
                        except:
                            pass

                        view_details_div = job_div.find('a', class_='view_detail_button')
                        view_details = 'https://internshala.com'+view_details_div['href']
                        print('Apply : ',view_details)

                        responce = get(view_details)
                        about_container = BeautifulSoup(responce.text, 'html.parser')
                        about_sub_container = about_container.find('div',class_='detail_view')
                        # print(about_sub_container)
                        try:
                            company_link_div = about_sub_container.find('div', class_='text-container website_link')
                            company_link = company_link_div.find('a')
                            company_link = company_link['href']
                            print("company_link : ",company_link)
                        except:
                            company_link = ''

    # -----------------   load data in CSV   -----------------------------------------------------------------#

                        List = [profile_name,company_name,location_name,joining,other_item_list[1],other_item_list[2],other_item_list[3],view_details,company_link]
                        writer_object = writer(f_object)
                        writer_object.writerow(List)
                        count+=1

                    except:
                        pass
            except:
                pass
    except:
        pass

f_object.close()









