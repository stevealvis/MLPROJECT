# Medical Portal - Mermaid Diagrams

This document contains all the Mermaid diagrams for the Medical Portal system design.

---

## 1. System Architecture Diagram

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Browser["Browser"]
        Mobile["Mobile"]
        Tablet["Tablet"]
    end

    subgraph WebServer["Web Server Layer"]
        Django["Django Application\n(WSGI/Gunicorn)"]
        
        subgraph Apps["Django Apps"]
            MainApp["Main App\n(Core)"]
            Accounts["Accounts\n(Auth/Users)"]
            Chats["Chats\n(Messaging)"]
        end
        
        Django --> MainApp
        Django --> Accounts
        Django --> Chats
    end

    subgraph Services["Infrastructure Services"]
        subgraph ML["ML Services"]
            SymptomModel["Symptom Model\n(Scikit-learn)"]
            ImageModel["Image CNN\n(TensorFlow/Keras)"]
        end
        
        subgraph Storage["File Storage"]
            Media["Media\n(Images)"]
            Static["Static\nFiles)"]
        end
        
        subgraph Database["Database"]
            SQLite["SQLite\n(Development)"]
            Postgres["PostgreSQL\n(Production)"]
        end
    end

    Client --> WebServer
    WebServer --> ML
    WebServer --> Storage
    WebServer --> Database

    Browser --> Django
    Mobile --> Django
    Tablet --> Django
```

---

## 2. User Authentication Flow

```mermaid
flowchart TD
    Start(["User accesses\nprotected resource"]) --> LoginReq{"@login_required\ndecorator"}
    
    LoginReq --> IsLoggedIn{"User\nlogged in?"}
    
    IsLoggedIn -- No --> RedirectLogin["Redirect to\nlogin page"]
    RedirectLogin --> LoginPage["Login Page"]
    
    IsLoggedIn -- Yes --> CheckUserType{"Check user type\n(patient/doctor)"}
    
    CheckUserType --> ProfileExists{"Profile\nexists?"}
    ProfileExists -- No --> RedirectSignup["Redirect to\nappropriate signup"]
    RedirectSignup --> SignupPage["Signup Page"]
    
    ProfileExists -- Yes --> RenderDashboard["Render\nappropriate dashboard"]
    
    subgraph LoginFlow["Login Flow"]
        LoginPage --> Validate["Validate credentials"]
        Validate --> Authenticate["auth.authenticate()"]
        Authenticate --> CheckProfile["Check profile\n(patient/doctor)"]
        CheckProfile --> SetSession["Set session data"]
        SetSession --> RedirectDashboard
    end
    
    subgraph SignupFlow["Signup Flow"]
        SignupPage --> CreateUser["Create User"]
        CreateUser --> CreateProfile["Create profile\n(patient/doctor)"]
        CreateProfile --> LoginPage
    end
```

---

## 3. Disease Prediction Flow

```mermaid
flowchart TD
    Start(["Patient accesses\nprediction page"]) --> ChooseMethod{"Choose prediction\nmethod?"}
    
    ChooseMethod -- Symptom-based --> SymptomPage["Symptom Selection Page"]
    ChooseMethod -- Image-based --> ImagePage["Image Upload Page"]
    
    subgraph SymptomPrediction["Symptom-Based Prediction"]
        SymptomPage --> SelectSymptoms["Select symptoms\nfrom 132 options"]
        SelectSymptoms --> CreateVector["Create binary\nfeature vector"]
        CreateVector --> SymptomModel["Load ML model\n(trained_model)"]
        SymptomModel --> PredictDisease["Predict disease"]
        PredictDisease --> GetConfidence["Get confidence\nscore"]
        GetConfidence --> MapSpecialist["Map to specialist"]
        MapSpecialist --> SymptomResult["Show results"]
    end
    
    subgraph ImagePrediction["Image-Based Prediction"]
        ImagePage --> UploadImage["Upload skin image"]
        UploadImage --> ValidateImage["Validate image\n(size, format, quality)"]
        ValidateImage --> SkinDetection["Skin detection\nalgorithm"]
        SkinDetection --> ValidSkin{"Is valid\nskin image?"}
        ValidSkin -- No --> ShowError["Show error message"]
        ValidSkin -- Yes --> PreprocessImage["Preprocess image\n(resize, normalize)"]
        PreprocessImage --> LoadCNN["Load CNN model\n(skin_cnn.h5)"]
        LoadCNN --> PredictCondition["Predict condition"]
        PredictCondition --> GetCNNConfidence["Get confidence"]
        GetCNNConfidence --> ImageResult["Show results"]
    end
    
    SymptomResult --> RecommendDoctor["Recommend doctor"]
    ImageResult --> RecommendDoctor
    
    RecommendDoctor --> StartConsultation{"Start\nconsultation?"}
    
    StartConsultation -- Yes --> ConsultDoctor["Consult Doctor"]
    StartConsultation -- No --> End(["End"])
    
    ConsultDoctor --> End
