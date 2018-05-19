# name: face_recognition
# author: liziniu
# website: https://www.liziniu.org
# description: 1. read video frame and process to recognize face.
#              2. show recognized pedestrian information on windows and add stranger information
#              3. record pedestrian information to txt file

import face_recognition
import cv2
from Tkinter import *
from threading import Thread
from PIL import Image, ImageTk
import sys
import webbrowser
reload(sys)  
sys.setdefaultencoding('utf8')
import os
import time
import numpy as np
from threading import Lock

thread_lock = Lock()

# pre include image for canvas in windows program
girl_img = Image.open('/home/nvidia/Desktop/girl.png')
current_frame = np.array(girl_img)
girl_img = ImageTk.PhotoImage(girl_img)
img = None
change_count = 0                                # for canvas image change

current_names = []
known_face_encodings = []
known_face_names = []
known_face_map = {'Li Ziniu': '李子牛',
	              'Zhang Pu': '张璞',
		   		  'Jin Yinbin': '金印斌',
		   		  'Yang Jianguo': '杨建国',
		   		  'Zhang Hong': '张虹',
		   		  'Shiyuan': '石原里美',
		   		  'Unknown': '未知'}

def task_2():
    # 窗口显示程序
    # windows program

    def add_face(new_name, frame):
        # on click触发程序，添加图片到数据库
        # triggered by the button to add new face to dataset
        cv2.imwrite("/home/nvidia/Desktop/picture/" + new_name+".jpg", frame)
        new_face = face_recognition.load_image_file("/home/nvidia/Desktop/picture/"+new_name+".jpg")
        try:
            new_face_encoding = face_recognition.face_encodings(new_face)[0]
            global known_face_encodings
            known_face_encodings.append(new_face_encoding)
            global known_face_names
            known_face_names.append(new_name)
            print("添加成功")
        except:
            l1_text.set("fail!")
            time.sleep(2)
            l1_text.set("")

    def change_text():
        # message触发程序，显示当前行人
        # triggered by the message to show current pedestrian
        global current_names
        info = ""
        for name in current_names:
            if name in known_face_map.keys():
                name = known_face_map[name]
            info += name +"   "
        l1_text.set(info)
        entry_1.after(2000, change_text)

    def change_time():
        # 窗口底部时间显示程序
        # Entry to show current time with form of xx-xx-xx
        t = time.localtime(time.time())
        ch = ['年', '月', '日', '时', '分', '秒']
        norm_t = "    "
        for i, c in enumerate(ch):
            norm_t += str(t[i]) + c
        l3_text.set(norm_t)
        l3.after(1000, change_time)

    def change_image():
        # canvas显示图片，当有行人的时候显示frame,没有行人的时候显示gril_img
        # Trigger by canvas. When there is pedestrian in the video,
        # it will show current frame on canvas. Otherwise,
        # it will show pre-include girl_img
        global current_frame, img, pic, change_count
        if len(current_names) >= 1 and current_frame is not None :
            change_count = 5
        else:
            change_count = -5
        if change_count > 0 :
            rgb_small_frame = current_frame[:, :, ::-1]
            small_frame = Image.fromarray(np.uint8(cv2.resize(rgb_small_frame, (300, 300))))
            img = ImageTk.PhotoImage(small_frame)
            change_count -= 1
        else:
            img = girl_img
        change_count += 2
        # canvas.delete(pic)
	    pic = canvas.create_image(150, 150, image=img)
        canvas.after(2000, change_image)
	    
    def click(event):
        # 链接点击程序
        # Triggered by link clicked
        webbrowser.open('http://www.liziniu.org')

    def on_click():
        # button触发程序，点击后添加人脸
        # triggered by the button to add new face
        new_name = l2_text.get()
        global current_frame
        if new_name is not None and current_frame is not None:
            add_face(new_name, current_frame)
            l2_text.set("")
            print("添加成功")

    # root
    root = Tk()
    root.title('李子牛的门禁系统')
    root.resizable(0, 0)
    root.geometry('550x550')

    # current recognized pedestrian
    l1 = Label(root, text='当前行人')
    l1.pack()
    l1_text = StringVar()
    entry_1 = Message(root, bg='yellow', relief=SUNKEN, width=40, justify=CENTER, textvariable=l1_text)
    l1_text.set(" ")
    entry_1.pack()
    entry_1.after(2000, change_text)

    # entry for strange people name
    l2 = Label(root, text='请输入陌生人的姓名')
    l2.place(relx=0.4, rely=0.15)
    l2_text = StringVar()
    entry_2 = Entry(root, bg='yellow', textvariable=l2_text)
    l2_text.set("")
    entry_2.place(relx=0.36, rely=0.18)

    # canvas for showing current frame or pre-included image
    canvas = Canvas(root, width=300, height=300, bg='white')
    global pic
    pic = canvas.create_image(150, 150, image=img)
    canvas.place(relx=0.23, rely=0.26)
    canvas.after(2000, change_image)
    button = Button(root, fg='red', text="将此人加入系统", command=on_click)
    button.place(relx=0.4, rely=0.82)

    # show information about the author
    l4 = Text(root, bg='yellow', width=43, height=3)
    l4.insert(END, "             Copyright@李子牛\n         All rights reserved!\t\n   For more information: www.liziniu.org")
    l4.place(relx=0.23, rely=0.87)
    # l4.pack()
    l4.tag_add('link', '3.25', '3.43')
    l4.tag_config('link', foreground='blue', underline=True)
    l4.tag_bind('link', '<Button-1>', click)

    # show the current time
    l3_text = StringVar()
    l3 = Entry(root, width=28, textvariable=l3_text, state='readonly')
    l3.pack(side="bottom")
    l3.after(1000, change_time)
    
    # root.after(1000, change_image)
    root.mainloop()


