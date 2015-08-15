from math import sqrt
from math import sin
from math import cos

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

   def rotate(self,angle,u):
      if (not isinstance(angle, float) and not isinstance(angle,int)):
         raise TypeError('Angle must be a number!')
      else:
         if not isinstance(u, vector):
            raise TypeError('Second argument must be a vector!')
         else:
            u = u/abs(u)
            a = sin(angle)
            b = 1-cos(angle)
            v = vector(0,0,0)
            v.x = self.x*((1-b)+b*u.x**2)+ self.y*(u.x*u.y*b-u.z*a)+self.z*(u.x*u.z*b+u.y*a)
            v.y = self.x*(u.x*u.y*b+u.z*a)+ self.y*((1-b)*u.y**2*b)+ self.z*(u.y*u.z*b - u.x*a)
            v.z = self.x*(u.z*u.x*b-u.y*a)+self.y*(u.z*u.y*b+u.x*a)+self.z*((1-b+u.z**2*b))
            self.x = v.x
            self.y = v.y
            self.z = v.z
      

def mag(vec):
   return abs(vec)

def mag2(vec):
   return vec.x**2 + vec.y**2 + vec.z**2

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

def strToVector(string):
   try:
      x = string[1:-1]
      y = x.split(',')
      z = vector(0,0,0)
      z.x = float(y[0])
      z.y = float(y[1])
      z.z = float(y[2])
      return z
   except:
      raise TypeError('Invalid string to convert to vector.')
      return vector(0,0,0)

def perp(u):

   if not isinstance(u,vector):
      raise TypeError('Argument must be a vector')
   elif mag(u) == 0:
         raise Exception('Must be non zero vector')
   else:
      t = vector(0,0,0)
      if (u.x != 0 or u.y != 0):
         t.x = u.y
         t.y = -u.x
      elif (u.x != 0 or u.z != 0):
         t.x = u.z
         t.z = -u.x
      elif (u.y != 0 or u.z != 0):
         t.y = u.z
         t.z = -u.y
      return norm(t)
