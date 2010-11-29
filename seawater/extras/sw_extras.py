# -*- coding: utf-8 -*-

"""
Extra seawater functions
===========================
"""

import numpy as np
import seawater.csiro as sw

def sigma_t(s, t, p):
    """
    :math:`\\sigma_{t}` is the remainder of subtracting 1000 kg m :sup:`-3` from the density of a sea water sample at atmospheric pressure.

    Parameters
    ----------
    s(p) : array_like
           salinity [psu (PSS-78)]
    t(p) : array_like
           temperature [:math:`^\\circ` C (ITS-90)]
    p : array_like
        pressure [db]. The shape can be "broadcasted"

    Returns
    -------
    sgmt : array_like
           density  [kg m :sup:`3`]

    See Also
    --------
    dens, sigmatheta

    Notes
    -----
    Density of Sea Water using UNESCO 1983 (EOS 80) polynomial.

    Examples
    --------
    Data from Unesco Tech. Paper in Marine Sci. No. 44, p22

    >>> import seawater.csiro as sw
    >>> import seawater.extras.sw_extras as swe
    >>> s = [0, 0, 0, 0, 35, 35, 35, 35]
    >>> t = sw.T90conv([0, 0, 30, 30, 0, 0, 30, 30])
    >>> p = [0, 10000, 0, 10000, 0, 10000, 0, 10000]
    >>> swe.sigma_t(s, t, p)
    array([ -0.157406  ,  45.33710972,  -4.34886626,  36.03148891,
            28.10633141,  70.95838408,  21.72863949,  60.55058771])

    References
    ----------
    .. [1] Fofonoff, P. and Millard, R.C. Jr UNESCO 1983. Algorithms for computation of fundamental properties of seawater. UNESCO Tech. Pap. in Mar. Sci., No. 44, 53 pp.  Eqn.(31) p.39. http://www.scor-int.org/Publications.htm

    .. [2] Millero, F.J., Chen, C.T., Bradshaw, A., and Schleicher, K. A new high pressure equation of state for seawater. Deap-Sea Research., 1980, Vol27A, pp255-264. doi:10.1016/0198-0149(80)90016-3

    Modifications: Filipe Fernandes, 2010
                   10-01-26. Filipe Fernandes, first version.
    """
    # Convert input to numpy arrays
    s = np.asarray(s); t = np.asarray(t); p = np.asarray(p)

    sgmt = sw.dens(s, t, p) - 1000.0
    return sgmt

def sigmatheta(s, t, p, pr=0):
    """
    :math:`\\sigma_{\\theta}` is a measure of the density of ocean water where the quantity :math:`\\sigma_{t}` is calculated using the potential temperature (:math:`\\theta`) rather than the in situ temperature and potential density of water mass relative to the specified reference pressure.

    Parameters
    ----------
    s(p) : array_like
           salinity [psu (PSS-78)]
    t(p) : array_like
           temperature [:math:`^\\circ` C (ITS-90)]
    p : array_like
        pressure [db]. The shape can be "broadcasted"
    pr : number
         reference pressure [db], default = 0

    Returns
    -------
    sgmte : array_like
           density  [kg m :sup:`3`]

    See Also
    --------
    dens, sigma_t

    Notes
    -----
    Density of Sea Water using UNESCO 1983 (EOS 80) polynomial.

    Examples
    --------
    Data from Unesco Tech. Paper in Marine Sci. No. 44, p22

    >>> import seawater.extras.sw_extras as swe
    >>> import seawater.csiro as sw
    >>> s = [0, 0, 0, 0, 35, 35, 35, 35]
    >>> t = sw.T90conv([0, 0, 30, 30, 0, 0, 30, 30])
    >>> p = [0, 10000, 0, 10000, 0, 10000, 0, 10000]
    >>> swe.sigmatheta(s, t, p)
    array([ -0.157406  ,  -0.20476006,  -4.34886626,  -3.63884068,
            28.10633141,  28.15738545,  21.72863949,  22.59634627])

    References
    ----------
    .. [1] Fofonoff, P. and Millard, R.C. Jr UNESCO 1983. Algorithms for computation of fundamental properties of seawater. UNESCO Tech. Pap. in Mar. Sci., No. 44, 53 pp.  Eqn.(31) p.39. http://www.scor-int.org/Publications.htm

    .. [2] Millero, F.J., Chen, C.T., Bradshaw, A., and Schleicher, K. A new high pressure equation of state for seawater. Deap-Sea Research., 1980, Vol27A, pp255-264. doi:10.1016/0198-0149(80)90016-3

    Modifications: Filipe Fernandes, 2010
                   10-01-26. Filipe Fernandes, first version.
    """
    # Convert input to numpy arrays
    s = np.asarray(s); t = np.asarray(t); p = np.asarray(p)
    pr = np.asarray(pr)

    sgmte = sw.pden(s, t, p, pr) - 1000.0
    return sgmte

