Metadata
========
event_type
----------
**id**: str
**name**: str


Definitions
===========
job_definition
--------------
**hash**: str
**name**: str
**entrypoint**: optional[str]
**command**: str
**environment**: dict
**active**: bool

trigger
-------
**hash**: str
**target**: (job_definition.hash) str
**event_type_id**: (event_type.id) int
**active**: bool

event_generator.time_interval
-----------------------------
**hash**: str
**event_type_id**: (event_type.id) int
**active**: bool

**base_datetime**: timestampz
**interval**: timestampz

event_generator.gate
-----------------------------
**hash**: str
**event_type_id**: (event_type.id) int
**active**: bool
...


Instances
=========
event
-----
**id**: str
**datetime**: timestampz
**event_type_id**: (event_type.id) int
**state**: Enum(created, claimed, processed)  # this actually probably needs to be more complex to handle mulitple parallel "schedulers"

job_instance
------------
**id**: str
**caused_by**: (event.id) str
**job_definition_hash**: (job_definition.hash) str
**status**: Enum(created, ...)  # Same
**created_at**: timestampz
**started_at**: timestampz
**completed_at**: timestampz
**updated_at**: timestampz

job_parameter
-------------
**id**: str
**job_id**: str
**type**: Enum(datetime, ...)
**value**: bytes
