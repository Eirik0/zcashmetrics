#!/usr/bin/env python2

import dbwrapper, tabledefs

# Make sure the database and tables exist
dbwrapper.ensureDatabaseExists()
tabledefs.ensureTablesExist()
