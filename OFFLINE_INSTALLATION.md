# Offline Installation Guide (PC1 with Internet → PC2 without Internet)

## Overview

Setup for transferring project and dependencies from PC1 (with internet) to PC2 (without internet).

---

## PC1 Steps (Connected to Internet)

### Step 1: Download Python Installer
**CRITICAL: Must have Python 3.8+ on PC2**

1. Visit: https://www.python.org/downloads/
2. Download: **Python 3.10.x or 3.11.x** (Windows installer .exe)
3. Choose: **Windows x86-64 executable installer** (for 64-bit systems)
4. Save to: USB or external drive

**Note**: If PC2 already has Python installed, skip this step

### Step 2: Download Project Zip

1. Download the project repository as ZIP
2. Save to: USB or external drive
3. Example: `RBAC_Project.zip`

### Step 3: Download All Pip Packages (Wheels)

**Create a folder for offline packages:**
```powershell
mkdir C:\pip_packages
cd C:\pip_packages
```

**Download all packages as wheel files:**
```powershell
pip download -r "path\to\requirements.txt" -d .
```

This creates a `pip_packages` folder with all .whl files (~200MB total)

**Example output:**
```
Django-4.2.7-py3-none-any.whl
pandas-2.1.3-cp310-cp310-win_amd64.whl
numpy-1.26.4-cp310-cp310-win_amd64.whl
... (and 10+ more)
```

### Step 4: Transfer to USB/External Drive

Copy to USB or external drive:
```
📦 USB Drive/
├── Python-3.10.x.exe
├── RBAC_Project.zip
└── pip_packages/
    ├── Django-4.2.7-py3-none-any.whl
    ├── pandas-2.1.3-cp310-cp310-win_amd64.whl
    ├── numpy-1.26.4-cp310-cp310-win_amd64.whl
    └── ... (all .whl files)
```

---

## PC2 Steps (No Internet Connection)

### Step 1: Install Python (If Not Already Installed)

1. Insert USB drive
2. Run: `Python-3.10.x.exe`
3. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for completion
6. Remove USB drive

**Verify installation:**
```powershell
python --version
# Should output: Python 3.10.x
```

### Step 2: Extract Project Files

1. Insert USB drive
2. Extract: `RBAC_Project.zip` to desired location
   - Example: `C:\Projects\RBAC_Project`
3. Navigate to project:
```powershell
cd C:\Projects\RBAC_Project
```

### Step 3: Create Virtual Environment

```powershell
python -m venv .venv
```

### Step 4: Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Packages from Local Wheels

**Copy pip_packages folder from USB to project:**
```powershell
# USB: pip_packages → C:\Projects\RBAC_Project\pip_packages
```

**Install from local packages:**
```powershell
pip install --no-index --find-links=./pip_packages -r requirements.txt
```

**This installs from local files without needing internet**

### Step 6: Setup Database

```powershell
python manage.py migrate
```

This creates `db.sqlite3` with all tables.

### Step 7: Create Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

Follow prompts to create admin account. Or use test accounts if database was pre-seeded.

### Step 8: Run Development Server

