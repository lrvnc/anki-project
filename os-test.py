import os
 
env_var = input('Please enter environment variable name:\n')
 
env_var_value = input('Please enter environment variable value:\n')
 
os.environ[env_var] = env_var_value
 
print(f'{env_var}={os.environ[env_var]} environment variable has been set.')

env_var = input('Please enter the environment variable name:\n')
 
if env_var in os.environ:
    print(f'{env_var} value is {os.environ[env_var]}')
else:
    print(f'{env_var} does not exist')