FROM node:18-alpine as build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

RUN npm install
RUN npm audit fix

COPY . .

ENV NODE_ENV=production
#ARG VITE_SSE_ADDR
#ENV VITE_REDIS_CONN_STRING=redis://redis:6379
#ENV VITE_MQTT_HOST=mqtt
#ENV VITE_MQTT_PORT=1883
# ARG VITE_CMS_SSL=false
# ENV VITE_CMS_HOST=${VITE_CMS_HOST}
RUN npm run build

FROM node:18-alpine

WORKDIR /usr/src/app

COPY --from=build /usr/src/app/build ./

# RUN echo '{"type": "module"}' > package.json
COPY package.json package-lock.json ./
#RUN npm i redis async-mqtt
#RUN npm audit fix

USER 1337:1337
ENV NODE_ENV=production
#ENV VITE_SSE_ADDR=http://sse:8080
ENTRYPOINT [ "node", "/usr/src/app/index.js" ]
