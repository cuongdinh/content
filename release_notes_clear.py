# remove all releaseNotes from files in: Itegrations, Playbooks, Reports and Scripts.
# Note: using yaml will destroy the file structures so filtering as regular text-file.\
# Note2: file must be run from root directory with 4 sub-directories: Integration, Playbook, Reports, Scripts
# Usage: python release_notes_clear.py
import os
import glob

def yml_remove_releaseNote_record(file_path):
    '''
    locate and remove release notes from a yaml file.
    :param file_path: path of the file
    :return: True if file was changed, otherwise False.
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    orig_size = len(lines)
    consider_multiline_notes = False
    new_lines = []
    for line in lines:
        if line.startswith('releaseNotes:'):
            # releaseNote title: ignore current line and consider following lines as part of it (multiline notes)
            consider_multiline_notes = True

        elif consider_multiline_notes:
            # not a releaseNote title (right after a releaseNote block (single or multi line)
            if not line[0].isspace():
                # regular line
                consider_multiline_notes = False
                new_lines.append(line)
            else:
                # line is part of a multiline releaseNote: ignore it
                pass
        else:
            # regular line
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.write(''.join(new_lines))

    return orig_size != len(new_lines)


def json_remove_releaseNote_record(file_path):
    '''
    locate and remove release notes from a json file.
    :param file_path: path of the file
    :return: True if file was changed, otherwise False.
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    orig_size = len(lines)
    consider_multiline_notes = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('"releaseNotes"'):
            # releaseNote title: ignore current line and consider following lines as part of it (multiline notes)
            consider_multiline_notes = True

        elif consider_multiline_notes:
            # not a releaseNote title (right after a releaseNote block (single or multi line)
            if line.strip() and line.strip()[0] == '"':
                # line
                consider_multiline_notes = False
                new_lines.append(line)
            else:
                # line is part of a multiline releaseNote: ignore it
                pass
        else:
            # regular line
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.write(''.join(new_lines))

    return orig_size != len(new_lines)


FILE_EXTRACTER_DICT = {
    '*.yml' : yml_remove_releaseNote_record,
    '*.json' : json_remove_releaseNote_record,
}


def remove_releaseNotes_folder(folder_path, files_extension):
    '''
    scan folder and remove all references to release notes
    :param folder_path: path of the folder
    :param files_extension: type of file to look for (json or yml)
    '''
    scan_files = glob.glob(os.path.join(folder_path, files_extension))

    count = 0
    for path in scan_files:
        if FILE_EXTRACTER_DICT[files_extension](path):
            count += 1

    print '--> Changed %d out of %d files' % (count, len(scan_files), )


def main(root_dir):
    yml_folders_to_scan = ['Integrations', 'Playbooks', 'Scripts', ] # yml
    json_folders_to_scan = ['Reports', ] # json

    for folder in yml_folders_to_scan:
        print 'Scanning directory: "%s"' % (folder, )
        remove_releaseNotes_folder(os.path.join(root_dir, folder), '*.yml')

    for folder in json_folders_to_scan:
        print 'Scanning directory: "%s"' % (folder, )
        remove_releaseNotes_folder(os.path.join(root_dir, folder), '*.json')


if __name__ == '__main__':
    main(os.path.dirname(__file__))