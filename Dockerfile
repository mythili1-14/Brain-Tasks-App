# Use a lightweight Nginx image to serve the static files.
FROM nginx:alpine

# Copy the static files from the 'dist' directory into the Nginx web root.
COPY ./dist /usr/share/nginx/html

# Expose port 80 to the host machine.
EXPOSE 80

# The default command for the Nginx image starts the server.
CMD ["nginx", "-g", "daemon off;"]
