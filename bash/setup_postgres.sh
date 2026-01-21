#!/bin/bash
set -e

DB_NAME="code_levels"
DB_USER="code_levels_hero"
DB_PASSWORD="super_hero_123"

echo "Creating PostgreSQL database and user..."

# 1. Create database (top-level, no DO)
psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 \
  || psql -U postgres -c "CREATE DATABASE $DB_NAME"

# 2. Create user
psql -U postgres <<EOF
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
      CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASSWORD';
   END IF;
END
\$\$;

-- Ownership
ALTER DATABASE $DB_NAME OWNER TO $DB_USER;

-- PRIVILEGES
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Role defaults
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
EOF

echo "Configuring schema privileges..."

psql -U postgres -d "$DB_NAME" <<EOF
-- Schema ownership
ALTER SCHEMA public OWNER TO $DB_USER;

-- Schema permissions
GRANT USAGE, CREATE ON SCHEMA public TO $DB_USER;

-- Default privileges (future objects)
ALTER DEFAULT PRIVILEGES FOR ROLE $DB_USER
IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;

ALTER DEFAULT PRIVILEGES FOR ROLE $DB_USER
IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;

ALTER DEFAULT PRIVILEGES FOR ROLE $DB_USER
IN SCHEMA public GRANT ALL ON FUNCTIONS TO $DB_USER;
EOF

echo "🟢 PostgreSQL user and database configured successfully."
echo "🔴 exec bash -l"

