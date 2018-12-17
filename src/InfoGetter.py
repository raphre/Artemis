class InfoGetter:
    def _make_conf_string(self, item):
        return 'Is '+item+' correct? (y/n): '

    def _make_query_string(self, item):
        return 'Enter '+item+': '

    def _get_info_with_message(self, message):
        info = input(message)
        confirmation = self._make_conf_string(info)
        reply = input(confirmation)
        if reply == "y":
            return info
        else:
            self._get_info_with_message(message)

    def get_info_for(self, items):
        data = {}
        for item_string in items:
            query_string = self._make_query_string(item_string)
            info = self._get_info_with_message(query_string)
            data[item_string] = info
        return data
