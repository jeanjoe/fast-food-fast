"""Input Validator."""
from flask import request


class InputValidator:
    """Validate Inputs."""

    def validate_input(self, validation_data=list):
        """Search order and update status if found."""
        error_message = []
        for data in validation_data:
            input = request.get_json()
            try:
                input[data]
                if not input[data]:
                    raise Exception(data)

            except:
                error_message.append({'field': data, 'message': data + ' is required'})

            # if data == 'password' and len(input[data]) < 5:
            #     error_message.append({'field': 'password_length', 'message': data + ' should be atleast 5 characters'})
        return error_message

    def validate_datatype(self, data_type, data=list):
        """Valdate Data type."""
        for item in data:
            try:
                int(item)
            except ValueError as error:
                return "Oops {}. Enter a valid value in {}".format(str(error), item)
        return None
        