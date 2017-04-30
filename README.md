### Overview

Multi Variant Fishtest, is a distributed tasks queue for testing new ideas and improvements for Multi Variant Stockfish, the main instance is:

http://35.161.250.236:6543/tests

Developers submit patches with new ideas and improvements, CPU contributors install a fishtest worker on their computers to play some chess games in the background to help the developers testing the patches.

The fishtest worker:
- automatically connects to the server to download: a chess opening book, the [cutechess-cli](https://github.com/ddugovic/Stockfish/wiki/How-To-build-cutechess-with-Qt-5-static) chess game manager and the chess engine sources (for the actual master and for the patch with the new idea) that will be compiled according to the type of worker platform.
- starts a batch of games using cutechess-cli.
- uploads the games results on the server.

#### Worker setup on Linux

Follow these instructions [[worker-setup-linux.md]]

#### Worker setup on Windows

Follow these instructions [[worker-setup-linux.md]]

#### Server setup on Ubuntu

Follow these instructions [[server-setup.md]]

