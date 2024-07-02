import serial
import subprocess
import time
import numpy as np  # Import numpy for array operations
import keyboard
import datetime
import threading
import cv2 as cv



# Define the warning_flag

global line_follow_flag
global motor_stop_flag 
global left_turn_flag1, left_turn_flag2, left_turn_flag3, left_turn_flag4, left_turn_flag5, left_turn_flag6, obstacle_flag, gcount,right_turn_flag1,gg_flag,home_turn_flag1,rev_home
global once1, once2, once3, once4, once5, once6, serial_send

def camera():
    template = cv.imread("tmatch1.jpg")
    template_gc=cv.cvtColor(template,cv.COLOR_BGR2GRAY)
    serial_port = serial.Serial('/dev/ttyUSB0')
    global serial_send
    global home_turn_flag1,rev_home
    home_turn_flag1 = False
    rev_home =  False
    configure_serial_port(serial_port)
    #cv.imshow("template",template_gc)
    w, h,y = template.shape[::-1]
    threshold = 0.5
    global bus_stop_flag
    bus_stop_flag = False
    onceeeee = True
    # Initialize camera
    camera = cv.VideoCapture(0)  # Use '0' for the default camera, or change if needed
    file_name = "1.jpg"
    # Check if camera opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera")
        exit()

    while True:
        # Read frame from camera
        ret, frame = camera.read()
        frame_gc=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        frame_rgb=image_rgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        #img_h=frame_gc.shape[0]
        #img_w=frame_gc.shape[1]
        #img_center=(int(img_h/2),int(img_w/2))
        #cropped_image=frame_gc[(img_center[0])-60:img_center[0]+60,img_center[1]-200:img_center[1]+100]
        #ret, thresh1 = cv.threshold(cropped_image, 120, 180, cv.THRESH_BINARY)
        #cv.imshow("threshold",thresh1)
        #cv.imwrite(file_name, frame)
        lower = np.array([115,1,1])
        upper = np.array([130,50,50])
        mask = cv.inRange(frame_rgb, lower, upper)
        whitepixels=cv.countNonZero(mask)
        #if home_turn_flag1:
           #print("in camera module")

        #cv.imshow('Frame', frame_gc)
        res = cv.matchTemplate(frame_gc, template_gc, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        #print("location", loc)
        if whitepixels>100 and home_turn_flag1 and onceeeee:
            serial_send = "S"
            send_string_to_serial(serial_port, serial_send)
            time.sleep(2)
            serial_send = "D"
            send_string_to_serial(serial_port, serial_send)
            print("red found")
            rev_home =  True
            onceeeee = False
        elif (whitepixels<100):
            rev_home =  False
            onceeeee = True
        if(res>=threshold).any():
            print(" Stop the Robot")
            bus_stop_flag = True
            serial_send = "C"
            send_string_to_serial(serial_port, serial_send)
        #elif home_turn_flag1:
            #print ("Baddddddd")
            #send_string_to_serial(serial_port, "D")
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
     
    # Release the camera and close the OpenCV window
    camera.release()
    cv.destroyAllWindows()

    
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

def emergency():
     serial_port = serial.Serial('/dev/ttyUSB0')
     configure_serial_port(serial_port)

     while (True):
         emergency1 = input()

         if emergency1=="W":
             serial_send ="W"
             send_string_to_serial(serial_port, serial_send)
             #print("UP ARROW")
         if emergency1=="S":
             serial_send ="S"
             send_string_to_serial(serial_port, serial_send )
             #print("STOP ARROW")

         if emergency1=="F":
             serial_send ="F"
             send_string_to_serial(serial_port, serial_send )
             #print("RIGHT ARROW")

         if emergency1=="A":
             serial_send ="A"
             send_string_to_serial(serial_port, serial_send )
             #print("LEFT ARROW")
 
         if emergency1=="D":
             serial_send ="D"
             send_string_to_serial(serial_port, serial_send)
             #print("LEFT ARROW")
         if emergency1=="X":
             serial_send ="X"
             send_string_to_serial(serial_port, serial_send)
             #print("LEFT ARROW")



             


def main():
    serial_port = serial.Serial('/dev/ttyUSB0')
    global rev_home
    try:
        configure_serial_port(serial_port)
        T1 = False
        T2 = False
        T3 = False
        home = False
        first_right = False
        first_left = False

        once1 = True
        once2 = False
        once3 = False
        once4 = False
        once5 = False
        once6 = False

        serial_send = "D"
        send_string_to_serial(serial_port, serial_send)

        
        while True:
            motor_stop_flag = False
            line_follow_flag = True
            total_positions = []
            count_obs = 0
            

            # Open the file in read mode
            with open('gps.txt', 'r') as file, open('tfl.txt', 'r') as file1:  # 'with' is used to properly handle file resources

                first_line = file.readline()
                first_line_tfl = file1.readline()

            if first_line:
                values = first_line.split('[')
                values = values[1]
                values = values.split(']')
                values = values[0]
                values = values.split(';')

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
                #if my_row == my_col == -1:  # Use 'and' instead of 'if other_row and other_col == -1:'
                       #print("Robot vanishes")


                our_robot_position = np.array([my_row, my_col])
                our_robot_index = 7
                distances = []
                index = [8]
                #for i in range(0,len(extracted_col)):
                for i in index:

                    if (i != our_robot_index) :
                        other_row = extracted_row[i]
                        other_col = extracted_col[i]
                        if other_row == other_col == -1:  # Use 'and' instead of 'if other_row and other_col == -1:'
                            other_row = 5000
                            other_col = 5000

                        other_robot_position = np.array([other_row, other_col])
                        distance = (((our_robot_position[0] - other_robot_position[0]) ** 2 +
                                    (our_robot_position[1] - other_robot_position[1]) ** 2) ** 0.5)
                        distances.append(distance)


                        #print(serial_send)
                        if ((distance < 200) and (serial_send != "T")):
                        #if (distance < 200):
                            #motor_stop_flag = True
                            line_follow_flag = False
                            serial_send ="T"
                            send_string_to_serial(serial_port, serial_send)
                            #print ("STOP")
                            #print(serial_send)
                            #print("Stopp1")
                            i = 11
                            break
                    

            
            # #first_left = my_row - 510
            # T1 = my_row - 860
            # first_left = my_row - 590
            # T2 = my_col - 720
            # #second_u = my_col - 200
            # #first_right = my_col - 310
            # first_right = my_col - 260
            # T3 = my_row - 590
            # repeat = my_col - 160
            # #home   = my_row - 965
            # home   = my_row - 910
            serial_send = "D"
            send_string_to_serial(serial_port, serial_send)

            if (abs(my_row - 890) <40 and abs(my_col -340)<40 and once1):
                serial_send = "S"
                send_string_to_serial(serial_port, serial_send)

                print("Junction1")
                while (1):
                    with open('tfl.txt', 'r') as file1:  # 'with' is used to properly handle file resources
                        first_line_tfl = file1.readline()

                    #values_tfl = first_line_tfl
                    if (first_line_tfl == '0'):
                        break
                once1 = False
                once2 = True
                serial_send = "D"
                send_string_to_serial(serial_port, serial_send)


            elif (abs(my_row - 580) <50 and abs(my_col -335)<50 and once2):
                serial_send = "S"
                send_string_to_serial(serial_port, serial_send)
                serial_send = "L"
                send_string_to_serial(serial_port, serial_send)
                print("Left")
                once2 = False
                once3 = True


            elif (abs(my_row - 758) <50 and abs(my_col -727)<50 and once3):
                serial_send = "S"
                send_string_to_serial(serial_port, serial_send)

                print("Junction2")
                while (1):
                    with open('tfl.txt', 'r') as file1:  # 'with' is used to properly handle file resources
                        first_line_tfl = file1.readline()

                    # values_tfl = first_line_tfl
                    if (first_line_tfl == '3'):
                        break
                once3 = False
                once4 = True
                serial_send = "D"
                send_string_to_serial(serial_port, serial_send)

            elif (abs(my_row - 502) <50 and abs(my_col -222)<50 and once4):
                serial_send = "S"
                send_string_to_serial(serial_port, serial_send)

                print("Right")
                while (1):
                    with open('tfl.txt', 'r') as file1:  # 'with' is used to properly handle file resources
                        first_line_tfl = file1.readline()

                    # values_tfl = first_line_tfl
                    if (first_line_tfl == '1'):
                        break
                serial_send = "D"
                send_string_to_serial(serial_port, serial_send)
                time.sleep(0.75)
                serial_send = "R"
                send_string_to_serial(serial_port, serial_send)
                once4 = False
                once5 = True


            elif (abs(my_row - 358) <50 and abs(my_col -591)<50 and once5):
                serial_send = "S"
                send_string_to_serial(serial_port, serial_send)

                print("Junction4")
                while (1):
                    with open('tfl.txt', 'r') as file1:  # 'with' is used to properly handle file resources
                        first_line_tfl = file1.readline()

                    # values_tfl = first_line_tfl
                    if (first_line_tfl == '2'):
                        break
                once5 = False
                once6 = True
                serial_send = "D"
                send_string_to_serial(serial_port, serial_send)





            elif (abs(my_row - 980) <40 and abs(my_col -580)<40 and once6):
                serial_send = "R"
                send_string_to_serial(serial_port, serial_send)
                time.sleep(2)
                serial_send = "Q"
                send_string_to_serial(serial_port, serial_send)
                time.sleep(1)

                while (1):
                    if (rev_home):
                        serial_send = "S"
                        send_string_to_serial(serial_port, serial_send)
                    else:
                        time.sleep(12)
                        serial_send = "Z"
                        send_string_to_serial(serial_port, serial_send)
                        #time.sleep(12)
                        break

                serial_send = "D"
                send_string_to_serial(serial_port, serial_send)
                #serial_send = "P"
                #send_string_to_serial(serial_port, serial_send)
                once6 = False
                once1 = True
                print("reverse done succs")


    except Exception as e:
        print(f"Error: {e}")

    finally:
        serial_port.close()

if __name__ == "__main__":
    # Create threads for each set of programs
    first_thread = threading.Thread(target=camera)
    second_thread = threading.Thread(target=main)
    third_thread = threading.Thread(target=emergency)

    # Start threads
    first_thread.start()
    second_thread.start()
    third_thread.start()

    # Wait for threads to complete (optional)
    first_thread.join()
    second_thread.join()
    third_thread.join()

    

