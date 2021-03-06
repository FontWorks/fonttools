"""Calculate the area of a glyph."""

from __future__ import print_function, division, absolute_import
from fontTools.misc.py23 import *
from fontTools.pens.basePen import BasePen


def polygon_area(p0, p1):
	return -(p1[0] - p0[0]) * (p1[1] + p0[1]) * 0.5


def quadratic_curve_area(p0, p1, p2):
	x0, y0 = p0[0], p0[1]
	x1, y1 = p1[0] - x0, p1[1] - y0
	x2, y2 = p2[0] - x0, p2[1] - y0
	return (x1*y2 - x2*y1) / 3


def cubic_curve_area(p0, p1, p2, p3):
	x0, y0 = p0[0], p0[1]
	x1, y1 = p1[0] - x0, p1[1] - y0
	x2, y2 = p2[0] - x0, p2[1] - y0
	x3, y3 = p3[0] - x0, p3[1] - y0
	return -(
		x1 * (   -   y2 -   y3) +
		x2 * (y1        - 2*y3) +
		x3 * (y1 + 2*y2       )
	) * 0.15


class AreaPen(BasePen):

	def __init__(self, glyphset=None):
		BasePen.__init__(self, glyphset)
		self.value = 0

	def _moveTo(self, p0):
		self.__startPoint = p0

	def _lineTo(self, p1):
		p0 = self._getCurrentPoint()
		self.value += polygon_area(p0, p1)

	def _curveToOne(self, p1, p2, p3):
		p0 = self._getCurrentPoint()
		self.value += cubic_curve_area(p0, p1, p2, p3)
		self.value += polygon_area(p0, p3)

	def _qCurveToOne(self, p1, p2):
		p0 = self._getCurrentPoint()
		self.value += quadratic_curve_area(p0, p1, p2)
		self.value += polygon_area(p0, p2)

	def _closePath(self):
		p0 = self._getCurrentPoint()
		if p0 != self.__startPoint:
			self.value += polygon_area(p0, self.__startPoint)
