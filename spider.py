from envparse import env

env.read_envfile()

print(env.str('db_ip'))