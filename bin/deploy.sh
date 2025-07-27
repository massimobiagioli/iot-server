#!/bin/bash

# IoT Server - Automated Deployment Script for Raspberry Pi
# This script automates the installation and configuration of the IoT Server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration variables
PYTHON_VERSION="3.11"
SERVICE_NAME="iot-server"
SERVICE_USER="pi"
SERVICE_GROUP="pi"
INSTALL_DIR="/home/pi/iot-server"
SERVICE_PORT="8000"

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This script should not be run as root. Please run as the pi user."
        exit 1
    fi
}

# Function to check if we're on a Raspberry Pi
check_raspberry_pi() {
    if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
        log_warning "This script is designed for Raspberry Pi. Proceeding anyway..."
    fi
}

# Function to update system packages
update_system() {
    log_info "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    log_success "System packages updated"
}

# Function to install system dependencies
install_dependencies() {
    log_info "Installing system dependencies..."
    sudo apt install -y \
        git \
        curl \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        python3-pip \
        python3-venv \
        nodejs \
        npm \
        sqlite3
    log_success "System dependencies installed"
}

# Function to install Python 3.11 if needed
install_python() {
    local current_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    local required_version="3.11"
    
    if [[ $(echo "$current_version >= $required_version" | bc -l 2>/dev/null || echo "0") -eq 1 ]]; then
        log_success "Python $current_version is already installed (>= $required_version)"
        return
    fi
    
    log_info "Installing Python $PYTHON_VERSION..."
    sudo apt install -y software-properties-common
    
    # For Debian/Ubuntu systems
    if command -v add-apt-repository >/dev/null 2>&1; then
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update
        sudo apt install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev
    else
        log_warning "Could not install Python $PYTHON_VERSION automatically. Please install manually."
    fi
    
    log_success "Python installation completed"
}

# Function to setup Python virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Python dependencies installed"
}

# Function to setup database
setup_database() {
    log_info "Setting up database..."
    
    # Install Node.js dependencies if package.json exists
    if [[ -f "package.json" ]]; then
        npm install
    fi
    
    # Generate Prisma client
    npx prisma generate
    
    # Push database schema
    npx prisma db push
    
    log_success "Database setup completed"
}

# Function to create environment file
create_env_file() {
    log_info "Creating environment configuration..."
    
    if [[ ! -f ".env" ]]; then
        cat > .env << EOF
# MQTT Configuration
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=

# Database Configuration
DATABASE_URL=file:./production.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
EOF
        log_success "Environment file created (.env)"
        log_warning "Please edit .env file to configure MQTT broker settings"
    else
        log_info "Environment file already exists"
    fi
}

# Function to create systemd service
create_systemd_service() {
    log_info "Creating systemd service..."
    
    sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null << EOF
[Unit]
Description=IoT Server FastAPI Application
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_GROUP
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/.venv/bin
ExecStart=$INSTALL_DIR/.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port $SERVICE_PORT
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME.service
    log_success "Systemd service created and enabled"
}

# Function to configure firewall
configure_firewall() {
    log_info "Configuring firewall..."
    
    if command -v ufw >/dev/null 2>&1; then
        sudo ufw --force enable
        sudo ufw allow ssh
        sudo ufw allow $SERVICE_PORT
        log_success "Firewall configured"
    else
        log_warning "UFW not found. Please configure firewall manually."
    fi
}

# Function to start service
start_service() {
    log_info "Starting IoT Server service..."
    
    sudo systemctl start $SERVICE_NAME.service
    sleep 3
    
    if sudo systemctl is-active --quiet $SERVICE_NAME.service; then
        log_success "IoT Server service started successfully"
    else
        log_error "Failed to start IoT Server service"
        log_info "Check logs with: sudo journalctl -u $SERVICE_NAME.service -f"
        exit 1
    fi
}

# Function to test installation
test_installation() {
    log_info "Testing installation..."
    
    local max_attempts=10
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s http://localhost:$SERVICE_PORT/health >/dev/null 2>&1; then
            log_success "Health check passed"
            break
        else
            log_info "Waiting for service to be ready... (attempt $attempt/$max_attempts)"
            sleep 2
            ((attempt++))
        fi
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        log_error "Health check failed after $max_attempts attempts"
        log_info "Check service status: sudo systemctl status $SERVICE_NAME.service"
        exit 1
    fi
}

# Function to display final information
display_final_info() {
    local ip_address=$(hostname -I | awk '{print $1}')
    
    echo
    log_success "🎉 IoT Server deployment completed successfully!"
    echo
    echo "📋 Service Information:"
    echo "   Service Name: $SERVICE_NAME"
    echo "   Service Status: $(sudo systemctl is-active $SERVICE_NAME.service)"
    echo "   Service Port: $SERVICE_PORT"
    echo
    echo "🌐 Access URLs:"
    echo "   Local: http://localhost:$SERVICE_PORT"
    echo "   Network: http://$ip_address:$SERVICE_PORT"
    echo
    echo "🔧 Useful Commands:"
    echo "   View logs: sudo journalctl -u $SERVICE_NAME.service -f"
    echo "   Restart service: sudo systemctl restart $SERVICE_NAME.service"
    echo "   Stop service: sudo systemctl stop $SERVICE_NAME.service"
    echo "   Service status: sudo systemctl status $SERVICE_NAME.service"
    echo
    echo "⚙️  Configuration:"
    echo "   Edit MQTT settings in: $INSTALL_DIR/.env"
    echo "   After editing .env, restart: sudo systemctl restart $SERVICE_NAME.service"
    echo
}

# Main deployment function
main() {
    echo "🚀 IoT Server Automated Deployment Script"
    echo "=========================================="
    echo
    
    check_root
    check_raspberry_pi
    
    log_info "Starting deployment process..."
    
    # System setup
    update_system
    install_dependencies
    install_python
    
    # Application setup
    setup_venv
    setup_database
    create_env_file
    
    # Service setup
    create_systemd_service
    configure_firewall
    start_service
    
    # Verification
    test_installation
    display_final_info
    
    log_success "Deployment completed! 🎉"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
