from typing import List

try:
    # Django Filter backend provided by django-filter
    from django_filters.rest_framework import DjangoFilterBackend as _DjangoFilterBackend
except Exception:  # pragma: no cover
    _DjangoFilterBackend = object  # type: ignore


class CompatDjangoFilterBackend(_DjangoFilterBackend):
    """Compatibility shim for schema generation.

    Some django-filter versions used with DRF do not implement
    `get_schema_operation_parameters`. DRF's OpenAPI generator
    expects this method to exist on filter backends. This subclass
    provides a minimal implementation so `generateschema` works.
    """

    def get_schema_operation_parameters(self, view) -> List[dict]:  # type: ignore[override]
        params: List[dict] = []

        # Prefer explicit filterset_fields when present
        fields = getattr(view, "filterset_fields", None)
        if isinstance(fields, dict):
            field_names = list(fields.keys())
        elif isinstance(fields, (list, tuple, set)):
            field_names = list(fields)
        else:
            field_names = []

        for name in field_names:
            params.append(
                {
                    "name": str(name),
                    "required": False,
                    "in": "query",
                    "description": "",
                    "schema": {"type": "string"},
                }
            )

        return params

