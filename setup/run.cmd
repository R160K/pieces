wslc run -d --name redis-pieces -p 6379:6379 redis:latest || wslc start redis-pieces
@REM  python .
@REM  wslc stop redis-pieces