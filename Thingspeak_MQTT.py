# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python

from __future__ import print_function
import paho.mqtt.publish as publish
import psutil
import serial

###   Start of user configuration   ###   

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "560057"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "YMBJKNG5ZQ3US7K3"

#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = False

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = True

###   End of user configuration   ###

# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey

#open serial port for arduino
ser = serial.Serial('/dev/ttyACM0', 9600)
line = ""

#function to find substring
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#function to find substring occur last
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Run a loop which calculates the system performance every
#   20 seconds and published that to a ThingSpeak channel
#   using MQTT.
while(True):
    
    # get the system performance data
    #cpuPercent = psutil.cpu_percent(interval=20)
    #ramPercent = psutil.virtual_memory().percent
    #temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
    #print (" CPU =",cpuPercent,"   TEMP =",temp)

    # build the payload string
    while(ser.in_waiting >0):
        line = ser.readline()
    if line:
        Temp1 = find_between( line, "Temp:", ",HUM" )
        print Temp1
        HUM = find_between( line, "HUM:", ",LUX" )
        print HUM
        print find_between( line, "LUX:", ",PWR" )
        print find_between( line, "PWR:", ",RD" )
        print find_between( line, "RD:", ",PIR" )
        print find_between( line, "PIR:", "\r\n" )
    tPayload = "field1=" + str(Temp1) + "&field2=" + str(HUM)

    # attempt to publish this data to the topic 
    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")