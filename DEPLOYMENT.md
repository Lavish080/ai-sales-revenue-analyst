# 🚀 Deployment Guide - AI Sales & Revenue Analyst

Complete guide for deploying the application to production.

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Configuration](#production-configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Deployment

### Development Setup
```bash
# Clone/download project
cd ai-sales-analyst

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API key

# Run application
streamlit run sales_analyst_app.py
```

### Access
- Local: `http://localhost:8501`
- Network: `http://your-ip:8501`

---

## Docker Deployment

### Prerequisites
- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)

### Quick Start with Docker Compose

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Start application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

### Access
- Main app: `http://localhost`
- Direct: `http://localhost:8501`

### Build Custom Docker Image

```bash
# Build image
docker build -t sales-analyst:latest .

# Run container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  sales-analyst:latest
```

### Docker Commands

```bash
# View running containers
docker ps

# View container logs
docker logs container_name

# Stop container
docker stop container_name

# Remove container
docker rm container_name

# Push to registry
docker tag sales-analyst:latest username/sales-analyst:latest
docker push username/sales-analyst:latest
```

---

## Cloud Deployment

### Option 1: Streamlit Cloud (Easiest)

**Pros**: Free tier available, instant deployment, automatic HTTPS

**Steps:**
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Select repository and branch
4. Deploy
5. Add secrets:
   - Go to app settings
   - Add `ANTHROPIC_API_KEY` in "Secrets"

**Limitations:**
- Shared resources
- Upload limit ~200MB
- Limited to 1GB storage

### Option 2: Heroku

**Pros**: Easy deployment, good performance tier

**Setup:**
```bash
# Install Heroku CLI
# Create account at heroku.com

# Login
heroku login

# Create app
heroku create your-app-name

# Add buildpack
heroku buildpacks:add heroku/python

# Set environment variable
heroku config:set ANTHROPIC_API_KEY=your_key_here

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Procfile** (create in root):
```
web: streamlit run sales_analyst_app.py --server.port=$PORT --server.address=0.0.0.0
```

### Option 3: AWS EC2

**Setup:**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Git
sudo apt install python3-pip python3-venv git -y

# Clone project
git clone your-repo-url
cd ai-sales-analyst

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run with Supervisor for auto-restart
sudo apt install supervisor -y

# Create config
sudo nano /etc/supervisor/conf.d/streamlit.conf
```

**Supervisor config:**
```ini
[program:streamlit]
directory=/home/ubuntu/ai-sales-analyst
command=/home/ubuntu/ai-sales-analyst/venv/bin/streamlit run sales_analyst_app.py --server.port=8501 --server.address=0.0.0.0
autostart=true
autorestart=true
user=ubuntu
environment=PYTHONUNBUFFERED=1
```

```bash
# Start supervisor
sudo service supervisor restart

# Check status
sudo supervisorctl status
```

**Use Nginx as reverse proxy:**
```bash
sudo apt install nginx -y

# Create config
sudo nano /etc/nginx/sites-available/sales-analyst
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/sales-analyst /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart
sudo service nginx restart

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 4: Google Cloud Run

**Setup:**
```bash
# Install gcloud CLI
# Authenticate
gcloud auth login

# Create project
gcloud projects create sales-analyst-001

# Build Docker image
gcloud builds submit --tag gcr.io/sales-analyst-001/sales-analyst

# Deploy
gcloud run deploy sales-analyst \
  --image gcr.io/sales-analyst-001/sales-analyst \
  --platform managed \
  --region us-central1 \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here
```

---

## Production Configuration

### Environment Variables
```bash
# Core
ANTHROPIC_API_KEY=your_api_key

# Performance
MAX_RECORDS_DASHBOARD=50000
CACHE_TTL_MINUTES=60

# Security
SECURE_COOKIES=true
ENABLE_XSRF=true

# Logging
LOG_LEVEL=INFO
```

### Security Checklist
- [ ] API key stored in environment, not code
- [ ] HTTPS enabled
- [ ] CORS configured properly
- [ ] Input validation on file uploads
- [ ] Database backups scheduled
- [ ] Rate limiting configured
- [ ] Error logs don't expose sensitive data
- [ ] Access logs enabled

### Performance Optimization

**Streamlit config** (`~/.streamlit/config.toml`):
```toml
[logger]
level = "info"

[client]
showErrorDetails = false
toolbarMode = "minimal"

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false
```

**Database indexing:**
```sql
CREATE INDEX idx_date ON sales(date);
CREATE INDEX idx_product ON sales(product);
CREATE INDEX idx_region ON sales(region);
CREATE INDEX idx_customer ON sales(customer_id);
```

### Backup Strategy

**Daily database backup:**
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

sqlite3 /app/sales_data.db ".backup /backups/sales_data_$DATE.db"
```

**Add to crontab:**
```bash
0 2 * * * /path/to/backup.sh
```

---

## Monitoring & Maintenance

### Health Checks

**Create health check endpoint** (optional):
```python
import streamlit as st
from datetime import datetime
import json

def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if st.sidebar.button("Health Check"):
    st.json(health_check())
```

### Logging

**Configure logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Monitoring Tools

- **Uptime**: UptimeRobot, StatusCake
- **Logs**: CloudWatch, DataDog, New Relic
- **Performance**: New Relic, Datadog
- **Errors**: Sentry, Rollbar

### Metrics to Monitor
- API response times
- CPU/Memory usage
- Error rates
- User sessions
- Database query performance
- API quota usage

---

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer (HAProxy, NGINX)
- Shared database for state
- Session management

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Cache aggregated data
- Limit analysis to smaller date ranges

### Database Scaling
- Use PostgreSQL instead of SQLite
- Add database indexes
- Implement query caching
- Archive old data

---

## Troubleshooting Production Issues

### App Crashes
```bash
# Check logs
docker logs sales-analyst

# Restart container
docker restart sales-analyst

# Check resources
docker stats sales-analyst
```

### High Memory Usage
- Reduce MAX_RECORDS_DASHBOARD
- Filter data by date range
- Use database instead of CSV
- Increase instance size

### Slow Performance
- Check database indexes
- Enable caching
- Use monthly aggregates
- Profile code with cProfile

### API Errors
- Verify API key
- Check rate limits
- Monitor quota usage
- Implement retry logic

---

## Maintenance Tasks

### Daily
- Monitor error logs
- Check API usage
- Verify backups

### Weekly
- Performance review
- User feedback check
- Database optimization

### Monthly
- Security updates
- Dependency updates
- Cost analysis
- Capacity planning

---

## Rollback Plan

```bash
# Keep previous version
docker images

# Roll back to previous image
docker run -d -p 8501:8501 \
  -e ANTHROPIC_API_KEY=$API_KEY \
  sales-analyst:v1.0.0

# Or with Heroku
heroku releases
heroku rollback v2
```

---

## Support & Documentation

- [Streamlit Docs](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [AWS EC2 Guide](https://aws.amazon.com/ec2/)

---

**Version 1.0** | Last Updated: 2024
