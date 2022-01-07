class AliasDict(dict):
    """
    A dictionary which allows aliases to be set for a value.
    Works exactly like a regular dict except for:
    - Items can be set with a list or tuple as key:
    >>> d = AliasDict({
    >>>     ("key", "alias", "another-alias"): "value",
    >>> })
    >>> d["key"], d["alias"], d["another-alias"]
    >>> "value", "value", "value"
    - Items can be checked for existence using all aliases:
    >>> "key" in d, "alias" in d
    >>> True, True
    - Items can be aliased after already being set:
    >>> d.alias("key", "yet-another-alias")
    >>> "key"
    >>> d["yet-another-alias"]
    >>> "value"
    - Aliases can be removed, one by one:
    >>> d.unalias("alias")
    - or all at once:
    >>> d.dealias("key")
    - Deleting by alias deletes the value and all aliases:
    >>> del d["alias"]
    """

    @classmethod
    def fromkeys(cls, keys, value=None):
        dct = dict.fromkeys(keys, value)
        return AliasDict(dct)

    @staticmethod
    def is_multi_key(key):
        return isinstance(key, (list, tuple))

    def _unpack_multi_keys(self):
        aliased = [item for item in self.items() if self.is_multi_key(item[0])]
        for keys, value in aliased:
            key = self.alias(*keys)
            super(AliasDict, self).__setitem__(key, value)
            super(AliasDict, self).__delitem__(keys)

    def __init__(self, *args, **kwargs):
        super(AliasDict, self).__init__(*args, **kwargs)
        self.aliases = {}
        self.reverse_aliases = {}
        self._unpack_multi_keys()

    def __setitem__(self, key, value):
        if self.is_multi_key(key):
            key = self.alias(*key)
        super(AliasDict, self).__setitem__(key, value)

    def __getitem__(self, item):
        return super(AliasDict, self).__getitem__(self.aliases.get(item, item))

    def __contains__(self, item):
        return super(AliasDict, self).__contains__(self.aliases.get(item, item))

    def __delitem__(self, key):
        real = self.aliases[key] if key in self.aliases else key
        self.dealias(real)
        super(AliasDict, self).__delitem__(real)

    def __deepcopy__(self, memodict):
        copied = super(AliasDict, self).__deepcopy__(memodict)
        for key, aliases in self.reverse_aliases.items():
            copied.alias(key, *aliases)
        return copied

    def get(self, key, *args):
        return super(AliasDict, self).get(self.aliases.get(key, key), *args)

    def pop(self, key, *args):
        real = self.aliases[key] if key in self.aliases else key
        if real in self:
            self.dealias(real)
        return super(AliasDict, self).pop(real, *args)

    def popitem(self):
        item = super(AliasDict, self).popitem()
        self.dealias(item[0])
        return item

    def clear(self):
        super(AliasDict, self).clear()
        self.aliases.clear()
        self.reverse_aliases.clear()

    def setdefault(self, key, *args):
        if self.is_multi_key(key):
            key = self.alias(*key)
        return super(AliasDict, self).setdefault(key, *args)

    def update(self, *args, **kwargs):
        update = super(AliasDict, self).update(*args, **kwargs)
        self._unpack_multi_keys()
        return update

    def copy(self):
        copied = AliasDict(super(AliasDict, self).copy())
        for key, aliases in self.reverse_aliases.items():
            copied.alias(key, *aliases)
        return copied

    def alias(self, key, *aliases):
        """
        Alias the given key with one or more aliases.
        :param str key: The original value.
        :param str[] aliases: The aliases to add.
        :return:
        """
        if aliases:
            self.aliases.update({alias: key for alias in aliases})
            self.reverse_aliases.setdefault(key, []).extend(aliases)
        return key

    def unalias(self, alias):
        """
        Remove the given alias.
        :param str alias:
        """
        # Remove the alias:
        key = self.aliases.pop(alias)
        # Remove the alias from the reverse aliases:
        aliases = self.reverse_aliases.get(key, [])
        aliases.remove(alias)
        if not aliases:
            # no more aliases, remove the key from reverse aliases:
            self.reverse_aliases.pop(key)

    def dealias(self, key):
        """
        Remove all aliases for the given key.
        :param str key:
        """
        aliases = self.reverse_aliases.pop(key, [])
        for alias in aliases:
            self.aliases.pop(alias)
@sanhancluster
