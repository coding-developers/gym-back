from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status


class StandardRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = response.status_code if response else 200
        is_error = status_code >= 400

        if is_error:
            wrapped = {
                "data": None,
                "message": self._extract_message(data),
            }
        else:
            wrapped = {
                "data": data,
                "message": "success",
            }

        return super().render(wrapped, accepted_media_type, renderer_context)

    def _extract_message(self, data):
        if isinstance(data, dict):
            for key in ("detail", "message", "error"):
                if key in data:
                    return str(data[key])
            # validação de campos (ex: {"email": ["Este campo é obrigatório."]})
            first_error = next(iter(data.values()), None)
            if isinstance(first_error, list):
                return str(first_error[0])
        return str(data) if data else "error"


class DestroyMixin:
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(None, status=status.HTTP_200_OK)
