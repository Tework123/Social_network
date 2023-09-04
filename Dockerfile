FROM node:20-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY frontend/social_network ./
RUN npm install
RUN npm run build


FROM nginx:1.25-alpine
COPY --from=build-step /app/build /usr/share/nginx/html
COPY deployment/nginx/nginx.default.conf /etc/nginx/conf.d/default.conf