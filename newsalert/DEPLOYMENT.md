# 🚀 Deployment Guide

## Quick Start

### 1. **Environment Setup**
```bash
# Clone and setup
cd /workspaces/space2/newsalert
npm install

# Create configuration files
cp .env.example .env  # Add your API keys
cp .env_keys.example .env_keys  # Add keywords
# .env_prompt is already configured with ULTIMATE-PROMPT v3.0
```

### 2. **Production Deployment**
```bash
# Install PM2 globally
npm install -g pm2

# Start the application
pm2 start space2_newsalert.js --name "sb2o3-newsalert"

# Enable auto-start on reboot
pm2 startup
pm2 save
```

### 3. **Access Points**
- **Admin Dashboard**: http://localhost:3656
- **Health Check**: http://localhost:3656/health
- **API Config**: http://localhost:3656/api/config

## Required Environment Variables

```env
# Essential Configuration (.env)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
OPENAI_API_KEY=your_openai_api_key
SCRAPINGDOG_API_KEY=your_scrapingdog_key
SERPAPI_KEY=your_serpapi_key

# Optional
NODE_ENV=production
CHECK_INTERVAL_HOURS=24
```

## Monitoring Commands

```bash
# Check status
pm2 status

# View logs
pm2 logs sb2o3-newsalert

# Monitor resources
pm2 monit

# Restart if needed
pm2 restart sb2o3-newsalert
```

## Health Verification

After deployment, verify:
1. ✅ Admin panel loads at http://localhost:3656
2. ✅ Configuration API shows all keys loaded
3. ✅ Manual news check triggers successfully
4. ✅ Test Telegram notification sends
5. ✅ Logs show no errors in PM2

---

**Ready for production use! 🎉**
