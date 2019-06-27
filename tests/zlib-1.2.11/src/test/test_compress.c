/* example.c -- usage example of the zlib compression library
 * Copyright (C) 1995-2006, 2011, 2016 Jean-loup Gailly
 * For conditions of distribution and use, see copyright notice in zlib.h
 */

/* @(#) $Id$ */

#include <sanitizer/dfsan_interface.h>

#include "zlib.h"
#include <stdio.h>

#ifdef STDC
#  include <string.h>
#  include <stdlib.h>
#endif

#if defined(VMS) || defined(RISCOS)
#  define TESTFILE "foo-gz"
#else
#  define TESTFILE "foo.gz"
#endif

#define CHECK_ERR(err, msg) { \
    if (err != Z_OK) { \
        fprintf(stderr, "%s error: %d\n", msg, err); \
        exit(1); \
    } \
}

static z_const char hello[] = "hello, hello!";
/* "hello world" would be more standard, but the repeated "hello"
 * stresses the compression code better, sorry...
 */

static const char dictionary[] = "hello";
static uLong dictId;    /* Adler32 value of the dictionary */

/*void test_deflate       OF((Byte *compr, uLong comprLen));*/
/*void test_inflate       OF((Byte *compr, uLong comprLen,*/
                            /*Byte *uncompr, uLong uncomprLen));*/
/*void test_large_deflate OF((Byte *compr, uLong comprLen,*/
                            /*Byte *uncompr, uLong uncomprLen));*/
/*void test_large_inflate OF((Byte *compr, uLong comprLen,*/
                            /*Byte *uncompr, uLong uncomprLen));*/
/*void test_flush         OF((Byte *compr, uLong *comprLen));*/
/*void test_sync          OF((Byte *compr, uLong comprLen,*/
                            /*Byte *uncompr, uLong uncomprLen));*/
/*void test_dict_deflate  OF((Byte *compr, uLong comprLen));*/
/*void test_dict_inflate  OF((Byte *compr, uLong comprLen,*/
                            /*Byte *uncompr, uLong uncomprLen));*/
int  main               OF((int argc, char *argv[]));


/*#ifdef Z_SOLO*/

/*void *myalloc OF((void *, unsigned, unsigned));*/
/*void myfree OF((void *, void *));*/

/*void *myalloc(q, n, m)*/
    /*void *q;*/
    /*unsigned n, m;*/
/*{*/
    /*(void)q;*/
    /*return calloc(n, m);*/
/*}*/

/*void myfree(void *q, void *p)*/
/*{*/
    /*(void)q;*/
    /*free(p);*/
/*}*/

/*static alloc_func zalloc = myalloc;*/
/*static free_func zfree = myfree;*/

/*#else [> !Z_SOLO <]*/

/*static alloc_func zalloc = (alloc_func)0;*/
/*static free_func zfree = (free_func)0;*/

void test_compress      OF((Byte *compr, uLong comprLen,
                            Byte *uncompr, uLong uncomprLen));
/*void test_gzio          OF((const char *fname,*/
                            /*Byte *uncompr, uLong uncomprLen));*/

/* ===========================================================================
 * Test compress() and uncompress()
 */
