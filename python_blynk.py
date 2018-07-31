import BlynkLib
import time
import serial
import random
import json
import requests
import zerosms


ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)

BLYNK_AUTH = '70455a8327e24a8490c23925c2bb50e0'

volt_max_threshold=4
volt_min_threshold=0.5
curr_max_threshold=1
curr_min_threshold=0


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

def weather():
    #5 day forecast for 'Ghaziabad'
    u="http://dataservice.accuweather.com/forecasts/v1/daily/5day/206683?apikey=t15pRtuQEKaAXv0oGJHUJ24ESJ6iyLov"
    json_data=requests.get(u).json()
    r=[]
    q=[]
    p=[]
    n=[]
    m=[]
    m.append(json_data['DailyForecasts'][0]['Day']['IconPhrase'])
    n.append(json_data['DailyForecasts'][1]['Day']['IconPhrase'])
    p.append(json_data['DailyForecasts'][2]['Day']['IconPhrase'])
    q.append(json_data['DailyForecasts'][3]['Day']['IconPhrase'])
    r.append(json_data['DailyForecasts'][4]['Day']['IconPhrase'])
    msg=time.ctime().split()[0]+':'+m[0]+'\nnext day: '+n[0]+'\nnext day: '+p[0]+'\nnext day: '+q[0]+'\nnext day: '+r[0]
    #now send this data as a 'message' to the user
    print 'weather data'
    zerosms.sms(phno='7906213826',passwd='itachi786',message=msg,receivernum='8795963828')
    

def Voltage(chk):
    output=" "
    while output != "":
        try:
            output=((ser.readline()).split())[1]
            currentflow= float(output)/11 ;
            if (time.localtime()[4]%3==0 and(time.localtime()[5]==0 or time.localtime()[5]==1)):
                f=open("/home/pi/Desktop/data.txt", "a+")
                f.write('\n'+time.ctime()+'\t\t'+output+'\t\t'+str(currentflow))
                f.close()
            if chk==1:
                return output
            else:
                return currentflow
        except:
            output=' '
            continue 



    
# Register virtual pin handler
@blynk.VIRTUAL_READ(1)
def v1_read_handler():
    
    try:
        current= Voltage(2)
        if(current<curr_min_threshold or current >= curr_max_threshold):
            #send a notification with required message
            print 'current error'
            msg='current error'
            zerosms.sms(phno='7906213826',passwd='itachi786',message=msg,receivernum='8795963828')
        blynk.virtual_write(1,current)
    except:
        current=''
        blynk.virtual_write(1,current)


# Register virtual pin handler
@blynk.VIRTUAL_READ(2)
def v2_read_handler():
    try:
        output=Voltage(1)
        if((float(output)<volt_min_threshold) or (float(output) >= volt_max_threshold)):
            #send a notification with required message
            print 'volt error'
            msg='votage  error'
            zerosms.sms(phno='7906213826',passwd='itachi786',message=msg,receivernum='8795963828')
        blynk.virtual_write(2,output)
    except:
        output=''
        blynk.virtual_write(2,output)

@blynk.VIRTUAL_READ(3)
def v3_read_handler():
    t=time.localtime()
    if t[2]==1:
        month='January'
    elif t[2]==2:
        month='February'
    elif t[2]==3:
        month='March'
    elif t[2]==4:
        month='April'
    elif t[2]==5:
        month='May'
    elif t[2]==6:
        month='June'
    elif t[2]==7:
        month='July'
    elif t[2]==8:
        month='August'
    elif t[2]==9:
        month='September'
    elif t[2]==10:
        month='October'
    elif t[2]==11:
        month='November'
    elif t[2]==12:
        month='December'
    if(t[3]==22 and t[4]==43 and (t[5]==10 or t[5]==11 or t[5]==12 or t[5]==13 or t[5]==14 )):
        #sending a weather update to the uesr
        try:
            weather()
        except:
            print " "
            
    if(t[2]==4 and t[3]==8 and (t[5]==10 or t[5]==11 or t[5]==12 or t[5]==13 or t[5]==14)):
        #send a message to user to provide cleanup
        print 'clean error'
        msg="Time to clean up the system"
        zerosms.sms(phno='7906213826',passwd='itachi786',message=msg,receivernum='8795963828')
    blynk.virtual_write(3,month)

# Start Blynk (this call should never return)
blynk.run()
