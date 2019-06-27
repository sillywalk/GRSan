#as: -32 -EB
#objdump: -dr --prefix-addresses -Mgpr-names=numeric
#name: ULH with relocation operators

.*file format.*

Disassembly of section \.text:
[0-9a-f]+ <[^>]*> lb	\$1,0\(\$4\)
[0-9a-f]+ <[^>]*> lbu	\$4,1\(\$4\)
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> lb	\$1,32766\(\$4\)
[0-9a-f]+ <[^>]*> lbu	\$4,32767\(\$4\)
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$4,32767
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> li	\$1,0x8000
[0-9a-f]+ <[^>]*> addu	\$1,\$1,\$4
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
#--------------------------------------------------------------------
[0-9a-f]+ <[^>]*> lb	\$1,0\(\$5\)
[0-9a-f]+ <[^>]*> lbu	\$4,1\(\$5\)
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> lb	\$1,32766\(\$5\)
[0-9a-f]+ <[^>]*> lbu	\$4,32767\(\$5\)
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,32767
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> li	\$1,0x8000
[0-9a-f]+ <[^>]*> addu	\$1,\$1,\$5
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
# Would be more efficient to apply the offset to the base register.
[0-9a-f]+ <[^>]*> lui	\$1,0x3
[0-9a-f]+ <[^>]*> ori	\$1,\$1,0x7ffe
[0-9a-f]+ <[^>]*> addu	\$1,\$1,\$5
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
# This one must use LUI/ORI
[0-9a-f]+ <[^>]*> lui	\$1,0x3
[0-9a-f]+ <[^>]*> ori	\$1,\$1,0x7fff
[0-9a-f]+ <[^>]*> addu	\$1,\$1,\$5
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
# Would be more efficient to apply the offset to the base register.
[0-9a-f]+ <[^>]*> lui	\$1,0x3
[0-9a-f]+ <[^>]*> ori	\$1,\$1,0x8000
[0-9a-f]+ <[^>]*> addu	\$1,\$1,\$5
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
#--------------------------------------------------------------------
[0-9a-f]+ <[^>]*> li	\$1,0
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_LO16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> li	\$1,0
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_HI16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> lb	\$1,0\(\$0\)
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_GPREL16	foo
[0-9a-f]+ <[^>]*> lbu	\$4,1\(\$0\)
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_GPREL16	foo
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> li	\$1,-30875
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> li	\$1,4661
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
#--------------------------------------------------------------------
[0-9a-f]+ <[^>]*> addiu	\$1,\$4,0
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_LO16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$4,0
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_HI16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> lb	\$1,0\(\$4\)
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_GPREL16	foo
[0-9a-f]+ <[^>]*> lbu	\$4,1\(\$4\)
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_GPREL16	foo
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
#--------------------------------------------------------------------
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,0
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_LO16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,0
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_HI16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> lb	\$1,0\(\$5\)
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_GPREL16	foo
[0-9a-f]+ <[^>]*> lbu	\$4,1\(\$5\)
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_GPREL16	foo
[0-9a-f]+ <[^>]*> sll	\$1,\$1,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,-30875
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,4661
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,-30875
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_LO16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
[0-9a-f]+ <[^>]*> addiu	\$1,\$5,4661
[ 	]*[0-9a-f]+: R_(MICRO|)MIPS_HI16	foo
[0-9a-f]+ <[^>]*> lb	\$4,0\(\$1\)
[0-9a-f]+ <[^>]*> lbu	\$1,1\(\$1\)
[0-9a-f]+ <[^>]*> sll	\$4,\$4,0x8
[0-9a-f]+ <[^>]*> or	\$4,\$4,\$1
#pass