```

---

## 4. Doctor Consultation Flow

```mermaid
flowchart TD
    Start(["Consultation\nstarts"]) --> PatientView["Patient views\nprediction results"]
    
    PatientView --> ViewDoctors{"View available\ndoctors?"}
    
    ViewDoctors -- Yes --> DoctorList["Show doctor list\n(filtered by specialty)"]
    DoctorList --> SelectDoctor["Select doctor"]
    SelectDoctor --> RequestConsult["Request\nconsultation"]
    
    ViewDoctors -- No --> SkipConsult["Skip consultation"]
    SkipConsult --> End1(["End"])
    
    RequestConsult --> CreateConsult["Create consultation\nrecord"]
    CreateConsult --> SetStatus["Set status='active'"]
    SetStatus --> OpenChat["Open chat interface"]
    
    subgraph ChatFlow["Chat Session"]
        OpenChat --> SendMessage["Send message"]
        SendMessage --> SaveMessage["Save to Chat model"]
        SaveMessage --> Broadcast["Broadcast to\nparticipants"]
        Broadcast --> ReceiveMessage["Receive message"]
        ReceiveMessage --> ContinueChat{"Continue\nchatting?"}
        
        ContinueChat -- Yes --> SendMessage
        ContinueChat -- No --> CloseConsult["Close consultation"]
    end
    
    CloseConsult --> UpdateStatus["Update status='closed'"]
    UpdateStatus --> RateReview{"Rate and review?"}
    
    RateReview -- Yes --> CreateReview["Create rating/review"]
    CreateReview --> UpdateDoctorRating["Update doctor rating"]
    UpdateDoctorRating --> End2(["End"])
    
    RateReview -- No --> End3(["End"])
```

---

## 5. Database Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o| PATIENT : "OneToOne"
    USER ||--o| DOCTOR : "OneToOne"
    USER ||--o{ CHAT : "sends"
    USER ||--o{ FEEDBACK : "submits"
    
    PATIENT ||--o{ DISEASEINFO : "has"
    PATIENT ||--o{ CONSULTATION : "initiates"
    PATIENT ||--o{ RATING_REVIEW : "gives"
    
    DOCTOR ||--o{ CONSULTATION : "participates"
    DOCTOR ||--o{ RATING_REVIEW : "receives"
    
    CONSULTATION ||--|| CHAT : "contains"
    CONSULTATION ||--|| DISEASEINFO : "linked"
    
    USER {
        string username PK
        string email
        string password
        boolean is_active
        boolean is_staff
        boolean is_superuser
    }
    
    PATIENT {
        string user_id PK,FK
        string name
        date dob
        string gender
        string address
        string mobile_no
    }
    
    DOCTOR {
        string user_id PK,FK
        string name
        date dob
        string gender
        string address
        string mobile_no
        string registration_no
        date year_of_registration
        string qualification
        string state_medical_council
        string specialization
        integer rating
    }
    
    DISEASEINFO {
        integer id PK
        integer patient_id FK
        string diseasename
        integer no_of_symp
        text symptomsname
        decimal confidence
        string consultdoctor
        image skin_image
        string prediction_method
    }
    
    CONSULTATION {
        integer id PK
        integer patient_id FK
        integer doctor_id FK
        integer diseaseinfo_id FK
        date consultation_date
        string status
    }
    
    CHAT {
        integer id PK
        integer consultation_id FK
        integer sender_id FK
        text message
        datetime created
    }
    
    RATING_REVIEW {
        integer id PK
        integer patient_id FK
        integer doctor_id FK
        integer rating
        text review
    }
    
    FEEDBACK {
        integer id PK
        integer sender_id FK
        text feedback
        datetime created
    }
```

