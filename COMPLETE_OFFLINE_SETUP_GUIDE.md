# Complete Offline Setup Guide: PC1 (Internet) → PC2 (No Internet)

**RBAC Excel Grid Integration - Full Project Dependencies & Installation**

---

## 📋 What You Need to Know

This guide covers **everything** needed to run the Django RBAC project offline on PC2:

### What Gets Downloaded:
1. **Python 3.10+** - Programming language runtime
2. **Django 4.2.7** - Web framework (backend)
3. **Data Libraries** - pandas, numpy, openpyxl (Excel handling)
4. **11 More Python Packages** - Dependencies for above
5. **AG Grid 32.0.0** - Data grid UI (frontend)
6. **Project Code** - Your Django application

### Total Size: ~400-500MB on USB

---

# PART 1: PC1 SETUP (WITH INTERNET)

## Quick Start - Copy & Paste Commands

### Step 1: Download Python Installer

**Download from:**
```
https://www.python.org/downloads/
```

**Choose:**
- Python 3.10.x or 3.11.x
- Windows x86-64 executable installer (.exe)
- Save to: `C:\downloads\` or your USB drive

**Verify after download:**
```powershell
# File should be around 100MB
ls C:\downloads\Python-3.10*.exe
```

---

### Step 2: Download Project Code as ZIP

**Option A: From GitHub (if available)**
```powershell
# Download repository as ZIP
# Visit your repository → Code → Download ZIP
# Save to: C:\downloads\RBAC_Project.zip
```

**Option B: Manual ZIP creation**
```powershell
# Navigate to project folder
cd "F:\Projects\Internship\Role based access control"

# Create ZIP (requires 7-Zip or built-in Windows compression)
# Right-click folder → Send to → Compressed folder
# Save as: RBAC_Project.zip
```

---

### Step 3: Download ALL Python Packages (Copy & Paste This)

**Create work folder:**
```powershell
mkdir C:\offline_setup
cd C:\offline_setup
mkdir pip_packages
cd pip_packages
```

**Download ALL Python packages as .whl files:**
```powershell
pip download -r "F:\Projects\Internship\Role based access control\requirements.txt" -d .
```

**Verify download (should show 13+ .whl files):**
```powershell
ls | Measure-Object
# Should show around 13+ items
```

**Files that should be downloaded:**
```
Django-4.2.7-py3-none-any.whl
pandas-2.1.3-cp310-cp310-win_amd64.whl
numpy-1.26.4-cp310-cp310-win_amd64.whl
openpyxl-3.1.2-py2.py3-none-any.whl
xlrd-2.0.2-py2.py3-none-any.whl
asgiref-3.11.0-py3-none-any.whl
sqlparse-0.5.5-py3-none-any.whl
python-dateutil-2.9.0.post0-py2.py3-none-any.whl
pytz-2025.2-py2.py3-none-any.whl
tzdata-2025.3-py2.py3-none-any.whl
et-xmlfile-2.0.0-py2.py3-none-any.whl
typing-extensions-4.15.0-py3-none-any.whl
six-1.17.0-py2.py3-none-any.whl
```

---

### Step 4: Download AG Grid Frontend Files (Copy & Paste This)

**Create AG Grid folder:**
```powershell
cd C:\offline_setup
mkdir ag_grid_files
cd ag_grid_files
```

**Run this PowerShell script to download 3 files:**
```powershell
# Create and move into AG Grid folder
$targetDir = "C:\offline_setup\ag_grid_files"
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
Set-Location $targetDir

# Correct AG Grid v32 URLs
$urls = @(
    "https://cdn.jsdelivr.net/npm/ag-grid-community@32.0.0/styles/ag-grid.css",
    "https://cdn.jsdelivr.net/npm/ag-grid-community@32.0.0/styles/ag-theme-quartz.css",
    "https://cdn.jsdelivr.net/npm/ag-grid-community@32.0.0/dist/ag-grid-community.min.js"
)

