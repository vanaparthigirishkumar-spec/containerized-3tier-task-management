# Frontend Dockerfile.
# Serves the HTML/CSS/JS frontend with Nginx and proxies /api to FastAPI.

FROM nginx:alpine

# Copy custom nginx config that proxies /api to the backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend static files
COPY index.html style.css app.js /usr/share/nginx/html/

EXPOSE 80

# Nginx runs as a non-root user (nginx) by default in the official image.
