
# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
import pandas as pd
import matplotlib.pyplot as plt
from collections import namedtuple
from pprint import pprint as pp
import sys

Pt = namedtuple('Pt', 'x, y')               # Point
Edge = namedtuple('Edge', 'a, b')           # Polygon edge from a to b
Poly = namedtuple('Poly', 'name, edges')    # Polygon

_eps = 0.00001
_huge = sys.float_info.max
_tiny = sys.float_info.min
# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
  
  
# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/okdollar/<float:xxx>/<float:yyy>', methods = ['GET'])
def disp(xxx,yyy):
    def rayintersectseg(p, edge):
        ''' takes a point p=Pt() and an edge of two endpoints a,b=Pt() of a line segment returns boolean
        '''
        a,b = edge
        if a.y > b.y:
            a,b = b,a
        if p.y == a.y or p.y == b.y:
            p = Pt(p.x, p.y + _eps)

        intersect = False

        if (p.y > b.y or p.y < a.y) or (
            p.x > max(a.x, b.x)):
            return False

        if p.x < min(a.x, b.x):
            intersect = True
        else:
            if abs(a.x - b.x) > _tiny:
                m_red = (b.y - a.y) / float(b.x - a.x)
            else:
                m_red = _huge
            if abs(a.x - p.x) > _tiny:
                m_blue = (p.y - a.y) / float(p.x - a.x)
            else:
                m_blue = _huge
            intersect = m_blue >= m_red
        return intersect

    def _odd(x): return x%2 == 1

    def ispointinside(p, poly):
        ln = len(poly)
        return _odd(sum(rayintersectseg(p, edge)
                        for edge in poly.edges ))

    def polypp(poly):
        print ("\n  Polygon(name='%s', edges=(" % poly.name)
        print ('   ', ',\n    '.join(str(e) for e in poly.edges) + '\n    ))')

    df=pd.read_csv('/home/deepak/Desktop/Projects/OK Dollar/Myanmar Division District Polygon.csv')
    maxx=df.ID.nunique()+1

    testpoints = (Pt(x=xxx,y=yyy),)

    maxx=df.ID.nunique()+1

    for i in range(1,maxx):
        ref=df[df['ID']==i]
        jmax=len(ref)
        coord=[]
        for j in range(0,jmax):
            ref1=ref.iloc[j,:]
            coord.append([ref1.Latitude,ref1.Longitude])


        edg=[]

        for j in range(0,len(coord)):
            if(j<=len(coord)-2):
                aa=coord[j]
                bb=coord[j+1]
                edg.append(Edge(a=Pt(x=aa[0],y=aa[1]), b=Pt(x=bb[0], y=bb[1])))

        polys=[Poly(name=str(ref1.Region)+"-"+str(ref1.District) ,edges=edg),]


        for poly in polys:
                x= ('\t'.join("%s" % (ispointinside(p, poly))
                                       for p in testpoints[:3]))
                y= ('\t'.join("%s" % (ispointinside(p, poly))
                                       for p in testpoints[3:6]))
                z= ('\t'.join("%s" % (ispointinside(p, poly))
                                       for p in testpoints[6:]))
        if(x=='True' or y=='True' or z=='True'):
#            return (ref1.Region,ref1.District)
            return jsonify({'Region': ref1.Region,'District':ref1.District})

  
  
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)