foreach ($url in $urls) {
    $filename = ($url -split "/")[-1]
    Write-Host "Downloading: $filename ..."

    try {
        Invoke-WebRequest -Uri $url -OutFile $filename -ErrorAction Stop
        Write-Host "✓ Downloaded: $filename"
    }
    catch {
        Write-Host "✗ FAILED: $filename"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host "`n✓ All AG Grid files downloaded successfully!"
Get-ChildItem

```

**Verify 3 files downloaded:**
```powershell
ls C:\offline_setup\ag_grid_files\
# Should show:
#   ag-grid.css
#   ag-theme-quartz.css
#   ag-grid-community.min.js
```

---

### Step 5: Organize Files for USB Transfer

**Create final USB structure:**
```powershell
cd C:\offline_setup

# Create USB layout
mkdir USB_Contents
cd USB_Contents

# Copy files here
# 1. Copy Python installer
Copy-Item C:\downloads\Python-3.10*.exe -Destination .

# 2. Copy Project ZIP
Copy-Item C:\downloads\RBAC_Project.zip -Destination .

# 3. Copy pip_packages folder
Copy-Item ..\pip_packages -Destination . -Recurse

# 4. Copy ag_grid_files folder
Copy-Item ..\ag_grid_files -Destination . -Recurse
```

**Verify structure:**
```powershell
tree C:\offline_setup\USB_Contents
# Should show:
# ├── Python-3.10.x.exe
# ├── RBAC_Project.zip
# ├── pip_packages/
# │   ├── Django-4.2.7...whl
# │   ├── pandas-2.1.3...whl
# │   └── ... (11 more)
# └── ag_grid_files/
#     ├── ag-grid.css
#     ├── ag-theme-quartz.css
#     └── ag-grid-community.min.js
```

---

### Step 6: Copy to USB Drive

**Insert USB drive (at least 512MB capacity)**

```powershell
# Find USB drive letter (usually D:, E:, F:)
Get-Volume

# Copy entire USB_Contents folder to USB
Copy-Item C:\offline_setup\USB_Contents\* -Destination "E:\" -Recurse -Force
# (Replace E:\ with your USB drive letter)

# Verify copy
ls "E:\"
# Should see: Python-3.10.exe, RBAC_Project.zip, pip_packages, ag_grid_files
```

**PC1 Setup Complete!** ✓

---

# PART 2: PC2 SETUP (NO INTERNET)

## Step-by-Step Installation

### Step 1: Install Python 3.10+ (Required First!)

**Insert USB drive into PC2**

```powershell
# Navigate to USB drive
cd E:\
# (Replace E:\ with your USB drive letter)

# Run Python installer
.\Python-3.10.*.exe
```

**In Python installer window:**
1. ✅ Check box: "Add Python to PATH"
2. Click: "Install Now"
3. Wait for completion (2-3 minutes)
4. Click: "Close"

**Verify Python installed:**
```powershell
python --version
# Should output: Python 3.10.x or 3.11.x

python -m pip --version
# Should show pip version
```

---

### Step 2: Extract Project ZIP

**Extract to desired location:**
```powershell
# Example: C:\Projects\
cd C:\
mkdir Projects
cd Projects

# Navigate to USB and extract
# Option A: PowerShell
Expand-Archive "E:\RBAC_Project.zip" -DestinationPath .

# Option B: Windows Explorer
# Right-click RBAC_Project.zip on USB → Extract All → C:\Projects\

# Verify extraction
cd RBAC_Project
ls
# Should show: manage.py, requirements.txt, config/, portal/, etc.
```

---

### Step 3: Copy Dependencies from USB

**Copy Python packages (pip_packages folder):**
```powershell
# While in C:\Projects\RBAC_Project
Copy-Item "E:\pip_packages" -Destination . -Recurse -Force
# (Replace E:\ with your USB drive letter)

# Verify
ls
# Should show pip_packages folder
```

**Copy AG Grid files:**
```powershell
# Create vendor folder structure
mkdir -Force portal\static\vendor\ag-grid

# Copy AG Grid files
Copy-Item "E:\ag_grid_files\*" -Destination "portal\static\vendor\ag-grid\" -Force
# (Replace E:\ with your USB drive letter)

# Verify
ls portal\static\vendor\ag-grid\
# Should show:
#   ag-grid.css
#   ag-theme-quartz.css
#   ag-grid-community.min.js
```

---

### Step 4: Create Python Virtual Environment

```powershell
# Make sure you're in project root: C:\Projects\RBAC_Project
cd C:\Projects\RBAC_Project

# Create virtual environment
python -m venv .venv

# Verify creation
ls .venv
# Should show Scripts, Lib, pyvenv.cfg
```

---

### Step 5: Activate Virtual Environment

**For PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**If you get execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again:
.\.venv\Scripts\Activate.ps1
```

**For Command Prompt (cmd.exe):**
```cmd
.venv\Scripts\activate.bat
```

**You should see: `(.venv)` at the start of terminal line**

---

### Step 6: Install Python Packages (Offline)

```powershell
# Make sure virtual environment is activated (should see (.venv) prefix)

# Install ALL packages from local pip_packages folder
pip install --no-index --find-links=./pip_packages -r requirements.txt
```

**Wait 2-5 minutes for installation**

**Verify installation:**
```powershell
pip list
# Should show: Django, pandas, numpy, openpyxl, xlrd, etc.
```

---

### Step 7: Setup Database

```powershell
# Apply database migrations
python manage.py migrate

# Should see: "Operations to perform: ... OK" messages
# Creates db.sqlite3 file
```

**Verify database created:**
```powershell
ls
# Should show: db.sqlite3
```

---

### Step 8: Create Admin Account (Optional but Recommended)

```powershell
python manage.py createsuperuser
```

**Follow prompts:**
```
Username: admin
Email: admin@example.com
Password: (enter password)
Password (again): (confirm)
```

---

### Step 9: Populate Test Data (Optional)

```powershell
# Load sample records into database
python manage.py populate_test_data

# Should see: "Test data populated successfully"
```

---

### Step 10: Run the Development Server

```powershell
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

### Step 11: Access the Application

**Open web browser on PC2:**
```
http://localhost:8000/
```

**Login with:**
- Username: `admin`
- Password: (what you set in Step 8)

**You should see:**
- ✓ Dashboard page loads
- ✓ AG Grid data table displays
- ✓ Excel import/export works
- ✓ All features work offline

---

# TROUBLESHOOTING

## Python Not Found
```powershell
# Check if Python is in PATH
python --version

# If not found, reinstall Python and make sure to:
# ✅ Check "Add Python to PATH"
```

## Virtual Environment Won't Activate
```powershell
# Try Command Prompt instead of PowerShell
cmd.exe
.venv\Scripts\activate.bat
```

## Pip Install Fails (Internet Error)
```powershell
# Make sure using --no-index flag:
pip install --no-index --find-links=./pip_packages -r requirements.txt

# Check pip_packages folder exists in current directory:
ls pip_packages
```

## AG Grid Grid Doesn't Show
```powershell
# Verify files copied correctly:
ls portal\static\vendor\ag-grid\

# Should show all 3 files
```

## Database Migration Error
```powershell
# Delete and recreate database:
rm db.sqlite3

# Run migrations again:
python manage.py migrate
```

---

# COMPLETE CHECKLIST

## PC1 (Before USB Transfer)
- [ ] Python 3.10.x installer downloaded (~100MB)
- [ ] Project code downloaded as RBAC_Project.zip (~20MB)
- [ ] Python packages downloaded to pip_packages/ (~200MB)
  - [ ] Django-4.2.7
  - [ ] pandas-2.1.3
  - [ ] numpy-1.26.4
  - [ ] openpyxl-3.1.2
  - [ ] xlrd-2.0.2
  - [ ] And 8 more packages
- [ ] AG Grid files downloaded (3 files, ~3MB total)
  - [ ] ag-grid.css
  - [ ] ag-theme-quartz.css
  - [ ] ag-grid-community.min.js
- [ ] All files copied to USB drive
- [ ] USB drive ready for PC2

## PC2 (Setup Steps)
- [ ] Python 3.10+ installed
  - [ ] "Add Python to PATH" was checked
- [ ] Project extracted from ZIP
- [ ] pip_packages folder copied to project root
- [ ] AG Grid files copied to portal/static/vendor/ag-grid/
- [ ] Virtual environment created (.venv folder)
- [ ] Virtual environment activated
- [ ] Python packages installed from local pip_packages
  - [ ] `pip list` shows all 13 packages
- [ ] Database migrated
  - [ ] db.sqlite3 file created
- [ ] Admin user created (optional)
- [ ] Server started successfully
  - [ ] http://localhost:8000 loads
  - [ ] AG Grid displays data
  - [ ] Login works

---

# WHAT'S INSTALLED

## Python Packages (Backend)

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.7 | Web framework, ORM, authentication |
| pandas | 2.1.3 | Data manipulation, Excel parsing |
| numpy | 1.26.4 | Numerical computing (pandas dependency) |
| openpyxl | 3.1.2 | Excel .xlsx file support |
| xlrd | 2.0.2 | Legacy Excel .xls file support |
| asgiref | 3.11.0 | ASGI/WSGI utilities |
| sqlparse | 0.5.5 | SQL parsing |
| python-dateutil | 2.9.0 | Advanced date handling |
| pytz | 2025.2 | Timezone support |
| tzdata | 2025.3 | Timezone database |
| et-xmlfile | 2.0.0 | XML handling |
| typing-extensions | 4.15.0 | Type hints |
| six | 1.17.0 | Python 2/3 compatibility |

## Frontend Assets

| Component | Version | Purpose |
|-----------|---------|---------|
| AG Grid Community | 32.0.0 | Excel-like data grid UI |
| HTML5/CSS3 | Latest | Layout and styling |
| JavaScript | Vanilla | Grid interactions |

---

# PROJECT STRUCTURE

```
C:\Projects\RBAC_Project\
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies list
├── db.sqlite3                  # SQLite database (created after migrate)
├── .venv/                      # Virtual environment (created)
├── pip_packages/               # Downloaded wheels (from USB)
├── config/                     # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portal/                     # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── vendor/
│   │       └── ag-grid/        # AG Grid files (from USB)
│   │           ├── ag-grid.css
│   │           ├── ag-theme-quartz.css
│   │           └── ag-grid-community.min.js
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── view_tab.html
│       └── view_tab_tabulator.html
```

---

# FINAL NOTES

✓ **All components downloaded and copied**
✓ **Project runs completely offline on PC2**
✓ **Database is local (SQLite)**
✓ **No internet needed after initial setup**
✓ **AG Grid UI works offline**
✓ **Excel import/export works**
✓ **Role-based access control works**

**Questions?** Check OFFLINE_INSTALLATION.md or SETUP_AND_CAPABILITIES.md