```powershell
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## Checklist for PC1

- [ ] Python 3.10+ installer downloaded (.exe)
- [ ] Project ZIP file prepared
- [ ] `pip download -r requirements.txt -d pip_packages/` completed
- [ ] All .whl files present (13 total)
- [ ] USB drive has:
  - [ ] Python installer
  - [ ] Project ZIP
  - [ ] pip_packages folder
- [ ] Total size ~500MB (Python + project + packages)

---

## Checklist for PC2

- [ ] USB drive received with all files
- [ ] Python 3.10+ installed (add to PATH)
- [ ] Project extracted from ZIP
- [ ] Virtual environment created (`.venv` folder)
- [ ] Virtual environment activated
- [ ] pip_packages folder copied to project root
- [ ] `pip install --no-index --find-links=./pip_packages -r requirements.txt` completed
- [ ] `python manage.py migrate` completed
- [ ] Development server running

---

## Verification Commands (PC2)

### Check Python Version
```powershell
python --version
# Expected: Python 3.10.x or higher
```

### Check Virtual Environment Active
```powershell
# Should show (.venv) at start of command line
```

### Check Django Installation
```powershell
python -m django --version
# Expected: 4.2.7
```

### Check Database
```powershell
python manage.py check
# Expected: System check identified no issues
```

### Check Installed Packages
```powershell
pip list
# Should show all 13 packages from requirements.txt
```

---

## Troubleshooting

### "Python not found" Error
**Solution**: Python not added to PATH
- Reinstall Python
- Check ✅ "Add Python to PATH" during installation
- Restart PowerShell/Command Prompt

### "Permission denied" on .venv\Scripts\Activate.ps1
**Solution**: Execution policy issue
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip install fails with "No module named 'wheel'"
**Solution**: Ensure pip_packages folder is in project root and use:
```powershell
pip install --no-index --find-links=./pip_packages -r requirements.txt
```

### "ModuleNotFoundError: No module named 'django'"
**Solution**: Virtual environment not activated
```powershell
.\.venv\Scripts\Activate.ps1
```

### Database migration fails
**Solution**: Ensure you're in project root directory
```powershell
cd C:\Projects\RBAC_Project
python manage.py migrate
```

### Port 8000 already in use
**Solution**: Use different port
```powershell
python manage.py runserver 8001
```

---

## Important Notes

### 1. Python Version Compatibility
- Download Python **3.8, 3.9, 3.10, 3.11, or 3.12**
- Wheels must match Python version
- Example: `pandas-2.1.3-cp310-cp310-win_amd64.whl` is for Python 3.10

### 2. System Architecture
- Download **x86-64 (64-bit)** for modern PCs
- Download **x86 (32-bit)** only if PC2 is 32-bit system
- Check: Settings → System → About → System type

### 3. Wheel File Naming
Wheels are named like: `package-version-python-abi-platform.whl`
- Example: `Django-4.2.7-py3-none-any.whl`
- Must match Python version and OS

### 4. No Internet on PC2 After Setup
Once installed, **no internet needed** for development:
- Development server works offline
- Database is local (SQLite)
- AG Grid loaded from CDN (only if you access web interface with internet)
- All code and data stays local

### 5. Frontend CDN
AG Grid is loaded from CDN (jsDelivr). If PC2 has **no internet at all**:
- Grid UI will fail to load
- **Solution**: Download AG Grid CSS/JS from CDN on PC1 and serve locally
  - See TECHSTACK.md for CDN URLs
  - Store in `portal/static/vendor/` folder
  - Update template to use local files instead

---

## File Size Estimates

| Item | Size | Count |
|------|------|-------|
| Python Installer | 100MB | 1 |
| Project ZIP | 20MB | 1 |
| pip_packages | 200-300MB | 13 wheels |
| **Total USB Space** | **~400-500MB** | - |

---

## What's Included in requirements.txt

All 13 packages automatically downloaded:
- Django==4.2.7
- pandas==2.1.3
- numpy==1.26.4
- openpyxl==3.1.2
- xlrd==2.0.2
- asgiref==3.11.0
- sqlparse==0.5.5
- python-dateutil==2.9.0.post0
- pytz==2025.2
- tzdata==2025.3
- et-xmlfile==2.0.0
- typing-extensions==4.15.0
- six==1.17.0

Plus all transitive dependencies automatically included.

---

## One-Line Download Command (PC1)

Copy-paste to download all packages:
```powershell
mkdir C:\pip_packages; cd C:\pip_packages; pip download -r "path\to\requirements.txt" -d .
```

---

## One-Line Install Command (PC2)

After copying pip_packages to project root:
```powershell
pip install --no-index --find-links=./pip_packages -r requirements.txt
```

---

## Success Indicators

✅ All items below working = Successful offline installation

1. ```powershell
   python --version
   # Output: Python 3.10.x or higher
   ```

2. ```powershell
   python -m django --version
   # Output: 4.2.7
   ```

3. ```powershell
   python manage.py check
   # Output: System check identified no issues
   ```

4. ```powershell
   python manage.py runserver
   # Output: Starting development server at http://127.0.0.1:8000/
   ```

5. Browser: http://localhost:8000 loads landing page

---

**Last Updated**: January 26, 2026
**Version**: Offline Setup 1.0
**Status**: Complete & Tested
