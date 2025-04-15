# Face Recognition Attendance System

The DEPI Facial Recognition System is an advanced, end-to-end platform designed to recognize individuals using facial images or live video. Built with Python, OpenCV, and deep learning frameworks, this project serves as a robust and efficient authentication and attendance tracking system, suitable for institutions such as universities, workplaces, or secure facilities.

This system automates the process of identifying individuals through face recognition, reducing the need for manual checks. Once a face is detected and recognized, the system updates the database in real-time and provides identity verification or attendance logging functionalities.


## Introduction

In traditional attendance systems, the process of marking attendance is often manual, time-consuming, and prone to errors. With the advent of machine learning and computer vision, we now have the tools to automate this process and make it more efficient and accurate.

Our Face Recognition Attendance System is designed to leverage these technologies to provide a seamless and automated attendance tracking solution. The system uses face recognition technology to identify individuals and mark their attendance. This process eliminates the need for manual entry and reduces the chances of errors or fraudulent entries.

The system is built using Python, fastapi, OpenCV, and Firebase. Python and fastapi provide the backend functionality, OpenCV is used for face detection and recognition, and Firebase is used as the database to store user information and attendance records.

Whether you're a university looking to streamline your attendance tracking process or a business looking to automate your employee check-in system, our Face Recognition Attendance System provides a robust and efficient solution.


## Features

The **Face Recognition Attendance System** comes with a host of features designed to make attendance tracking as seamless and efficient as possible:

1. **Face Recognition**: The system uses advanced face recognition technology to identify individuals and mark their attendance. This eliminates the need for manual entry and ensures accuracy in attendance tracking.

2. **Real-Time Attendance Tracking**: The system tracks attendance in real-time. As soon as an individual is recognized by the system, their attendance is marked and updated in the database.

3. **Database Integration**: The system is integrated with Firebase, a cloud-based NoSQL database. This allows for efficient storage and retrieval of user information and attendance records.

4. **Webcam Support**: The system supports webcam input for face recognition. This makes it easy to set up and use in a variety of settings.

5. **Open Source**: The system is open source. Developers are welcome to contribute and help improve the system.

### Screenshots



## Installation

To get the Face Recognition Attendance System up and running on your local machine, follow these steps:

1. **Clone the Repository**: First, clone the repository to your local machine. You can do this by running the following command in your terminal:

   ```
   git clone https://github.com/sameh12353/DEPI-Facial-Recognition-System.git
   ```


2. Create a virtual environment and activate it. You can do this by running the following commands in your terminal:

   **python environment**   
   ```
   python3.12.0 -m venv your_env_name
   ```

   ```
   source your_env_name/bin/activate
   ```
   
   or 

   **conda environment**
   ```
   conda create -n your_env_name python=3.12.0
   ```

   ```
   conda activate your_env_name
   ```

This will create a virtual environment and activate it. All the dependencies will be installed in this virtual environment. 

3. **Install Dependencies**: Navigate into the cloned project directory and install the necessary dependencies by running:

   ```
   pip install -r requirements.txt
   ```

   This command will install all the necessary libraries and packages listed in the `requirements.txt` file.

