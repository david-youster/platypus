from util import generate_secret_key
import json

config = {'title': None, 'secret_key': None}


def main():
    print('Initialising a new project...')
    init_project()
    save_config_file()
    print('Finished setting up project. To start web application, run: ')
    print('python3 webapp.py')

def init_project():
    while not config['title']:
        config['title'] = input('Enter a project title: ')
    print('Creating a secret key...')
    config['secret_key'] = generate_secret_key()


def save_config_file():
    print('Building config file...')
    with open('config.json', 'w') as f:
        f.write(json.dumps(config))


if __name__ == '__main__':
    main()