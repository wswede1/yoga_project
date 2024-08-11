FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=strongpassword
ENV MYSQL_DATABASE=yoga

COPY init.sql /docker-entrypoint-initdb.d/
