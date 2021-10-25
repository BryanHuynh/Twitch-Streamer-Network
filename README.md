# Turning Data into network Format for gephi

Run `python3 script.py <streamer>` on a streamer to get a new data set in /links/. 

combine the data sets you've created with `python3 merge_formated.py <dataset>` in /links/

    Skip step if you only want to use one dataset. Just replace dataset filename with `complete.csv`
  
run `python3 get_unique_streamer.py ./links/complete.csv` this will generate/update the streamer.csv in the root directory with all streamers

run `python3 get_games.py` to populate streamer.csv with the streamers top 5 games

run `python3 network_format.py` to generate a nodes and edge list that can be used in gephi


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
