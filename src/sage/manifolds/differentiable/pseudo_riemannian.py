r"""
Pseudo-Riemannian Manifolds

A *pseudo-Riemannian manifold* is a pair `(M,g)` where `M` is a real
differentiable manifold `M` (see
:class:`~sage.manifolds.differentiable.manifold.DifferentiableManifold`)
and `g` is a field non-degenerate symmetric bilinear forms on `M`, which is
called the *metric tensor*, or simply the *metric* (see
:class:`~sage.manifolds.differentiable.metric.PseudoRiemannianMetric`).

Two important subcases are

- *Riemannian manifold*: the metric `g` is definite-positive
- *Lorentzian manifold*: the metric `g` has signature `n-2` (positive
  convention) or `2-n` (negative convention), where `n = \dim M`.

All pseudo-Riemannian manifolds are implemented via the class
:class:`PseudoRiemannianManifold`.

.. RUBRIC:: Example 1: the sphere as a Riemannian manifold of dimension 2

We start by declaring `S^2` as a 2-dimensional Riemannian manifold::

    sage: M = Manifold(2, 'S^2', structure='Riemannian')
    sage: M
    2-dimensional Riemannian manifold S^2

We then cover `S^2` by two stereographic charts, from the North pole and from
the South pole respectively::

    sage: U = M.open_subset('U')
    sage: stereoN.<x,y> = U.chart()
    sage: V = M.open_subset('V')
    sage: stereoS.<u,v> = V.chart()
    sage: M.declare_union(U,V)
    sage: stereoN_to_S = stereoN.transition_map(stereoS,
    ....:                [x/(x^2+y^2), y/(x^2+y^2)], intersection_name='W',
    ....:                restrictions1= x^2+y^2!=0, restrictions2= u^2+v^2!=0)
    sage: W = U.intersection(V)
    sage: stereoN_to_S
    Change of coordinates from Chart (W, (x, y)) to Chart (W, (u, v))
    sage: stereoN_to_S.display()
    u = x/(x^2 + y^2)
    v = y/(x^2 + y^2)
    sage: stereoN_to_S.inverse().display()
    x = u/(u^2 + v^2)
    y = v/(u^2 + v^2)

We get the metric defining the Riemannian structure by::

    sage: g = M.metric()
    sage: g
    Riemannian metric g on the 2-dimensional Riemannian manifold S^2

At this stage, the metric `g` is defined a Python object but there remains to
initialize it by setting its components with respect to the vector frames
associated with the stereographic coordinates. Let us begin with the frame
of chart ``stereoN``::

    sage: eU = stereoN.frame()
    sage: g[eU, 0, 0] = 4/(1 + x^2 + y^2)^2
    sage: g[eU, 1, 1] = 4/(1 + x^2 + y^2)^2

The metric components in the frame of chart ``stereoS`` are obtained by
continuation of the expressions found in `W = U\cap V` from the known
change-of-coordinate formulas::

    sage: eV = stereoS.frame()
    sage: g.add_comp_by_continuation(eV, W)

At this stage, the metric `g` is well defined in all `S^2`::

    sage: g.display(eU)
    g = 4/(x^2 + y^2 + 1)^2 dx*dx + 4/(x^2 + y^2 + 1)^2 dy*dy
    sage: g.display(eV)
    g = 4/(u^4 + v^4 + 2*(u^2 + 1)*v^2 + 2*u^2 + 1) du*du
     + 4/(u^4 + v^4 + 2*(u^2 + 1)*v^2 + 2*u^2 + 1) dv*dv

The expression in frame ``eV`` can be given a shape similar to that in frame
``eU``, by factorizing the components::

    sage: g[eV, 0, 0].factor()
    4/(u^2 + v^2 + 1)^2
    sage: g[eV, 1, 1].factor()
    4/(u^2 + v^2 + 1)^2
    sage: g.display(eV)
    g = 4/(u^2 + v^2 + 1)^2 du*du + 4/(u^2 + v^2 + 1)^2 dv*dv

Let us consider a scalar field `f` on `S^2`::

    sage: f = M.scalar_field({stereoN: 1/(1+x^2+y^2)}, name='f')
    sage: f.add_expr_by_continuation(stereoS, W)
    sage: f.display()
    f: S^2 --> R
    on U: (x, y) |--> 1/(x^2 + y^2 + 1)
    on V: (u, v) |--> (u^2 + v^2)/(u^2 + v^2 + 1)

The gradient of `f` (with respect to the metric `g`) is::

    sage: gradf = f.grad()
    sage: gradf
    Vector field grad(f) on the 2-dimensional Riemannian manifold S^2
    sage: gradf.display(eU)
    grad(f) = -1/2*x d/dx - 1/2*y d/dy
    sage: gradf.display(eV)
    grad(f) = 1/2*u d/du + 1/2*v d/dv

The Laplacian of `f`  (with respect to the metric `g`) is::

    sage: Df = f.laplacian()
    sage: Df
    Scalar field Delta(f) on the 2-dimensional Riemannian manifold S^2
    sage: Df.display()
    Delta(f): S^2 --> R
    on U: (x, y) |--> (x^2 + y^2 - 1)/(x^2 + y^2 + 1)
    on V: (u, v) |--> -(u^2 + v^2 - 1)/(u^2 + v^2 + 1)

Let us check the standard formula
`\Delta f = \mathrm{div}( \mathrm{grad}\,  f )`::

    sage: Df == f.grad().div()
    True

Since each open subset of `S^2` inherits the structure of a Riemannian
manifold, we can get the metric on it via the method ``metric()``::

    sage: gU = U.metric()
    sage: gU
    Riemannian metric g on the Open subset U of the 2-dimensional Riemannian
     manifold S^2
    sage: gU.display()
    g = 4/(x^2 + y^2 + 1)^2 dx*dx + 4/(x^2 + y^2 + 1)^2 dy*dy

On course, ``gU`` is nothing but the restriction of `g` to `U`::

    sage: gU is g.restrict(U)
    True

.. RUBRIC:: Example 2: Minkowski spacetime as a Lorentzian manifold of
  dimension 4

We start by declaring 4-dimensional Lorentzian manifold::

    sage: M = Manifold(4, 'M', structure='Lorentzian')
    sage: M
    4-dimensional Lorentzian manifold M

We define Minkowskian coordinates on ``M``::

    sage: X.<t,x,y,z> = M.chart()

We get the metric by::

    sage: g = M.metric()
    sage: g
    Lorentzian metric g on the 4-dimensional Lorentzian manifold M

and initialize it to the Minkowskian value::

    sage: g[0,0], g[1,1], g[2,2], g[3,3] = -1, 1, 1, 1
    sage: g.display()
    g = -dt*dt + dx*dx + dy*dy + dz*dz

We may check that the metric is flat, i.e. has a vanishing Riemann curvature
tensor::

    sage: g.riemann().display()
    Riem(g) = 0


AUTHORS:

- Eric Gourgoulhon (2018): initial version

REFERENCES:

- \B. O'Neill : *Semi-Riemannian Geometry* [ONe1983]_
- \J. M. Lee : *Riemannian Manifolds* [Lee1997]_

"""

