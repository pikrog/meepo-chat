# meepo-chat
A distirbuted chat system

# Local tests
Run the command below and wait for all the services to initialize.
`$ docker compose up`

# Swarm
On the manager node:
`$ docker swarm init`
`$ docker network create -d overlay --attachable meepo-chat-network`
`$ docker stack deploy -c compose-swarm.yml meepo-chat`
On the worker nodes:
`$ docker join ...`
On any node:
`$ docker compose -f compose-chat-server.yml --env-file .env.chat-server.example -p chat-server-example up`
