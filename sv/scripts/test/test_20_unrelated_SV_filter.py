
#################################################################
#   Libraries
#################################################################
import sys, os
import pytest
import shutil
from subprocess import Popen

overlap = __import__('20_unrelated_SV_filter')

#################################################################
#   Tests
#################################################################


def test_recip():
    assert overlap.recip_overlap([0,100],[0,100]) == 1.0
    assert overlap.recip_overlap([0,80],[0,100]) == 0.8
    assert overlap.recip_overlap([0,20],[20,100]) == 0
    assert overlap.recip_overlap([0,100],[1000,1100]) == 0

#################################################################
#            Description of files in same_file.tar
# We only need 2 fabricated "unrelated" files for testing
# GAPFI1PXGJFI_chr1.vcf.gz (input) has been copied 2x to make:
# GAPFI1PXGJFI_chr1_unrelated_1.vcf.gz and _unrelated_2.vcf.gz
# these were placed in same_file.tar
#################################################################


def test_same_file():
    shutil.copyfile('test/files/same_file.tar', 'same_file.tar')
    args = {'inputSampleVCF': 'test/files/GAPFI1PXGJFI_chr1.vcf.gz', 'max_unrelated': '1', 'outputfile':'output.vcf', 'wiggle': '50', 'recip': '0.8', 'dirPath20vcf': 'same_file.tar', 'SVtypes': '[DEL, DUP]'}
    overlap.match(args)
    overlap.filter(args)
    a = os.popen('bgzip -c -d output.vcf.gz')
    b = os.popen('bgzip -c -d test/files/GAPFIAFHF16S_header_only.vcf.gz')
    assert [row for row in a.read()] == [row for row in b.read()]

    os.remove('output.vcf.gz')
    os.remove('output.vcf.gz.tbi')
    os.remove('matched_GAPFI1PXGJFI_chr1_unrelated_1.vcf')
    os.remove('matched_GAPFI1PXGJFI_chr1_unrelated_2.vcf')
    os.remove('same_file.tar')
    shutil.rmtree('unrelated')