#*****************************************************************************
#       Copyright (C) 2018 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.rings.infinity import infinity
from sage.rings.integer import Integer
from sage.manifolds.structure import (PseudoRiemannianStructure,
                                      RiemannianStructure, LorentzianStructure)
from sage.manifolds.differentiable.manifold import DifferentiableManifold
from sage.manifolds.differentiable.metric import PseudoRiemannianMetric
from sage.manifolds.differentiable.tensorfield import TensorField

###############################################################################

class PseudoRiemannianManifold(DifferentiableManifold):
    r"""
    PseudoRiemannian manifold.

    A *pseudo-Riemannian manifold* is a pair `(M,g)` where `M` is a real
    differentiable manifold `M` (see
    :class:`~sage.manifolds.differentiable.manifold.DifferentiableManifold`)
    and `g` is a field non-degenerate symmetric bilinear forms on `M`, which is
    called the *metric tensor*, or simply the *metric* (see
    :class:`~sage.manifolds.differentiable.metric.PseudoRiemannianMetric`).

    Two important subcases are

    - *Riemannian manifold*: the metric `g` is definite-positive
    - *Lorentzian manifold*: the metric `g` has signature `n-2` (positive
      convention) or `2-n` (negative convention), where `n = \dim M`.

    INPUT:

    - ``n`` -- positive integer; dimension of the manifold
    - ``name`` -- string; name (symbol) given to the manifold
    - ``metric_name`` -- (default: ``'g'``) string; name (symbol) given to the
      metric
    - ``signature`` -- (default: ``None``) signature `S` of the metric as a
      single integer: `S = n_+ - n_-`, where `n_+` (resp. `n_-`) is the
      number of positive terms (resp. number of negative terms) in any
      diagonal writing of the metric components; if ``signature`` is not
      provided, `S` is set to the manifold's dimension (Riemannian
      signature)
    - ``ambient`` -- (default: ``None``) if not ``None``, must be a
      differentiable manifold; the created object is then an open subset of
      ``ambient``
    - ``diff_degree`` -- (default: ``infinity``) degree `k` of
      differentiability
    - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
      denote the manifold; if none is provided, it is set to ``name``
    - ``metric_latex_name`` -- (default: ``None``) string; LaTeX symbol to
      denote the metric; if none is provided, it is set to ``metric_name``
    - ``start_index`` -- (default: 0) integer; lower value of the range of
      indices used for "indexed objects" on the manifold, e.g. coordinates
      in a chart
    - ``category`` -- (default: ``None``) to specify the category; if ``None``,
      ``Manifolds(RR).Differentiable()`` (or ``Manifolds(RR).Smooth()``
      if ``diff_degree`` = ``infinity``) is assumed (see the category
      :class:`~sage.categories.manifolds.Manifolds`)
    - ``unique_tag`` -- (default: ``None``) tag used to force the construction
      of a new object when all the other arguments have been used previously
      (without ``unique_tag``, the
      :class:`~sage.structure.unique_representation.UniqueRepresentation`
      behavior inherited from
      :class:`~sage.manifolds.subset.ManifoldSubset`, via
      :class:`~sage.manifolds.differentiable.manifold.DifferentiableManifold`
      and :class:`~sage.manifolds.manifold.TopologicalManifold`,
      would return the previously constructed object corresponding to these
      arguments).

    EXAMPLES:

    Pseudo-Riemannian manifolds are constructed via the generic function
    :func:`~sage.manifolds.manifold.Manifold`, using the keyword
    ``structure``::

        sage: M = Manifold(4, 'M', structure='pseudo-Riemannian', signature=0)
        sage: M
        4-dimensional pseudo-Riemannian manifold M
        sage: M.category()
        Category of smooth manifolds over Real Field with 53 bits of precision

    The metric associated with ``M`` is::

        sage: M.metric()
        Pseudo-Riemannian metric g on the 4-dimensional pseudo-Riemannian
         manifold M
        sage: M.metric().signature()
        0
        sage: M.metric().tensor_type()
        (0, 2)

    Its value has to be initialized either by setting its components in various
    vector frames or by using the method :meth:`set_metric` (see the
    documentation of this method, or the full example of `S^2` above).

    The default name of the metric is ``g``; it can be customized::

        sage: M = Manifold(4, 'M', structure='pseudo-Riemannian',
        ....:              metric_name='gam', metric_latex_name=r'\gamma')
        sage: M.metric()
        Riemannian metric gam on the 4-dimensional Riemannian manifold M
        sage: latex(M.metric())
        \gamma

    A Riemannian manifold is constructed by the proper setting of the keyword
    ``structure``::

        sage: M = Manifold(4, 'M', structure='Riemannian'); M
        4-dimensional Riemannian manifold M
        sage: M.metric()
        Riemannian metric g on the 4-dimensional Riemannian manifold M
        sage: M.metric().signature()
        4

    Similarly, a Lorentzian manifold is obtained by::

        sage: M = Manifold(4, 'M', structure='Lorentzian'); M
        4-dimensional Lorentzian manifold M
        sage: M.metric()
        Lorentzian metric g on the 4-dimensional Lorentzian manifold M

    The default Lorentzian signature is taken to be positive::

        sage: M.metric().signature()
        2

    but one can opt for the negative convention via the keyword ``signature``::

        sage: M = Manifold(4, 'M', structure='Lorentzian', signature='negative')
        sage: M.metric()
        Lorentzian metric g on the 4-dimensional Lorentzian manifold M
        sage: M.metric().signature()
        -2

    """
    def __init__(self, n, name, metric_name='g', signature=None, ambient=None,
                 diff_degree=infinity, latex_name=None,
                 metric_latex_name=None, start_index=0, category=None,
                 unique_tag=None):
        r"""
        Construct a pseudo-Riemannian manifold.

        TESTS::

            sage: M = Manifold(4, 'M', structure='pseudo-Riemannian',
            ....:              signature=0)
            sage: M
            4-dimensional pseudo-Riemannian manifold M
            sage: type(M)
            <class 'sage.manifolds.differentiable.pseudo_riemannian.PseudoRiemannianManifold_with_category'>
            sage: X.<w,x,y,z> = M.chart()
            sage: M.metric()
            Pseudo-Riemannian metric g on the 4-dimensional pseudo-Riemannian manifold M
            sage: TestSuite(M).run()

        """
        if ambient and not isinstance(ambient, PseudoRiemannianManifold):
            raise TypeError("the argument 'ambient' must be a " +
                            "pseudo-Riemannian manifold")
        if signature is None or signature == n:
            structure = RiemannianStructure()
        elif signature == n-2 or signature == 2-n:
            structure = LorentzianStructure()
        else:
            structure = PseudoRiemannianStructure()
        DifferentiableManifold.__init__(self, n, name, 'real', structure,
                                        ambient=ambient,
                                        diff_degree=diff_degree,
                                        latex_name=latex_name,
                                        start_index=start_index,
                                        category=category)
        self._metric = None # to be initialized by set_metric() or by metric()
        self._metric_signature = signature
        if not isinstance(metric_name, str):
            raise TypeError("{} is not a string".format(metric_name))
        self._metric_name = metric_name
        if metric_latex_name is None:
            self._metric_latex_name = self._metric_name
        else:
            if not isinstance(metric_latex_name, str):
                raise TypeError("{} is not a string".format(metric_latex_name))
            self._metric_latex_name = metric_latex_name

    def set_metric(self, metric):
        r"""
        Set the metric on ``self``.

        INPUT:

        - ``metric`` -- either a metric tensor defined on ``self`` or a field
          of nondegenerate symmetric bilinear forms defined on ``self``,
          assuming in both cases that the signature agrees with that declared
          at the construction of ``self``.

        EXAMPLES:

        Let us consider a 2-dimensional Lorentzian manifold::

            sage: M = Manifold(2, 'M', structure='Lorentzian')
            sage: X.<x,y> = M.chart()

        We construct a field of symmetric bilinear forms on ``M`` as follows::

            sage: X.coframe()
            Coordinate coframe (M, (dx,dy))
            sage: dx = X.coframe()[0]
            sage: dy = X.coframe()[1]
            sage: a = dx*dx - dy*dy
            sage: a
            Field of symmetric bilinear forms dx*dx-dy*dy on the 2-dimensional
             Lorentzian manifold M

        Since ``a`` has the correct signature, we can use it to set the value
        of the manifold's metric::

            sage: M.set_metric(a)
            sage: M.metric().display()
            g = dx*dx - dy*dy

        """
        if isinstance(metric, PseudoRiemannianMetric):
            if metric._name != self._metric_name:
                raise ValueError("name of {} does not match ".format(metric) +
                                 "the name '{}' ".format(self._metric_name) +
                                 "declared at the construction of the " +
                                 "{}".format(self))
            if metric.parent()._dest_map is not self.identity_map():
                raise ValueError("{} is not a metric ".format(metric) +
                                 "defined on {}".format(self))
            self._metric = metric
            metric._latex_name = self._metric_latex_name
        elif isinstance(metric, TensorField):
            self._metric = self.metric(self._metric_name,
                                       signature=self._metric_signature,
                                       latex_name=self._metric_latex_name)
            self._metric.set(metric)
        else:
            raise TypeError("{} must be a metric or a ".format(metric) +
                            "of bilinear forms")

    def metric(self, name=None, signature=None, latex_name=None,
               dest_map=None):
        r"""
        Return the metric of the pseudo-Riemannian manifold ``self`` or
        defines a new metric tensor on ``self``.

        INPUT:

        - ``name`` -- (default: ``None``) name given to the metric; if
          ``name`` is ``None`` or matches the name of the metric defining the
          pseudo-Riemannian structure of ``self``, the latter metric is
          returned
        - ``signature`` -- (default: ``None``; ignored if ``name`` is ``None``)
          signature `S` of the metric as a single integer: `S = n_+ - n_-`,
          where `n_+` (resp. `n_-`) is the number of positive terms (resp.
          number of negative terms) in any diagonal writing of the metric
          components; if ``signature`` is not provided, `S` is set to the
          manifold's dimension (Riemannian signature)
        - ``latex_name`` -- (default: ``None``; ignored if ``name`` is ``None``)
          LaTeX symbol to denote the metric; if ``None``, it is formed from
          ``name``
        - ``dest_map`` -- (default: ``None``; ignored if ``name`` is ``None``)
          instance of
          class :class:`~sage.manifolds.differentiable.diff_map.DiffMap`
          representing the destination map `\Phi:\ U \rightarrow M`, where `U`
          is the current manifold; if ``None``, the identity map is assumed
          (case of a metric tensor field *on* `U`)

        OUTPUT:

        - instance of
          :class:`~sage.manifolds.differentiable.metric.PseudoRiemannianMetric`

        EXAMPLES:

        Metric of a 3-dimensional Riemannian manifold::

            sage: M = Manifold(3, 'M', structure='Riemannian', start_index=1)
            sage: X.<x,y,z> = M.chart()
            sage: g = M.metric(); g
            Riemannian metric g on the 3-dimensional Riemannian manifold M

        The metric remains to be initialized, for instance by setting its
        components in the coordinate frame associated to the chart ``X``::

            sage: g[1,1], g[2,2], g[3,3] = 1, 1, 1
            sage: g.display()
            g = dx*dx + dy*dy + dz*dz

        Another metric can be defined on ``M`` by specifying a metric name
        distinct from that chosen at the creation of the manifold (which
        is ``g`` by default, but can be changed thanks to the keyword
        ``metric_name`` in :func:`~sage.manifolds.manifold.Manifold`)::

            sage: h = M.metric('h'); h
            Riemannian metric h on the 3-dimensional Riemannian manifold M
            sage: h[1,1], h[2,2], h[3,3] = 1+y^2, 1+z^2, 1+x^2
            sage: h.display()
            h = (y^2 + 1) dx*dx + (z^2 + 1) dy*dy + (x^2 + 1) dz*dz

        The metric tensor ``h`` is distinct from the metric entering in the
        definition of the Riemannian manifold ``M``::

            sage: h is M.metric()
            False

        while we have of course::

            sage: g is M.metric()
            True

        Providing the same name as the manifold's default metric returns the
        latter::

            sage: M.metric('g') is M.metric()
            True

        In the present case (``M`` is diffeomorphic to `\RR^3`), we can even
        create a Lorentzian metric on ``M``::

            sage: h = M.metric('h', signature=1); h
            Lorentzian metric h on the 3-dimensional Riemannian manifold M

        """
        if name is None or name == self._metric_name:
            # Default metric associated with the manifold
            if self._metric is None:
                if self._manifold is not self and self._manifold._metric is not None:
                    # case of an open subset with a metric already defined on
                    # the ambient manifold:
                    self._metric = self._manifold._metric.restrict(self)
                else:
                    # creation from scratch:
                    self._metric = DifferentiableManifold.metric(self,
                                           self._metric_name,
                                           signature=self._metric_signature,
                                           latex_name=self._metric_latex_name)
            return self._metric
        # Metric distinct from the default one: it is created by the method
        # metric of the superclass for generic differentiable manifolds:
        return DifferentiableManifold.metric(self, name, signature=signature,
                                             latex_name=latex_name,
                                             dest_map=dest_map)

    def open_subset(self, name, latex_name=None, coord_def={}):
        r"""
        Create an open subset of ``self``.

        An open subset is a set that is (i) included in the manifold and (ii)
        open with respect to the manifold's topology. It is a differentiable
        manifold by itself. Moreover, equipped with the restriction of the
        manifold metric to itself, it is a pseudo-Riemannian manifold. Hence
        the returned object is an instance of
        :class:`PseudoRiemannianManifold`.

        INPUT:

        - ``name`` -- name given to the open subset
        - ``latex_name`` --  (default: ``None``) LaTeX symbol to denote the
          subset; if none is provided, it is set to ``name``
        - ``coord_def`` -- (default: {}) definition of the subset in
          terms of coordinates; ``coord_def`` must a be dictionary with keys
          charts in the manifold's atlas and values the symbolic expressions
          formed by the coordinates to define the subset.

        OUTPUT:

        - instance of :class:`PseudoRiemannianManifold` representing the
          created open subset

        EXAMPLES:

        Open subset of a 2-dimensional Riemannian manifold::

            sage: M = Manifold(2, 'M', structure='Riemannian')
            sage: X.<x,y> = M.chart()
            sage: U = M.open_subset('U', coord_def={X: x>0}); U
            Open subset U of the 2-dimensional Riemannian manifold M
            sage: type(U)
            <class 'sage.manifolds.differentiable.pseudo_riemannian.PseudoRiemannianManifold_with_category'>

        We initialize the metric of ``M``::

            sage: g = M.metric()
            sage: g[0,0], g[1,1] = 1, 1

        Then the metric on ``U`` is determined as the restriction of ``g`` to
        ``U``::

            sage: gU = U.metric(); gU
            Riemannian metric g on the Open subset U of the 2-dimensional Riemannian manifold M
            sage: gU.display()
            g = dx*dx + dy*dy
            sage: gU is g.restrict(U)
            True

        TESTS:

        Open subset created after the initialization of the metric::

            sage: V = M.open_subset('V', coord_def={X: x<0}); V
            Open subset V of the 2-dimensional Riemannian manifold M
            sage: gV = V.metric()
            sage: gV.display()
            g = dx*dx + dy*dy
            sage: gV is g.restrict(V)
            True

        """
        resu = PseudoRiemannianManifold(self._dim, name,
                                        metric_name=self._metric_name,
                                        signature=self._metric_signature,
                                        ambient=self._manifold,
                                        diff_degree=self._diff_degree,
                                        latex_name=latex_name,
                                        metric_latex_name=self._metric_latex_name,
                                        start_index=self._sindex)
        resu._calculus_method = self._calculus_method
        resu._supersets.update(self._supersets)
        for sd in self._supersets:
            sd._subsets.add(resu)
        self._top_subsets.add(resu)
        # Charts on the result from the coordinate definition:
        for chart, restrictions in coord_def.items():
            if chart not in self._atlas:
                raise ValueError("the {} does not belong to ".format(chart) +
                                 "the atlas of {}".format(self))
            chart.restrict(resu, restrictions)
        # Transition maps on the result inferred from those of self:
        for chart1 in coord_def:
            for chart2 in coord_def:
                if chart2 != chart1 and (chart1, chart2) in self._coord_changes:
                    self._coord_changes[(chart1, chart2)].restrict(resu)
        #!# update non-coordinate vector frames and change of frames
        #
        return resu
