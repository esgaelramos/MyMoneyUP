


class FormatHelper:

    @classmethod
    def str_to_bool(value: str =  None) -> bool:
        """
            Convert a string to a boolean value.

            Very useful for converting environment variables to boolean values.
        """
        return bool(value.lower() == 'true')



FORMAT_HELPER = FormatHelper()