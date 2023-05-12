from django.db import models

class Point(models.Model):
    iaga=models.CharField(max_length=10, null=True,blank=True)
    glon=models.FloatField(null=True,blank=True)
    glat = models.FloatField(null=True,blank=True)
    sza = models.FloatField(null=True,blank=True)

    def get_glon_glat(self):
        return [self.glon,self.glat]


class Triangles(models.Model):
    vertex1 = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='triangles_vertex1')
    vertex2 = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='triangles_vertex2')
    vertex3 = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='triangles_vertex3')

    def __str__(self):
        return f"Triangle: {self.vertex1} - {self.vertex2} - {self.vertex3}"
    def get_list(self):
        return [self.vertex1.get_glon_glat(),self.vertex2.get_glon_glat(),self.vertex3.get_glon_glat()]