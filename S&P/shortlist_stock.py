import csv
import os
import glob
import datetime
import re
# import pandas as pd
path = "tickers_history/*.csv"
# dirs = os.listdir(path)

def consecutive_dates(d1,d2):
    if (d2-d1).days == 1 or (d2-d1).days==30 or (d2-d1).days==29:
        # print("intial: {}  final: {}".format(d1,d2))
        return True
    return False

total_filtered_stocks=0
ticker_name_list = []

for fname in glob.glob(path):
        # print(fname)
        with open(fname) as csvfile:
            readCSV = csv.reader(csvfile,delimiter=',')
            header = next(readCSV)
            total=0
            

            #this is the working function for weekly trend
            if header !=None:
                week_high_condition = 0
                week_low_condition = 0
                week_total = 0
                week_group =  '2000-01-01'
                d1 = datetime.datetime.strptime(week_group, "%Y-%m-%d")
                week_highest_val = 0
                prev_week_highest_val = 0
                week_lowest_val =0
                prev_week_lowest_val=0
                consecutive =0
                for row in readCSV:
                    datee = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                    # print(datee.date)
                    # day_no = str(datee.date)
                    # new = int(re.sub('[^0-9]', '', str(day_no)))
                    # print(day_no)
                    if (consecutive_dates(d1,datee)): 
                        consecutive+=1          
                        if float(week_highest_val) < float(row[1]):
                            week_highest_val = row[1]
                        if float(week_lowest_val) < float(row[2]):
                            week_lowest_val = row[2]
                    else: 
                        week_total+=1
                        if float(week_highest_val) > float(prev_week_highest_val):
                            week_high_condition+=1
                            # print("{} > {}".format(week_highest_val,prev_week_highest_val))
                        prev_week_highest_val = week_highest_val
                        if float(week_lowest_val) > float(prev_week_lowest_val):
                            week_low_condition+=1
                            # print("{} > {}".format(week_lowest_val,prev_week_lowest_val))
                        prev_week_lowest_val = week_lowest_val
                        week_highest_val = 0
                        week_lowest_val = 0
                    d1 = datee
                    
                # print(consecutive)
                # print(week_high_condition)
                # print(week_total)

                accuracy_true_high_week = ((week_high_condition-1)/(week_total-1))*100
                # print("Accuracy for week high: {}%".format(accuracy_true_high_week))
                accuracy_true_low_week = ((week_low_condition-1)/(week_total-1))*100
                # print("Accuracy for week low: {}%".format(accuracy_true_low_week))
                
            csvfile.seek(0)
            header = next(readCSV)

            #wokring monthly uptrend from high and low
            if header !=None:
                month_group = 0
                month_highest_val = 0
                prev_month_highest_val = 0
                month_lowest_val =0
                prev_month_lowest_val=0
                month_high_condition = 0
                month_low_condition = 0
                month_total = 0
                for row in readCSV:
                    datee = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                    if month_group == datee.month:
                        if float(month_highest_val) < float(row[1]):
                            month_highest_val = row[1]
                        if float(month_lowest_val) < float(row[2]):
                            month_lowest_val = row[2]
                    if month_group != datee.month:
                        month_total+=1
                        if float(month_highest_val) > float(prev_month_highest_val):
                            month_high_condition+=1
                            # print("{} > {}".format(month_highest_val,prev_month_highest_val))
                        prev_month_highest_val = month_highest_val
                        if float(month_lowest_val) > float(prev_month_lowest_val):
                            month_low_condition+=1
                            # print("{} > {}".format(month_lowest_val,prev_month_lowest_val))
                        prev_month_lowest_val = month_lowest_val
                        month_group = datee.month 
                        month_highest_val = 0
                        month_lowest_val = 0
                # print(month_total)
                accuracy_true_high_month = ((month_high_condition-1)/(month_total-1))*100
                # print("Accuracy for month high: {}%".format(accuracy_true_high_month))
                accuracy_true_low_month = ((month_low_condition-1)/(month_total-1))*100
                # print("Accuracy for month low: {}%".format(accuracy_true_low_month))
                

                    


            csvfile.seek(0)
            header = next(readCSV)



        
        
        
            #merged together and finished day uptrend comparision
            if header!= None:
                prev_elem_high = 0
                prev_elem_low = 0
                true_high_day=0
                true_latestlow_day = 0
                for row in readCSV:
                    if float(row[1])>float(prev_elem_high):   
                        true_high_day+=1      
                    if float(row[2])>float(prev_elem_low):
                        true_latestlow_day+=1
                    prev_elem_high = row[1]
                    prev_elem_low = row[2]
                    total+=1
                # print(total)
                #remember to print the stock name beside it in main function
                accuracy_true_high_day = (true_high_day/total)*100
                # print('Accuracy for high day trend condition: {} %'.format(accuracy_true_high_day))
                accuracy_true_latestlow_day = (true_latestlow_day/total)*100
                # print('Accuracy for latest low day trend condition: {} %'.format(accuracy_true_latestlow_day))
        
            csvfile.seek(0)
            header = next(readCSV)



            if header != None:
                week_low_condition_stable = 0
                week_total_stable = 0
                week_group_stable =  '2000-01-01'
                d1_stable = datetime.datetime.strptime(week_group, "%Y-%m-%d")
                week_lowest_val_stable = 0
                prev_week_lowest_val_stable = 0
                consecutive_stable =0

                prev_elem = 0
                true_stable_day = 0
                for row in readCSV:
                    datee = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                    # print(datee.date)
                    # day_no = str(datee.date)
                    # new = int(re.sub('[^0-9]', '', str(day_no)))
                    # print(day_no)
                    if (consecutive_dates(d1_stable,datee)): 
                        consecutive_stable+=1          
                        if float(week_lowest_val_stable) < float(row[2]):
                            week_lowest_val_stable = row[2]
                    else: 
                        week_total_stable+=1
                        if float(row[4]) < 1.03*float(prev_week_lowest_val_stable):
                            week_low_condition_stable+=1
                            # print("{} > {}".format(week_lowest_val,prev_week_lowest_val))
                        prev_week_lowest_val_stable = week_lowest_val_stable
                        week_lowest_val_stable = 0
                    d1_stable = datee
                    if float(row[4])>float(prev_elem) and float(row[4])<1.01*float(prev_elem):
                        true_stable_day+=1
                    prev_elem = row[2]
                accuracy_true_stable_day = (true_stable_day/total)*100
                # print('Accuracy for stable stock condition 1: {} %'.format(accuracy_true_stable_day))
                accuracy_true_low_week_stable = ((week_low_condition_stable-1)/(week_total_stable-1))*100
                # print("Accuracy for stable stock condition 2: {}%".format(accuracy_true_low_week_stable))
                

                if  accuracy_true_high_week >= 65 and  accuracy_true_low_week >= 65 and accuracy_true_high_month>=60 and accuracy_true_low_month>=60 and accuracy_true_latestlow_day >=55 and accuracy_true_high_day >=55 and accuracy_true_stable_day >=15 and accuracy_true_low_week_stable>=70:
                    total_filtered_stocks+=1
                    x = re.findall("[A-Z]",fname)
                    print(fname)
                    ticker_name = ''.join(x)
                    ticker_name_list.append(ticker_name)
                    print(ticker_name)
                    # print("Accuracy for week high: {}%".format(accuracy_true_high_week))
                    # print("Accuracy for week low: {}%".format(accuracy_true_low_week))
                    # print("Accuracy for month high: {}%".format(accuracy_true_high_month))
                    # print("Accuracy for month low: {}%".format(accuracy_true_low_month))
                    # print('Accuracy for high day trend condition: {} %'.format(accuracy_true_high_day))
                    # print('Accuracy for latest low day trend condition: {} %'.format(accuracy_true_latestlow_day))
                    # print('Accuracy for stable stock condition 1: {} %'.format(accuracy_true_stable_day))
                    # print("Accuracy for stable stock condition 2: {}%".format(accuracy_true_low_week_stable))
        
print("The total no. of shortlisted stocks are: {}".format(total_filtered_stocks))

#ticker_name_list is the final list of tickers(shortlisted stocks)