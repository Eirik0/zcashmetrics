ZcashMetrics
============

ZcashMetrics will connect to a running instance of the Zcash daemon and execute a series of RPCs to populate a local PosgreSQL database. The database can then be queried to generate metrics pertaining to the Zcash blockchain.

Installation
------------
**1. Install Zcash**

See [Zcash 1.0 User Guide](https://github.com/zcash/zcash/wiki/1.0-User-Guide)


**2. Install PostgreSQL**

	$ sudo apt-get install postgresql postgresql-contrib

**3. Set PostgreSQL to boot on startup**

	$ sudo update-rc.d postgresql enable
	
**4. Start PostgreSQL**

	$ sudo service postgresql start

**5. Set the password for the PostgreSQL user**

	$ sudo -u postgres psql postgres
	$ \password postgres
	<enter password twice>
	$ \q

**6. Allow local connections to PostgreSQL**

As the super user edit "/etc/postgresql/9.5/main/pg_hba.conf"
Find the following lines:

	# Database administrative login by Unix domain socket
	local   all             postgres                                peer

and change "peer" to "md5"

**7. Restart and test PostgreSQL**

	$ sudo service postgresql restart
	$ psql -U postgres -W


**8. Install dependencies**

	$ sudo pip install psycopg2-binary
	$ sudo pip install python-bitcoinrpc

Usage
-----
Start the Zcash daemon and execute the following command:

	$ python zcashmetrics.py
