# -*- coding: utf-8 -*-

"""
Isobaric melting enthalpy and isobaric evaporation enthalpy.

Functions:
----------

  latentheat_evap_t(SA, t)
      latent heat, or enthalpy, of evaporation at p = 0

This is part of the python Gibbs Sea Water library
http://code.google.com/p/python-seawater/

"""

from __future__ import division

import numpy as np

#from seawater.constants import SSO, cp0, Kelvin, sfac, db2Pascal, gamma, P0, M_S
#from library import entropy_part, gibbs, gibbs_pt0_pt0
from utilities import match_args_return
from conversions import CT_from_pt


__all__ = [
           'latentheat_melting',
           'latentheat_evap_CT',
           'latentheat_evap_t'
          ]


@match_args_return
def latentheat_evap_t(SA, t):
    r"""
    Calculates latent heat, or enthalpy, of evaporation at p = 0 (the surface).
    It is defined as a function of Absolute Salinity, SA, and in-situ
    temperature, t, and is valid in the ranges 0 < SA < 40 g/kg and 0 < CT <
    42 deg C. The errors range between -0.4 and 0.6 J/kg.

    Parameters
    ----------
    ----------
    SA : array_like
         Absolute salinity [g kg :sup:`-1`]
    t : array_like
        in situ temperature [:math:`^\circ` C (ITS-90)]

    Returns
    -------
    latentheat_evap_t : array_like
        latent heat of evaporation [J kg :sup:`-1`]

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    Examples
    --------
    TODO

    References
    ----------
    .. [1] IOC, SCOR and IAPSO, 2010: The international thermodynamic equation
    of seawater - 2010: Calculation and use of thermodynamic properties.
    Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
    UNESCO (English), 196 pp.
    See section 3.39.

    Modifications:
    2011-03-29. Paul Barker, Trevor McDougall & Rainer Feistel
    """

    CT = CT_from_pt(SA, t)

    latentheat_evap_t = latentheat_evap_CT(SA, CT)

    return latentheat_evap_t