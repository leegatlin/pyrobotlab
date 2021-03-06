from org.myrobotlab.service import Speech
from org.myrobotlab.service import Sphinx
from java.lang import String
from java.lang import Class
from java.awt import Rectangle
from org.myrobotlab.service import Runtime
from org.myrobotlab.service import OpenCV
from org.myrobotlab.opencv import OpenCVData
from com.googlecode.javacv.cpp.opencv_core import CvPoint;
from org.myrobotlab.service import OpenCV
from org.myrobotlab.service import Arduino
from org.myrobotlab.service import Servo
from time import sleep
 
# create ear and mouth
ear = Runtime.createAndStart("ear","Sphinx")
mouth = Runtime.createAndStart("mouth","Speech")
mouth.setLanguage("it")

ear.startListening("find me") 

tracker = Runtime.create("tracker","Tracking")

def heard():
      data = msg_ear_recognized.data[0]
      print "heard ", data
      if (data == "find me"):
         mouth.speak("Ciao Alessandro.Ti ho trovato.Ti vedo")
         tracker.trackPoint(newx,newy)
         
# set up a message route from the ear --to--> python method "heard"
ear.addListener("recognized", python.name, "heard", String().getClass()); 

ear.attach("mouth")
 
# create all the peer services
rotation = Runtime.create("rotation","Servo")
neck = Runtime.create("neck","Servo")
arduino = Runtime.create("arduino","Arduino")
xpid = Runtime.create("xpid","Pid");
ypid = Runtime.create("ypid","Pid");
 
# adjust values
arduino.connect("COM3")
eye = Runtime.create("eye","OpenCV")
opencv = Runtime.create("opencv","OpenCV")
opencv.startService()
opencv.setCameraIndex(1)
eye.setCameraIndex(1)


xpid.setOutputRange(-3, 3)
xpid.setSetpoint(0.5) # we want the target in the middle of the x

ypid.setOutputRange(-3, 3)

ypid.setSetpoint(0.5)
 
# set safety limits - servos
# will not go beyond these limits
rotation.setMinMax(50,170)
 
neck.setMinMax(50,170)
 
# here we are attaching to the
# manually created peer services
 
tracker.attach(arduino)
tracker.attachServos(rotation, 3, neck, 9)
tracker.attach(eye)
tracker.attachPIDs(xpid, ypid)
tracker.xpid.setPID(10.0, 0, 0.1)
tracker.ypid.setPID(10.0, 0, 0.1)
# flip the pid if needed
tracker.xpid.invert()
tracker.ypid.invert()
 
tracker.setRestPosition(90, 72)
 
tracker.startService()
tracker.trackPoint(0.5,0.5)

opencv.addFilter("pd1", "PyramidDown")
opencv.addFilter("FaceDetect1", "FaceDetect")
 
def input():
 
    #print 'found face at (x,y) ', msg_opencv_publishOpenCVData.data[0].x(), msg_opencv_publish.data[0].y()
    opencvData = msg_opencv_publishOpenCVData.data[0]
    global x
    global y
    global sposx
    global sposy
    global posx
    global posy
    global newx
    global newy
    if (opencvData.getBoundingBoxArray().size() > 0) :
     rect = opencvData.getBoundingBoxArray().get(0)
     posx = rect.x
     posy = rect.y
     
     w = rect.width
     h = rect.height
     sposx = (w/2)
     sposy = (h/2)
     x = (posx + sposx)
     y = (posy + sposy)
     print x
     print y
     newx = (x/320.0)
     newy = (y/240.0)
     print newx
     print newy
     return object
# create a message route from opencv to python so we can see the coordinate locations
opencv.addListener("publishOpenCVData", python.name, "input", OpenCVData().getClass());

opencv.capture()