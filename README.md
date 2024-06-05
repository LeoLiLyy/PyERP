# PyERP

***READ BEFORE DEPLOYMENT!!!***

Thank you for choosing PyERP! Me, as the one and only individual in charge of this massive project, give you my best wishes!

Also check out the license file, thank you very much!

### If you are a user of this project and is willing to deploy this project to your production line:

I have no warranty over whatever happened to your production line, because I like my life.

I do recommend you to do a full installation, with an empty server that have MySQL(or MariaDB) installed

Docker is NOT recommended for a production deployment as the author is not very good at configuring it (STOP LAUGHING THIS INSTANT!!!)

Nginx is recommended to be set up, so is Treafik

You also need to install Ntfy (for sending notification), osTicket (for helpdesk integration), and Vikunja (for giving out task to your employees).

You should also update the ERP system AT LEAST TWICE A WEEK to prevent vulnerabilities from harming your system, datas and businesses.

DO NOT use flask or python to start the program

Use uWSGI or npm to start it

### If you are a developer wanting to help with the production (or some geeks just checking out the code):

I think a simple "docker-compose up -d" is enough

Do note that Ntfy and Vikunja is NOT needed in order for the ERP to work(Yet, it's a promised feature tho).

Docker desktop is recommended for docker, it got a GUI, so it's simple to boot

AND please PULL when doing a modification on the code, then submit a merge request when committing the code

DO NOT edit the code on GitHub