4. **Set Up Firebase**: The system uses Firebase for database operations. You need to set up a Firebase project and replace the Firebase configuration in the project with your own. You can follow the [Firebase setup guide](https://firebase.google.com/docs/web/setup) for instructions.
   1. First you need to create a project in Firebase.
   1. Later, you need to create Realtime Database (Start in test mode).
   1. Copy your database URL and paste it to the configs/database.yaml file into enter-your-databaseURL section. Example: https://abcd-6ccf7-default-rtdb.firebaseio.com/
   2. Now, start storage in test mode.
   3. Copy the folder path without 'gs://' part and paste it to.the configs/database.yaml file into enter-your-storageBucket section. Example: abcd-6ccf7.appspot.com
   4. Finally you need to create a service account key as json file. You can do it via project settings on Firebase project. Then copy the path of the json file and paste it to the configs/database.yaml file into enter-your-serviceAccountKey-path section. Example: /home/your_user_name/Downloads/serviceAccountKey.json


Once all the setup is complete, you can run the application by executing the following command in the terminal:
  
   ```
   python main.py
   ```

   This will start the fastapi server and the application will be accessible at `http://127.0.0.1:5000/`.

Please note that you need a webcam connected to your machine for the face recognition feature to work. If you are using a laptop, the built-in webcam will work fine.

## Dependencies

The Face Recognition Attendance System relies on several Python libraries to function correctly. Here is a list of the main dependencies:

- **FastAPI** : Lightweight, high-performance web framework for building REST APIs.

- **Uvicorn** : ASGI server used to run FastAPI apps.

- **OpenCV**: A library of programming functions mainly aimed at real-time computer vision. It is used to capture images from the webcam and perform face detection.

- **Firebase Admin**: A library for interacting with Firebase services. It is used to interact with the Firebase Realtime Database and Firebase Storage.

- **TensorFlow** : For loading and running face embedding models.

- **numpy**: A library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.

To install these dependencies, you can use pip, a package manager for Python. Simply run the following command in your terminal:

```bash
pip install -r requirements.txt
```

This will install all the required packages. Make sure you are in the correct directory when you run this command (the directory should contain the `requirements.txt` file).


## Future Improvements

There are several areas where the system could be improved or expanded in the future:

- **Student ID Assignment**: In the future, we plan to optimize the student ID Assignment  process by assigning missing student IDs (e.g., if the IDs are 1,2,3,4,[],6,7,8, the new image's ID will be 5).

- **Add Face Alignment**: Faces in the input images might be tilted or turned, which can reduce the accuracy of your face recognition algorithm. To correct this, we use an alignment algorithm to align the detected faces. This typically involves rotating and scaling the face so that the eyes and mouth are in fixed positions.

- **User Interface Improvements**: We aim to add the aesthetic appeal of the interface to provide a more engaging user experience.

- **Database Image Addition**: We plan to modify this process so that an image is added to the database after the corresponding information is entered.

- **Database Optimization**: We aim to optimize database operations to speed up the process by calling them only once.

- **Security Enhancements**: We plan to implement more secure methods for data handling and user authentication.

- **Class Selection**: If a match is found, you will be redirected to a page where you can select the class. The attendance for the selected class will be updated in the database.

- **Student Login**: In the future, we plan to allow students to log into the system using their passwords.

- **Teacher Login**: If you are a teacher, you can view the attendance by clicking on the "Teacher Login" button on the home page. You will be asked to enter a password. Once the correct password is entered, you will be redirected to the attendance page where you can see the list of students and their attendance.

- **Teacher Database**: We aim to create a separate database for teachers. When the 'Teacher Login' button is pressed, a username and password will be requested.

- **Teacher View**: Once logged in, teachers will be able to view student attendance based on the classes they teach.

- **Deployment**: Currently, the system is designed to run locally. In the future, we plan to deploy the system on a platform like Heroku, which would make it accessible from anywhere and not just on the local machine.

- **Improved error handling and user feedback**: While the system currently handles errors and provides feedback to the user, these aspects could be improved to make the system more robust and user-friendly.

- **Integration with other systems**: The system could be integrated with other systems used in educational institutions, such as learning management systems or student information systems. This would allow for a more seamless experience for both students and teachers.

- **Additional Features**: There are many additional features that could be added to the system, such as support for multiple cameras, recognition of multiple faces at once, or the ability to handle different lighting conditions.

These are just a few ideas for future improvements. We are always open to new ideas and suggestions, so feel free to contribute!

## License

This project is licensed under the MIT License. This means you are free to use, modify, and distribute the project under the terms of this license. Please see the [LICENSE](LICENSE) file for more details. 

Please note that this project is provided "as is" without any warranty. The authors are not responsible for any damage or issues that may arise from using the project. Always check the code yourself before using it in a production environment.

