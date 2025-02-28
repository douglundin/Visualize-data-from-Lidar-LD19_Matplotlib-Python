import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math

# Create a figure with matplotlib's pyplot
# Figure can be understood as a canvas, on which we can draw many diagrams
fig = plt.figure(figsize=(8,8))

# Create a chart on Figure
  # At coordinates 111, which is (1, 1) and has index = 1 on the figure
  # Polar coordinate system, circular, often used in radar maps
ax = fig.add_subplot(111, projection='polar')
# Title for the chart
ax.set_title('Lidar LD19 (exit: Key E)',fontsize=18)

# Com port serial connection
#com_port = "COM5"
com_port = "/dev/ttyUSB0"

# Create an event for pyplot
  # 'key_press_event': event nhấn 1 key
  # 1 The function is triggered with the event
  # Press E to exit
plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

# Create Serial connection
ser = serial.Serial(port=com_port,
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

tmpString = ""
lines = list()
angles = list()
distances = list()

with open('LD19out.txt', 'w') as f:

    i = 0
    while True:
        loopFlag = True
        flag2c = False

        if (i % 40 == 39):
            if ('line' in locals()):
                line.remove()

        # Draw a scatter chart (point chart)
        # Usually represents the correlation between two values, here angle + distance
            # c: color, s: size of points
            #print(angles, file=f)
            print(len(angles))
            line = ax.scatter(angles, distances, c="blue", s=5)
        # Set offset for the position of the 0 degree angle in the polar coordinate system
        # With Lidar's coordinate system, the angle 0 degrees corresponds to the 0y axis, so it is necessary to set offset pi / 2
            ax.set_theta_offset(math.pi / 2)
        # Update Figure, or delay 1 period of time
            plt.pause(0.01)
        # Clear value set
            angles.clear()
            distances.clear()

            i = 0


        while loopFlag:
            # Read data from Serial
            b = ser.read()
#            print (b, file=f)
            # Convert int from readable bytes
                # Cobig: byte order of the bit string, the most significant bits are at the beginning of the int from the read byte
            tmpInt = int.from_bytes(b, 'big')

            # 0x54, indicating the beginning of the data packet (LD19 document)
            if (tmpInt == 0x54):
                tmpString += b.hex() + " "
                flag2c = True
                continue

            # 0x2c: fixed value of VerLen (LD19 document)
            elif (tmpInt == 0x2c and flag2c):
                tmpString += b.hex()


                if (not len(tmpString[0:-5].replace(' ','')) == 90):
                    tmpString = ""
                    loopFlag = False
                    flag2c = False
                    continue

#                print (tmpString[0:-5])

                # After reading a full Lidar data packet, size = 90, take the string and put it into the CalcLidarData() function.
                lidarData = CalcLidarData(tmpString[0:-5])
                # Get the value of angle and distance
                angles.extend(lidarData.Angle_i)
                distances.extend(lidarData.Distance_i)
#                print("angles",angles,file=f)				# Doug
#                print("distances",distances,file=f)			# Doug

                tmpString = ""
                loopFlag = False
            else:
                tmpString += b.hex()+ " "

            flag2c = False

        i += 1

    ser.close()