---

## 6. User Roles and Permissions Matrix

```mermaid
flowchart LR
    subgraph Features["Features"]
        Homepage["View Homepage"]
        SignupLogin["Signup/Login"]
        SymptomPred["Symptom Prediction"]
        ImagePred["Image Prediction"]
        DoctorList["View Doctor List"]
        StartConsult["Start Consultation"]
        Chat["Chat with Doctor"]
        RateReview["Rate/Review"]
        Dashboard["View Dashboard"]
        Analytics["View Analytics"]
        AdminDash["Admin Dashboard"]
        UserMgmt["User Management"]
        ViewFeedback["View Feedback"]
    end
    
    subgraph Roles["User Roles"]
        Guest["👤 Guest"]
        Patient["🏥 Patient"]
        Doctor["👨‍⚕️ Doctor"]
        Admin["👔 Admin"]
    end
    
    Guest -->|"✅"| Homepage
    Guest -->|"✅"| SignupLogin
    
    Patient -->|"✅"| Homepage
    Patient -->|"✅"| SignupLogin
    Patient -->|"✅"| SymptomPred
    Patient -->|"✅"| ImagePred
    Patient -->|"✅"| DoctorList
    Patient -->|"✅"| StartConsult
    Patient -->|"✅"| Chat
    Patient -->|"✅"| RateReview
    Patient -->|"✅"| Dashboard
    Patient -->|"✅"| Analytics
    
    Doctor -->|"✅"| Homepage
    Doctor -->|"✅"| Dashboard
    Doctor -->|"✅"| Chat
    
    Admin -->|"✅"| Homepage
    Admin -->|"✅"| AdminDash
    Admin -->|"✅"| UserMgmt
    Admin -->|"✅"| ViewFeedback
```

---

## 7. URL Routing Structure

```mermaid
flowchart TB
    subgraph Root["Root URL Conf"]
        direction TB
        Admin["admin/"]
        Main[""""]
        Accounts[""""]
        Chats[""""]
    end
    
    subgraph MainApp["main_app/urls.py"]
        direction LR
        Home["home"]
        PatientUI["patient_ui"]
        CheckDisease["checkdisease"]
        ScanImage["scan_image"]
        Analytics["disease_analytics_dashboard"]
        ConsultDoctor["consult_a_doctor"]
        MakeConsult["make_consultation/<doctorusername>"]
        DoctorUI["doctor_ui"]
        ConsultView["consultationview/<consultation_id>"]
        ChatPost["post"]
        ChatMessages["chat_messages"]
    end
    
    subgraph AccountsApp["accounts/urls.py"]
        direction LR
        SignupPatient["signup_patient"]
        SigninPatient["sign_in_patient"]
        SignupDoctor["signup_doctor"]
        SigninDoctor["sign_in_doctor"]
        SigninAdmin["sign_in_admin"]
        Logout["logout"]
    end
    
    subgraph ChatsApp["chats/urls.py"]
        direction LR
        PostFeedback["post_feedback"]
        GetFeedback["get_feedback"]
    end
    
    Root --> Admin
    Root --> Main
    Root --> Accounts
    Root --> Chats
    
    Main --> Home
    Main --> PatientUI
    Main --> CheckDisease
    Main --> ScanImage
    Main --> Analytics
    Main --> ConsultDoctor
    Main --> MakeConsult
    Main --> DoctorUI
    Main --> ConsultView
    Main --> ChatPost
    Main --> ChatMessages
    
    Accounts --> SignupPatient
    Accounts --> SigninPatient
    Accounts --> SignupDoctor
    Accounts --> SigninDoctor
    Accounts --> SigninAdmin
    Accounts --> Logout
```

