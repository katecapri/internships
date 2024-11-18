""" verification_value {min:18, max:35} -> {"min":18, "max":35}

Revision ID: 015
Revises: 014
Create Date: 2023-05-24 12:00:00

"""
from sqlalchemy.sql import table, column
from sqlalchemy import String
from alembic import op

# revision identifiers, used by Alembic.
revision = '015'
down_revision = '014'
branch_labels = None
depends_on = None


def upgrade() -> None:
    template_request_field_templates = table("template_request_field_templates", column("verification_value", String))
    route_request_field_templates = table("route_request_field_templates", column("verification_value", String))
    request_fields = table("request_fields", column("verification_value", String))
    op.execute(
        template_request_field_templates.update()
        .where(template_request_field_templates.c.verification_value == op.inline_literal('{min:18, max:35}'))
        .values({"verification_value": op.inline_literal('{"min":18, "max":35}')})
    )
    op.execute(
        route_request_field_templates.update()
        .where(route_request_field_templates.c.verification_value == op.inline_literal('{min:18, max:35}'))
        .values({"verification_value": op.inline_literal('{"min":18, "max":35}' )})
    )
    op.execute(
        request_fields.update()
        .where(request_fields.c.verification_value == op.inline_literal('{min:18, max:35}'))
        .values({"verification_value": op.inline_literal('{"min":18, "max":35}')})
    )


def downgrade() -> None:
    template_request_field_templates = table("template_request_field_templates", column("verification_value", String))
    route_request_field_templates = table("route_request_field_templates", column("verification_value", String))
    request_fields = table("request_fields", column("verification_value", String))
    op.execute(
        template_request_field_templates.update()
        .where(template_request_field_templates.c.verification_value == op.inline_literal('{"min":18, "max":35}'))
        .values({"verification_value": op.inline_literal('{min:18, max:35}')})
    )
    op.execute(
        route_request_field_templates.update()
        .where(route_request_field_templates.c.verification_value == op.inline_literal('{"min":18, "max":35}'))
        .values({"verification_value": op.inline_literal('{min:18, max:35}')})
    )
    op.execute(
        request_fields.update()
        .where(request_fields.c.verification_value == op.inline_literal('{"min":18, "max":35}'))
        .values({"verification_value": op.inline_literal('{min:18, max:35}')})
    )
