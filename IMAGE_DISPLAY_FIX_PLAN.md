# Image Display Fix Plan

## Problem Analysis
- Images exist in `templates/homepage/` directory (admin.PNG, doctor.PNG, patient.PNG, etc.)
- Templates use `{% static 'homepage/admin.PNG' %}` which looks for images in static directory
- Static directory only contains CSS files, missing all image files
- This causes images not to display on the website

## Solution Strategy
Move/copy images from `templates/homepage/` to `static/homepage/` to make them accessible via Django's static file system.

## Files to Process

### Images in templates/homepage/ that need to be copied to static/homepage/:
- admin.PNG
- background.jpg  
- bgimg.jpg
- c31.jpg
- c41.jpg
- doctor.PNG
- gray.jpg
- patient.PNG
- s72.jpg

### Templates that reference these images:
- templates/basic.html (admin.PNG, doctor.PNG, patient.PNG)
- templates/homepage/index.html (various images)
- templates/patient/viewdoctor/index.html (c172.jpg, c31.jpg, c41.jpg, s62.jpg, s72.jpg, s83.jpg, c94.jpg)
- templates/admin/signin/signin.html (admin.png)

### Static image references that need verification:
- static/patient/viewdoctor/img/ (c172.jpg, c31.jpg, c41.jpg, s62.jpg, s72.jpg, s83.jpg, c94.jpg)
- static/admin/signin/admin.png

## Implementation Steps

1. **Create static/homepage/ directory**
2. **Copy all images from templates/homepage/ to static/homepage/**
3. **Create missing static directories and copy remaining images**
4. **Verify Django static files configuration**
5. **Test image loading**

## Expected Outcome
All images referenced in templates using `{% static '...' %}` will load correctly and display on the website.

## Backup Plan
If moving files doesn't work, modify templates to reference images directly from templates directory using `{% load static %}` and proper path resolution.
