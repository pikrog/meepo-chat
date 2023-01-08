# meepo-chat
A distirbuted chat system

# Local tests

Run the command below and wait for all the services to initialize.

    $ docker compose up
    
# Swarm

## Configuring Swarm
Modify `.env` and `.env.chat-server.base` according to your needs. Remember to change these variables when deploying to production:
- `BACKEND_CORS_ORIGINS`
- `MASTER_SERVER_ADDRESS`
- `JWT_PRIVATE_KEY`
- `JWT_PUBLIC_KEY`

Also consider modifying these variables for security reasons (especially if RabbitMQ or PostgreSQL are going to be available externally):
- `RABBITMQ_DEFAULT_USER`
- `RABBITMQ_DEFAULT_PASS`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

See [Environmental variables](#environmental-variables) section for more details.


Use the command below to generate a Swarm configuration from the template:

    $ docker-compose -f swarm-template.yml config > swarm.yml

Then depending on the `docker compose` version, you might need to edit `swarm.yml` and for example:
- insert `version: "3.8"` line,
- remove `name: ...` line,
- remove quote characters from the numeric values of `published:` nodes,
- delete the `networks.default` and `services.front-end.networks` nodes.

If the generated `swarm.yml` file is invalid, `docker stack deploy` will fail.

## Deployment
On the manager node:

    $ docker swarm init
    $ docker network create -d overlay --attachable meepo-chat-network
    $ docker stack deploy -c swarm.yml meepo-chat
    
On the worker nodes apply the `join` command printed from previously issued `docker swarm init`:

    $ docker join ...

Choose a Swarm node to serve the main database:

    $ docker node ls
    $ docker node update --label-add maindb=true <id-of-selected-node>

Deploy a chat server on any Swarm node:

    $ docker compose -f compose-chat-server.yml --env-file .env.chat-server.example -p chat-server-example up
    
## Environmental variables
- `BACKEND_CORS_ORIGINS` – a list of allowed cross origin domains.
- `SERVER_NAME` – a chat server name.
- `MAX_CLIENTS` – a maximum number of users in the chat room.
- `ADVERTISED_ADDRESS` – a published (external) chat server address (IP or domain).
- `ADVERTISED_PORT` – a published (external) chat server port.
- `MASTER_SERVER_ADDRESS` – a master server address (reachable by users).
- `JWT_PUBLIC_KEY` - an RSA public key used to verify JWT tokens.
- `JWT_PRIVATE_KEY` – an RSA private key used to sign JWT tokens. Must be kept secret.
- `RABBITMQ_DEFAULT_USER` – a default user name for the Message Broker.
- `RABBITMQ_DEFAULT_PASS` – a default user password for the Message Broker.
- `POSTGRES_USER` – a default user name for the Main Database server.
- `POSTGRES_PASSWORD` – a default user's password for the Main Database server.
- `POSTGRES_DB` – a default database name for the Main Database server.