def N(bvfr2):
    """
    Buoyancy frequency is the frequency with which a parcel or particle of fluid displaced a small vertical distance from its equilibrium position in a stable environment will oscillate. It will oscillate in simple harmonic motion with an angular frequency defined by

    .. math:: N = \\left(\\frac{-g}{\\sigma_{\\theta}} \\frac{d\\sigma_{\\theta}}{dz}\\right)^{2}

    Parameters
    ----------
    n2 : array_like
         Brünt-Väisälä Frequency squared [s :sup:`-2`]

    Returns
    -------
    n : array_like
        Brünt-Väisälä Frequency not-squared [s :sup:`-1`]

    Examples
    --------
    >>> import numpy as np
    >>> import seawater.extras.sw_extras as swe
    >>> s = np.array([[0, 0, 0], [15, 15, 15], [30, 30, 30],[35,35,35]])
    >>> t = np.repeat(15, s.size).reshape(s.shape)
    >>> p = [0, 250, 500, 1000]
    >>> lat = [30,32,35]
    >>> swe.N(sw.bfrq(s, t, p, lat)[0])
    array([[ 0.02124956,  0.02125302,  0.02125843],
           [ 0.02110919,  0.02111263,  0.02111801],
           [ 0.00860812,  0.00860952,  0.00861171]])

    References
    ----------
    .. [1] A.E. Gill 1982. p.54  eqn 3.7.15 "Atmosphere-Ocean Dynamics" Academic Press: New York. ISBN: 0-12-283522-0

    .. [2] Jackett, David R., Trevor J. Mcdougall, 1995: Minimal Adjustment of Hydrographic Profiles to Achieve Static Stability. J. Atmos. Oceanic Technol., 12, 381-389. doi: 10.1175/1520-0426(1995)012<0381:MAOHPT>2.0.CO;2

    Modifications: Filipe Fernandes, 2010
                   10-01-26. Filipe Fernandes, first version.
    """

    # Convert input to numpy arrays
    bvfr2 = np.asarray(bvfr2)

    bvfr  = np.sqrt( np.abs( bvfr2 ) ) * np.sign( bvfr2 )
    return bvfr

def shear(p, u, v=0):
    """
    Calculates the vertical shear for u, v velocity section.

    .. math::
        \\textrm{shear} = \\frac{\\partial (u^2 + v^2)^{0.5}}{\partial z}

    Parameters
    ----------
    p : array_like
        pressure [db]. The shape can be "broadcasted"
    u(p) : array_like
           Eastward velocity [m s :sup:`-1`]
    v(p) : array_like
           Northward velocity [m s :sup:`-1`]

    Returns
    -------
    shr : array_like
          frequency [s :sup:`-1`]
    p_ave : array_like
            mid pressure between p grid (M-1xN)  [db]

    See Also
    --------
    TODO

    Notes
    -----
    TODO check where depth increases to find dimension

    Examples
    --------
    >>> import seawater.extras.sw_extras as swe
    >>> p = [0, 250, 500, 1000]
    >>> vel = [[0.5, 0.5, 0.5], [0.15, 0.15, 0.15], [0.03, 0.03, .03],[0.,0.,0.]]
    >>> swe.shear(p, vel)[0]
    array([[ -1.40000000e-03,  -1.40000000e-03,  -1.40000000e-03],
           [ -4.80000000e-04,  -4.80000000e-04,  -4.80000000e-04],
           [ -6.00000000e-05,  -6.00000000e-05,  -6.00000000e-05]])

    AUTHOR:  Filipe Fernandes, 2010

    MODIFICATIONS:
    10-01-28. Filipe Fernandes, first version.
    """
    # Convert input to numpy arrays
    p = np.asarray(p); u = np.asarray(u); v = np.asarray(v)

    # if pressure is a vector make it a array of the same size as t/s
    if p.ndim == 1:
        p = np.repeat(p[np.newaxis,:], u.shape[1], axis=1).reshape(u.shape)

    m,n      = p.shape
    iup      = np.arange(0,m-1)
    ilo      = np.arange(1,m)
    p_ave    = ( p[iup,:] + p[ilo,:] )/2.
    vel      = np.sqrt( u**2 + v**2 )
    diff_vel = np.diff( vel, axis=0 )
    diff_z   = np.diff(   p, axis=0 ) # TODO to Z ?
    shr      = diff_vel / diff_z

    return shr, p_ave

