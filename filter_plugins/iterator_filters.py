"""iterator_filters.py
Ansible custom filter to check if a given value is present into a given list
of object.

Filters are available to check if the value is present in different type of
given objects:
- a single list
- a single dictionary (key or values)
- a list containing multiple lists
- a list containing multiple dictionaries
- a dictionary containing multiple lists
- a dictionary containing multiple dictionaries
"""


class FilterModule(object):
    def filters(self):
        """Dictionary with the list of filters which can be used from Ansible.

        The dictionary must contain a list of filters in the form of:
        'filter_name': function to execute

        Example:
            Declare a filter named "foo_filter" which executed the
            self.bar_function function:

                return {
                    'foo_filter': self.bar_function,
                }
        """
        return {
            'string_in_list': self.string_in_list,
            'list_in_list': self.list_in_list,
            'in_list': self.in_list,
            'string_in_dict': self.string_in_dict,
            'string_in_list_multilist': self.string_in_list_multilist,
            'string_in_list_multidict': self.string_in_list_multidict,
            'string_in_dict_multilist': self.string_in_dict_multilist,
            'list_in_dict_multilist': self.list_in_dict_multilist,
            'in_dict_multilist': self.in_dict_multilist
        }

    def string_in_list(self, needle, haystack):
        """Checks if a given string is into one of the value of the given list.

        Args:
            needle(str): the string to look for.
            haystack(list): the list in which the string should be searched.

        Returns:
            True if the needle is found, False otherwise.
        """
        return needle in haystack

    def list_in_list(self, needle, haystack):
        """Checks if a given list (needle) has at least one element which is
        included into one of the value of the given list (haystack).

        Args:
            needle(list): the list which contains the string to look for.
            haystack(list): the list in which the elements should be searched.

        Returns:
            True if at least one element of needle is found, False otherwise.
        """
        for item in needle:
            if self.string_in_list(item, haystack):
                return True
        return False

    def in_list(self, needle, haystack):
        """Checks if a given object (needle) has at least one element which is
        included into one of the value of the given list (haystack).

        Args:
            needle(str|list): the object which contains the string to look for.
            haystack(list): the list in which the elements should be searched.

        Returns:
            True if at least one element of needle is found, False otherwise.
        """
        needle_type = type(needle)

        if needle_type in (str, unicode):
            return self.string_in_list(needle, haystack)
        elif needle_type is list:
            return self.list_in_list(needle, haystack)
        else:
            msg = 'Unsupported given needle type: {}'.format(needle_type)
            raise TypeError(msg)

    def string_in_dict(self, needle, haystack, search_type="values"):
        """Checks if a given string is into the given dictionary.
        The function can compare key or values of the dictionary, based on the
        given type of comparison.

        Args:
            needle(str): the string to look for.
            haystack(dict): the dictionary in which the string should be
                searched.
            search_type(str): define if the given string should be searched
                into keys or values of the given dictionary (possible values:
                'keys|values', default 'values')

        Returns:
            True if the needle is found, False otherwise.
        """

        # Check
        supported_types = ["keys", "values"]
        search_type = search_type.lower()
        if search_type not in supported_types:
            msg = 'Unsupported search_type: {}, accepted values: {}'
            msg = msg.format(search_type, "|".join(supported_types))
            raise ValueError(msg)

        for key, value in haystack.items():
            if search_type == "keys":
                compare = key
            elif search_type == "values":
                compare = value
            else:
                raise NotImplementedError()

            if needle == compare:
                return True
        return False

    def string_in_list_multilist(self, needle, haystack):
        """Checks if a given string is into one of the value of one of the
        lists present into the given list of lists.

        Args:
            needle(str): the string to look for.
            haystack(list): the list of lists in which the string should be
                searched.

        Returns:
            True if the needle is found, False otherwise.
        """
        for item in haystack:
            if self.string_in_list(needle, item):
                return True
        return False

    def string_in_list_multidict(self, needle, haystack, search_type="values"):
        """Checks if a given string is into one of the dictionaries included
        into the given list.
        The function can compare key or values of the dictionaries, based on
        the given type of comparison.

        Args:
            needle(str): the string to look for.
            haystack(list): the list of dictionaries in which the string
                should be searched.
            search_type(str): define if the given string should be searched
                into keys or values of the given dictionary (possible values:
                'keys|values', default 'values')

        Returns:
            True if the needle is found, False otherwise.
        """
        for item in haystack:
            if self.string_in_dict(needle, item, search_type):
                return True
        return False

    def string_in_dict_multilist(self, needle, dictionary,
                                 search_type="values"):
        """Checks if a given value is into one of the lists included
        into the given dictionary.
        The function can compare key or values of the dictionary, based on
        the given type of comparison.

        Args:
            needle(str): the string to look for.
            dictionary(dict): the dictionary of lists in which the string
                should be searched.
            search_type(str): define if the given string should be searched
                into keys or values of the given dictionary (possible values:
                'keys|values', default 'values')

        Returns:
            True if the needle is found, False otherwise.
        """
        search_type = search_type.lower()

        for key, list in dictionary.items():
            if search_type == "keys":
                if needle == key:
                    return True
            else:
                if self.string_in_list(needle, list):
                    return True
        return False

    def list_in_dict_multilist(self, needles, haystack, search_type="values"):
        """Checks if at least one element of the given list is into one of the
        lists included into the given dictionary.
        The function can compare key or values of the dictionary, based on
        the given type of comparison.

        Args:
            needles(list): the list of strings to look for.
            haystack(dict): the dictionary of lists in which the strings
                should be searched.
            search_type(str): define if the given string should be searched
                into keys or values of the given dictionary (possible values:
                'keys|values', default 'values')

        Returns:
            True if at least one string is found, False otherwise.
        """
        for item in needles:
            if self.string_in_dict_multilist(item, haystack, search_type):
                return True
        return False

    def in_dict_multilist(self, needle, haystack, search_type="values"):
        needle_type = type(needle)

        if needle_type in (str, unicode):
            return self.string_in_dict_multilist(needle, haystack, search_type)
        elif needle_type is list:
            return self.list_in_dict_multilist(needle, haystack, search_type)
        else:
            msg = 'Unsupported given needle type: {}'.format(needle_type)
            raise TypeError(msg)
