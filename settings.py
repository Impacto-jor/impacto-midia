import environ


root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env()  # reading .env file

FACEBOOK_TOKEN = env('FACEBOOK_TOKEN')
MEDIACLOUD_API = env('MEDIACLOUD_API')
