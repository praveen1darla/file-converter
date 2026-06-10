# 🚀 Complete Deployment Guide - File Converter to Production (24/7)

This guide will help you deploy your File Converter app on a domain with 24/7 uptime.

---

## 📋 Prerequisites

- Linux server (Ubuntu 20.04+, CentOS 8+, etc.)
- Domain name pointing to your server
- SSH access to your server
- `sudo` privileges

---

## 🔧 Step 1: Server Setup

### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx
```

### 1.2 Clone/Upload Your Project
```bash
cd /home/praveen
git clone https://github.com/yourusername/PDF_app.git
# OR upload files via SFTP
```

### 1.3 Create Virtual Environment
```bash
cd /home/praveen/PDF_app
python3 -m venv venv
source venv/bin/activate
```

### 1.4 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements-prod.txt
```

---

## 🔐 Step 2: SSL Certificate (HTTPS)

### 2.1 Get Free SSL with Let's Encrypt
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

This will save certificates to:
```
/etc/letsencrypt/live/yourdomain.com/
```

### 2.2 Auto-Renewal
```bash
sudo certbot renew --dry-run
sudo systemctl enable certbot.timer
```

---

## ⚙️ Step 3: Configure Nginx

### 3.1 Edit Nginx Config
```bash
sudo cp /home/praveen/PDF_app/nginx-config.conf /etc/nginx/sites-available/file-converter
sudo nano /etc/nginx/sites-available/file-converter
```

**Replace these lines:**
```nginx
server_name yourdomain.com www.yourdomain.com;
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

### 3.2 Enable Nginx Config
```bash
sudo ln -s /etc/nginx/sites-available/file-converter /etc/nginx/sites-enabled/
sudo nginx -t  # Test config
sudo systemctl restart nginx
```

### 3.3 Create Log Directory
```bash
sudo mkdir -p /var/log/file-converter
sudo chown praveen:praveen /var/log/file-converter
```

---

## 🔄 Step 4: Setup Systemd Service (24/7 Auto-Start)

### 4.1 Install Service
```bash
sudo cp /home/praveen/PDF_app/file-converter.service /etc/systemd/system/
```

### 4.2 Edit Service File (if needed)
```bash
sudo nano /etc/systemd/system/file-converter.service
```

Make sure paths match your setup:
- `User=praveen`
- `WorkingDirectory=/home/praveen/PDF_app`
- `ExecStart=/home/praveen/PDF_app/venv/bin/gunicorn ...`

### 4.3 Enable & Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable file-converter.service
sudo systemctl start file-converter.service
```

### 4.4 Check Status
```bash
sudo systemctl status file-converter.service
```

You should see: **Active: active (running)**

---

## 📥 Step 5: Configure Download Folder (24/7 Access)

### 5.1 Public Download Folder
```bash
mkdir -p /home/praveen/Downloads/FileConverter
chmod 755 /home/praveen/Downloads/FileConverter
```

### 5.2 Via Web (Optional - Serve Downloads)
To allow users to download via web:

```bash
mkdir -p /var/www/file-converter-downloads
sudo chown praveen:www-data /var/www/file-converter-downloads
```

Update Nginx config:
```nginx
location /downloads/ {
    alias /var/www/file-converter-downloads/;
    expires 1h;
}
```

---

## 🌐 Step 6: Domain Setup

### 6.1 DNS Configuration
Point your domain to your server's IP:
```
A Record: yourdomain.com → YOUR_SERVER_IP
A Record: www.yourdomain.com → YOUR_SERVER_IP
```

### 6.2 Test Your Domain
```bash
# Wait 5-10 minutes for DNS propagation
curl https://yourdomain.com
```

---

## 📊 Step 7: Monitoring & Logs

### 7.1 View App Logs
```bash
sudo journalctl -u file-converter.service -f
```

### 7.2 View Nginx Logs
```bash
sudo tail -f /var/log/nginx/file-converter-access.log
sudo tail -f /var/log/nginx/file-converter-error.log
```

### 7.3 View App Logs
```bash
sudo tail -f /var/log/file-converter/access.log
sudo tail -f /var/log/file-converter/error.log
```

---

## 🔄 Step 8: Automatic Restart on Crash

The systemd service automatically restarts the app if it crashes. To verify:

```bash
sudo systemctl status file-converter.service
```

The `Restart=always` setting in `file-converter.service` handles this.

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Nginx Error
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Service Won't Start
```bash
sudo systemctl status file-converter.service
sudo journalctl -u file-converter.service -n 50
```

### Check if Gunicorn is Running
```bash
ps aux | grep gunicorn
```

---

## 📈 Performance Optimization

### 4.1 Increase Workers (for more concurrent users)
Edit `/etc/systemd/system/file-converter.service`:
```bash
ExecStart=/home/praveen/PDF_app/venv/bin/gunicorn \
    --workers 8 \  # Increase from 4 to 8
    --worker-class sync \
    ...
```

### 4.2 Enable Caching
Nginx already caches static files (30 days).

### 4.3 Monitor CPU & Memory
```bash
htop
# or
top
```

---

## 🔒 Security Checklist

- ✅ SSL/TLS enabled (HTTPS)
- ✅ Auto-renew certificates (Let's Encrypt)
- ✅ Security headers configured
- ✅ Firewall rules set
- ✅ File size limit (100MB)
- ✅ Input validation enabled

---

## 🚀 Complete Deployment Command Cheat Sheet

```bash
# 1. Setup
cd /home/praveen/PDF_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt

# 2. SSL
sudo certbot certonly --standalone -d yourdomain.com

# 3. Nginx
sudo cp nginx-config.conf /etc/nginx/sites-available/file-converter
sudo nano /etc/nginx/sites-available/file-converter  # Edit domain
sudo ln -s /etc/nginx/sites-available/file-converter /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# 4. Service
sudo cp file-converter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable file-converter.service
sudo systemctl start file-converter.service

# 5. Verify
sudo systemctl status file-converter.service
curl https://yourdomain.com
```

---

## 📞 Quick Commands

```bash
# Start/Stop/Restart Service
sudo systemctl start file-converter.service
sudo systemctl stop file-converter.service
sudo systemctl restart file-converter.service

# View Status
sudo systemctl status file-converter.service

# View Real-time Logs
sudo journalctl -u file-converter.service -f

# Check if Running
ps aux | grep gunicorn

# Update Code
cd /home/praveen/PDF_app
git pull  # if using git
sudo systemctl restart file-converter.service
```

---

## ✅ Final Verification

After deployment, verify:

1. **App is running**: `https://yourdomain.com`
2. **HTTPS works**: Check for green lock icon
3. **Uploads folder accessible**: Should have `/tmp` folder
4. **Downloads work**: Files saved to `~/Downloads/FileConverter`
5. **24/7 uptime**: Check with `sudo systemctl status file-converter.service`

---

## 📝 Notes

- **Downloads Location**: `/home/praveen/Downloads/FileConverter`
- **Logs Location**: `/var/log/file-converter/`
- **Workers**: 4 (adjust based on CPU cores)
- **Timeout**: 120 seconds (for large files)
- **Max File Size**: 100MB

---

**🎉 Your File Converter is now live 24/7 on your domain!**

For updates, just restart the service:
```bash
sudo systemctl restart file-converter.service
```
