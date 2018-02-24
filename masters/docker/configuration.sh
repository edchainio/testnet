#!/usr/bin/env bash

usermod -aG docker <username>

su - <username>

# docker run --rm -it -p "8000:8000" --name stellar stellar/quickstart --testnet

# docker run -it ubuntu