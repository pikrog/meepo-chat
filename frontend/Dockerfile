###################################################
#                      Build                      #
###################################################
FROM node:16.18.0-bullseye-slim as build

# Build under unprivileged user
USER node

# Build in the temporary directory
WORKDIR /home/node

# Copy Node dependency lists
COPY --chown=node package.json package-lock.json .

# Install Node dependencies
RUN npm ci

# Copy remaining sources
COPY --chown=node . .

# Run the build task
RUN npm run vite:build
RUN npm run nest:build

# Delete unused development dependencies
RUN npm prune --omit=dev

###################################################
#                      Deploy                     #
###################################################
FROM node:16.18.0-bullseye-slim

# Run in production
ENV NODE_ENV=production

# Run under unprivileged user
USER node

# Application directory
ARG APP_PATH="/home/node"
WORKDIR ${APP_PATH}

# Copy only necessary application files
COPY --from=build --chown=node:node /home/node/package*.json /home/node/
COPY --from=build --chown=node:node /home/node/node_modules/ /home/node/node_modules/
COPY --from=build --chown=node:node /home/node/dist/ /home/node/dist/
COPY --from=build --chown=node:node /home/node/.vite/ /home/node/.vite/
COPY --from=build --chown=node:node /home/node/public/ /home/node/public/

# Run Node server
CMD ["node", "dist/main"]
EXPOSE 3000