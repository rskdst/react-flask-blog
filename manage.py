import os
import sys
from flask_cors import CORS


def init_env_path(_file_):
    package_dir = os.path.join(os.path.dirname(_file_), '../')
    abs_path = os.path.abspath(package_dir)
    if abs_path not in sys.path:
        print(f'Add {abs_path} to python path')
        sys.path.insert(0, abs_path)


init_env_path(__file__)

from apps.utils import parse_args
from apps import create_app

__all__ = ['main']


def main():
    app = create_app()
    args = parse_args()
    app.debug=False
    CORS(app, supports_credentials=True) # 允许跨域
    if args.cmd.isdigit():
        cmd = 'runserver'
        port = int(args.cmd)
    else:
        cmd = args.cmd
        port = args.port if args.port else 8080

    if cmd == 'runserver':
        app.run('localhost', port)
        app.logger.info(f'run server at port {port}')
    else:
        print('run command error')

if __name__ == '__main__':
    main()
