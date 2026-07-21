# Use the official NGINX image
FROM nginx:alpine

# Remove the default NGINX web page
RUN rm -rf /usr/share/nginx/html/*

# Copy all frontend files into the NGINX web root
COPY . /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
