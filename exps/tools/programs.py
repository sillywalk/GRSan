import os, sys

# programs
ZLIB = 'zlib'
LIBJPEG = 'jpeg'
MUPDF = 'mupdf'
LIBXML = 'libxml'
READELF = 'readelf'
OBJDUMP = 'objdump'
STRIP = 'strip'

valid_programs = [ZLIB, LIBJPEG, MUPDF, LIBXML, READELF, OBJDUMP, STRIP]

# modes
GRAD = 'grad'
TAINT = 'taint'
BASE = 'base'


def get_cmd(program, mode, fname, byte_ind = None):

    if program == ZLIB:
        cmd = ['minigzip_'+mode, '-d', '-c']
    elif program == LIBJPEG:
        cmd = ['djpeg_'+mode]
    elif program == MUPDF:
        cmd = ['mutool_'+mode, 'show']
    elif program == LIBXML:
        cmd = ['xmllint_'+mode]
        if (os.path.splitext(fname)[1] in ['.htm', '.html']):
            cmd.append('--html')
    elif program == READELF:
        cmd = ['readelf_'+mode, '-a']
    elif program == OBJDUMP:
        cmd = ['objdump_'+mode, '-xD']
    elif program == STRIP:
        cmd = ['strip_'+mode, '-o', '/dev/null']

    if mode in [GRAD, TAINT] and byte_ind is not None:
        if program in [OBJDUMP, READELF]:
            cmd += ['-k', str(byte_ind)]
        else:
            cmd += ['-m', str(byte_ind)]

    cmd.append(fname)

    return cmd
    
