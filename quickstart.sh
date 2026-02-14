#!/bin/bash

# XIDS Quick Start Script
# This script helps you get started with XIDS quickly

echo "======================================"
echo "XIDS - Quick Start Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

# Menu
echo ""
echo "What would you like to do?"
echo "1. Setup (Install dependencies)"
echo "2. Train Model"
echo "3. Start Backend (API)"
echo "4. Start Frontend (UI)"
echo "5. Run with Docker"
echo "6. Run Tests"
echo "7. Exit"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        print_info "Installing dependencies..."
        
        echo "Installing backend dependencies..."
        cd backend
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            print_success "Backend dependencies installed"
        else
            print_error "Failed to install backend dependencies"
            exit 1
        fi
        
        cd ..
        echo "Installing frontend dependencies..."
        cd frontend
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            print_success "Frontend dependencies installed"
        else
            print_error "Failed to install frontend dependencies"
            exit 1
        fi
        
        cd ..
        print_success "All dependencies installed successfully!"
        ;;
        
    2)
        echo ""
        print_info "Training model..."
        print_error "Please update DATA_PATH in backend/model/train.py first!"
        echo ""
        read -p "Have you updated the dataset path? (y/n): " confirm
        
        if [ "$confirm" = "y" ]; then
            cd backend/model
            python train.py
            if [ $? -eq 0 ]; then
                print_success "Model training completed!"
            else
                print_error "Model training failed"
                exit 1
            fi
            cd ../..
        else
            print_info "Please update the dataset path and try again"
        fi
        ;;
        
    3)
        echo ""
        print_info "Starting backend API..."
        
        # Check if model exists
        if [ ! -f "backend/model/saved_model.pkl" ]; then
            print_error "Model file not found. Please train the model first (option 2)"
            exit 1
        fi
        
        cd backend
        print_success "Backend starting at http://localhost:8000"
        print_info "API Docs available at http://localhost:8000/docs"
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
        
    4)
        echo ""
        print_info "Starting frontend UI..."
        cd frontend
        print_success "Frontend starting at http://localhost:8501"
        streamlit run app.py
        ;;
        
    5)
        echo ""
        print_info "Starting with Docker..."
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            print_error "Docker not found. Please install Docker first."
            exit 1
        fi
        
        # Check if model exists
        if [ ! -f "backend/model/saved_model.pkl" ]; then
            print_error "Model file not found. Please train the model first (option 2)"
            exit 1
        fi
        
        print_success "Building and starting containers..."
        docker-compose up --build
        ;;
        
    6)
        echo ""
        print_info "Running API tests..."
        
        # Check if backend is running
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            python test_api.py
        else
            print_error "Backend not running. Please start the backend first (option 3)"
            exit 1
        fi
        ;;
        
    7)
        echo ""
        print_info "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_success "Done!"
