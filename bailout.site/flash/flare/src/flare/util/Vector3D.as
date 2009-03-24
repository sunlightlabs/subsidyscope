/*
 * Vector3D for ActionScript 3  
 * Author: Mohammad Haseeb aka M.H.A.Q.S. 
 * http://www.tabinda.net
 * 
 * Licence Agreement
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
 
package flare.util
{ 
	public class Vector3D
	{
		//*********************************************************************************	
		// Variables
		//*********************************************************************************	

		// Coordinate Points in 3D Vector Space
		public var x:Number, y:Number, z:Number = 0.0;
		
		// Special points in Vector Space
		public static const Zero:Vector3D = new Vector3D(0, 0, 0);
		public static const Side:Vector3D= new Vector3D(-1, 0, 0);
		public static const Up:Vector3D = new Vector3D(0, 1, 0);
		public static const Left:Vector3D = new Vector3D( -1, 0, 0);
		public static const Right:Vector3D = new Vector3D(1, 0, 0);
		public static const Forward:Vector3D = new Vector3D(0, 0, -1);
		public static const Backward:Vector3D = new Vector3D(0, 0, 1);
		public static const Down:Vector3D = new Vector3D(0, -1, 0);
		public static const UnitX:Vector3D=new Vector3D(1,0,0);
		public static const UnitY:Vector3D=new Vector3D(0,1,0);
		public static const UnitZ:Vector3D = new Vector3D(0, 0, 1);
		public static const UnitVector:Vector3D = new Vector3D(1, 1, 1);

		//*********************************************************************************	
		// Constructors
		//*********************************************************************************	

		// A mutliple constructor handler
		// input is x,y,z
		public function Vector3D(... args) 
		{
			if(args.length == 3) 
			{
				x = args[0]; 
				y = args[1]; 
				z = args[2];
			} 
			else if(args.length == 2) 
			{
				x = args[0]; 
				y = args[1];
				z = 0;
			} 
			else 
			{
				x = 0; 
				y = 0; 
				z = 0;		
			}
		}
		
		// This serves as an alternate Constructor
		// Returns a new Vector3D instance
		public function Constructor():Vector3D
		{
			return new Vector3D(this.x, this.y, this.z);
		}
		
		// Serves as a Copy Constructor
		public function CopyConstructor(v:Vector3D):Vector3D
		{
			return new Vector3D(v.x, v.y, v.z);
		}

		//*********************************************************************************	
		// Operator Functions
		//*********************************************************************************	

		// Checks if a Vector is equal to another
		// Serves as an == operator
		public static function isEqual(lhs:Vector3D,rhs:Vector3D):Boolean
		{ 
			return (lhs.x == rhs.x) && (lhs.y == rhs.y) && (lhs.z == rhs.z);
		}

		// Checks if a Vector is not equal to another
		// Serves as an != operator
		public static function isNotEqual(lhs:Vector3D,rhs:Vector3D):Boolean
		{
			return (lhs.x != rhs.x) || (lhs.y != rhs.y) || (lhs.z != rhs.z);
		}
		
		// Returns true if the vector's scalar components are all greater
        // that the ones of the vector it is compared against.
		// Serves as a < operator
		public static function isLesser(lhs:Vector3D,rvec:Vector3D):Boolean
		{
			if (lhs.x < rvec.x && lhs.y < rvec.y && lhs.z < rvec.z)
			{
				return true;
			}
			return false;
		}

		// Returns true if the vector's scalar components are all smaller
        // than the ones of the vector it is compared against.
		// Serves as a > operator
		public static function isGreater(lhs:Vector3D,rhs:Vector3D):Boolean
		{
			if (lhs.x > rhs.x && lhs.y > rhs.y && lhs.z > rhs.z)
			{
				return true;
			}
			return false;
		}
		
		//*********************************************************************************	
		// Setter Functions
		//*********************************************************************************	
		
		public function setX(x2:Number=0.0):void
		{
			this.x = x2;
		}
		
		public function setY(y2:Number=0.0):void
		{
			this.y = y2;
		}
		
		public function setZ(z2:Number=0.0):void
		{
			this.z = z2;
		}
		
		public function getX():Number
		{
			return x;
		}
		
		public function getY():Number
		{
			return y;
		}
		
		public function getZ():Number
		{
			return z;
		}
		
		public function setXY(x2:Number=0.0,y2:Number=0.0):void
		{
			this.x = x2;
			this.y = y2;
		}
		
		public function setXYZ(x2:Number=0.0, y2:Number=0.0, z2:Number=0.0):void
		{
			this.x = x2;
			this.y = y2;
			this.z = z2;
		}
		
		public function v_setXYZ(v:Vector3D):void
		{
			this.x = v.x;
			this.y = v.y;
			this.z = v.z;
		}
		
		//*********************************************************************************		
		//  Utility Functions
		//*********************************************************************************		

		// Sets this vector's components to the minimum of its own and the
		// ones of the passed in vector.
		
		// 'Minimum' in this case means the combination of the lowest
		// value of x, y and z from both vectors. Lowest is taken just
		// numerically, not magnitude, so -1 < 0.
		public function MakeFloor(cmp:Vector3D):void
		{
			if (cmp.x < x)
			{
				x=cmp.x;
			}
			if (cmp.y < y)
			{
				y=cmp.y;
			}
			if (cmp.z < z)
			{
				z=cmp.z;
			}
		}
		
		// Sets this vector's components to the maximum of its own and the
		// ones of the passed in vector.
		
		// 'Maximum' in this case means the combination of the highest
		// value of x, y and z from both vectors. Highest is taken just
		// numerically, not magnitude, so 1 > -3.
		public function MakeCeil(cmp:Vector3D):void
		{
			if (cmp.x > x)
			{
				x=cmp.x;
			}
			if (cmp.y > y)
			{
				y=cmp.y;
			}
			if (cmp.z > z)
			{
				z=cmp.z;
			}
		}
		
		// Generates a vector perpendicular to this vector (eg an 'up' vector).
       
		// This method will return a vector which is perpendicular to this
		// vector. There are an infinite number of possibilities but this
		// method will guarantee to generate one of them. If you need more
		// control you should use the Quaternion class.
		public function Perpendicular():Vector3D
		{
			var fSquareZero:Number = 0.000001 * 0.000001;

			var perp:Vector3D = CrossProduct(this,Vector3D.UnitX);

			// Check length
			if (perp.SquaredMagnitude() < fSquareZero)
			{
				//This vector is the Y axis multiplied by a scalar, so we have
  		 		//to use another axis.
				perp = CrossProduct(this,Vector3D.UnitY);
			}

			return perp;
		}
		
		// Returns true if this vector is zero length.
		public function IsZeroLength():Boolean
		{
			var sqlen:Number = this.x * this.x + this.y * this.y + this.z * this.z;
			return sqlen < 0.000001 * 0.000001;
		}

		// As normalise, except that this vector is unaffected and the
       		// normalised vector is returned as a copy.
		public function NormalisedCopy():Vector3D
		{
			var ret:Vector3D=new Vector3D(this);
			ret.fNormalize();
			return ret;
		}

		// Calculates a reflection vector to the plane with the given normal .
       	// NB assumes 'this' is pointing AWAY FROM the plane, invert if it is not.
		public function Reflect(normal:Vector3D):Vector3D
		{
			return new Vector3D(VectorSubtraction(this,ScalarMultiplication(2, ScalarMultiplication(DotProduct(this,normal), normal))));
		}
		
		// Calculates the Magnitude of the Vector
		public function Magnitude():Number
		{
			return Number(Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z));
		}
		
		// Calculates the Square of the Magnitude of a Vector
		public function SquaredMagnitude():Number
		{
			return this.x * this.x + this.y * this.y + this.z * this.z;
		}
		
		// Calculates the MidPoint of Vector
		public function VectorMidPoint(vec:Vector3D):Vector3D
		{
			return new Vector3D(this.x + vec.x * 0.5, this.y + vec.y * 0.5, this.z + vec.z * 0.5);
		}
		
		// Calculates the Normal
		public function fNormalize():void
		{
			var m:Number = 0.0;
			m = Magnitude();
			if (m > 0)
			{
				UnaryScalarDivision(m);
			}
		}
		
		// Calculates the limiting Values
		public function Limit(max:Number=0.0):void
		{
			if (Magnitude() > max)
			{
				fNormalize();
				UnaryScalarMultiplication(max);
			}
		}
		
		// Calculates a 2 Dimensional Angle of Direction
		public function angle2D():Number
		{
			var angle:Number = 0.0;
			angle = Math.atan2( -this.y, this.x);
			return -1 * angle;
		}
		
		// Calculates the Distance of a Vector from Another
		public function Distance(v1:Vector3D, v2:Vector3D):Number
		{
			var dx:Number = 0.0;
			dx=v1.x - v2.x;
			
			var dy:Number = 0.0;
			dy=v1.y - v2.y;
			
			var dz:Number = 0.0;
			dz=v1.z - v2.z;
			
			return Number(Math.sqrt(dx * dx + dy * dy + dz * dz));
		}
		
		// Calculates the dot (scalar) product of this vector with another.
		//
		// The dot product can be used to calculate the angle between 2
		// vectors. If both are unit vectors, the dot product is the
		// cosine of the angle; otherwise the dot product must be
		// divided by the product of the lengths of both vectors to get
		// the cosine of the angle. This result can further be used to
		// calculate the distance of a point from a plane.

		public static function DotProduct(lvec:Vector3D,rvec:Vector3D):Number
		{
			return lvec.x * rvec.x + lvec.y * rvec.y + lvec.z * rvec.z;
		}
		
		// Calculates the cross-product of 2 vectors, i.e. the vector that
		// lies perpendicular to them both.
	
		// The cross-product is normally used to calculate the normal
		// vector of a plane, by calculating the cross-product of 2
		// non-equivalent vectors which lie on the plane (e.g. 2 edges
		// of a triangle).
	
		// Returns a vector which is the result of the cross-product. This
		// vector will <b>NOT</b> be normalised, to maximise efficiency
		// - call Vector3::normalise on the result if you wish this to
		// be done. As for which side the resultant vector will be on, the
		// returned vector will be on the side from which the arc from 'this'
		// to rkVector is anticlockwise, e.g. UNIT_Y.CrossProduct(UNIT_Z)
		// = UNIT_X, whilst UNIT_Z.CrossProduct(UNIT_Y) = -UNIT_X.
		// This is because PV3D uses a right-handed coordinate system.

		public static function CrossProduct(lvec:Vector3D, rvec:Vector3D):Vector3D
		{
			var kCross:Vector3D = new Vector3D();

			kCross.x=lvec.y * rvec.z - lvec.z * rvec.y;
			kCross.y=lvec.z * rvec.x - lvec.x * rvec.z;
			kCross.z=lvec.x * rvec.y - lvec.y * rvec.x;

			return kCross;
		}
		
		//**************************************************************************************		
		// Arithmetic Functions
		//**************************************************************************************
		
		// Serves as Vector Addition but takes on 1 argument
		public function UnaryVectorAddition(v:Vector3D):Vector3D
		{
			this.x += v.x;
			this.y += v.y;
			this.z += v.z;
			return this;
		}
		
		// Same as above but takes two vectors as arguments
		public static function VectorAddition(v1:Vector3D, v2:Vector3D):Vector3D 
		{
    		var v:Vector3D = new Vector3D(v1.x + v2.x,v1.y + v2.y, v1.z + v2.z);
   			return v;
  		}
		
		// Serves as Vector Subtraction but takes on 1 argument
		public function UnaryVectorSubtraction(v:Vector3D):void
		{
			this.x -= v.x;
			this.y -= v.y;
			this.z -= v.z;
		}
		
		// Same as above but takes two vectors as arguments
 	 	public static function VectorSubtraction(v1:Vector3D, v2:Vector3D):Vector3D 
		{
    		var v:Vector3D = new Vector3D(v1.x - v2.x,v1.y - v2.y,v1.z - v2.z);
    		return v;
  		}
		
		// This function does Scalar Multiplication and takes a 
		// scalar component as the argument
		public function UnaryScalarMultiplication(n:Number=0.0):Vector3D
		{
			this.x *= n;
			this.y *= n;
			this.z *= n;
			return this;
		}
		
		// This function is same as the above but takes two arguments
		// A scalar component and the Vector to multiply it with
		public static function ScalarMultiplication(n:Number,vec:Vector3D):Vector3D
		{
			vec.x *= n;
			vec.y *= n;
			vec.z *= n;
			
			return vec;
		}
				
		// This function does Scalar Division and takes a 
		// scalar component as the argument
		public function UnaryScalarDivision(n:Number):Vector3D
		{
			if (n == 0.0)
			{
				return new Vector3D();
			}
			this.x /= n;
			this.y /= n;
			this.z /= n;
			return this;
		}
		
		// This function is same as the above but takes two arguments
		// A scalar component and the Vector to divide it from
		public static function ScalarDivision(lvec:Vector3D,fScalar:Number):Vector3D
		{
			var kDiv:Vector3D=new Vector3D;

			var fInv:Number=1.0 / fScalar;
			kDiv.x=lvec.x * fInv;
			kDiv.y=lvec.y * fInv;
			kDiv.z=lvec.z * fInv;

			return kDiv;
		}
		
		// This will inverse a Vector3D object
		public static function Negate(v:Vector3D):Vector3D
		{
			v.x = -v.x;
			v.y = -v.y;
			v.z = -v.z;
			
			return v;
		}
		
		// Prints the Vector 
		public function tostring():String
		{
			return("x= " + x + " y= " + y + " z= " + z + "\n");
		}
	}
}