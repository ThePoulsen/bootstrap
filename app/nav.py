from flask_nav.elements import *

topbar = Navbar('Project title',
    View('Index', 'indexBP.indexView'),
    Subgroup(
        'auth',
        View('Log in', 'authBP.loginView'),
        View('Register', 'authBP.registerView'),
        View('Set Password', 'authBP.setPasswordView'),
            ), )
