from django import forms


class FormFieldsFormatMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for (field_name, field) in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})

            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['class'] = ''

            field.widget.attrs['class'] = "form-control rounded-0"
            field.widget.attrs['placeholder'] = f"Enter {field_name.title()}"
