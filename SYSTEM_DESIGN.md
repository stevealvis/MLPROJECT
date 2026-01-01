# Medical Portal System Design

## 1. Executive Summary

This document outlines the comprehensive system design for a **Medical Portal** web application built with Django. The portal provides disease prediction services (symptom-based and image-based), facilitates doctor-patient consultations, and includes an analytics dashboard for tracking disease trends.

**Technology Stack:**
- **Backend:** Django 2.2.5 (Python)
- **Database:** SQLite3 (development) / PostgreSQL (production)
- **ML Models:** Scikit-learn (symptom prediction), TensorFlow/Keras (image classification)
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Railway, Docker-ready

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Client Layer                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Browser   │  │   Mobile    │  │   Tablet    │  │  Web App    │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
└─────────┼────────────────┼────────────────┼────────────────┼───────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Web Server Layer                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              Django Application (WSGI/Gunicorn)                  │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │   │
│  │  │  Main App   │ │  Accounts   │ │   Chats     │               │   │
│  │  │  (Core)     │ │ (Auth/Users)│ │ (Messaging) │               │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ML Services   │    │   File Storage  │    │    Database     │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │ Symptom   │  │    │  │  Media    │  │    │  │  SQLite   │  │
│  │ Model     │  │    │  │  (Images) │  │    │  │  / Postgres│  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
│  ┌───────────┐  │    │  ┌───────────┐  │    │                 │
│  │ Image CNN │  │    │  │ Static    │  │    │                 │
│  │ Model     │  │    │  │  Files    │  │    │                 │
│  └───────────┘  │    │  └───────────┘  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.2 Application Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           User Authentication Flow                        │
└──────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
    │  Home    │────▶│  Login   │────▶│ Validate │────▶│  Dashboard│
    │  Page    │     │  Page    │     │  Credentials│   │   (Role-based)│
    └──────────┘     └──────────┘     └──────────┘     └──────────┘
         │                                      │
         │                                      │
         │         ┌────────────────────────────┘
         │         │
         ▼         ▼
    ┌─────────────────────────┐
    │  Registration (if new)  │
    │  ┌───────────────────┐  │
    │  │   Patient Signup  │  │
    │  │   Doctor Signup   │  │
    │  │   Admin (manual)  │  │
    │  └───────────────────┘  │
    └─────────────────────────┘
```

---

## 3. Database Schema Design

### 3.1 Core Models

#### 3.1.1 User Model (Django Built-in)
- username (Unique)
- email
- password (hashed)
- first_name, last_name
- is_active, is_staff, is_superuser
- last_login, date_joined

#### 3.1.2 Patient Model
- user (OneToOneField → User)
- is_patient, is_doctor (Boolean)
- name, dob, address, mobile_no, gender
- age (Computed Property)

#### 3.1.3 Doctor Model
- user (OneToOneField → User)
- is_patient, is_doctor (Boolean)
- name, dob, address, mobile_no, gender
- registration_no, year_of_registration
- qualification, State_Medical_Council
- specialization, rating

#### 3.1.4 DiseaseInfo Model
- patient (ForeignKey)
- diseasename, no_of_symp, symptomsname (JSON)
- confidence, consultdoctor
- skin_image, prediction_method ('symptoms' or 'image')

#### 3.1.5 Consultation Model
- patient, doctor (ForeignKey)
- diseaseinfo (OneToOneField)
- consultation_date, status ('active', 'closed')

#### 3.1.6 Rating & Review Model
- patient, doctor (ForeignKey)
- rating, review
- rating_is (Computed Property - average)

#### 3.1.7 Chat Model
- created, consultation_id, sender, message

#### 3.1.8 Feedback Model
- created, sender, feedback

---

## 4. API Endpoints

### Main App URLs
| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/` | GET | Public | Homepage |
| `/admin_ui` | GET | Admin | Admin dashboard |
| `/patient_ui` | GET/POST | Patient | Patient dashboard |
| `/checkdisease` | GET/POST | Patient | Symptom-based prediction |
| `/scan_image` | GET/POST | Patient | Image-based prediction |
| `/disease_analytics_dashboard` | GET | Patient | Analytics dashboard |
| `/consult_a_doctor` | GET | Patient | List available doctors |
| `/make_consultation/<str:doctorusername>` | POST | Patient | Start consultation |
| `/doctor_ui` | GET/POST | Doctor | Doctor dashboard |
| `/consultationview/<int:consultation_id>` | GET | Doctor/Patient | View consultation |
| `/post` | POST | Doctor/Patient | Send chat message |
| `/chat_messages` | GET | Doctor/Patient | Get chat messages |

