from shared import settings
from peewee import Model, PostgresqlDatabase, IntegerField, CharField, DateTimeField, FloatField, BigIntegerField, BlobField, TextField, BooleanField
from playhouse.postgres_ext import BinaryJSONField

db = PostgresqlDatabase('tuxcoin', user='postgres', password='postgres', host=settings.DB_HOST, port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Block(BaseModel):
    height = IntegerField(index=True)
    hash = CharField(max_length=64, unique=True, index=True)
    timestamp = DateTimeField(index=True)
    merkle_root = CharField(max_length=64, unique=True)
    tx = BinaryJSONField()
    difficulty = FloatField()
    size = IntegerField()
    version = BlobField()
    bits = BlobField()
    nonce = BigIntegerField()
    coinbase = BlobField()
    tx_count = IntegerField()
    orphaned = BooleanField(default=False, index=True)


class Transaction(BaseModel):
    txid = CharField(max_length=64, unique=True, index=True)
    block = CharField(max_length=64, null=True, index=True)
    block_height = IntegerField(null=True)
    timestamp = DateTimeField(index=True)
    vin = BinaryJSONField()
    addresses_in = BinaryJSONField()
    addresses_out = BinaryJSONField()
    vout = BinaryJSONField()
    input_value = BigIntegerField()
    output_value = BigIntegerField()


class Utxo(BaseModel):
    address = CharField(index=True)
    txid = CharField(index=True)
    vout = IntegerField()
    spent = BooleanField(default=False, index=True)
    scriptPubKey = CharField()
    amount = BigIntegerField()
    block_height = IntegerField(null=True)
    # timestamp = DateTimeField()

    class Meta:
        indexes = (
            (('txid', 'vout'), True),
        )

class Message(BaseModel):
    message = TextField()

class AddressChanges(BaseModel):
    address = TextField(index=True)
    balance_change = BigIntegerField()
    sent_change = BigIntegerField()
    received_change = BigIntegerField()

class Address(BaseModel):
    address = TextField(unique=True, index=True)
    balance = BigIntegerField()
    sent = BigIntegerField()
    received = BigIntegerField()

    def to_dict(self):
        return {
            'address': self.address,
            'balance': self.balance,
            'sent': self.sent,
            'received': self.received,
        }

db.connect()
# db.drop_tables([Block, Transaction, Address, AddressChanges, Message])
db.create_tables([Block, Transaction, Address, AddressChanges, Message, Utxo])