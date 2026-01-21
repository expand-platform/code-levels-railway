#!/bin/bash
DB_USER="code_levels_admin"

REASSIGN OWNED BY $DB_USER TO postgres;
DROP OWNED BY $DB_USER;
DROP ROLE $DB_USER;