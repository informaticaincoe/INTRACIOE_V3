FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

# Instalar dependencias de desarrollo
RUN npm audit fix

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
