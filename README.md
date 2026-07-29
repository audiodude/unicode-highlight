# unicode-highlight
Simple webpage which highlights all non-ASCII characters in a given text

The UNIDATA-Blocks file needs to be periodically updated (extremely rarely):

    wget -O unidata-blocks.txt http://www.unicode.org/Public/UNIDATA/Blocks.txt

## Deploy

Deployed to fly.io from the `Dockerfile` (python:3.12-slim + gunicorn):

    flyctl deploy
