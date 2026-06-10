#!/bin/bash
# Production Deployment Helper Script
# Run this script on your server to automatically setup everything

set -e

echo "================================================"
echo "🚀 File Converter - Production Deployment Setup"
echo "================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Please don't run this script as root!${NC}"
    echo "Run as regular user: bash deploy.sh"
    exit 1
fi

# Get user input
read -p "Enter your domain (e.g., yourdomain.com): " DOMAIN
read -p "Enter your email (for SSL certificate): " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo -e "${RED}❌ Domain and email are required!${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}📋 Setup Summary:${NC}"
echo "  Domain: $DOMAIN"
echo "  Email: $EMAIL"
echo "  App Path: /home/$USER/PDF_app"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Step 1: System Updates
echo ""
echo -e "${YELLOW}📦 Step 1: Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git

echo -e "${GREEN}✅ System packages installed${NC}"

# Step 2: Project Setup
echo ""
echo -e "${YELLOW}📦 Step 2: Setting up Python environment...${NC}"
cd /home/$USER/PDF_app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-prod.txt

echo -e "${GREEN}✅ Python environment ready${NC}"

# Step 3: Create Directories
echo ""
echo -e "${YELLOW}📁 Step 3: Creating necessary directories...${NC}"
mkdir -p ~/Downloads/FileConverter
mkdir -p /var/log/file-converter
sudo chown $USER:$USER /var/log/file-converter

echo -e "${GREEN}✅ Directories created${NC}"

# Step 4: SSL Certificate
echo ""
echo -e "${YELLOW}🔐 Step 4: Getting SSL certificate from Let's Encrypt...${NC}"
sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN -m $EMAIL --agree-tos -n

echo -e "${GREEN}✅ SSL certificate installed${NC}"

# Step 5: Nginx Configuration
echo ""
echo -e "${YELLOW}🌐 Step 5: Configuring Nginx...${NC}"
sudo cp /home/$USER/PDF_app/nginx-config.conf /etc/nginx/sites-available/file-converter

# Replace domain in config
sudo sed -i "s/yourdomain.com/$DOMAIN/g" /etc/nginx/sites-available/file-converter

# Enable the site
sudo ln -sf /etc/nginx/sites-available/file-converter /etc/nginx/sites-enabled/

# Test and restart nginx
sudo nginx -t
sudo systemctl restart nginx

echo -e "${GREEN}✅ Nginx configured${NC}"

# Step 6: Systemd Service
echo ""
echo -e "${YELLOW}🔄 Step 6: Setting up systemd service...${NC}"
sudo cp /home/$USER/PDF_app/file-converter.service /etc/systemd/system/

# Replace username if different
sudo sed -i "s/User=praveen/User=$USER/g" /etc/systemd/system/file-converter.service
sudo sed -i "s|WorkingDirectory=/home/praveen/PDF_app|WorkingDirectory=/home/$USER/PDF_app|g" /etc/systemd/system/file-converter.service
sudo sed -i "s|/home/praveen/PDF_app/venv|/home/$USER/PDF_app/venv|g" /etc/systemd/system/file-converter.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable file-converter.service
sudo systemctl start file-converter.service

echo -e "${GREEN}✅ Service installed and running${NC}"

# Step 7: Verify
echo ""
echo -e "${YELLOW}✓ Step 7: Verifying deployment...${NC}"
sleep 2

if sudo systemctl is-active --quiet file-converter.service; then
    echo -e "${GREEN}✅ Service is running${NC}"
else
    echo -e "${RED}❌ Service failed to start${NC}"
    sudo systemctl status file-converter.service
    exit 1
fi

# Final Summary
echo ""
echo "================================================"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "================================================"
echo ""
echo -e "${GREEN}Your app is now live:${NC}"
echo "  🌐 https://$DOMAIN"
echo "  📥 Downloads: ~/Downloads/FileConverter"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  Status:   sudo systemctl status file-converter.service"
echo "  Logs:     sudo journalctl -u file-converter.service -f"
echo "  Restart:  sudo systemctl restart file-converter.service"
echo "  Stop:     sudo systemctl stop file-converter.service"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Wait 5-10 minutes for DNS to propagate"
echo "  2. Visit https://$DOMAIN in your browser"
echo "  3. Check logs if something goes wrong"
echo ""
echo "For detailed help, see: DEPLOYMENT.md"
echo ""
