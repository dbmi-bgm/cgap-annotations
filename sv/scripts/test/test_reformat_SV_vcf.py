
#################################################################
#   Libraries
#################################################################
import sys, os
import pytest

from reformat_SV_vcf import (
                            main as main_reformat_SV_vcf
                           )


#################################################################
#   Tests
#################################################################

def test_full_process():
    # Variables and Run
    args = {'inputVCF': 'test/files/parliament2_test_out.vcf.gz', 'inputContig': 'test/files/input_contig.txt','outputfile':'output.vcf'}
    # Test
    main_reformat_SV_vcf(args)
    a = os.popen('bgzip -c -d output.vcf.gz')
    b = os.popen('bgzip -c -d test/files/reformatted_reference.vcf.gz')

    assert [row for row in a.read()] == [row for row in b.read()]

    # Clean
    os.remove('output.vcf.gz')
