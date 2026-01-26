# Technology Stack Overview

## Backend Framework

### Django 4.2.7
- **Purpose**: Web framework for server-side logic, routing, and ORM
- **Key Features Used**:
  - URL routing (`urls.py`)
  - View functions for request handling
  - Django ORM for database interactions
  - Built-in authentication system
  - Form validation framework
  - CSRF protection middleware
- **Documentation**: https://docs.djangoproject.com/en/4.2/

### Python 3.x
- **Purpose**: Server-side programming language
- **Key Libraries**:
  - `json`: JSON encoding/decoding
  - `io.BytesIO`: In-memory file handling
  - `datetime`: Timestamp management

## Database

### SQLite3
- **Purpose**: Lightweight, file-based SQL database
- **Advantages**:
  - Zero configuration
  - Perfect for development and small deployments
  - No separate database server needed
- **Django Integration**: Built-in Django support via ORM
- **File Location**: `db.sqlite3` in project root

## Frontend Framework

### AG Grid Community Edition v32.0.0
- **Purpose**: Professional spreadsheet-like data grid component
- **Key Features**:
  - Inline cell editing
  - Column sorting (click headers)
  - Floating filter boxes for searching
  - Pagination (configurable rows per page)
  - Copy/paste support
  - Row virtualization for large datasets
  - Responsive design
- **Why Community Edition**:
  - Free and open-source
  - Excellent feature set for CRUD operations
  - Large active community
  - Good documentation
