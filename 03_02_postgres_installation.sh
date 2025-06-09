sudo apt install -y wget ca-certificates

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

sudo apt update
sudo apt install postgresql-16 postgresql-contrib-16 postgresql-16-pgvector
sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo service postgresql start

sudo service postgresql status
#psql -U postgres

sudo emacs /etc/postgresql/16/main/pg_hba.conf

#CREATE EXTENSION vector;
#CREATE DATABASE text_embeddings OWNER postgres;
#GRANT ALL PRIVILEGES ON DATABASE text_embeddings TO postgres;
