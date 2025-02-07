<div align="center">
    <img alt=" logo" src="/static/images/icon.png" width="12%">
    <h1> &dollar; Fantasy finance </h1>
</div>

## Local setup
```console
cp .env.template .env
docker compose up -d
docker exec -it [[CONTAINER_ID]] python manage.py migrate
docker exec -it [[CONTAINER_ID]] python manage.py createsuperuser
docker exec -it [[CONTAINER_ID]] python manage.py init
```

## Class diagram
```mermaid
classDiagram
    class User {
        +String username
    }
    class League {
        +User author
        +Decimal start_value
        +String name
        +String description
        +int num_portfolios
        +int num_users
        +Datetime created
    }
    note for LeagueUser "Determines invite permissions"
    note for LeagueUser "Allows for Portfolio creation"
    class LeagueUser {
        +User user
        +League league
        +Datetime created
    }
    class Portfolio {
        +League league
        +User User
        +String name
        +Datetime created
    }
    note for Snapshot "Calculated portfolio value"
    class Snapshot {
        +Portfolio portfolio
        +Decimal value
        +Datetime created
    }
    class Asset {
        +Portfolio portfolio
        +String ticker
        +int quantity
        +Decimal value
        +Decimal total_value
    }
    class Transaction {
        +Portfolio portfolio
        +String ticker
        +int quantity
        +Decimal value
        +bool is_purchase
        +Datetime created
    }
    User ..> League
    User ..> LeagueUser
    User ..> Portfolio
    League --> "many" LeagueUser : Contains
    League --> "many" Portfolio : Contains
    Portfolio --> "many" Asset : Contains
    Portfolio --> "many" Transaction : Contains
    Portfolio --> "many" Snapshot : Contains
```