"""init

Revision ID: 03f13f5f2449
Revises: 
Create Date: 2020-02-15 15:24:11.759657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03f13f5f2449'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logLevel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logLevel_level'), 'logLevel', ['level'], unique=False)
    op.create_table('logType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logType_type'), 'logType', ['type'], unique=False)
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=32), nullable=False),
    sa.Column('address', sa.Integer(), nullable=True),
    sa.Column('i2c_channel', sa.Integer(), nullable=True),
    sa.Column('isEnabled', sa.Integer(), nullable=True),
    sa.Column('isConnected', sa.Integer(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=256), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('value', sa.String(length=256), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('alert_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp_triggered', sa.DateTime(), nullable=False),
    sa.Column('threshold', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('timestamp_cleared', sa.DateTime(), nullable=True),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alert_log_timestamp_cleared'), 'alert_log', ['timestamp_cleared'], unique=False)
    op.create_index(op.f('ix_alert_log_timestamp_triggered'), 'alert_log', ['timestamp_triggered'], unique=False)
    op.create_index(op.f('ix_alert_log_type'), 'alert_log', ['type'], unique=False)
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('message', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('logType_id', sa.Integer(), nullable=True),
    sa.Column('logLevel_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['logLevel_id'], ['logLevel.id'], ),
    sa.ForeignKeyConstraint(['logType_id'], ['logType.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_log_timestamp'), 'log', ['timestamp'], unique=False)
    op.create_table('reading_temperature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('value_min', sa.Float(), nullable=False),
    sa.Column('value_max', sa.Float(), nullable=False),
    sa.Column('value_avg', sa.Float(), nullable=True),
    sa.Column('pixel_array', sa.PickleType(), nullable=True),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reading_temperature_timestamp'), 'reading_temperature', ['timestamp'], unique=False)
    op.create_index(op.f('ix_reading_temperature_value_avg'), 'reading_temperature', ['value_avg'], unique=False)
    op.create_index(op.f('ix_reading_temperature_value_max'), 'reading_temperature', ['value_max'], unique=False)
    op.create_index(op.f('ix_reading_temperature_value_min'), 'reading_temperature', ['value_min'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reading_temperature_value_min'), table_name='reading_temperature')
    op.drop_index(op.f('ix_reading_temperature_value_max'), table_name='reading_temperature')
    op.drop_index(op.f('ix_reading_temperature_value_avg'), table_name='reading_temperature')
    op.drop_index(op.f('ix_reading_temperature_timestamp'), table_name='reading_temperature')
    op.drop_table('reading_temperature')
    op.drop_index(op.f('ix_log_timestamp'), table_name='log')
    op.drop_table('log')
    op.drop_index(op.f('ix_alert_log_type'), table_name='alert_log')
    op.drop_index(op.f('ix_alert_log_timestamp_triggered'), table_name='alert_log')
    op.drop_index(op.f('ix_alert_log_timestamp_cleared'), table_name='alert_log')
    op.drop_table('alert_log')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('setting')
    op.drop_table('sensor')
    op.drop_index(op.f('ix_logType_type'), table_name='logType')
    op.drop_table('logType')
    op.drop_index(op.f('ix_logLevel_level'), table_name='logLevel')
    op.drop_table('logLevel')
    # ### end Alembic commands ###
