"""Input Validator."""
from flask import request


class InputValidator:
    """Validate Inputs."""

    def validate_input(self, validation_data=list):
        """Search order and update status if found."""
        error_message = []
        for data in validation_data:
            input = request.get_json()
            message =  data.strip() + ' is required'
            try:
                input[data]
                if not input[data]:
                    raise Exception(data)
                elif data.strip() == 'password' and len(input[data]) < 5:
                    message = data + ' should be atleast 5 characters'
                    raise Exception(data)
                elif data.strip() in ['quantity', 'price'] and not isinstance(input[data], int):
                    message = "Please enter a valid integer for " + data
                    raise Exception(data)
                elif data.strip() == 'status' and input[data].strip() not in ['Processing', 'Cancelled', 'Complete']:
                    message = "Status must be Processing, Cancelled or Complete"
                    raise Exception(data)
            except:
                error_message.append({'field': data, 'message': message})

        return error_message

    def validate_datatype(self, data_type, data=list):
        """Valdate Data type."""
        for item in data:
            try:
                int(item)
            except ValueError as error:
                return "Oops {}. Enter a valid value in {}".format(str(error), item)
        return None
        