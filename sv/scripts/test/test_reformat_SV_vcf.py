
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
    args = {'inputVCF': 'test/files/parliament2_test_out.vcf', 'inputContig': 'test/files/input_contig.txt','outputfile':'output.vcf'}
    # Test
    main_reformat_SV_vcf(args)
    assert [row for row in open('output.vcf')] == [row for row in open('test/files/reformatted_reference.vcf')]

    # Clean
    os.remove('output.vcf')
