# EventSourcingTemplate

Template for
[Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
implementation.

## Prerequisites

Running of this project locally requires the following tools to be
present on the host system:

* `docker` (version 23.05.0+)
* `docker compose` (version 2.21.0+)

## Tests environment

To run tests:
1. Go into `docker/tests/` folder
2. Execute

    ```bash
    docker compose up --abort-on-container-exit
    ```

## Working with repository

1. `backend` folder must be marked as `Sources Root` in `IDE` to make imports work
