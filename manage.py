## -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Enable flask-migrate
migrate = Migrate(app, db)

# Enable flask-manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
