FROM node:18-alpine

WORKDIR /app

# The package.json will be created by Vite, but we copy it if it exists
COPY package*.json ./
# RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
