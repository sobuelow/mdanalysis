# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8
#
# MDAnalysis --- https://www.mdanalysis.org
# Copyright (c) 2006-2017 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler,
# D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein.
# MDAnalysis: A Python package for the rapid analysis of molecular dynamics
# simulations. In S. Benthall and S. Rostrup editors, Proceedings of the 15th
# Python in Science Conference, pages 102-109, Austin, TX, 2016. SciPy.
#
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#
from __future__ import print_function, absolute_import
import MDAnalysis
import MDAnalysis.analysis.waterdynamics
import pytest

from MDAnalysisTests.datafiles import waterPSF, waterDCD
from numpy.testing import assert_almost_equal

SELECTION1 = "byres name OH2"
SELECTION2 = "byres name P1"


@pytest.fixture(scope='module')
def universe():
    return MDAnalysis.Universe(waterPSF, waterDCD)


def test_HydrogenBondLifetimes(universe):
    hbl = MDAnalysis.analysis.waterdynamics.HydrogenBondLifetimes(universe,
                                                                  SELECTION1,
                                                                  SELECTION1,
                                                                  0, 5, 3)
    hbl.run()
    assert_almost_equal(hbl.timeseries[2][1], 0.75, 5)


def test_WaterOrientationalRelaxation(universe):
    wor = MDAnalysis.analysis.waterdynamics.WaterOrientationalRelaxation(
        universe,
        SELECTION1, 0, 5, 2)
    wor.run()
    assert round(wor.timeseries[1][2], 5) == 0.35887


def test_WaterOrientationalRelaxation_zeroMolecules(universe):
    wor_zero = MDAnalysis.analysis.waterdynamics.WaterOrientationalRelaxation(
        universe,
        SELECTION2, 0, 5, 2)
    wor_zero.run()
    assert wor_zero.timeseries[1] == (0.0, 0.0, 0.0)


def test_AngularDistribution(universe):
    ad = MDAnalysis.analysis.waterdynamics.AngularDistribution(universe,
                                                               SELECTION1,
                                                               40)
    ad.run()
    assert str(ad.graph[0][39]) == str("0.951172947884 0.48313682125")


def test_MeanSquareDisplacement(universe):
    msd = MDAnalysis.analysis.waterdynamics.MeanSquareDisplacement(universe,
                                                                   SELECTION1,
                                                                   0, 10, 2)
    msd.run()
    assert round(msd.timeseries[1], 5) == 0.03984


def test_MeanSquareDisplacement_zeroMolecules(universe):
    msd_zero = MDAnalysis.analysis.waterdynamics.MeanSquareDisplacement(
        universe,
        SELECTION2, 0, 10, 2)
    msd_zero.run()
    assert msd_zero.timeseries[1] == 0.0


def test_SurvivalProbability(universe):
    sp = MDAnalysis.analysis.waterdynamics.SurvivalProbability(universe,
                                                               SELECTION1,
                                                               0, 6, 3)
    sp.run()
    assert round(sp.timeseries[1], 5) == 1.0


def test_SurvivalProbability_zeroMolecules(universe):
    sp_zero = MDAnalysis.analysis.waterdynamics.SurvivalProbability(universe,
                                                                    SELECTION2,
                                                                    0, 6, 3)
    sp_zero.run()
    assert sp_zero.timeseries[1] == 0.0
