from math import sqrt

class vector:
   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   def __add__(self, other):
      if not isinstance(other, vector):
         raise TypeError('Can only add vectors')
      else:
         return vector(self.x + other.x,
                                  self.y + other.y,
                                  self.z + other.z)

   def __sub__(self, other):
      if not isinstance(other, vector):
         raise TypeError('Can only subtract vectors')
      else:
         return vector(self.x - other.x,
                                  self.y - other.y,
                                  self.z - other.z)

   def __mul__(self, other):
      if (not isinstance(other, int)) and (not isinstance(other, float)):
         raise TypeError('Can only multiply by a scalar')
      else:
         return vector(other*self.x,
                                 other* self.y,
                                 other*self.z)

   def __rmul__(self, other):
      return self*other

   def __truediv__(self, other):
      if not isinstance(other, int) and not isinstance(other, float):
         raise TypeError('Can only divide by a scalar')
      return self*(1/other)

   def __abs__(self):
      return sqrt(self.x**2 + self.y**2 + self.z**2)

   def __str__(self):
      return str((self.x, self.y, self.z))

def mag(vec):
   return abs(vec)

def mag2(vec):
   return abs(vec)**2

def norm(vec):
   m = abs(vec)
   if m == 0:
      return vector(0, 0, 0)
   else:
      return vec/abs(vec)

def dot(vec1, vec2):
   return vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z

def cross(u, v):
   return vector(u.y*v.z - u.z*v.y, u.z*v.x - u.x*v.z, u.x*v.y - u.y*v.x)

def proj(vec1, vec2):
   return dot(vec1, norm(b))*norm(b)

