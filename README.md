# PyERP

***Introduction***

PyERP is a Python-powered ERP system with Ntfy integration, osTickit integration, and Vikunja integration planned.
The project is so tiring that it cannot be finished quickly but soon.
You will not be charged for using this project and can use it commercially (why would anybody do that though?).
For more legal information, please refer to the GNU license.

***READ BEFORE DEPLOYMENT!!!***

Thank you for choosing PyERP! As the only individual in charge of this massive project, I give you my best wishes!

### If you are a user of this project and are willing to deploy this project to your production line:

I have no warranty over whatever happened to your production line because I like my life.

I do recommend you do a full installation, with an empty server that has MySQL(or MariaDB) installed

Docker is NOT recommended for a production deployment as the author is not very good at configuring it (STOP LAUGHING THIS INSTANT!!!)

Nginx is recommended to be set up, and so is Treafik

DO NOT use Flask or Python to start the program

Use uWSGI to start it

### If you are a developer wanting to help with the production (or some geeks just checking out the code):

I think a simple "docker-compose up -d" is enough

Do note that Ntfy and Vikunja are NOT needed for the ERP to work(Yet, it's a promised feature tho).

Docker Desktop is recommended for docker, it has a GUI, so it's simple to boot

Please PULL when doing a modification on the code, then submit a merge request when committing the code

DO NOT edit the code on GitHub
