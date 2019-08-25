import os
target = r"Z:\photo"
ignoreFiles = ['Thumbs.db']
rules = []


class Entry:
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory

    def get_path(self):
        return os.path.join(self.directory, self.name)


class Rule:
    def __init__(self, dir1, dir2):
        self.trash = dir1
        self.remain = dir2  # PRIORITY

    def __str__(self):
        return '{} -> {}'.format(self.trash, self.remain)


# check_rule checks if there is a rule regarding duplicates in certain directories
# and creates a new one if no rule present
def check_rule(dir1, dir2):
    for rule in rules:
        if (rule.trash == dir1 and rule.remain == dir2) or (rule.trash == dir2 and rule.remain == dir1):
            return rule
    while True:
        choice = input('{} (0)\nor\n{} (1)?'.format(dir1, dir2))
        if choice == '0':
            rule = Rule(dir2, dir1)  # dir1 has priority
            rules.append(rule)
            return rule

        if choice == '1':
            rule = Rule(dir1, dir2)  # dir2 has priority
            rules.append(rule)
            return rule


def find_dupes(entries):
    for i, entry in enumerate(entries):
        dupes = list(filter(lambda cur_entry: cur_entry.name == entry.name, entries[i+1:]))
        if dupes:
            for dupe in dupes:
                rule = check_rule(entry.directory, dupe.directory)
                # if there is a duplicate files, file from `trash` directory will be removed
                trash = rule.trash
                # checking if both files are present
                # just in case one of files was already deleted in different conflict
                if os.path.exists(entry.get_path()) and os.path.exists(dupe.get_path()):
                    if entry.directory == trash:
                        print('REMOVING', entry.get_path())
                        os.remove(entry.get_path())
                    else:
                        print('REMOVING', dupe.get_path())
                        os.remove(dupe.get_path())
                else:
                    print('skipping', entry.name)


def list_all_files(directory):
    contents = map(lambda name: Entry(name, directory), os.listdir(directory))

    list_contents = list(contents)
    files = filter(lambda entry: os.path.isfile(entry.get_path()), list_contents)
    folders = filter(lambda entry: os.path.isdir(entry.get_path()), list_contents)
    for folder in folders:
        print('running', folder.get_path())
        yield from list_all_files(folder.get_path())

    yield from filter(lambda entry: entry.name not in ignoreFiles, files)


all_files = list(list_all_files(target))
find_dupes(all_files)

