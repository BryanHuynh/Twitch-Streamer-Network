# To run

`python3 script.py <streamer_name>`

# twitch-network

install all the required packages with

`pip install -r requirements.txt`

If you add another package with pip please add it to the requirements list

# setting up a virtual environment (optional)

Install virtualenv with`pip install virtualenv`

create a new environment with: `virtualenv environment`

start the environment with by cd'ing into environment/bin or environment/script and running `source activate`

to stop the environment run `deactivate`

## Adding new packages to requirements list

if you're using virtual environment,

`pip freeze > requirements.txt `

## Setting up .env

create a new file called .env in the root folder.

the contents of the file should be along the lines of

`client_id = '<client_id>'
client_secret = 'client_secret'
app_access_token = 'Bearer <app_access_token>`

dm me to get this file.

to use these variables in your project add:

`config = dotenv_values('.env')`

config is type dictionary so you can` config[<variable>]`
