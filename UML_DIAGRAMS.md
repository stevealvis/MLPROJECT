# Medical Portal - UML Diagrams

This document contains comprehensive UML diagrams for the Medical Portal system including Class Diagrams, Sequence Diagrams, Use Case Diagrams, Activity Diagrams, and Component Diagrams.

---

## Table of Contents

1. [Use Case Diagrams](#1-use-case-diagrams)
2. [Class Diagrams](#2-class-diagrams)
3. [Sequence Diagrams](#3-sequence-diagrams)
4. [Activity Diagrams](#4-activity-diagrams)
5. [Component Diagrams](#5-component-diagrams)
6. [State Diagrams](#6-state-diagrams)

---

## 1. Use Case Diagrams

### 1.1 Overall Use Case Diagram

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Guest" as Guest
actor "Patient" as Patient
actor "Doctor" as Doctor
actor "Admin" as Admin

rectangle "Medical Portal" {
  
  -- Authentication --
  usecase "Login" as UC1
  usecase "Register" as UC2
  usecase "Logout" as UC3
  
  -- Disease Prediction --
  usecase "Symptom-based\nPrediction" as UC4
  usecase "Image-based\nPrediction" as UC5
  usecase "View Prediction\nHistory" as UC6
  
  -- Doctor Consultation --
  usecase "View Doctors" as UC7
  usecase "Request\nConsultation" as UC8
  usecase "Chat with Doctor" as UC9
  usecase "Close Consultation" as UC10
  
  -- Rating & Review --
  usecase "Rate Doctor" as UC11
  usecase "Write Review" as UC12
  
  -- Analytics --
  usecase "View Analytics\nDashboard" as UC13
  
  -- Admin Functions --
  usecase "View Feedback" as UC14
  usecase "Manage Users" as UC15
  usecase "View Reports" as UC16
}

Guest --> UC1
Guest --> UC2

Patient --> UC1
Patient --> UC3
Patient --> UC4
Patient --> UC5
Patient --> UC6
Patient --> UC7
Patient --> UC8
Patient --> UC9
Patient --> UC11
Patient --> UC12
Patient --> UC13

Doctor --> UC1
Doctor --> UC3
Doctor --> UC9
Doctor --> UC10

Admin --> UC1
Admin --> UC3
Admin --> UC14
Admin --> UC15
Admin --> UC16

@enduml
```

### 1.2 Patient Use Case Diagram

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Patient" as Patient

rectangle "Patient Functions" {

  usecase "UC01" as "Login"
  usecase "UC02" as "Register"
  usecase "UC03" as "Logout"
  usecase "UC04" as "View Dashboard"
  usecase "UC05" as "Check Disease\nby Symptoms"
  usecase "UC06" as "Scan Skin Image"
  usecase "UC07" as "View Doctors"
  usecase "UC08" as "Request Consultation"
  usecase "UC09" as "Chat with Doctor"
  usecase "UC10" as "View Consultation\nHistory"
  usecase "UC11" as "View Prediction\nHistory"
  usecase "UC12" as "View Profile"
  usecase "UC13" as "Update Profile"
  usecase "UC14" as "Rate Doctor"
  usecase "UC15" as "Write Review"
  usecase "UC16" as "View Analytics\nDashboard"
}

Patient --> UC01
Patient --> UC02
Patient --> UC03
Patient --> UC04
Patient --> UC05
Patient --> UC06
Patient --> UC07
Patient --> UC08
Patient --> UC09
Patient --> UC10
Patient --> UC11
Patient --> UC12
Patient --> UC13
Patient --> UC14
Patient --> UC15
Patient --> UC16

@enduml
```

### 1.3 Doctor Use Case Diagram

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Doctor" as Doctor

rectangle "Doctor Functions" {

  usecase "UC01" as "Login"
  usecase "UC02" as "Register"
  usecase "UC03" as "Logout"
  usecase "UC04" as "View Dashboard"
  usecase "UC05" as "View Profile"
  usecase "UC06" as "Update Profile"
  usecase "UC07" as "View Consultation\nHistory"
  usecase "UC08" as "Receive Consultation\nRequest"
  usecase "UC09" as "Chat with Patient"
  usecase "UC10" as "Close Consultation"
  usecase "UC11" as "View Ratings"
  usecase "UC12" as "View Reviews"
}

Doctor --> UC01
Doctor --> UC02
Doctor --> UC03
Doctor --> UC04
Doctor --> UC05
Doctor --> UC06
Doctor --> UC07
Doctor --> UC08
Doctor --> UC09
Doctor --> UC10
Doctor --> UC11
Doctor --> UC12

@enduml
```

---

## 2. Class Diagrams

### 2.1 Core Domain Model Class Diagram

```plantuml
@startuml
skinparam classAttributeIconSize 0

package "Django Authentication" {
  class User {
    - username: str
    - email: str
    - password: str
    - first_name: str
    - last_name: str
    - is_active: bool
    - is_staff: bool
    - is_superuser: bool
    - last_login: datetime
    - date_joined: datetime
    + authenticate()
    + get_username()
  }
}

package "Main App Models" {
  
  class patient {
    - user: OneToOneField
    - is_patient: bool
    - is_doctor: bool
    - name: str
    - dob: date
    - address: str
    - mobile_no: str
    - gender: str
    + age: property
  }
  
  class doctor {
    - user: OneToOneField
    - is_patient: bool
    - is_doctor: bool
    - name: str
    - dob: date
    - address: str
    - mobile_no: str
    - gender: str
    - registration_no: str
    - year_of_registration: date
    - qualification: str
    - State_Medical_Council: str
    - specialization: str
    - rating: int
    + age: property
  }
  
  class diseaseinfo {
    - patient: ForeignKey
    - diseasename: str
    - no_of_symp: int
    - symptomsname: TextField
    - confidence: Decimal
    - consultdoctor: str
    - skin_image: ImageField
    - prediction_method: str
    + get_symptomsname_list()
  }
  
  class consultation {
    - patient: ForeignKey
    - doctor: ForeignKey
    - diseaseinfo: OneToOneField
    - consultation_date: date
    - status: str
  }
  
  class rating_review {
    - patient: ForeignKey
    - doctor: ForeignKey
    - rating: int
    - review: TextField
    + rating_is: property
  }
}

package "Chats App Models" {
  class Chat {
    - created: datetime
    - consultation_id: ForeignKey
    - sender: ForeignKey
    - message: TextField
  }
  
  class Feedback {
    - created: datetime
    - sender: ForeignKey
    - feedback: TextField
  }
}

User <|-- patient : "OneToOne"
User <|-- doctor : "OneToOne"
User <|-- Chat : "sends"
User <|-- Feedback : "submits"

patient "1" --> "*" diseaseinfo : "has"
patient "1" --> "*" consultation : "initiates"
patient "1" --> "*" rating_review : "gives"

doctor "1" --> "*" consultation : "participates"
doctor "1" --> "*" rating_review : "receives"

consultation "1" --> "1" Chat : "contains"
consultation "1" --> "1" diseaseinfo : "linked"

@enduml
```

### 2.2 View/Controller Class Diagram

```plantuml
@startuml
skinparam classAttributeIconSize 0

package "Main App Views" {
  
  abstract class View {
    # request: HttpRequest
    # args: tuple
    # kwargs: dict
    + dispatch()
    + get()
    + post()
    + render_to_response()
  }
  
  class HomeView {
    + get()
  }
  
  class PatientUIView {
    + get()
    + post()
  }
  
  class DoctorUIView {
    + get()
  }
  
  class AdminUIView {
    + get()
    + post()
  }
  
  class CheckDiseaseView {
    + get()
    + post()
    - predict_disease()
  }
  
  class ScanImageView {
    + get()
    + post()
    - validate_image()
    - predict_from_image()
  }
  
  class DiseaseAnalyticsView {
    + get()
    - aggregate_stats()
  }
  
  class ConsultDoctorView {
    + get()
  }
  
  class MakeConsultationView {
    + post()
    - create_consultation()
  }
  
  class ConsultationView {
    + get()
  }
  
  class ChatView {
    + post()
    + get()
  }
  
  class RateReviewView {
    + post()
  }
}

View <|-- HomeView
View <|-- PatientUIView
View <|-- DoctorUIView
View <|-- AdminUIView
View <|-- CheckDiseaseView
View <|-- ScanImageView
View <|-- DiseaseAnalyticsView
View <|-- ConsultDoctorView
View <|-- MakeConsultationView
View <|-- ConsultationView
View <|-- ChatView
View <|-- RateReviewView

@enduml
```

### 2.3 Accounts/Auth Class Diagram

```plantuml
@startuml
skinparam classAttributeIconSize 0

package "Django Auth" {
  class AuthenticationForm {
    + username: CharField
    + password: CharField
    + clean()
    + authenticate()
  }
  
  class User {
    + username: str
    + password: str
    + email: str
    + is_authenticated: bool
    + is_anonymous: bool
    + get_username()
  }
}

package "Accounts App" {
  
  abstract class BaseSignupView {
    + form_class: Form
    + template_name: str
    + get()
    + post()
    - create_user()
    - create_profile()
    - login()
  }
  
  class SignupPatientView {
    + form_class: PatientSignupForm
    + template_name: str
  }
  
  class SignupDoctorView {
    + form_class: DoctorSignupForm
    + template_name: str
  }
  
  class SigninPatientView {
    + form_class: Form
    + template_name: str
    + post()
    - authenticate()
    - login()
    - validate()
  }
  
  class SigninDoctorView {
    + form_class: Form
    + template_name: str
    + post()
    - authenticate()
    - login()
    - validate()
  }
  
  class SigninAdminView {
    + form_class: Form
    + template_name: str
    + post()
    - authenticate()
    - login()
    - validate()
  }
  
  class LogoutView {
    + get()
    - clear_session()
    - logout()
  }
  
  class PatientSignupForm {
    - username: CharField
    - email: EmailField
    - password: CharField
    - name: CharField
    - dob: DateField
    - gender: ChoiceField
    - address: CharField
    - mobile_no: CharField
    + clean()
    + validate_mobile()
  }
  
  class DoctorSignupForm {
    - username: CharField
    - email: EmailField
    - password: CharField
    - name: CharField
    - dob: DateField
    - gender: ChoiceField
    - address: CharField
    - mobile_no: CharField
    - registration_no: CharField
    - year_of_registration: DateField
    - qualification: CharField
    - State_Medical_Council: CharField
    - specialization: ChoiceField
    + clean()
    + validate_registration()
  }
}

BaseSignupView <|-- SignupPatientView
BaseSignupView <|-- SignupDoctorView

@enduml
```

---

## 3. Sequence Diagrams

### 3.1 Patient Login Sequence

```plantuml
@startuml
title Patient Login Sequence Diagram

actor Patient
participant "Login Page" as Page
participant "SignInPatientView" as View
participant "auth.authenticate()" as Auth
participant "User Model" as User
participant "patient Model" as Patient
participant "Session" as Session

Patient -> Page: GET /accounts/sign_in_patient
Page --> Patient: Render login form

Patient -> Page: POST (username, password)
Page -> View: dispatch(request)
View -> Auth: authenticate(username, password)
Auth -> User: User.objects.get(username=username)
alt User exists
    User --> Auth: User object
    Auth --> Auth: check_password()
    Auth --> View: User or None
    alt Authentication successful
        View -> Patient: patient.objects.get(user=user)
        Patient --> View: patient object
        View -> Session: Set session data
        Session --> View: Session updated
        View --> Patient: Redirect to patient_ui
    else Authentication failed
        View --> Page: Show error message
        Page --> Patient: Render login form with error
    end
else User not found
    User --> Auth: DoesNotExist
    Auth --> View: None
    View --> Page: Show "Invalid credentials"
    Page --> Patient: Render login form with error
end

@enduml
```

### 3.2 Symptom Prediction Sequence

```plantuml
@startuml
title Symptom Prediction Sequence Diagram

actor Patient
participant "CheckDisease\nTemplate" as Page
participant "CheckDiseaseView" as View
participant "ML Model\n(trained_model)" as Model
participant "diseaseinfo Model" as Disease
participant "Session" as Session

Patient -> Page: GET /checkdisease
Page --> Patient: Render symptom selection form

Patient -> Page: POST (selected_symptoms)
Page -> View: post(request)
View -> View: Extract symptoms list
View -> View: Create binary feature vector (132 features)

loop For each symptom
    View -> View: Set 1 if selected, 0 otherwise
end

View -> Model: predict(feature_vector)
Model --> View: Predicted disease

View -> Model: predict_proba(feature_vector)
Model --> View: Confidence scores
View -> View: Calculate confidence %

View -> View: Map disease to specialist
View -> Disease: diseaseinfo.objects.create()
Disease --> View: diseaseinfo object
View -> Session: Set diseaseinfo_id

View --> Patient: JSON response
Patient --> Page: Display results
Page --> Patient: Show disease, confidence, specialist

@enduml
```

### 3.3 Image Prediction Sequence

```plantuml
@startuml
title Image-Based Prediction Sequence Diagram

actor Patient
participant "ScanImage\nTemplate" as Page
participant "ScanImageView" as View
participant "Image\nValidator" as Validator
participant "CNN Model\n(skin_cnn.h5)" as CNN
participant "diseaseinfo Model" as Disease

Patient -> Page: GET /scan_image
Page --> Patient: Render image upload form

Patient -> Page: POST (skin_image file)
Page -> View: post(request)
View -> View: Get uploaded file
View -> Validator: validate_skin_image(img)
alt Image validation passed
    Validator --> View: is_valid=True
    View -> View: Preprocess image
    View -> View: Resize to 224x224
    View -> View: Normalize pixels
    View -> View: Create batch
    
    View -> CNN: predict(image_batch)
    CNN --> View: Prediction probabilities
    View -> View: Get argmax (predicted class)
    View -> View: Get max confidence
    View -> View: Map to condition name
    
    View -> Disease: diseaseinfo.objects.create()
    Disease --> View: diseaseinfo object
    
    View --> Patient: JSON response
    Patient --> Page: Display condition, confidence
else Image validation failed
    Validator --> View: is_valid=False, reason
    View --> Patient: Error message
    Page --> Patient: Show validation error
end

@enduml
```

### 3.4 Consultation Request Sequence

```plantuml
@startuml
title Consultation Request Sequence Diagram

actor Patient
participant "ConsultDoctor\nTemplate" as Page
participant "MakeConsultationView" as View
participant "doctor Model" as Doctor
participant "diseaseinfo Model" as Disease
participant "consultation Model" as Consult
participant "Session" as Session

Patient -> Page: GET /consult_a_doctor
Page --> Patient: Render doctor list

Patient -> Page: POST /make_consultation/dr_username
Page -> View: post(request, doctorusername)
View -> Doctor: User.objects.get(username=doctorusername)
Doctor --> View: Doctor object

View -> Session: Get diseaseinfo_id
alt diseaseinfo exists
    Session --> View: diseaseinfo_id
    View -> Disease: diseaseinfo.objects.get(id=diseaseinfo_id)
    Disease --> View: diseaseinfo object
else No diseaseinfo
    View -> Disease: Create new diseaseinfo
    Disease --> View: diseaseinfo object
end

View -> Consult: consultation.objects.create()
Consult --> View: consultation object
View -> Session: Set consultation_id
View --> Patient: Redirect to consultation view

@enduml
```

### 3.5 Chat Message Sequence

```plantuml
@startuml
title Chat Message Sequence Diagram

actor "Patient or Doctor" as User
participant "Chat Template" as Page
participant "post View" as View
participant "Chat Model" as Chat
participant "Consultation Model" as Consult

User -> Page: Enter message
Page --> User: Message input field

User -> Page: POST /post (msg)
Page -> View: post(request)
View -> View: Get message content
View -> Session: Get consultation_id
Session --> View: consultation_id

View -> Consult: consultation.objects.get(id=consultation_id)
Consult --> View: consultation object

View -> Chat: Chat.objects.create()
Chat --> View: Chat object saved
View --> Page: JSON response {success: true}
Page --> User: Display sent message

par Broadcast to other user
    Page -> Page: Poll /chat_messages
    View -> Chat: Chat.objects.filter(consultation_id=consultation_id)
    Chat --> View: All messages
    View --> Page: Render chat messages
    Page --> User: Update chat display
end

@enduml
```

---

## 4. Activity Diagrams

### 4.1 Patient Activity Diagram

```plantuml
@startuml
start
:Access Medical Portal;

if (Logged in?) then (No)
  :View Homepage;
  :Choose Sign Up or Login;
  
  if (Choose Sign Up) then (Patient)
    :Fill Patient Signup Form;
    if (Valid data?) then (Yes)
      :Create User Account;
      :Create Patient Profile;
      :Redirect to Login;
    else (No)
      :Show Validation Errors;
      :Retry Signup;
    endif
  else (Doctor)
    :Fill Doctor Signup Form;
    if (Valid data?) then (Yes)
      :Create User Account;
      :Create Doctor Profile;
      :Redirect to Login;
    else (No)
      :Show Validation Errors;
      :Retry Signup;
    endif
  endif
  
  :Login with credentials;
endif

:View Dashboard;
:Choose Activity;

if (Activity) then (Disease Prediction)
  :Choose Method;
  
  if (Method) then (Symptoms)
    :Select Symptoms;
    :Submit for Prediction;
    :View Results;
  else (Image)
    :Upload Skin Image;
    :Submit for Analysis;
    :View Results;
  endif
  
  if (Consult Doctor?) then (Yes)
    :View Doctor List;
    :Select Doctor;
    :Request Consultation;
    :Start Chat;
  endif
  
elseif (Activity) then (View History)
  :View Consultation History;
  :View Prediction History;
  
elseif (Activity) then (Analytics)
  :View Analytics Dashboard;
  
elseif (Activity) then (Profile)
  :View Profile;
  :Update Profile;
endif

stop
@enduml
```

### 4.2 Disease Prediction Activity Diagram

```plantuml
@startuml
start
:User selects prediction type;

if (Type == Symptom) then
  :Load 132 symptoms list;
  :User selects symptoms;
  :Create binary feature vector;
  :Load ML model;
  
  :model.predict(vector);
  :model.predict_proba(vector);
  :Extract disease and confidence;
  
else (Image)
  :User uploads image;
  :Validate image format;
  :Check image quality;
  
  if (Validation passed?) then (No)
    :Show error message;
    stop
  endif
  
  :Preprocess image;
  :Resize to 224x224;
  :Normalize pixels;
  :Load CNN model;
  
  :model.predict(image);
  :Extract condition and confidence;
endif

:Map disease to specialist;
:Save prediction to database;
:Display results to user;

if (User wants consultation?) then (Yes)
  :Filter doctors by specialization;
  :Show doctor list;
else (No)
  :End prediction session;
endif

stop
@enduml
```

### 4.3 Consultation Lifecycle Activity Diagram

```plantuml
@startuml
start
:Patient requests consultation;
:Doctor receives notification;

:Consultation created (status=active);

repeat
  :Chat session active;
  
  if (Doctor messages?) then (Yes)
    :Doctor types message;
    :Send message;
    :Patient receives;
  else (Patient messages?)
    :Patient types message;
    :Send message;
    :Doctor receives;
  endif
  
  if (Continue consultation?) then (Yes)
    :Continue chatting;
  else (No)
    if (Who closes?) then (Doctor)
      :Doctor clicks "Close Consultation";
      :Update status to "closed";
    else (Patient)
      :Patient requests to close;
      :Doctor approves;
      :Update status to "closed";
    endif
    
    if (Patient rates?) then (Yes)
      :Patient submits rating;
      :Patient submits review;
      :Update doctor rating average;
    endif
    
  endif
  
repeat while (Status == active)

:Consultation archived;
stop
@enduml
```

---

## 5. Component Diagrams

### 5.1 System Component Diagram

```plantuml
@startuml
package "Client Tier" {
  component "Web Browser" as Browser
  component "Mobile App" as Mobile
}

package "Presentation Tier" {
  component "HTML Templates" as Templates
  component "CSS Styles" as CSS
  component "JavaScript" as JS
}

package "Application Tier" {
  component "Django Views" as Views
  component "Django URLs" as URLs
  component "Django Forms" as Forms
}

package "Business Logic Tier" {
  component "ML Prediction\nService" as ML
  component "Authentication\nService" as Auth
  component "Consultation\nService" as Consult
  component "Chat\nService" as Chat
}

package "Data Tier" {
  database "SQLite/PostgreSQL" as DB
  file "Static Files" as Static
  file "Media Files" as Media
}

Browser --> Templates
Mobile --> Templates

Templates --> Views
Views --> URLs

URLs --> Views
Forms --> Views

Views --> Auth
Views --> ML
Views --> Consult
Views --> Chat

Auth --> DB
ML --> DB
ML --> Media
Consult --> DB
Chat --> DB

Views --> Static
Views --> Media

@enduml
```

### 5.2 ML Component Diagram

```plantuml
@startuml
component "Image Upload\nComponent" as Upload
component "Image\nPreprocessor" as Preprocess
component "Skin Detection\nValidator" as Validator

component "Symptom\nPreprocessor" as SymPreprocess

component "CNN Model\n(skin_cnn.h5)" as CNN
component "ML Model\n(trained_model)" as MLModel

component "Prediction\nAggregator" as Aggregator
component "Result\nRenderer" as Renderer

Upload --> Validator
Validator --> Preprocess
Preprocess --> CNN

SymPreprocess --> MLModel

CNN --> Aggregator
MLModel --> Aggregator

Aggregator --> Renderer

@enduml
```

---

## 6. State Diagrams

### 6.1 Consultation State Diagram

```plantuml
@startuml
[*] --> Created : Consultation created

Created --> Active : Doctor accepts

Active --> Chatting : Messages exchanged

Chatting --> Chatting : New message

Active --> Closed : Consultation ended

Chatting --> Closed : Consultation ended

Closed --> [*] : Archived

state Active {
  [*] --> Waiting
  Waiting --> Chatting : Start messaging
}

state Closed {
  [*] --> Rated
  Rated --> [*]
}

note right of Active
  Doctor and Patient
  can exchange messages
end note

note right of Closed
  Patient can rate
  and review doctor
end note

@enduml
```

### 6.2 User Authentication State Diagram

```plantuml
@startuml
[*] --> Unauthenticated

Unauthenticated --> Unauthenticated : Login failed

Unauthenticated --> Authenticated : Login successful
Authenticated --> Unauthenticated : Logout

state Authenticated {
  [*] --> PatientProfile
  PatientProfile --> PatientDashboard : View dashboard
  PatientDashboard --> SymptomPrediction : Check disease
  PatientDashboard --> ImagePrediction : Scan image
  PatientDashboard --> ConsultDoctor : Request consultation
  
  [*] --> DoctorProfile
  DoctorProfile --> DoctorDashboard : View dashboard
  DoctorDashboard --> ConsultationList : View consultations
  DoctorDashboard --> ChatSession : Chat with patient
  
  [*] --> AdminProfile
  AdminProfile --> AdminDashboard : View dashboard
  AdminDashboard --> UserManagement : Manage users
  AdminDashboard --> FeedbackView : View feedback
}

@enduml
```

### 6.3 Prediction State Diagram

```plantuml
@startuml
[*] --> InputSelection

InputSelection --> SymptomInput : Select symptoms
InputSelection --> ImageInput : Upload image

state SymptomInput {
  [*] --> SelectSymptoms
  SelectSymptoms --> ValidateCount : Min 1 symptom
  ValidateCount --> CreateVector : Valid
  ValidateCount --> SelectSymptoms : Invalid
}

state ImageInput {
  [*] --> UploadImage
  UploadImage --> ValidateImage : File uploaded
  ValidateImage --> Preprocess : Valid format
  ValidateImage --> UploadImage : Invalid format
  ValidateImage --> CheckQuality : Size/quality check
  CheckQuality --> Preprocess : Quality OK
  CheckQuality --> UploadImage : Quality poor
}

SymptomInput --> Prediction : Input ready
ImageInput --> Prediction : Input ready

state Prediction {
  [*] --> LoadModel
  LoadModel --> ProcessInput : Model loaded
  ProcessInput --> GetResults : Prediction done
  GetResults --> CalculateConfidence : Confidence score
}

Prediction --> Results : Prediction complete

state Results {
  [*] --> DisplayDisease
  DisplayDisease --> DisplayConfidence : Show confidence
  DisplayConfidence --> RecommendDoctor : Map to specialist
  RecommendDoctor --> UserDecision
}

UserDecision --> ConsultDoctor : Request consultation
UserDecision --> [*] : Skip consultation

@enduml
```

---

**Document Version:** 1.0  
**Last Updated:** 2024

