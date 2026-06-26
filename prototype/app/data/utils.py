import re

def camel_to_snake_case(col):
    col = re.sub(r'(.)([A-Z][a-z0-9]+)', r'\1_\2', col)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', col)

def clean_column(col):
    return (
        col.replace("(", "")
           .replace(")", "")
           .replace(" ", "_")
           .replace("__", "_")
           .replace("/", "")
    )
