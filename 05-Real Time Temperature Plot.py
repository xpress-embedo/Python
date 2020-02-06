import matplotlib.pyplot as plt
import numpy as np
import serial
DATA_SIZE = 100
temperature = np.zeros(DATA_SIZE, dtype=np.float32)
index = 0
samples = range(0, DATA_SIZE)

fig = plt.figure()
ax = fig.gca()
ax.set_ylim([0, 60])
ax.set_title('Real-Time Temperature Monitoring')
ax.set_xlabel('Time->')
ax.set_ylabel('Temperature(C)->')

# Enable Interactive Plotting, use plt.ioff() to turn off
plt.ion()

# Open Serial Port
ser = serial.Serial('COM5',baudrate=9600,timeout=10
                    ,parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
try:
    while True:
        temp = ser.readline()
        if index < DATA_SIZE:
            # Convert String to a Number
            temperature[index] = float(temp)
            # Clear the Old Plot from Screen
            ax.cla()
            ax.grid(True)
            ax.set_ylim([0, 60])
            ax.set_title('Real-Time Temperature Monitoring')
            ax.set_xlabel('Samples ->')
            ax.set_ylabel('Temperature$^\circ$(C) ->')
            ax.plot(samples, temperature,'b')
            plt.pause(0.01)
            index +=1
        else:
            index = 0
        
except KeyboardInterrupt:
    print ('Exiting Program')

except:
    print ('Error Occurs, Exiting Program')

finally:
    plt.ioff()
    plt.show()
    ser.close()
