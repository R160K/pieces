# Pieces

This a, still nascent, attempt to create a modular, portable, (relatively) stateless social media website using existing protocols and infrastructure.

Right now, the project (barely) supports logging in with an existing atproto/Bluesky account. It will come to support atproto feeds, alongside chats -- likely using Matrix -- and rooms, which will in turn be made up of feeds, chats and widgets.

Another element that this project would like to implement is portable, private storage for userdata, in effect a private data counterpart to an atproto PDS. Unfortunately, no existing projects have yet reached maturity, with a least one project with promise seemingly having been abandoned.

This project will not just allow feeds from atproto Lexicons, but other federeated and even proprietary social media services. All protocols for chats and feeds should be available from a single atproto sign-on.

This is still very much a work in progress.

***

## Setup

1. Clone the repository:

```bash/Powershell
git clone https://github.com/R160K/pieces.git
```

2. Run venv setup helper script:

```bash/Powershell
python setup/venv_setup.py
```

3. Activate the virtual environment:

```bash/Powershell
. .venv/Scripts/activate
```

4. The app requires a secret key for Flask, as well as a keypair for JWT signing of atproto requests. These are stored in the environment variables: FLASK_SECRET_KEY and OAUTH_PRIVATE_JWK. There is a helper script to generate these and store them in a .env file (.env.secrets):

```bash/Powershell
python setup/generate_secrets.py
```

5. The app needs a hostname for callbacks, stored in the environment variable HOSTNAME. This should be set to the hostname of the server running the app, e.g. https://testapp.bstools.co.uk. You can set this in the .env file (.env.secrets) or in your shell environment.

```.env
HOSTNAME=https://myhostname.com
```

6. The app requires a Redis server to store session data. You can run a Redis server in a Docker container using docker or wslc:

```bash
docker run -d --name redis-pieces -p 6379:6379 redis:latest
```
```Powershell
wslc run -d --name redis-pieces -p 6379:6379 redis:latest
```

7. Run the app (during testing it is using Flask's built-in development server, which is not suitable for production):

```bash/Powershell
python .
```