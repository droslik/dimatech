import sqlalchemy

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('username', sqlalchemy.String(50), nullable=False, unique=True),
    sqlalchemy.Column('hashed_password', sqlalchemy.String(128)),
    sqlalchemy.Column('is_admin', sqlalchemy.Boolean, unique=False, default=False),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, default=False),
)

accounts = sqlalchemy.Table(
    'accounts',
    metadata,
    sqlalchemy.Column('bill_id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('balance', sqlalchemy.Integer),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey("users.id")),
)


goods = sqlalchemy.Table(
    'goods',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('title', sqlalchemy.String(50), nullable=False, unique=True),
    sqlalchemy.Column('description', sqlalchemy.String(128), nullable=False),
    sqlalchemy.Column('price', sqlalchemy.Integer, nullable=False)
)


transactions = sqlalchemy.Table(
    'transactions',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('bill_id', sqlalchemy.ForeignKey("accounts.bill_id")),
    sqlalchemy.Column('amount', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id')),
)

