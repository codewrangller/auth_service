from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    """A class that defines the structure of API Responses"""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": True,
            "code": status_code,
            "data": data,
            "message": None  # Initialize message as None
        }

        if str(status_code).startswith('2'):
            # Success case
            if isinstance(data, dict) and 'detail' in data:
                # If there's a detail message in the response, use it
                response["message"] = data['detail']
                # Remove detail from data to avoid duplication
                data.pop('detail')
                response["data"] = data
            elif isinstance(data, dict) and 'message' in data:
                # If there's a message in the response, use it
                response["message"] = data['message']
                # Remove message from data to avoid duplication
                data.pop('message')
                response["data"] = data
            else:
                # Use generic success message if no specific message found
                response["message"] = "Request processed successfully"
                response["data"] = data
        else:
            # Error case (unchanged)
            response["status"] = False
            response["data"] = None
            try:
                response["message"] = data['detail']
            except KeyError:
                error_list = []
                for k, v in data.items():
                    for value_data in v:
                        error_values = f"{k}: {value_data.title()}"
                    error_list.append(error_values)
                    for i in error_list[:1]:
                        final_error = i
                response["message"] = final_error

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)