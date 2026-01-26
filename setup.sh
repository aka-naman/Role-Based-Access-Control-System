#!/bin/bash
# Setup script for the Data Management Portal

echo "=================================="
echo "Data Management Portal - Setup"
echo "=================================="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv\Scripts\activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "Create superuser account:"
python manage.py createsuperuser

# Collect static files (optional)
# python manage.py collectstatic --noinput

echo ""
echo "=================================="
echo "Setup completed successfully!"
echo "=================================="
echo ""
echo "To run the development server, use:"
echo "  python manage.py runserver"
echo ""
echo "Admin interface: http://localhost:8000/admin/"
echo "Portal: http://localhost:8000/"
