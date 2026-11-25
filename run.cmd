wslc run -d --name redis-pieces -p 6379:6379 redis:latest || wslc start redis-pieces
python .
wslc stop redis-pieces