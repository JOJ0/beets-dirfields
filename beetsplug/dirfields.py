# This file is part of beets.
# Copyright 2014, Malte Ried
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

import os
from beets.importer import SingletonImportTask
from beets.plugins import BeetsPlugin


class DirFieldsPlugin(BeetsPlugin):
    def __init__(self):
        super(DirFieldsPlugin, self).__init__()
        self.import_stages = [self.stage]

    def stage(self, config, task):
        highest_level = float('inf')
        levels = []
        if 'levels' in self.config and self.config['levels'].get():
            level_split = str(self.config['levels'].get()).split(',')
            for level_config in level_split:
                level_config = level_config.replace(' ', '')
                if len(level_config) == 0:
                    continue
                if '-' in level_config:
                    if level_config[-1] == '-':
                        highest_level = int(level_config[:-1])
                    else:
                        start_level = 0
                        if level_config[0] != '-':
                            start_level = int(level_config[0:level_config.index('-')])
                        end_level = int(level_config[level_config.index('-') + 1:])
                        if end_level < start_level:
                            start_level, end_level = end_level, start_level
                        for idx in range(start_level, end_level + 1):
                            levels.append(idx)
                else:
                    levels.append(int(level_config))
        if len(levels) == 0:
            highest_level = 0

        items = [task.item] if isinstance(task, SingletonImportTask) else task.items + [task.album]

        for item in items:
            # On reimports prevent overwriting original path.
            # top-most dir check should suffice but for newer plugin versions or
            # manually set dirs attributes, additionally check for dirs.
            if "dirs" in item or "dir1" in item:
                self._log.info(
                    "Preserving dirfields attributes of reimported item {}", item.id
                )
                continue

            dirs = []
            path = os.path.normpath(item.path)
            # Save the full path in a similarily named attribute
            item["dirs"] = path

            # Collect path parts
            while path and len(path) > 0:
                path, file_system_object = os.path.split(path)
                if not file_system_object or len(file_system_object) == 0:
                    file_system_object = b""
                    path = b""
                dirs.append(file_system_object)

            # Save path parts to item attributes
            dirs.reverse()
            for idx, dir_name in enumerate(dirs):
                if idx >= highest_level or idx in levels:
                    key = 'dir%i' % idx
                    if key in self.config:
                        key = self.config[key].get()
                    item[key] = dir_name
            item.store()
