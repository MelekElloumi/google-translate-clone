FROM node:lts-alpine

WORKDIR /app

COPY package* ./

RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 3000

CMD ["npm","start"]