---

## 8. Deployment Architecture

```mermaid
flowchart TB
    subgraph DNS["DNS Layer"]
        Route53["Route 53\nDNS Provider"]
    end
    
    subgraph CDN["CDN Layer"]
        CloudFront["CloudFront\nCDN"]
    end
    
    subgraph LoadBalancer["Load Balancer"]
        ALB["Application Load\nBalancer"]
    end
    
    subgraph EC2["EC2 Instances"]
        EC2_1["EC2 Instance 1\n(App Server)"]
        EC2_2["EC2 Instance 2\n(App Server)"]
        EC2_3["EC2 Instance 3\n(App Server)"]
    end
    
    subgraph Database["Database Layer"]
        RDS["RDS PostgreSQL\n(Multi-AZ)"]
    end
    
    subgraph Storage["Storage Layer"]
        S3["S3 Bucket\n(Media Files)"]
    end
    
    Route53 --> CloudFront
    CloudFront --> ALB
    ALB --> EC2_1
    ALB --> EC2_2
    ALB --> EC2_3
    
    EC2_1 --> RDS
    EC2_2 --> RDS
    EC2_3 --> RDS
    
    EC2_1 --> S3
    EC2_2 --> S3
    EC2_3 --> S3
```

---

## 9. Data Flow Diagram - Symptom Prediction

```mermaid
flowchart TD
    subgraph Input["User Input"]
        Symptoms["132 Symptom\nCheckboxes"]
    end
    
    subgraph Processing["Processing"]
        FeatureVector["Binary Feature\nVector Creation"]
        ModelLoad["Load Trained\nModel"]
        Prediction["model.predict()"]
        Probability["model.predict_proba()"]
    end
    
    subgraph Output["Output"]
        Disease["Predicted Disease"]
        Confidence["Confidence Score"]
        Specialist["Recommended\nSpecialist"]
    end
    
    Symptoms --> FeatureVector
    FeatureVector --> ModelLoad
    ModelLoad --> Prediction
    Prediction --> Probability
    Probability --> Disease
    Disease --> Specialist
    Probability --> Confidence
```

---

## 10. Data Flow Diagram - Image Prediction

```mermaid
flowchart TD
    subgraph Input["User Input"]
        Image["Skin Image\nUpload"]
    end
    
    subgraph Validation["Validation"]
        FileType["File Type Check"]
        SizeCheck["Size/Resolution Check"]
        SkinDetect["Skin Detection\nAlgorithm"]
        AspectRatio["Aspect Ratio Check"]
    end
    
    subgraph Preprocessing["Preprocessing"]
        RGBConvert["Convert to RGB"]
        Resize["Resize to 224x224"]
        Normalize["Normalize Pixels"]
        Batch["Create Batch"]
    end
    
    subgraph Prediction["Prediction"]
        CNNModel["CNN Model\nLoad & Predict"]
        ArgMax["argmax()"]
        ConfidenceMax["max()"]
    end
    
    subgraph Output["Output"]
        Condition["Predicted Condition"]
        ImageConfidence["Confidence Score"]
        Recommend["Recommend\nDermatologist"]
    end
    
    Image --> FileType
    FileType --> SizeCheck
    SizeCheck --> SkinDetect
    SkinDetect --> AspectRatio
    
    AspectRatio --> RGBConvert
    RGBConvert --> Resize
    Resize --> Normalize
    Normalize --> Batch
    
    Batch --> CNNModel
    CNNModel --> ArgMax
    ArgMax --> Condition
    CNNModel --> ConfidenceMax
    ConfidenceMax --> ImageConfidence
    Condition --> Recommend
```

---

**Document Version:** 1.0  
**Last Updated:** 2024

