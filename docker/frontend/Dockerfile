FROM node:14

WORKDIR /usr/src/app

COPY spa/package.json package.json
COPY spa/package-lock.json package-lock.json

RUN npm install

COPY spa/swagger.json swagger.json
COPY spa/views views
COPY spa/index.js index.js

EXPOSE 3000

CMD npm start
