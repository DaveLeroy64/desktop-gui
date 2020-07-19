from datetime import datetime
import time
scanning_active = True
intervals = {
    '3_per_day':['18:59:50', '19:00:00', '19:02:00'],
    '2_per_day':['09:00:00','21:00:00'],
    '1_per_day':['12:00:00']
}




while scanning_active == True:
    current_time = datetime.now().strftime("%H:%M:%S")
    if str(current_time) in  intervals['3_per_day']:
        print("it is now THAT time!!!" + str(current_time))
        time.sleep(1)

# this WORKS for scan intervals