void test_compress(compr, comprLen, uncompr, uncomprLen)
    Byte *compr, *uncompr;
    uLong comprLen, uncomprLen;
{
    int err;
    uLong len = (uLong)strlen(hello)+1;

    err = compress(compr, &comprLen, (const Bytef*)hello, len);
    CHECK_ERR(err, "compress");

#ifdef GRSAN
    /*for (size_t i=0; i<comprLen; i++) {*/
      /*dfsan_label l = dfsan_get_label(compr[i]);*/
      /*struct dfsan_label_info* li;*/
      /*if (l) {*/
        /*li = dfsan_get_label_info(l);*/
        /*[>printf("%zu: %u lbl %u ps %u %u dx %f %f\n",<]*/
            /*[>i, compr[i], l, li->l1, li->l2, li->neg_dydx, li->pos_dydx);<]*/
        /*printf("out, %u, %u, %f, %f\n", compr[i],*/
                /*li, li->neg_dydx, li->pos_dydx);*/

      /*} else {*/
        /*printf("out, %u, %u, 0.0, 0.0 \n", compr[i], li);*/
      /*}*/
    /*}*/
#endif

    /*strcpy((char*)uncompr, "garbage");*/

    /*err = uncompress(uncompr, &uncomprLen, compr, comprLen);*/
    /*CHECK_ERR(err, "uncompress");*/

    /*if (strcmp((char*)uncompr, hello)) {*/
        /*fprintf(stderr, "bad uncompress\n");*/
        /*exit(1);*/
    /*} else {*/
        /*printf("uncompress(): %s\n", (char *)uncompr);*/
    /*}*/
}

int main(argc, argv)
    int argc;
    char *argv[];
{
    Byte *compr, *uncompr;
    uLong comprLen = 10000*sizeof(int); /* don't overflow on MSDOS */
    uLong uncomprLen = comprLen;
    static const char* myVersion = ZLIB_VERSION;

    size_t ind = 0;
    if (argc > 1) {
      ind = atoi(argv[1]);
    }

    char diff = 0;
    if (argc > 2) {
      diff = atoi(argv[2]);
    }

    /*printf("input %u %u\n", ind, diff);*/

    float initial = 1.0;
    /*dfsan_label i_label = dfsan_create_label("comprLen", initial);*/
    /*dfsan_set_label(i_label, &comprLen, sizeof(comprLen));*/

    hello[ind] += diff;

#ifdef GRSAN
    dfsan_label i_label = dfsan_create_label("hello", initial);
    dfsan_set_label(i_label, &hello[ind], sizeof(hello[ind]));
#endif
 
    /*if (zlibVersion()[0] != myVersion[0]) {*/
        /*fprintf(stderr, "incompatible zlib version\n");*/
        /*exit(1);*/

    /*} else if (strcmp(zlibVersion(), ZLIB_VERSION) != 0) {*/
        /*fprintf(stderr, "warning: different zlib version\n");*/
    /*}*/

    /*printf("zlib version %s = 0x%04x, compile flags = 0x%lx\n",*/
            /*ZLIB_VERSION, ZLIB_VERNUM, zlibCompileFlags());*/

    compr    = (Byte*)calloc((uInt)comprLen, 1);
    uncompr  = (Byte*)calloc((uInt)uncomprLen, 1);
    /* compr and uncompr are cleared to avoid reading uninitialized
     * data and to ensure that uncompr compresses well.
     */
    if (compr == Z_NULL || uncompr == Z_NULL) {
        printf("out of memory\n");
        exit(1);
    }

/*#ifdef Z_SOLO*/
    /*(void)argc;*/
    /*(void)argv;*/
/*#else*/
    test_compress(compr, comprLen, uncompr, uncomprLen);

    /*test_gzio((argc > 1 ? argv[1] : TESTFILE),*/
              /*uncompr, uncomprLen);*/
/*#endif*/

    /*printf("len size: %d", sizeof(comprLen));*/

    /*test_deflate(compr, comprLen);*/
    /*test_inflate(compr, comprLen, uncompr, uncomprLen);*/

    /*test_large_deflate(compr, comprLen, uncompr, uncomprLen);*/
    /*test_large_inflate(compr, comprLen, uncompr, uncomprLen);*/

    /*test_flush(compr, &comprLen);*/
    /*test_sync(compr, comprLen, uncompr, uncomprLen);*/
    /*comprLen = uncomprLen;*/

    /*test_dict_deflate(compr, comprLen);*/
    /*test_dict_inflate(compr, comprLen, uncompr, uncomprLen);*/

    free(compr);
    free(uncompr);

    return 0;
}