def task_1():
    # opencv读取视频流, 进行人脸识别分析。并将部分信息存储，用于task_2
    # opencv to read video frame and analyze the face recognition
    # what's more, store important information to show in windows program

    # Get a reference to webcam #1
	video_capture = cv2.VideoCapture(1)

    # Load the face files
	global known_face_encodings
    global known_face_names
    res = os.walk("/home/nvidia/Desktop/picture").next()
    files = res[-1]
    thread_lock.acquire()
	for image in files:
		name = image.split('.')[0]
		path = "/home/nvidia/Desktop/picture/" + image
		image_ = face_recognition.load_image_file(path)
		try:
		    image_encoding = face_recognition.face_encodings(image_)[0]
		    known_face_encodings.append(image_encoding)
		    known_face_names.append(name)
		    print(name)
		except:
		    print(name, "fail!")
		    pass
	thread_lock.release()
	print("Here are {} faces konwn".format(len(known_face_names)))

	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	count = {}
	info = []
	frame_count = 0            # process frame each two times

	while True:
		# Grab a single frame of video
		ret, frame = video_capture.read()

        # Store the frame to use in windows program
		global current_frame
		current_frame = frame

		# Resize frame of video to 1/4 size for faster face recognition processing
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
		
		# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
		# rgb_small_frame = small_frame[:, :, ::-1]
		rgb_small_frame = small_frame
		
		# Only process every other frame of video to save time
		if frame_count % 2 == 0:
		    # Find all the faces and face encodings in the current frame of video
		    face_locations = face_recognition.face_locations(rgb_small_frame)
		    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
				
		    face_names = []
		    for face_encoding in face_encodings:
		        # See if the face is a match for the known face(s)
		        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
		        name = "Unknown"

		        # If a match was found in known_face_encodings, just use the first one.
		        if True in matches:
		            first_match_index = matches.index(True)
		            name = known_face_names[first_match_index]
			    name_ = name 
			    if name_ in known_face_map.keys():
			        name_ = known_face_map[name_]
			    if name_ not in count.keys():
				count[name_] = 0
			    else:
				count[name_] += 1
				
		        face_names.append(name)
		
		# Record the pedestrian information
		t = time.localtime(time.time())
		day = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2])
		ch = ['年', '月', '日', '时', '分', '秒']
		second = ""
		for i, c in enumerate(ch):
		    second += str(t[i]) + c
		for name in count.keys():
		    if count[name] >= 5:
			i = name + "-->" + second
			info.append(i)
			count[name] = -10000            # not be written in this minute
				
		# Write pedestrian information into txt file every minute
		if t[5] % 59 == 0:
			if not os.path.exists("/home/nvidia/Desktop/record"):
			    os.makedirs("/home/nvidia/Desktop/record")
			    file = open("/home/nvidia/Desktop/record/" + day + ".txt", 'w')
			    for i in info:
				file.writelines(i + "\n")
			    file.close()
			else:
			    file = open("/home/nvidia/Desktop/record/" + day + ".txt", 'a')
			    for i in info:
			        file.writelines(i + "\n")
			    file.close()
			info = []
			count = {}

		# Record the recognized names to show in windows program
		global current_names
		if frame_count % 4 == 0:
		    current_names = face_names

		# Display the results
		for (top, right, bottom, left), name in zip(face_locations, face_names):
		    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
		    top *= 4
		    right *= 4
		    bottom *= 4
		    left *= 4

		    # Draw a box around the face
		    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		    # Draw a label with a name below the face
		    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255))
		    font = cv2.FONT_HERSHEY_DUPLEX
		    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

		# Display the resulting image
		cv2.imshow('Video', frame)
		
		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break

        # process frame count
		frame_count += 1
		if frame_count > 100:
		    frame_count = 0
	# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
    # windows show
    t1 = Thread(target=task_1)
    t1.start()
    # face recognition
    t2 = Thread(target=task_2)
    t2.start()


