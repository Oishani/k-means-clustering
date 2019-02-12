"""
Cluster class for k-Means clustering

This file contains the class cluster,
which is the second part of the assignment.  With this class done,
the visualization can display the centroid of a single cluster.

Authors: Oishani Ganguly (og58), Mihikaa Goenka (mg897)
Date: November 14th, 2018
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6checks
import a6dataset


class Cluster(object):
    """
    A class representing a cluster, a subset of the points in a dataset.

    A cluster is represented as a list of integers that give the indices
    in the dataset of the points contained in the cluster.
    For instance, a cluster consisting of the points with indices 0, 4,
    and 5 in the dataset's data array would be represented by the index list
    [0,4,5].

    A cluster instance also contains a centroid that is used as part of the
    k-means algorithm.  This centroid is an n-D point (where n is the dimension
    of the dataset),represented as a list of n numbers, not as an index into
    the dataset. (This is because the centroid is generally not a point in the
    dataset, but rather is usually in between the data points.)

    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset this cluster is a subset of
        _indices [list of int]: the indices of this cluster's points in the
        dataset
        _centroid [list of numbers]: the centroid of this cluster
    EXTRA INVARIANTS:
        len(_centroid) == _dataset.getDimension()
        0 <= _indices[i] < _dataset.getSize(), for all 0 <= i < len(_indices)
    """

    # Part A
    def __init__(self, dset, centroid):
        """
        Initializes a new empty cluster whose centroid is a copy of <centroid>

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter centroid: the cluster centroid
        Precondition: centroid is a list of ds.getDimension() numbers
        """
        assert isinstance(dset,a6dataset.Dataset)
        assert type(centroid)==list
        assert len(centroid)==dset.getDimension()
        assert a6checks.is_point(centroid)

        copy=[]
        for k in centroid:
            copy.append(k)
        self._dataset=dset
        self._centroid=copy
        self._indices=[]


    def getCentroid(self):
        """
        Returns the centroid of this cluster.

        This getter method is to protect access to the centroid.
        """
        return self._centroid


    def getIndices(self):
        """
        Returns the indices of points in this cluster

        This method returns the attribute _indices directly.
        Any changes made to this list will modify the cluster.
        """
        return self._indices


    def addIndex(self, index):
        """
        Adds the given dataset index to this cluster.

        If the index is already in this cluster, this method leaves the
        cluster unchanged.

        Precondition: index is a valid index into this cluster's dataset.
        That is, index is an int in the range 0.._dataset.getSize()-1.
        """
        assert type(index)==int
        assert 0<=index and index < self._dataset.getSize()

        if not (index in self._indices):
            self._indices.append(index)


    def clear(self):
        """
        Removes all points from this cluster, but leaves the centroid unchanged.
        """
        del self._indices[:]


    def getContents(self):
        """
        Returns a new list containing copies of the points in this cluster.

        The result is a list of list of numbers.  It has to be computed from
        the indices.
        """
        cont=[]
        for i in range (len(self._indices)):
            cont.append(self._dataset.getPoint(self._indices[i]))
        return cont


    # Part B
    def distance(self, point):
        """
        Returns the euclidean distance from point to this cluster's centroid.

        Parameter point: The point to be measured
        Precondition: point is a list of numbers (int or float), with the
        same dimension as the centroid.
        """
        assert a6checks.is_point(point)
        assert len(point)==len(self._centroid)

        sum=0
        for i in range (len(self._centroid)):
            sum+=(point[i]-self._centroid[i])*(point[i]-self._centroid[i])
        dist=math.sqrt(sum)
        return dist


    def getRadius(self):
        """
        Returns the maximum distance from any point in this cluster, to the
        centroid.

        This method loops over the contents to find the maximum distance from
        the centroid.  If there are no points in this cluster, it returns 0.
        """
        if len(self._indices)==0:
            return 0
        big=Cluster.distance(self,self._dataset.getPoint(self._indices[0]))
        for i in range (len(self._indices)):
            dist=Cluster.distance(self,self._dataset.getPoint(self._indices[i]))
            if (dist>big):
                big=dist
        return big


    def update(self):
        """
        Returns True if the centroid remains the same after recomputation;
        False otherwise.

        This method recomputes the _centroid attribute of this cluster.
        The new _centroid attribute is the average of the points of _contents
        (To average a point, average each coordinate separately).

        Whether the centroid "remained the same" after recomputation is
        determined by numpy.allclose.  The return value should be interpreted
        as an indication of whether the starting centroid was a "stable"
        position or not.

        If there are no points in the cluster, the centroid does not change.
        """
        l=len(self.getContents())
        cent=[]
        sum=0
        if l==0:
            return True
        for i in range(len(self.getContents()[0])):
            sum=0
            for j in range(len(self.getContents())):
                sum+=self.getContents()[j][i]
            avg=sum/l
            cent.append(avg)
        value=numpy.allclose(cent, self._centroid)
        if value==False:
            self._centroid=cent
            return False
        return True


    # PROVIDED METHODS: Do not modify!
    def __str__(self):
        """
        Returns a String representation of the centroid of this cluster.
        """
        return str(self._centroid)


    def __repr__(self):
        """
        Returns an unambiguous representation of this cluster.
        """
        return str(self.__class__) + str(self)
