# GPSI
A simple service that stores your GPS coordinates and tells you how much you
have travelled.

## Design
The GPS coordinates are stored in a database with spatial indexes. In this case
we use Postgres@9.6 with the postgis extension.

On the initial request, a "Route" is created with a a unique id. More way
points can then be added to the created route by posting them to 'way_point'
endpoint.

A waypoint is stored in the database, with coordinates that are the ``Point``
type available from Postgis. We also store the SRID (4326) with it, as the coordinates
used as input are WGS84. (It also stores data in metres, that is always good)

When we calculate the length, we create a ``Line`` type using the points that we
have for a particular route and then calculate the length on the fly; using the
`ST_MakeLine` and `ST_Lengt`h.

Alternative could have been using a `MultiGeometry` type and store all the
points in that or store a `Line` type directly and modify it on the fly when a
new point is added. However, simply saving a point as a new row in the database
seemed like the cleanest solution of them all.

## Usage
To run this you would need to install Postgres 9.6 with the postgis extension.
Then create a database called `GPSI` in your postgres server.

```psql
create database gpsi;
create extension postgis;
```

You should aslo create a test database that will be used to run tests.

```psql
create database "gpsi-test";
create extension postgis;
```

Then you can install the requirements.
```bash
pip install -r requirements.txt
```

After that you can run run the command to create the tables for the database you just created.
```bash
PYTHONPATH='.' python gpsi/commands/create_all_db.py
```

To run the server use the following command
```
PYTHONPATH='.' python gpsi/runserver.py
```

And finally, to test the code
```bash
PYTHONPATH='.' nosetests
```

## What next?

- Right not we do not verify the data we get when we store the waypoint. Add a way to verify that.
- Use The ORM more, especially for the length query
- We should accept the "CreatedAt" for the way point endpoint and store it, that way we can ensure that we are reading the points in the right order when we recreate the path.

## The Longest Path

The longest Path per day can be calculated using the the following query

```
    SELECT route_id, ST_Length(ST_MakeLine(ST_AsText(coordinate))::geography) as length
    FROM way_point
    WHERE created_at > start_date
    AND created_at < end_date
    GROUP BY route_id
    ORDER BY length desc;
```

We can store this data in a new table, as it will be requested quite often
every night using a job.

However we can also calculte this data on the fly, by grouping by the created
date too.
