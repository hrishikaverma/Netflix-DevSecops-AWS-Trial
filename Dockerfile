# =========================
# Stage 1: Build (Vite App)
# =========================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build-time environment variables
ARG TMDB_V3_API_KEY
ENV VITE_APP_TMDB_V3_API_KEY=${TMDB_V3_API_KEY}
ENV VITE_APP_API_ENDPOINT_URL=https://api.themoviedb.org/3

# Build production bundle
RUN npm run build


# =========================
# Stage 2: Production (Nginx)
# =========================
FROM nginx:stable-alpine

# Copy build output
COPY --from=builder /app/dist /usr/share/nginx/html

# Remove default nginx configuration
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

RUN apk update && apk upgrade --no-cache

# Prepare nginx for non-root execution
RUN mkdir -p /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    && chown -R nginx:nginx /var/cache/nginx /etc/nginx /usr/share/nginx/html

# Run nginx as non-root user
USER nginx

# Expose non-privileged port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