- **CDN Source**: jsDelivr (https://cdn.jsdelivr.net/)
- **Documentation**: https://www.ag-grid.com/

### HTML5 + CSS3 + JavaScript (Vanilla)
- **Purpose**: Web page structure, styling, and client-side logic
- **Frameworks/Libraries**:
  - Bootstrap: CSS framework for responsive design
  - Fetch API: Async HTTP requests to backend
- **Key Features**:
  - DOM manipulation
  - Event handling (cell editing, button clicks)
  - Toast notifications
  - Form submissions

## Data Processing

### Pandas 2.1.3
- **Purpose**: Excel file parsing and dataframe manipulation
- **Key Functions**:
  - `pd.read_excel()`: Read .xlsx and .xls files
  - DataFrame operations for row iteration
  - Automatic NaN value handling
  - Type inference for columns
- **Why Pandas**:
  - Robust Excel support
  - Handles multiple formats (.xlsx, .xls)
  - Memory-efficient for moderate file sizes
  - Type conversion built-in
- **Dependencies**:
  - `openpyxl 3.1.2`: Excel (.xlsx) file format support
  - `xlrd 2.0.2`: Legacy Excel (.xls) file format support
  - `numpy 1.26.4`: Underlying numerical library

## Supporting Libraries

### asgiref 3.11.0
- **Purpose**: ASGI/WSGI utilities for Django
- **Usage**: Server request/response handling

### sqlparse 0.5.5
- **Purpose**: SQL statement parsing
- **Usage**: Django query debugging and formatting

### python-dateutil 2.9.0.post0
- **Purpose**: Advanced date/time handling
- **Usage**: Pandas datetime column processing

### pytz 2025.2
- **Purpose**: Timezone support
- **Usage**: Handling timezone-aware timestamps

### typing-extensions 4.15.0
- **Purpose**: Type hints for Python < 3.10
- **Usage**: Code documentation and IDE support

### tzdata 2025.3
- **Purpose**: Timezone database
- **Usage**: Timezone conversion accuracy

### six 1.17.0
- **Purpose**: Python 2/3 compatibility utilities
- **Usage**: Third-party library dependency

### et-xmlfile 2.0.0
- **Purpose**: XML handling for openpyxl
- **Usage**: Excel (.xlsx) internal XML parsing

## Dependency Management

### pip
- **Purpose**: Python package manager
- **Usage**: Install packages from PyPI
- **Requirements File**: `requirements.txt`

### Virtual Environment
- **Tool**: `venv` (Python standard library)
- **Location**: `.venv/` directory
- **Purpose**: Isolated Python environment for this project
- **Activation**:
  - Windows: `.venv\Scripts\Activate.ps1`
  - Linux/Mac: `source .venv/bin/activate`

## Development & Deployment

### Django Development Server
- **Command**: `python manage.py runserver`
- **Default Port**: 8000
- **URL**: http://localhost:8000
- **Features**:
  - Auto-reloads on code changes
  - Debug error pages
  - Static file serving

### Database Migrations
- **Tool**: Django ORM migration framework
- **Commands**:
  - `python manage.py makemigrations`: Create migration files
  - `python manage.py migrate`: Apply migrations to database
- **Files Location**: `portal/migrations/`

## Code Organization

### Directory Structure
```
Project Root/
├── config/              # Django settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # Production server entry
├── portal/              # Main application
│   ├── models.py        # Data models (User, Department, Tab, Record)
│   ├── views.py         # Request handlers & API endpoints
│   ├── urls.py          # App URL patterns
│   ├── forms.py         # Django forms
│   ├── utils.py         # Helper functions (import_excel_data)
│   ├── static/          # CSS, JavaScript files
│   ├── templates/       # HTML templates
│   │   ├── view_tab_tabulator.html  # Main grid interface
│   │   ├── dashboard.html            # Home page
│   │   └── ...other pages
│   └── management/      # Custom Django commands
└── db.sqlite3           # Database file
```

### Models File (models.py)
- **User Model**: Custom authentication with roles
- **Department Model**: Organizational units
- **Tab Model**: Data tables within departments
- **Record Model**: Individual data rows with JSONField

### Views File (views.py)
- **Authentication Views**: login, signup, logout
- **Dashboard View**: Department and tab listing
- **API Endpoints**:
  - `api_fetch_records`: GET data
  - `api_create_record`: POST new record
  - `api_update_record`: PATCH field update
  - `api_delete_record`: DELETE record

### Utilities File (utils.py)
- `import_excel_data(file, tab, user)`: Excel import processor

## Browser Compatibility

### Supported Browsers
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Required Features
- ES6 JavaScript support
- Fetch API
- LocalStorage (for CSRF token)

## External Services

### CDN (Content Delivery Network)
- **Provider**: jsDelivr
- **URL**: https://cdn.jsdelivr.net/
- **Serves**:
  - AG Grid Community JavaScript
  - AG Grid CSS stylesheets
- **Fallback**: unpkg CDN as secondary source

## Security Technologies

### CSRF Protection
- **Django Feature**: Built-in CSRF token middleware
- **Token Source**: `getCookie('csrftoken')` in main.js
- **Implementation**: X-CSRFToken header on API requests

### Authentication
- **Django Sessions**: Server-side session management
- **Password Storage**: Django's PBKDF2 hashing
- **Decorators**: @login_required on protected views

## Performance Optimization

### Frontend
- **Pagination**: 20 rows per page
- **Lazy Rendering**: AG Grid virtualizes off-screen rows
- **CDN Caching**: Assets cached by CDN infrastructure

### Backend
- **Database**: SQLite3 indexes on foreign keys
- **Query Optimization**: Django ORM select_related/prefetch_related
- **Column Detection**: O(n) loop through records (acceptable for <100k records)

## Development Dependencies

### Not in Production
- Django Debug Toolbar (for development)
- Code editors: VS Code, PyCharm, etc.

## Version Specifications

All versions in `requirements.txt`:
```
Django==4.2.7
openpyxl==3.1.2
pandas==2.1.3
xlrd==2.0.2
asgiref==3.11.0
sqlparse==0.5.5
tzdata==2025.3
python-dateutil==2.9.0.post0
pytz==2025.2
numpy==1.26.4
typing-extensions==4.15.0
six==1.17.0
et-xmlfile==2.0.0
```

## Future Technology Considerations

### Potential Upgrades
- **Django 5.x**: When stability preferred over features
- **async/await**: For real-time WebSocket updates
- **React/Vue**: For complex frontend logic (if needed)
- **PostgreSQL**: For production deployment
- **Redis**: For caching and session management
- **Celery**: For background job processing

### Alternative Options Considered
- **TabulatorJS**: Initial choice, switched to AG Grid for better UX
- **Tauri**: For desktop app packaging
- **FastAPI**: Alternative backend framework

## Deployment Considerations

### Development (Current)
- Django development server
- SQLite3 database
- Single-user development

### Production
- **Web Server**: Gunicorn or uWSGI
- **Database**: PostgreSQL recommended
- **Static Files**: Nginx serving assets
- **Reverse Proxy**: Nginx for HTTPS
- **Security**: SSL/TLS certificates

### Environment Variables Needed
- `DEBUG = False`
- `SECRET_KEY = [generated value]`
- `ALLOWED_HOSTS = ['yourdomain.com']`
- `DATABASE_URL = [PostgreSQL connection]`

## Development Workflow

### Setup
1. Clone repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.\.venv\Scripts\Activate.ps1` (Windows)
4. Install: `pip install -r requirements.txt`
5. Migrate: `python manage.py migrate`
6. Create user: `python manage.py createsuperuser`

### Running
```bash
python manage.py runserver
# Visit http://localhost:8000
```

### Testing (Manual)
1. Login with test account credentials
2. Create department
3. Create tab
4. Import Excel file
5. Test CRUD operations
6. Verify permissions

## Monitoring & Debugging

### Debug Mode (Development)
- **Setting**: `DEBUG = True` in settings.py
- **Features**:
  - Detailed error pages with stack traces
  - Runserver auto-reload
  - Static file auto-serving

### Logging
- Django logs to console in development
- Production setup recommended: File-based logging

### Browser DevTools
- Chrome DevTools for JavaScript debugging
- Network tab for API request inspection
- Console for error messages
