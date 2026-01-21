#!/bin/bash

# ----------------------------
# Config - change these values
# ----------------------------
DB_NAME="django_store"        
DB_USER="hero_2"             
DB_PASSWORD="super_hero_123_2"     
DB_HOST="localhost"
DB_PORT="5432"
# ----------------------------

echo "Creating new PostgreSQL user '$DB_USER' and granting access to database '$DB_NAME'..."

psql -U postgres <<EOF
-- Create user
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Set default settings for user
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';

-- Grant privileges on the database
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
EOF

echo "User '$DB_USER' created and granted privileges on '$DB_NAME'."
