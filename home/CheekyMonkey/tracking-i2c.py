# A script to test tracking on the Raspberry Pi driving servos with the AdaFruit16ServoDriver service
# as at mrl development build version 2489
# a mashup of code taken from Mats:
# https://github.com/MyRobotLab/pyrobotlab/blob/master/home/Mats/Tracking.py
# and also from Grog:
# http://myrobotlab.org/content/tracking-results
#

import time
from org.myrobotlab.opencv import OpenCVFilterPyramidDown

xPin = 0;
yPin = 1;

arduinoPort = "/dev/ttyAMA0";

cameraIndex = 0;


#start an AdaFruit16C I2C servo driver instance
adaFruit16c3 = Runtime.createAndStart("AdaFruit16C3","Adafruit16CServoDriver")

#start a Raspberry Pi instance
raspi = Runtime.createAndStart("RasPi","RasPi")

#attach the AdaFruit16C I2C servo driver to the Raspberry Pi
adaFruit16c3.setController("RasPi","1","0x42")

#set the frequency for the AdaFruit16C I2C servo driver to 50 Hz
adaFruit16c3.setPWMFreq(0,50) 



#start and connect a Virtual Arduino instance
virtual = Runtime.start("virtual", "VirtualArduino");
virtual.connect(arduinoPort);


#start a tracker instance
tracker = Runtime.start("tracker", "Tracking");
x = tracker.getX();
# invert if necessary
# x.setInverted(True);

y = tracker.getY();
# invert if necessary
# y.setInverted(True);


tracker.connect(arduinoPort, xPin, yPin, cameraIndex);

#small delay here to resolve servo/attach glitch
sleep(5)

#detach x and y servos from Virtual Arduino
tracker.x.detach()
tracker.y.detach()

#attach x and y servos to AdaFruit servo driver
tracker.x.attach(adaFruit16c3,xPin,70,20);
tracker.y.attach(adaFruit16c3,yPin,60,20);

tracker.x.setVelocity(20);
tracker.x.setMinMax(60,90);
#x.setInverted(True);
tracker.x.setRest(70);
tracker.x.rest();
tracker.y.setVelocity(20);
tracker.y.setInverted(True);
tracker.y.setMinMax(50,75);
tracker.y.setRest(60);
tracker.y.rest();

#adjust PID values to suit
pid = Runtime.start("tracker.pid","Pid")


#tracker.pid.setPID("tracker.x", 5.0, 1.0, 0.1);
#tracker.pid.setPID("tracker.y", 20.0, 1.0, 0.1);
#pid.setPID("x", 10.0, 1.0, 0.1);
#pid.setPID("y", 50.0, 1.0, 0.1);

#opencv = tracker.getOpenCV();
#opencv.broadcastState();

opencv = Runtime.start("tracker.opencv","OpenCV")
pid.setPID("x", 5.0, 1.0, 0.1);
pid.setPID("y", 5.0, 1.0, 0.1);
sleep(1);

tracker.y.setInverted(True);
sleep(1);

# additional PyramidDown filter for improved framerate on the Pi (~15 fps)
PreFilterPyramidDown = OpenCVFilterPyramidDown("PreFilterPyramidDown") 
tracker.preFilters.add(PreFilterPyramidDown)
tracker.opencv.setDisplayFilter("PreFilterPyramidDown")

#opencv.capture();

# do lk optical point tracking
# tracker.startLKTracking();

# do face tracking
#tracker.faceDetect();
