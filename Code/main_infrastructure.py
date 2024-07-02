import serial
import subprocess
import numpy as np  # Import numpy for array operations
import RPi.GPIO as GPIO
import time
import subprocess
import threading
import cv2 as cv

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, False)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, False)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, False)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)

# Specify the path to your .txt file
file_path = 'output.txt'

# Define the warning_flag
global gate_flag

def send_string_to_serial(serial_port, data):
    try:
        serial_port.write(data.encode())
    except Exception as e:
        print(f"Error writing to serial port: {e}")

def configure_serial_port(serial_port):
    # Configure the serial port settings
    serial_port.baudrate = 115200
    serial_port.timeout = 1

    # Configure additional settings
    serial_port.parity = serial.PARITY_NONE    # No parity
    serial_port.stopbits = serial.STOPBITS_ONE  # 1 stop bit
    serial_port.bytesize = serial.EIGHTBITS     # 8 data bits

    # You can add more configuration settings if needed
def camera():
    #serial_port = serial.Serial('/dev/bus/usb/001/005')
    serial_port = serial.Serial('/dev/my_usb_serial')
    configure_serial_port(serial_port)
    template = cv.imread("tempfinal1.jpg")
    #template = cv.imread("1_large.jpg")
    template_gc=cv.cvtColor(template,cv.COLOR_BGR2GRAY)
    #print(template_gc)
    w, h, y = template.shape[::-1]
    threshold = 0.6
    # Initialize camera
    camera = cv.VideoCapture(0)  # Use '0' for the default camera, or change if needed
    global gate_flag
    gate_flag = False
    # Check if camera opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera")
        exit()

    while True:
        # Read frame from camera
        ret, frame = camera.read()
        frame_gc=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        #print(frame_gc)
        
        #cv2.imshow('Frame', frame)
        res = cv.matchTemplate(frame_gc, template_gc, cv.TM_CCOEFF_NORMED)
        #loc = np.where(res >= threshold)
        #gate_flag=True
       # print(res)
       # print(gate_flag)
        #print("location", loc)
        if (res>=threshold).any() and gate_flag:
            print(" Open the gate")
            send_string_to_serial(serial_port, "O")
            gate_flag = False

        # Draw a rectangle around the matched region.
        #for pt in zip(*loc[::-1]):
            #cv.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)

        # Show the final image with the matched area.
        #cv.imshow('Detected', frame)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    camera.release()
    cv.destroyAllWindows()

def main():
    #serial_port = serial.Serial('/dev/bus/usb/001/003')
    serial_port = serial.Serial('/dev/my_usb_serial')
    configure_serial_port(serial_port)
    global gate_flag
    gate_flag = False
    try:
        #configure_serial_port(serial_port)
        while True:
            
            total_positions = [] 
            with open(file_path, 'r') as file:
                # Read the first line
                first_line = file.readline()
                if first_line:
                    # Splitting the string based on '[' and ']'
                    values = first_line.split('[')
                    values = values[1]
                    values = values.split(']')
                    values = values[0]
                    values = values.split(';')
	 
                    # Iterate over the split values in a for loop
                    # Extract and save the 7th and 8th positions
                    for value in values:
                        integers = value.split()
                        for integer in integers:
                            total_positions.append(float(integer)) 
                    
                    total_positions = np.array(total_positions)
                    
                    indices_to_extract_col = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
                    indices_to_extract_row = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
                    
                    extracted_col = total_positions[indices_to_extract_col]
                    extracted_row = total_positions[indices_to_extract_row]
                    my_row = extracted_row[7]
                    my_col = extracted_col[7]
                    street_row1 = 1069
                    street_col1 = 682
                    
                    street_row2 = 875
                    street_col2 = 694
                    
                    street_row3 = 423
                    street_col3 = 832
                    
                    street_row4 = 250
                    street_col4 = 697

                    home_row = 968
                    home_col = 566
                    
                    distances1 = []
                    distances2 = []
                    distances3 = []
                    distances4 = []
                    
                    for i in range(len(extracted_row)):
                        other_row = extracted_row[i]
                        other_col = extracted_col[i]
                        if i == 7:
                            my_row = other_row
                            my_col = other_col
                            #distance_gate = ((((my_row - home_row)**2) + ((my_col - home_row)**2))**(1/2))
                            distance_gate = my_row - home_row
                            if distance_gate < 50 and distance_gate>0 and gate_flag:
                                gate_flag = True
                                #print("gate_flagset")
                                #send_string_to_serial(serial_port, "O")
                                #gate_flag = False


                        if other_row and other_col == -1:
                            other_row = 3000
                            other_col = 3000
                        other_ropos = np.array([other_row, other_col])

                        #distance_row1 = abs(street_row1 - other_ropos[0])
                        distance_row1 =((((street_row1 - other_ropos[0])**2) + ((street_col1 - other_ropos[1])**2))**(1/2))

                        #distance_row2 = abs(street_row2 - other_ropos[0])
                        distance_row2 =((((street_row2 - other_ropos[0])**2) + ((street_col2 - other_ropos[1])**2))**(1/2))

                        #distance_row3 = abs(street_row3 - other_ropos[0])
                        distance_row3 =((((street_row3 - other_ropos[0])**2) + ((street_col3 - other_ropos[1])**2))**(1/2))

                        #distance_row4 = abs(street_row4 - other_ropos[0])
                        distance_row4 =((((street_row4 - other_ropos[0])**2) + ((street_col4 - other_ropos[1])**2))**(1/2))

                        distances1.append(distance_row1)
                        dist1 = min(distances1)
                        distances2.append(distance_row2)
                        dist2 = min(distances2)
                        distances3.append(distance_row3)
                        dist3 = min(distances3)
                        distances4.append(distance_row4)
                        dist4 = min(distances4)
                    
                    #print(distances1)
                    # for street light 1
                    if dist1 <= 175:
                        #print("robot is near switch on the light1")
                        
                        GPIO.output(11, True)
                        #time.sleep(1)
                    if dist1 > 175:
                        GPIO.output(11, False)
                        #time.sleep(1)
                    
                    # for street light 2
                    if dist2 <= 175:
                        #print("robot is near switch on the light2")
                        #gate_flag = True
                        GPIO.output(13, True)
                        #time.sleep(1)
                    if dist2 > 175:
                        GPIO.output(13, False)
                        #time.sleep(1)
                    
                    # for street light 3
                    if dist3 <= 175:
                        #print("robot is near switch on the light3")
                        GPIO.output(15, True)
                        #time.sleep(1)
                    if dist3 > 175:
                        GPIO.output(15, False)
                        #time.sleep(1)
                    
                    # for street light 4
                    if dist4 <= 175:
                        #print("robot is near switch on the light4")
                        gate_flag = True
                        GPIO.output(16, True)
                        #time.sleep(1)
                    if dist4 > 175:
                        GPIO.output(16, False)
                        #time.sleep(1)
                    
                    file.close()
                


    except Exception as e:
        print(f"Error: {e}")

    #finally:
        #serial_port.close()

if __name__ == "__main__":
     
    first_thread = threading.Thread(target=camera)
    second_thread = threading.Thread(target=main)
    

    # Start threads
    first_thread.start()
    second_thread.start()
    

    # Wait for threads to complete (optional)
    first_thread.join()
    second_thread.join()
    