### Accounts URLs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/signup_patient` | GET/POST | Patient registration |
| `/accounts/sign_in_patient` | GET/POST | Patient login |
| `/accounts/signup_doctor` | GET/POST | Doctor registration |
| `/accounts/sign_in_doctor` | GET/POST | Doctor login |
| `/accounts/sign_in_admin` | GET/POST | Admin login |
| `/accounts/logout` | GET | Logout user |

---

## 5. Machine Learning Integration

### 5.1 Symptom-Based Prediction Model
- **Model Type:** Scikit-learn Classifier (Random Forest)
- **Input:** 132 symptom features (binary)
- **Process:** User selects symptoms → Create feature vector → ML prediction → Get disease + confidence → Map to specialist
- **Supported Diseases:** 41 conditions including Fungal infection, Diabetes, Hepatitis, Malaria, etc.

### 5.2 Image-Based Prediction Model
- **Model Type:** CNN (TensorFlow/Keras)
- **Input:** RGB image (224x224 pixels)
- **Process:** Upload image → Validate → Preprocess → CNN prediction → Get condition + confidence
- **Supported Conditions:** Acne, Psoriasis, Eczema, Melanoma, etc.

### 5.3 Doctor Specialization Mapping
```python
SPECIALIZATION_MAPPING = {
    'Rheumatologist': ['Osteoarthristis', 'Arthritis'],
    'Cardiologist': ['Heart attack', 'Bronchial Asthma', 'Hypertension'],
    'Dermatologist': ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo'],
    'Gastroenterologist': ['Peptic ulcer disease', 'GERD', 'Hepatitis', 'Gastroenteritis'],
    # ... more mappings
}
```

---

## 6. User Roles & Permissions

| Feature | Guest | Patient | Doctor | Admin |
|---------|-------|---------|--------|-------|
| View Homepage | ✅ | ✅ | ✅ | ✅ |
| Signup/Login | ✅ | ✅ | ✅ | ❌ |
| Symptom Prediction | ❌ | ✅ | ❌ | ❌ |
| Image Prediction | ❌ | ✅ | ❌ | ❌ |
| Consult Doctor | ❌ | ✅ | ❌ | ❌ |
| Chat | ❌ | ✅ | ✅ | ❌ |
| Admin Dashboard | ❌ | ❌ | ❌ | ✅ |

---

## 7. Security Measures

- **Password Validation:** Minimum length, user attribute check, common password detection
- **Session Management:** Secure sessions, IP tracking, logout cleanup
- **Rate Limiting:** Max 5 login attempts per IP
- **CSRF Protection:** Django CSRF middleware enabled
- **Input Validation:** Form validation, regex for mobile numbers
- **Image Validation:** File type check, skin detection, brightness/aspect checks

---

## 8. Deployment Architecture

### Current (Railway)
- Django Application with Gunicorn
- PostgreSQL Database (Railway provided)
- Environment variables for configuration
- Domain: skinpro.up.railway.app

### Recommended Production
- CDN (Cloudflare/AWS CloudFront)
- Load Balancer (AWS ALB)
- Multiple EC2 instances (auto-scaling)
- RDS PostgreSQL (Multi-AZ)
- S3 Bucket for media files

---

## 9. File Structure

```
MLproject/
├── manage.py
├── requirements.txt
├── requirements-cnn.txt
├── runtime.txt
├── disease_prediction/     # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main_app/              # Core app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── management/commands/
├── accounts/              # Auth app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── chats/                 # Chat app
│   ├── models.py
│   └── views.py
├── templates/             # HTML templates
├── static/                # Static files
├── staticfiles/           # Collected static
├── media/                 # User uploads
│   ├── skin_images/
│   └── profile_pics/
└── models/                # ML models
    ├── trained_model
    ├── skin_cnn.h5
    └── skin_cnn_labels.json
```

---

## 10. Future Enhancements

### Short-term
- Appointment scheduling system
- Email notifications
- Password reset functionality
- Social login (Google/Facebook)
- Mobile app development

### Long-term
- Video consultations (WebRTC)
- AI symptom checker chatbot
- Health analytics dashboard
- E-prescription system
- Pharmacy integration
- Multi-language support
- Blockchain medical records

---

## 11. Conclusion

This medical portal provides a comprehensive solution for disease prediction and doctor-patient consultation. The system is built on robust Django architecture with integrated machine learning capabilities for both symptom-based and image-based disease prediction. The modular design allows for easy expansion and enhancement to meet future healthcare needs.

---

**Document Version:** 1.0  
**Last Updated:** 2024