def richnumb(n, s):
    """
    Calculates  the ratio of buoyancy to inertial forces which measures the stability of a fluid layer.
    this functions computes the gradient Richardson number in the form of:

    .. math::
        Ri = \\frac{N^2}{S^2}

    Representing a dimensionless number that expresses the ratio of the energy extracted by buoyancy forces to the energy gained from the shear of the large-scale velocity field.

    Parameters
    ----------
    n : array_like
        Brünt-Väisälä [s :sup:`-1`]
    shr : array_like
          shear [s :sup:`-1`]

    Returns
    -------
    ri : array_like
         non-dimensional

    Examples
    --------
    TODO: check the example and add real values

    >>> import numpy as np
    >>> import seawater.extras.sw_extras as swe
    >>> import seawater.csiro as sw
    >>> s   = np.array([[0, 0, 0], [15, 15, 15], [30, 30, 30],[35,35,35]])
    >>> t   = np.repeat(15, s.size).reshape(s.shape)
    >>> p   = [0, 250, 500, 1000]
    >>> lat = [30, 32, 35]
    >>> n   = swe.N(sw.bfrq(s, t, p, lat)[0])
    >>> vel = [[0.5, 0.5, 0.5], [0.15, 0.15, 0.15], [0.03, 0.03, .03],[0.,0.,0.]]
    >>> s   = swe.shear(p, vel)[0]
    >>> swe.richnumb(n, s)
    array([[   230.37941215,    230.45444299,    230.57181258],
           [  1934.01949759,   1934.64933431,   1935.63457818],
           [ 20583.24410868,  20589.94661835,  20600.43125069]])

    Modifications: Filipe Fernandes, 2010
                   10-01-26. Filipe Fernandes, first version.
    """
    # Convert input to numpy arrays
    n = np.asarray(n); s = np.asarray(s)

    n2 = n**2 * np.sign(n)
    s2 = s**2
    ri = n2 / s2
    return ri

def cor_beta(lat):
    """
    Calculates the Coriolis :math:`\\beta` factor defined by:

    .. math::
        beta = 2 \\Omega \\cos(lat)

    where:

    .. math::
        \\Omega = \\frac{2 \\pi}{\\textrm{sidereal day}} = 7.292e^{-5} \\textrm{ radians sec}^{-1}

    Parameters
    ----------
    lat : array_like
          latitude in decimal degrees north [-90..+90].

    Returns
    -------
    beta : array_like
        Beta Coriolis [s :sup:`-1`]

    See Also
    --------
    sw.cor

    Notes
    -----
    TODO

    Examples
    --------
    >>> import seawater.extras.sw_extras as swe
    >>> swe.cor_beta(0)
    2.2891586878041123e-11

    References
    ----------
    .. [1] S. Pond & G.Pickard 2nd Edition 1986 Introductory Dynamical Oceanogrpahy Pergamon Press Sydney. ISBN 0-08-028728-X

    .. [2] A.E. Gill 1982. p.54  eqn 3.7.15 "Atmosphere-Ocean Dynamics" Academic Press: New York. ISBN: 0-12-283522-0
    """

    # Convert input to numpy arrays
    lat = np.asarray(lat)

    beta = 2 * sw.OMEGA * np.cos(lat)/ sw.a

    return beta

def inertial_period(lat):
    """
    Calculate the inertial period as:

    .. math::
        Ti = \\frac{2\\pi}{f} = \\frac{T_{sd}}{2\\sin\\phi}

    Parameters
    ----------
    lat : array_like
          latitude in decimal degress north [-90..+90]

    Returns
    -------
    Ti : array_like
         period in seconds

    Examples
    --------
    >>> import seawater.extras.sw_extras as swe
    >>> lat = 30
    >>> swe.inertial_period(lat)/3600
    23.934472399219292

    Modifications: Filipe Fernandes, 2010
                   10-01-26. Filipe Fernandes, first version.
    """
    # Convert input to numpy arrays
    lat = np.asarray(lat)

    Ti = 2 * np.pi / sw.cor(lat)

    return Ti

