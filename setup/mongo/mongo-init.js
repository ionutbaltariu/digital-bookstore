db.createUser(
    {
        user: "user",
        pwd: "pass",
        roles: [
            {
                role: "readWrite",
                db: "orders"
            }
        ]
    }
)

db.createUser(
    {
        user: "admin",
        pwd: "pass",
        roles: [
            {
                role: "dbOwner",
                db: "orders"
            }
        ]
    }
)