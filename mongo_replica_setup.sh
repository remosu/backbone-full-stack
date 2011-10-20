#!/bin/bash

mkdir -p data/r0
mkdir -p data/r1
mkdir -p data/r2

mongod --replSet foo --port 27017 --dbpath data/r0 --fork --logpath data/r0.log --rest
mongod --replSet foo --port 27018 --dbpath data/r1 --fork --logpath data/r1.log --rest
mongod --replSet foo --port 27019 --dbpath data/r2 --fork --logpath data/r2.log --rest

./mongo_replica_activate.py
