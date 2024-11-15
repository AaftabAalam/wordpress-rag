# Use the official Node.js image as the base image
FROM node:18 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json (if present) to install dependencies first
COPY package.json package-lock.json ./

# Install the project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Use Nginx to serve the production build
FROM nginx:alpine

# Copy the build output from the build stage into Nginx's html directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to access the app via HTTP
EXPOSE 80

# Start Nginx to serve the app
CMD ["nginx", "-g", "daemon off;"]