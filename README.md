<div align="center">
    <img alt="logo" src="/static/images/icon.png" width="12%">
    <h1>Fantasy Finance</h1>
</div>

## Local setup
```console
cp .env.template .env
vim .env
docker compose up -d
docker exec -it [[CONTAINER_ID]] /bin/sh
python manage.py migrate
python manage.py createsuperuser
python manage.py init
```

## Class diagram
```mermaid
classDiagram
    class User {
        +String username
        +Sting email
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
    }
    class Portfolio {
        +League league
        +User User
        +String name
        +Datetime created
        +Decimal value
        +Decimal perc_change
    }
    note for Snapshot "Calculated portfolio value"
    class Snapshot {
        +Portfolio portfolio
        +Decimal value
        +Datetime created
    }
    class Asset {
        +Portfolio portfolio
        +bool is_currency
        +String ticker
        +int quantity
        +Decimal value
        +Decimal total_value
    }
    class FollowAsset {
        +User user
        +String ticker
    }
    class Transaction {
        +Portfolio portfolio
        +String ticker
        +int quantity
        +Decimal value
        +bool is_purchase
        +Datetime created
        +Decimal total_value
    }
    User ..> League
    User ..> LeagueUser
    User ..> Portfolio
    User --> "many" FollowAsset : Contains
    League --> "many" LeagueUser : Contains
    League --> "many" Portfolio : Contains
    Portfolio --> "many" Asset : Contains
    Portfolio --> "many" Transaction : Contains
    Portfolio --> "many" Snapshot : Contains
```