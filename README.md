# meepo-chat
A distirbuted chat system

# Local tests
Run the command below and wait for all the services to initialize.

    $ docker compose up

# Swarm

## Generating Swarm configuration from the template

    $ docker-compose -f swarm-template.yml config > swarm.yml

Then you need to edit `swarm.yml` and:
- insert `version: "3.8"` line,
- remove `name: ...` line,
- remove quote characters from the numeric values of `published:` nodes.

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
