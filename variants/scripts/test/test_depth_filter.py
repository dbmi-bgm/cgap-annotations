#################################################################
#   Libraries
#################################################################
import sys, os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from depth_filter import (
                            main as main_depth_filter
                           )

#################################################################
#   Tests
#################################################################

def test_depth_filter_proband_only():
    # Variables
    args = {'inputSampleVCF': 'test/files/depth_test_file_proband.vcf', 'outputfile': 'proband3.vcf', 'min_depth': '3'}
    # Run
    main_depth_filter(args)
    # Tests
    assert [row for row in open('proband3.vcf')] == [row for row in open('test/files/depth_test_file_proband_3.vcf')]
    # Clean
    os.remove('proband3.vcf')

def test_depth_filter_trio():
    # Variables
    args = {'inputSampleVCF': 'test/files/depth_test_file_trio.vcf', 'outputfile': 'trio3.vcf', 'min_depth': '3'}
    # Run
    main_depth_filter(args)
    # Tests
    assert [row for row in open('trio3.vcf')] == [row for row in open('test/files/depth_test_file_trio_3.vcf')]
    # Clean
    os.remove('trio3.vcf')
