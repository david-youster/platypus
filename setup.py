from util import generate_secret_key, save_config_file
import json

config = {'title': None, 'secret_key': None, 'dev': True}


def main():
    init_project()
    save_config_file(config)
    print('Finished setting up project. To start web application, run: ')
    print('python3 webapp.py')

def init_project():
    print('Initialising a new project...')
    while not config['title']:
        config['title'] = input('Enter a project title: ')
    print('Creating a secret key...')
    config['secret_key'] = generate_secret_key()


if __name__ == '__main__':
    main()