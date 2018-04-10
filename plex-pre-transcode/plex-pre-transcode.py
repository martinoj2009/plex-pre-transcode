#!/usr/bin/env python3

__author__ = 'Martino Jones'

# Requires packages
import argparse
from sys import stdout, stderr, stdin, exit
from os import walk, path
import subprocess


def main():
    # Get the folder path(s)
    parser = argparse.ArgumentParser(description='Plex Pre-Transcode allows you to pre transcode videos so that your '
                                                 'Plex/Emby server doesn\'t need to waste time transcoding videos '
                                                 'when the clients can do that.')
    parser.add_argument('--folder', type=str, required=True,
                        help='Path to the root directory of folders to check for transcoding.')
    parser.add_argument('--extension', type=str, required=True,
                        help='The extension you wish to convert.')
    args = parser.parse_args()

    # Make sure we have ffmpeg
    if subprocess.getstatusoutput('which ffmpeg')[0]:
        stderr.write("You need to install ffmpeg\n")
        exit(-155)

    # Get files recursively
    allFiles = getFiles(args.folder, args.extension)

    # Lets start converting files
    for line in allFiles:
        convertFile(line)


def getFiles(rootDire, extension):
    """
    Get all files recursively.
    :param rootDire: Folder to start at
    :param extension: The extension you're looking for
    :return: List of strings
    """
    allFiles = []
    for root, directories, filenames in walk(rootDire):
        for filename in filenames:
            if filename.endswith(extension):
                allFiles.append(path.join(root, filename))

    return allFiles


def convertFile(filePath, verbose=False):
    """
    Convert a file to a supported video format
    :param filePath: Full path to the file
    :param verbose: If True then print stdout
    :return: Boolean
    """
    result = True
    if filePath is not None:
        try:
            process = subprocess.Popen("ls", shell=True)
            process.wait()

            # Check if they want verbose
            if verbose:
                process.communicate()

        except subprocess.CalledProcessError as e:
            result = False
            stderr.write(e)

    return result


# RUN MAIN
if __name__ == '__main__':
    main()