def strat_period(N):
    """
    Stratifitcation period is the inverse of the Bouyancy frequency, defined by

    .. math:: Tn = \\frac{2\\pi}{N}

    Parameters
    ----------
    N : array_like
         Brünt-Väisälä Frequency [s :sup:`-1`]

    Returns
    -------
    Tn : array_like
        Brünt-Väisälä Period [s]

    Examples
    --------
    >>> import numpy as np
    >>> import seawater.csiro as sw
    >>> import seawater.extras.sw_extras as swe
    >>> s = np.array([[0, 0, 0], [15, 15, 15], [30, 30, 30],[35,35,35]])
    >>> t = np.repeat(15, s.size).reshape(s.shape)
    >>> p = [0, 250, 500, 1000]
    >>> lat = [30,32,35]
    >>> swe.strat_period( swe.N( sw.bfrq(s, t, p, lat)[0] ) )
    array([[ 295.68548089,  295.63734267,  295.56208791],
           [ 297.6515901 ,  297.60313502,  297.52738493],
           [ 729.91402019,  729.79520847,  729.60946944]])

    References
    ----------
    .. [1] TODO: Pickard

    Modifications: Filipe Fernandes, 2010
                   10-10-06. Filipe Fernandes, first version.
    """
    # Convert input to numpy arrays
    N = np.asarray(N)

    Tn = 2 * np.pi / N
    return Tn

def visc(s, t, p):
    """
    Calculates kinematic viscosity of sea-water.

    Parameters
    ----------
    s(p) : array_like
           salinity [psu (PSS-78)]
    t(p) : array_like
           temperature [:math:`^\\circ` C (ITS-90)]
    p : array_like
        pressure [db]. The shape can be "broadcasted"

    Returns
    -------
    visw : array_like
           [m :sup: `2` s :sup: `-1`]

    See Also
    --------
    visc_air from airsea toolbox

    Notes
    -----
    From matlab airsea

    Examples
    --------
    >>> import seawater.extras.sw_extras as swe
    >>> swe.visc(40, 40, 1000)
    8.2001924966338036e-07

    References
    ----------
    .. [1] Dan Kelley's fit to Knauss's TABLE II-8.
    """
    # Convert input to numpy arrays
    s = np.asarray(s); t = np.asarray(t); p = np.asarray(p)

    viscw = 1e-4 * (17.91 - 0.5381 * t + 0.00694 * t**2 + 0.02305*s ) / sw.dens(s, t, p);
    return viscw

def tcond(s, t, p):
    """
    Calculates thermal conductivity of sea-water.

    Parameters
    ----------
    s(p) : array_like
           salinity [psu (PSS-78)]
    t(p) : array_like
           temperature [:math:`^\\circ` C (ITS-90)]
    p : array_like
        pressure [db]. The shape can be "broadcasted"

    Returns
    -------
    therm : array_like
           thermal conductivity [W m :sup: `-1` K :sup: `-1`]

    See Also
    --------
    TODO

    Notes
    -----
    From matlab airsea

    Examples
    --------
    >>> import seawater.extras.sw_extras as swe
    >>> swe.tcond(35, 20, 0)
    0.5972445569999999

    References
    ----------
    .. [1] Caldwell's DSR 21:131-137 (1974)  eq. 9
    .. [2] Catelli et al.'s DSR 21:311-3179(1974)  eq. 5
    """

    """
    Castelli's option
    tcond = 100*(5.5286e-3+3.4025e-8*P+1.8364e-5*T-3.3058e-9*T.^3); # [W/m/K]
    tcond = tcond # [W/m/K]
    """

    # Convert input to numpy arrays
    s = np.asarray(s); t = np.asarray(t); p = np.asarray(p)

    # 1) Caldwell's option # 2 - simplified formula, accurate to 0.5% (eqn. 9) in [cal/cm/C/sec]
    therm = 0.001365 * ( 1 + 0.003 * t - 1.025e-5 * t ** 2 + 0.0653 * ( 1e-4 * p ) - 0.00029 * s )
    therm = therm * 418.4 # [cal/cm/C/sec] ->[W/m/K]
    return therm

def mlife():
    """
    >>> import seawater.extras.sw_extras as swe
    >>> swe.mlife()
    42
    """
    print 42