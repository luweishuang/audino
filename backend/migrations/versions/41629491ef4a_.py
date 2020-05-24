"""empty message

Revision ID: 41629491ef4a
Revises: 
Create Date: 2020-04-24 09:42:58.879484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41629491ef4a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    label_type = op.create_table(
        "label_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_label_type_type"), "label_type", ["type"], unique=True)
    op.bulk_insert(
        label_type, [{"id": 1, "type": "select"}, {"id": 2, "type": "multiselect"}]
    )
    role = op.create_table(
        "role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_role_role"), "role", ["role"], unique=True)
    op.bulk_insert(role, [{"id": 1, "role": "admin"}, {"id": 2, "role": "user"}])
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("creator_user_id", sa.Integer(), nullable=False),
        sa.Column("api_key", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["creator_user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_key"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("assigned_user_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=100), nullable=False),
        sa.Column("original_filename", sa.String(length=100), nullable=False),
        sa.Column("reference_transcription", sa.Text(), nullable=True),
        sa.Column("is_marked_for_review", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.ForeignKeyConstraint(["assigned_user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("filename"),
    )
    op.create_table(
        "label",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
        sa.ForeignKeyConstraint(["type_id"], ["label_type.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint("_name_project_id_uc", "label", ["name", "project_id"])
    op.create_table(
        "user_project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "label_value",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("label_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(length=200), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.ForeignKeyConstraint(["label_id"], ["label.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint(
        "_label_id_value_uc", "label_value", ["label_id", "value"]
    )
    op.create_table(
        "segmentation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Float(), nullable=False),
        sa.Column("end_time", sa.Float(), nullable=False),
        sa.Column("transcription", sa.Text(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.ForeignKeyConstraint(["data_id"], ["data.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "annotation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("segmentation_id", sa.Integer(), nullable=False),
        sa.Column("label_value_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "last_modified",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.utc_timestamp(),
        ),
        sa.ForeignKeyConstraint(["label_value_id"], ["label_value.id"]),
        sa.ForeignKeyConstraint(["segmentation_id"], ["segmentation.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("annotation")
    op.drop_table("segmentation")
    op.drop_table("label_value")
    op.drop_table("user_project")
    op.drop_table("label")
    op.drop_table("data")
    op.drop_table("project")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_role_name"), table_name="role")
    op.drop_table("role")
    op.drop_table("label_type")
    # ### end Alembic commands ###
