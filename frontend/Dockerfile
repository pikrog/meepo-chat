###################################################
#                      Build                      #
###################################################
FROM node:16.18.0-bullseye-slim as build

# Build under unprivileged user
USER node

# Build in the temporary directory
WORKDIR /tmp

# Copy Node dependency lists
COPY --chown=node package.json package-lock.json .

# Install Node dependencies
RUN npm ci

# Copy remaining sources
COPY --chown=node . .

# Run the build task
RUN npm run build

# Delete unused development dependencies
RUN npm prune --omit=dev

###################################################
#                      Deploy                     #
###################################################
FROM httpd:2.4.54

# Copy only necessary application files
# COPY --from=build --chown=node /tmp/dist/ dist/
COPY --from=build /tmp/dist/ /usr/local/apache2/htdocs/

EXPOSE 80