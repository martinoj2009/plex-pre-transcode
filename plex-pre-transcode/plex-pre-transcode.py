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
    converter_location = subprocess.run(['which', 'ffmpeg'], stdout=subprocess.PIPE).\
        stdout.decode('ascii').replace('\n', '')

    if "ffmpeg" not in converter_location:
        stderr.write("You need to install ffmpeg\n")
        exit(-155)

    # Get files recursively
    allFiles = getFiles(args.folder, args.extension)


    # Lets start converting files
    for line in allFiles:
        convertFile(line, converter_location)


def getFiles(rootdir, extension):
    """
    Get all files recursively.
    :param rootdir: Folder to start at
    :param extension: The extension you're looking for
    :return: List of strings
    """
    allFiles = []
    for root, directories, filenames in walk(rootdir):
        for filename in filenames:
            if filename.endswith(extension):
                allFiles.append(path.join(root, filename))

    return allFiles


def convertFile(filepath, convertExecutable,verbose=False):
    """
    Convert a file to a supported video format
    :param filepath: Full path to the file
    :param verbose: If True then print stdout
    :return: Boolean
    """
    result = True
    if filepath is not None:
        print('Converting: ' + filepath)
        try:
            process = subprocess.Popen(convertExecutable + " -loglevel panic -y -i " + filepath +
                                       " -metadata title="" -c:v copy -ac 2 -movflags +faststart "
                                       + filepath[:-3] + "mp4", shell=True)
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
