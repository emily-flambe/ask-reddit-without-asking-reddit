# Use the official Node.js image
FROM node:18-alpine


# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
# Ensure node_modules and package-lock.json are cleaned before npm install
RUN npm install @rollup/rollup-linux-x64-musl
RUN rm -rf node_modules package-lock.json && npm install

# Copy the rest of the application source code
COPY . .

# Expose the port for Vite
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev", "--", "--host=0.0.0.0"]
