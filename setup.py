from util import generate_secret_key, save_config_file
import json

config = {
    'title': None,
    'secret_key': None,
    'dev': True,
    'port': 5000}


def main():
    init_project()
    save_config_file(config)
    print('Application setup complete. To launch, run: ')
    print('python3 webapp.py')


def init_project():
    print('Initialising a new project...')
    populate_config_fields()
    print('Creating a secret key...')
    config['secret_key'] = generate_secret_key()


def populate_config_fields():
    read_title()
    read_port_number()


def read_title():
    while not config['title']:
        config['title'] = input('Enter a project title: ')


def read_port_number():
    port = input('Enter the port number (default {}): '.format(config['port']))
    if port.isnumeric():
        config['port'] = port
    else:
        print('Using default port number.')


if __name__ == '__main__':
    main()
