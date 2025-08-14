# Deployment Guide - Image to AutoCAD Converter

This guide will help you deploy the Image to AutoCAD Converter application to Fly.io.

## Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **flyctl CLI**: Install the Fly.io CLI tool
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
3. **Docker**: Make sure Docker is installed and running

## Quick Deployment

### Option 1: Using the Deploy Script (Recommended)

1. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

2. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

The script will automatically:
- Create the Fly.io app
- Create a volume for file storage
- Deploy the application
- Show you the app URL and login credentials

### Option 2: Manual Deployment

1. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

2. **Create the app**:
   ```bash
   flyctl apps create autocad-converter
   ```

3. **Create a volume for file storage**:
   ```bash
   flyctl volumes create autocad_data --region ord --size 1 -a autocad-converter
   ```

4. **Deploy the application**:
   ```bash
   flyctl deploy
   ```

## Configuration

### Environment Variables

The application uses these environment variables (already configured in `fly.toml`):
- `FLASK_ENV=production`
- `FLASK_APP=app.py`
- `DATA_DIR=/app/data` (for volume storage)

### Volume Storage

The app uses a Fly.io volume mounted at `/app/data` for:
- Uploaded images (`/app/data/uploads/`)
- Converted CAD files (`/app/data/converted/`)

## Access the Application

After deployment, your app will be available at:
**https://autocad-converter.fly.dev**

### Login Credentials
- **Username**: `admin`
- **Password**: `password123`

## Useful Commands

### View Application Logs
```bash
flyctl logs -a autocad-converter
```

### Check Application Status
```bash
flyctl status -a autocad-converter
```

### SSH into the Application
```bash
flyctl ssh console -a autocad-converter
```

### Scale the Application
```bash
flyctl scale count 2 -a autocad-converter  # Scale to 2 instances
```

### Update the Application
After making changes to your code:
```bash
flyctl deploy
```

## Troubleshooting

### Common Issues

1. **App not starting**: Check logs with `flyctl logs -a autocad-converter`
2. **File upload issues**: Ensure the volume is properly mounted
3. **Memory issues**: Consider scaling up the VM size in `fly.toml`

### Volume Issues

If you need to recreate the volume:
```bash
flyctl volumes destroy autocad_data -a autocad-converter
flyctl volumes create autocad_data --region ord --size 1 -a autocad-converter
flyctl deploy
```

### Changing Configuration

Edit `fly.toml` and redeploy:
```bash
flyctl deploy
```

## Security Notes

⚠️ **Important**: The current setup uses hardcoded credentials for demo purposes. For production use:

1. Change the hardcoded username/password in `app.py`
2. Use environment variables for sensitive data
3. Consider implementing proper user authentication
4. Use HTTPS (already configured in `fly.toml`)

## Support

For Fly.io specific issues, check:
- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io Community](https://community.fly.io/)

For application issues, check the logs and ensure all dependencies are properly installed.
