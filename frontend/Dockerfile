FROM node:24-alpine as build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

RUN npm install
#RUN npm audit fix

COPY . .

ENV NODE_ENV=production
RUN npm run build

FROM node:24-alpine

WORKDIR /usr/src/app

COPY --from=build /usr/src/app/build ./

COPY package.json package-lock.json ./

RUN npm install --only=production

USER 1337:1337
ENV NODE_ENV=production
ENTRYPOINT [ "node", "/usr/src/app/index.js" ]
