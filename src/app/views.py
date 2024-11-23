from .db import db
from wtforms import StringField, IntegerField, DecimalField
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.form import BaseForm
from flask_admin.form import rules

# Define a custom ModelView for Usuario
class CustomModelView(ModelView):
    
    column_display_pk = True
    can_export = True
    can_view_details = True

    def __init__(self, model, session, **kwargs):
        self.column_list = [column.key for column in model.__table__.columns]
        self.column_searchable_list = [column.key for column in model.__table__.columns]
        self.column_filters = [column.key for column in model.__table__.columns]
        self.column_sortable_list = [column.key for column in model.__table__.columns]
        
        self.form_create_rules = self._generate_form_create_rules(model)
        self.form_extra_fields = self._generate_form_extra_fields(model)
        super().__init__(model, session, **kwargs)
    
    def _generate_form_create_rules(self, model):
        fields = [column.key for column in model.__table__.columns  if not column.primary_key and column.autoincrement]
        return (rules.FieldSet(fields, f"{model.__name__} Campos"),)

    def _generate_form_extra_fields(self, model):
        extra_fields = {}
        for column in model.__table__.columns:
            if column.primary_key and column.autoincrement:
                continue
            # Verifica o tipo da coluna e associa ao campo correspondente
            if isinstance(column.type, db.Integer):
                extra_fields[column.key] = IntegerField(column.key.capitalize())
            elif isinstance(column.type, db.Numeric):
                extra_fields[column.key] = DecimalField(
                    column.key.capitalize(), places=2
                )
            elif isinstance(column.type, (db.String, db.Text)):
                extra_fields[column.key] = StringField(column.key.capitalize())
        return extra_fields
