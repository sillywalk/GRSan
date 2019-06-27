

all: grsan dfsan base


grsan: jpeggrsan libxmlgrsan zlibgrsan binutilsgrsan mupdfgrsan

dfsan: jpegdfsan libxmldfsan zlibdfsan binutilsdfsan mupdfdfsan

fast: jpegfast libxmlfast zlibfast binutilsfast mupdffast

fuzz: jpegfuzz libxmlfuzz zlibfuzz binutilsfuzz mupdffuzz

bug: jpegbug libxmlbug zlibbug binutilsbug mupdfbug

base: jpegbase libxmlbase zlibbase binutilsbase mupdfbase


jpeggrsan: zlibgrsan
	$(MAKE) -C jpeg-9c grsan

libxmlgrsan:  zlibgrsan
	$(MAKE) -C libxml2-2.9.7 grsan

zlibgrsan:
	$(MAKE) -C zlib-1.2.11 grsan

binutilsgrsan:  zlibgrsan
	$(MAKE) -C binutils-2.30 grsan

mupdfgrsan: zlibgrsan
	$(MAKE) -C mupdf-1.14.0-source grsan


jpegdfsan: zlibdfsan
	$(MAKE) -C jpeg-9c dfsan

libxmldfsan:  zlibdfsan
	$(MAKE) -C libxml2-2.9.7 dfsan

zlibdfsan:
	$(MAKE) -C zlib-1.2.11 dfsan

binutilsdfsan:  zlibdfsan
	$(MAKE) -C binutils-2.30 dfsan

mupdfdfsan: zlibdfsan
	$(MAKE) -C mupdf-1.14.0-source dfsan


jpegfuzz: zlibfuzz
	$(MAKE) -C jpeg-9c fuzz

libxmlfuzz:  zlibfuzz
	$(MAKE) -C libxml2-2.9.7 fuzz

zlibfuzz:
	$(MAKE) -C zlib-1.2.11 fuzz

binutilsfuzz:  zlibfuzz
	$(MAKE) -C binutils-2.30 fuzz

mupdffuzz: zlibfuzz
	$(MAKE) -C mupdf-1.14.0-source fuzz


jpegfast: zlibfast
	$(MAKE) -C jpeg-9c fast

libxmlfast:  zlibfast
	$(MAKE) -C libxml2-2.9.7 fast

zlibfast:
	$(MAKE) -C zlib-1.2.11 fast

binutilsfast:  zlibfast
	$(MAKE) -C binutils-2.30 fast

mupdffast: zlibfast
	$(MAKE) -C mupdf-1.14.0-source fast


jpegbug: zlibbug
	$(MAKE) -C jpeg-9c bug

libxmlbug:  zlibbug
	$(MAKE) -C libxml2-2.9.7 bug

zlibbug:
	$(MAKE) -C zlib-1.2.11 bug

binutilsbug:  zlibbug
	$(MAKE) -C binutils-2.30 bug

mupdfbug: zlibbug
	$(MAKE) -C mupdf-1.14.0-source bug


jpegbase: zlibbase
	$(MAKE) -C jpeg-9c base

libxmlbase:  zlibbase
	$(MAKE) -C libxml2-2.9.7 base

zlibbase:
	$(MAKE) -C zlib-1.2.11 base

binutilsbase:  zlibbase
	$(MAKE) -C binutils-2.30 base

mupdfbase: zlibbase
	$(MAKE) -C mupdf-1.14.0-source base



clean:
	$(MAKE) -C jpeg-9c distclean
	$(MAKE) -C libxml2-2.9.7 distclean
	$(MAKE) -C zlib-1.2.11 distclean
	$(MAKE) -C binutils-2.30 distclean
	$(MAKE) -C mupdf-1.14.0-source distclean
