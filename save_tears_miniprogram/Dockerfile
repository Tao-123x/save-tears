FROM node:20-bookworm-slim AS build

WORKDIR /app

ARG NPM_CONFIG_REGISTRY=https://registry.npmmirror.com

COPY package.json package-lock.json ./
RUN npm ci --registry=$NPM_CONFIG_REGISTRY

COPY . .
ARG VITE_API_BASE_URL=""
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build:h5

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/build/h5 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
