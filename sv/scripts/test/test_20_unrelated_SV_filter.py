
#################################################################
#   Libraries
#################################################################
import sys, os
import pytest

overlap = __import__('20_unrelated_SV_filter')

#################################################################
#   Tests
#################################################################


def test_recip():
    assert overlap.recip_overlap([0,100],[0,100]) == 1.0
    assert overlap.recip_overlap([0,80],[0,100]) == 0.8
    assert overlap.recip_overlap([0,20],[20,100]) == 0
    assert overlap.recip_overlap([0,100],[1000,1100]) == 0
