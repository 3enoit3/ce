
from __future__ import unicode_literals

from django.db import models

class ceNodes(models.Model):
    # Id
    id = models.CharField(max_length=200, primary_key=True)

    # Data
    props = models.TextField(default="{}")

    def __str__(self):
        return "{} {}".format(self.id, self.props)

class ceEdges(models.Model):
    # Link
    n1 = models.ForeignKey(ceNodes, related_name='n1')
    n2 = models.ForeignKey(ceNodes, related_name='n2')
    directed = models.CharField(max_length=200, default="")

    # Data
    props = models.TextField(default="{}")

    def __str__(self):
        aLink = "{} {} {}".format(
                self.n1_id if self.directed == self.n1_id else self.n2_id,
                "->" if self.directed else "-",
                self.n2_id if self.directed == self.n1_id else self.n1_id)
        return "{} {}".format(aLink, self.directed)

