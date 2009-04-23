from cfda.models import *
from decimal import Decimal

# CFDA numbers copied & pasted from PDF
CFDA_NUMBERS = (
	10.153,
	10.155,
	10.156,
	10.162,
	10.163,
	10.164,
	10.165,
	10.167,
	10.168,
	10.169,
	10.170,
	10.256,
	10.290,
	10.084,
	10.309,
	10.679,
	10.860,
	10.862,
	10.001,
	10.700,
	10.025,
	10.028,
	10.029,
	10.200,
	10.202,
	10.203,
	10.205,
	10.206,
	10.207,
	10.210,
	10.212,
	10.215,
	10.216,
	10.217,
	10.219,
	10.220,
	10.221,
	10.222,
	10.223,
	10.224,
	10.225,
	10.226,
	10.227,
	10.228,
	10.303,
	10.304,
	10.305,
	10.306,
	10.307,
	10.308,
	10.500,
	10.250,
	10.253,
	10.254,
	10.255,
	10.051,
	10.053,
	10.054,
	10.055,
	10.056,
	10.066,
	10.069,
	10.073,
	10.077,
	10.078,
	10.079,
	10.080,
	10.081,
	10.082,
	10.404,
	10.406,
	10.407,
	10.421,
	10.435,
	10.437,
	10.443,
	10.449,
	10.451,
	10.452,
	10.994,
	10.995,
	10.999,
	10.551,
	10.553,
	10.555,
	10.556,
	10.557,
	10.558,
	10.559,
	10.560,
	10.561,
	10.565,
	10.566,
	10.567,
	10.568,
	10.569,
	10.572,
	10.574,
	10.576,
	10.578,
	10.579,
	10.580,
	10.582,
	10.475,
	10.477,
	10.479,
	10.600,
	10.601,
	10.603,
	10.604,
	10.606,
	10.607,
	10.608,
	10.609,
	10.960,
	10.961,
	10.962,
	10.652,
	10.664,
	10.665,
	10.666,
	10.670,
	10.671,
	10.672,
	10.674,
	10.675,
	10.676,
	10.677,
	10.678,
	10.680,
	10.681,
	10.684,
	10.950,
	10.774,
	10.070,
	10.072,
	10.901,
	10.902,
	10.903,
	10.904,
	10.905,
	10.906,
	10.907,
	10.910,
	10.912,
	10.913,
	10.914,
	10.916,
	10.917,
	10.918,
	10.919,
	10.920,
	10.921,
	10.922,
	10.923,
	10.450,
	10.454,
	10.455,
	10.456,
	10.457,
	10.458,
	10.459,
	10.778,
	10.447,
	10.085,
	10.350,
	10.352,
	10.405,
	10.410,
	10.411,
	10.415,
	10.417,
	10.420,
	10.427,
	10.433,
	10.438,
	10.441,
	10.442,
	10.444,
	10.445,
	10.446,
	10.760,
	10.761,
	10.762,
	10.763,
	10.766,
	10.767,
	10.768,
	10.769,
	10.770,
	10.771,
	10.772,
	10.773,
	10.775,
	10.850,
	10.851,
	10.854,
	10.855,
	10.856,
	10.857,
	10.858,
	10.859,
	10.861,
	10.863,
	10.864,
	10.886,
	11.001,
	11.002,
	11.003,
	11.004,
	11.005,
	11.006,
	11.025,
	11.026,
	11.106,
	11.108,
	11.110,
	11.111,
	11.112,
	11.113,
	11.150,
	11.300,
	11.302,
	11.303,
	11.307,
	11.312,
	11.313,
	11.400,
	11.405,
	11.407,
	11.408,
	11.413,
	11.415,
	11.417,
	11.419,
	11.420,
	11.426,
	11.427,
	11.429,
	11.430,
	11.431,
	11.432,
	11.433,
	11.434,
	11.435,
	11.436,
	11.437,
	11.438,
	11.439,
	11.440,
	11.441,
	11.443,
	11.444,
	11.445,
	11.449,
	11.450,
	11.452,
	11.454,
	11.455,
	11.457,
	11.459,
	11.460,
	11.462,
	11.463,
	11.467,
	11.468,
	11.469,
	11.472,
	11.473,
	11.474,
	11.477,
	11.478,
	11.480,
	11.481,
	11.550,
	11.553,
	11.554,
	11.555,
	11.556,
	11.601,
	11.603,
	11.604,
	11.606,
	11.609,
	11.610,
	11.611,
	11.612,
	11.616,
	11.617,
	11.618,
	11.650,
	11.702,
	11.900,
	11.800,
	11.801,
	11.803,
	12.002,
	12.614,
	12.100,
	12.101,
	12.102,
	12.103,
	12.104,
	12.105,
	12.106,
	12.107,
	12.108,
	12.109,
	12.110,
	12.111,
	12.112,
	12.113,
	12.114,
	12.116,
	12.404,
	12.300,
	12.350,
	12.400,
	12.401,
	12.420,
	12.431,
	12.550,
	12.551,
	12.552,
	12.553,
	12.554,
	12.555,
	12.607,
	12.610,
	12.611,
	12.351,
	12.352,
	12.360,
	12.630,
	12.700,
	12.800,
	12.900,
	12.901,
	12.902,
	12.910,
	14.103,
	14.108,
	14.110,
	14.112,
	14.117,
	14.119,
	14.122,
	14.123,
	14.126,
	14.127,
	14.128,
	14.129,
	14.133,
	14.134,
	14.135,
	14.138,
	14.139,
	14.142,
	14.149,
	14.151,
	14.155,
	14.157,
	14.159,
	14.162,
	14.163,
	14.164,
	14.167,
	14.168,
	14.169,
	14.171,
	14.172,
	14.175,
	14.181,
	14.183,
	14.184,
	14.188,
	14.189,
	14.191,
	14.195,
	14.197,
	14.198,
	14.199,
	14.311,
	14.313,
	14.314,
	14.315,
	14.316,
	14.515,
	14.876,
	14.877,
	14.218,
	14.225,
	14.227,
	14.228,
	14.231,
	14.235,
	14.238,
	14.239,
	14.241,
	14.244,
	14.246,
	14.247,
	14.248,
	14.249,
	14.250,
	14.251,
	14.252,
	14.400,
	14.401,
	14.402,
	14.404,
	14.405,
	14.406,
	14.407,
	14.408,
	14.412,
	14.414,
	14.415,
	14.506,
	14.514,
	14.516,
	14.517,
	14.519,
	14.520,
	14.850,
	14.856,
	14.862,
	14.865,
	14.866,
	14.867,
	14.869,
	14.870,
	14.871,
	14.872,
	14.873,
	14.874,
	14.875,
	14.878,
	14.879,
	14.880,
	14.881,
	14.900,
	14.901,
	14.902,
	14.903,
	14.904,
	14.905,
	14.906,
	15.020,
	15.021,
	15.022,
	15.024,
	15.025,
	15.026,
	15.027,
	15.028,
	15.029,
	15.030,
	15.031,
	15.032,
	15.033,
	15.034,
	15.035,
	15.036,
	15.037,
	15.038,
	15.040,
	15.041,
	15.042,
	15.043,
	15.044,
	15.045,
	15.046,
	15.047,
	15.048,
	15.051,
	15.052,
	15.053,
	15.055,
	15.057,
	15.058,
	15.059,
	15.060,
	15.061,
	15.062,
	15.063,
	15.064,
	15.065,
	15.108,
	15.113,
	15.114,
	15.124,
	15.130,
	15.141,
	15.144,
	15.146,
	15.147,
	15.133,
	15.214,
	15.222,
	15.224,
	15.225,
	15.226,
	15.227,
	15.228,
	15.229,
	15.230,
	15.231,
	15.232,
	15.233,
	15.234,
	15.235,
	15.236,
	15.237,
	15.238,
	15.239,
	15.240,
	15.242,
	15.250,
	15.252,
	15.253,
	15.254,
	15.255,
	15.504,
	15.506,
	15.507,
	15.508,
	15.509,
	15.510,
	15.511,
	15.512,
	15.513,
	15.514,
	15.515,
	15.516,
	15.517,
	15.518,
	15.519,
	15.520,
	15.521,
	15.522,
	15.523,
	15.524,
	15.525,
	15.526,
	15.527,
	15.528,
	15.529,
	15.530,
	15.531,
	15.532,
	15.533,
	15.534,
	15.602,
	15.605,
	15.608,
	15.611,
	15.614,
	15.615,
	15.616,
	15.619,
	15.620,
	15.621,
	15.622,
	15.623,
	15.625,
	15.626,
	15.628,
	15.629,
	15.630,
	15.631,
	15.632,
	15.633,
	15.634,
	15.635,
	15.636,
	15.637,
	15.638,
	15.639,
	15.640,
	15.641,
	15.642,
	15.643,
	15.644,
	15.645,
	15.647,
	15.648,
	15.649,
	15.650,
	15.651,
	15.652,
	15.653,
	15.654,
	15.655,
	15.805,
	15.807,
	15.808,
	15.809,
	15.810,
	15.811,
	15.812,
	15.813,
	15.814,
	15.815,
	15.816,
	15.978,
	15.850,
	15.875,
	15.406,
	15.407,
	15.904,
	15.912,
	15.914,
	15.915,
	15.916,
	15.918,
	15.921,
	15.922,
	15.923,
	15.926,
	15.927,
	15.928,
	15.929,
	15.930,
	15.931,
	15.421,
	15.422,
	15.423,
	15.424,
	15.425,
	15.426,
	15.427,
	15.428,
	16.001,
	16.003,
	16.004,
	16.012,
	16.750,
	16.100,
	16.101,
	16.103,
	16.104,
	16.105,
	16.108,
	16.109,
	16.110,
	16.749,
	16.200,
	16.300,
	16.301,
	16.302,
	16.303,
	16.304,
	16.305,
	16.307,
	16.308,
	16.309,
	16.523,
	16.540,
	16.541,
	16.543,
	16.547,
	16.548,
	16.726,
	16.727,
	16.730,
	16.731,
	16.735,
	16.737,
	16.550,
	16.554,
	16.734,
	16.739,
	16.560,
	16.562,
	16.566,
	16.741,
	16.742,
	16.748,
	16.571,
	16.578,
	16.579,
	16.580,
	16.597,
	16.606,
	16.607,
	16.608,
	16.609,
	16.610,
	16.611,
	16.612,
	16.614,
	16.615,
	16.616,
	16.738,
	16.740,
	16.744,
	16.745,
	16.746,
	16.751,
	16.752,
	16.753,
	16.754,
	16.320,
	16.321,
	16.575,
	16.576,
	16.582,
	16.583,
	16.747,
	16.585,
	16.202,
	16.203,
	16.586,
	16.593,
	16.596,
	16.013,
	16.014,
	16.016,
	16.017,
	16.019,
	16.524,
	16.525,
	16.526,
	16.527,
	16.528,
	16.529,
	16.556,
	16.557,
	16.587,
	16.588,
	16.589,
	16.590,
	16.736,
	16.601,
	16.602,
	16.603,
	16.710,
	17.002,
	17.003,
	17.004,
	17.005,
	17.807,
	17.309,
	17.150,
	17.201,
	17.207,
	17.225,
	17.235,
	17.245,
	17.258,
	17.259,
	17.260,
	17.261,
	17.264,
	17.265,
	17.266,
	17.267,
	17.268,
	17.269,
	17.270,
	17.271,
	17.272,
	17.273,
	17.274,
	17.301,
	17.302,
	17.303,
	17.306,
	17.307,
	17.308,
	17.310,
	17.502,
	17.503,
	17.504,
	17.505,
	17.600,
	17.601,
	17.602,
	17.603,
	17.604,
	17.700,
	17.801,
	17.802,
	17.803,
	17.804,
	17.805,
	17.806,
	17.720,
	19.430,
	19.204,
	19.300,
	19.400,
	19.401,
	19.402,
	19.403,
	19.408,
	19.409,
	19.410,
	19.415,
	19.418,
	19.421,
	19.423,
	19.425,
	19.431,
	19.432,
	19.500,
	19.510,
	19.511,
	19.517,
	19.518,
	19.519,
	19.520,
	19.522,
	20.233,
	20.607,
	20.608,
	20.721,
	20.760,
	20.761,
	20.762,
	20.100,
	20.106,
	20.108,
	20.109,
	20.200,
	20.205,
	20.215,
	20.219,
	20.223,
	20.240,
	20.301,
	20.303,
	20.312,
	20.313,
	20.314,
	20.315,
	20.316,
	20.317,
	20.318,
	20.500,
	20.505,
	20.507,
	20.509,
	20.513,
	20.514,
	20.515,
	20.516,
	20.518,
	20.519,
	20.521,
	20.522,
	20.600,
	20.601,
	20.602,
	20.605,
	20.609,
	20.610,
	20.611,
	20.612,
	20.613,
	20.614,
	20.701,
	20.704,
	20.764,
	20.763,
	20.802,
	20.803,
	20.806,
	20.807,
	20.808,
	20.810,
	20.812,
	20.813,
	20.814,
	20.900,
	20.901,
	20.904,
	20.905,
	20.910,
	20.930,
	20.931,
	20.700,
	20.703,
	20.720,
	20.218,
	20.231,
	20.232,
	20.234,
	20.235,
	20.236,
	20.237,
	20.238,
	21.003,
	21.004,
	21.006,
	21.008,
	21.020,
	21.021,
	23.001,
	23.002,
	23.003,
	23.009,
	23.011,
	27.001,
	27.002,
	27.003,
	27.005,
	27.006,
	27.011,
	27.013,
	29.001,
	30.001,
	30.002,
	30.005,
	30.008,
	30.009,
	30.010,
	30.011,
	32.001,
	33.001,
	34.001,
	36.001,
	39.002,
	39.003,
	39.009,
	39.012,
	40.001,
	40.002,
	42.001,
	42.002,
	42.008,
	42.009,
	43.001,
	43.002,
	44.001,
	44.002,
	45.024,
	45.025,
	45.129,
	45.130,
	45.149,
	45.160,
	45.161,
	45.162,
	45.163,
	45.164,
	45.168,
	45.169,
	45.201,
	45.301,
	45.302,
	45.303,
	45.304,
	45.307,
	45.308,
	45.309,
	45.310,
	45.311,
	45.312,
	45.313,
	46.001,
	47.041,
	47.049,
	47.050,
	47.070,
	47.074,
	47.075,
	47.076,
	47.078,
	47.079,
	47.080,
	47.081,
	57.001,
	58.001,
	59.006,
	59.007,
	59.008,
	59.009,
	59.011,
	59.012,
	59.016,
	59.026,
	59.037,
	59.041,
	59.043,
	59.044,
	59.046,
	59.049,
	59.050,
	59.051,
	59.052,
	59.053,
	59.054,
	59.055,
	59.070,
	64.005,
	64.007,
	64.008,
	64.009,
	64.010,
	64.011,
	64.012,
	64.013,
	64.014,
	64.015,
	64.016,
	64.018,
	64.019,
	64.022,
	64.024,
	64.100,
	64.101,
	64.103,
	64.104,
	64.105,
	64.106,
	64.109,
	64.110,
	64.114,
	64.115,
	64.116,
	64.117,
	64.118,
	64.119,
	64.120,
	64.124,
	64.125,
	64.126,
	64.127,
	64.128,
	64.026,
	64.201,
	64.202,
	64.203,
	66.001,
	66.032,
	66.033,
	66.034,
	66.035,
	66.036,
	66.037,
	66.038,
	66.039,
	66.040,
	66.112,
	66.113,
	66.115,
	66.117,
	66.418,
	66.419,
	66.424,
	66.432,
	66.433,
	66.436,
	66.437,
	66.439,
	66.454,
	66.456,
	66.458,
	66.460,
	66.461,
	66.462,
	66.463,
	66.466,
	66.467,
	66.468,
	66.469,
	66.471,
	66.472,
	66.473,
	66.474,
	66.475,
	66.478,
	66.479,
	66.481,
	66.510,
	66.517,
	66.716,
	66.508,
	66.509,
	66.511,
	66.512,
	66.516,
	66.202,
	66.513,
	66.514,
	66.515,
	66.518,
	66.600,
	66.605,
	66.608,
	66.609,
	66.610,
	66.611,
	66.612,
	66.305,
	66.700,
	66.701,
	66.709,
	66.306,
	66.312,
	66.604,
	66.801,
	66.802,
	66.804,
	66.805,
	66.806,
	66.808,
	66.809,
	66.810,
	66.812,
	66.813,
	66.814,
	66.815,
	66.816,
	66.817,
	66.818,
	66.110,
	66.111,
	66.116,
	66.119,
	66.203,
	66.309,
	66.310,
	66.480,
	66.940,
	66.952,
	66.707,
	66.708,
	66.714,
	66.715,
	66.717,
	66.718,
	66.926,
	66.931,
	66.950,
	66.951,
	68.001,
	70.002,
	70.003,
	77.006,
	77.007,
	77.008,
	78.004,
	81.003,
	81.022,
	81.036,
	81.041,
	81.042,
	81.049,
	81.057,
	81.064,
	81.065,
	81.079,
	81.086,
	81.087,
	81.089,
	81.104,
	81.105,
	81.106,
	81.108,
	81.112,
	81.113,
	81.114,
	81.117,
	81.119,
	81.121,
	81.122,
	81.123,
	81.124,
	81.126,
	84.002,
	84.048,
	84.051,
	84.101,
	84.191,
	84.243,
	84.245,
	84.257,
	84.259,
	84.331,
	84.145,
	84.293,
	84.027,
	84.126,
	84.128,
	84.129,
	84.132,
	84.133,
	84.160,
	84.161,
	84.169,
	84.173,
	84.177,
	84.181,
	84.187,
	84.224,
	84.234,
	84.235,
	84.240,
	84.246,
	84.250,
	84.263,
	84.264,
	84.265,
	84.275,
	84.315,
	84.323,
	84.324,
	84.325,
	84.326,
	84.327,
	84.328,
	84.329,
	84.343,
	84.373,
	84.380,
	84.004,
	84.010,
	84.011,
	84.013,
	84.040,
	84.041,
	84.060,
	84.083,
	84.141,
	84.144,
	84.149,
	84.165,
	84.184,
	84.186,
	84.196,
	84.213,
	84.214,
	84.256,
	84.258,
	84.282,
	84.283,
	84.298,
	84.310,
	84.318,
	84.330,
	84.349,
	84.350,
	84.351,
	84.354,
	84.356,
	84.357,
	84.358,
	84.359,
	84.360,
	84.361,
	84.362,
	84.363,
	84.364,
	84.366,
	84.367,
	84.369,
	84.370,
	84.371,
	84.372,
	84.374,
	84.377,
	84.007,
	84.032,
	84.033,
	84.037,
	84.038,
	84.063,
	84.069,
	84.268,
	84.376,
	84.203,
	84.206,
	84.215,
	84.286,
	84.287,
	84.295,
	84.304,
	84.305,
	84.015,
	84.016,
	84.017,
	84.018,
	84.019,
	84.021,
	84.022,
	84.031,
	84.042,
	84.044,
	84.047,
	84.066,
	84.103,
	84.116,
	84.120,
	84.153,
	84.170,
	84.185,
	84.200,
	84.217,
	84.220,
	84.229,
	84.269,
	84.274,
	84.332,
	84.333,
	84.334,
	84.335,
	84.336,
	84.337,
	84.345,
	84.375,
	84.378,
	84.381,
	84.382,
	84.379,
	84.365,
	85.001,
	85.100,
	85.200,
	85.500,
	85.400,
	85.401,
	85.402,
	85.300,
	85.601,
	86.001,
	88.001,
	89.001,
	89.003,
	89.005,
	90.100,
	90.200,
	90.201,
	90.202,
	90.300,
	90.400,
	90.401,
	90.402,
	90.500,
	91.001,
	91.002,
	93.001,
	93.003,
	93.007,
	93.008,
	93.012,
	93.013,
	93.014,
	93.015,
	93.017,
	93.018,
	93.088,
	93.100,
	93.239,
	93.252,
	93.290,
	93.294,
	93.295,
	93.296,
	93.775,
	93.004,
	93.006,
	93.105,
	93.137,
	93.910,
	93.289,
	93.990,
	93.225,
	93.226,
	93.111,
	93.217,
	93.260,
	93.974,
	93.995,
	93.041,
	93.042,
	93.043,
	93.044,
	93.045,
	93.047,
	93.048,
	93.051,
	93.052,
	93.053,
	93.054,
	93.071,
	93.010,
	93.086,
	93.087,
	93.254,
	93.550,
	93.551,
	93.556,
	93.557,
	93.558,
	93.560,
	93.563,
	93.564,
	93.566,
	93.567,
	93.568,
	93.569,
	93.570,
	93.575,
	93.576,
	93.579,
	93.581,
	93.583,
	93.584,
	93.586,
	93.587,
	93.590,
	93.591,
	93.592,
	93.593,
	93.594,
	93.595,
	93.596,
	93.597,
	93.598,
	93.599,
	93.600,
	93.601,
	93.602,
	93.603,
	93.604,
	93.605,
	93.612,
	93.613,
	93.616,
	93.617,
	93.618,
	93.623,
	93.630,
	93.631,
	93.632,
	93.643,
	93.645,
	93.647,
	93.648,
	93.652,
	93.658,
	93.659,
	93.667,
	93.669,
	93.670,
	93.671,
	93.674,
	93.676,
	93.760,
	93.767,
	93.768,
	93.769,
	93.770,
	93.773,
	93.774,
	93.776,
	93.777,
	93.778,
	93.779,
	93.780,
	93.781,
	93.783,
	93.784,
	93.785,
	93.786,
	93.789,
	93.790,
	93.791,
	93.793,
	93.794,
	93.103,
	93.448,
	93.449,
	93.061,
	93.063,
	93.064,
	93.065,
	93.066,
	93.067,
	93.068,
	93.069,
	93.116,
	93.118,
	93.135,
	93.136,
	93.184,
	93.185,
	93.197,
	93.262,
	93.268,
	93.269,
	93.270,
	93.283,
	93.919,
	93.938,
	93.939,
	93.940,
	93.941,
	93.942,
	93.943,
	93.944,
	93.945,
	93.946,
	93.947,
	93.977,
	93.978,
	93.988,
	93.991,
	93.993,
	93.009,
	93.442,
	93.443,
	93.107,
	93.110,
	93.117,
	93.124,
	93.127,
	93.129,
	93.130,
	93.134,
	93.145,
	93.153,
	93.155,
	93.156,
	93.157,
	93.162,
	93.165,
	93.178,
	93.181,
	93.186,
	93.189,
	93.191,
	93.192,
	93.211,
	93.212,
	93.223,
	93.224,
	93.234,
	93.235,
	93.236,
	93.241,
	93.247,
	93.249,
	93.250,
	93.251,
	93.253,
	93.255,
	93.256,
	93.257,
	93.259,
	93.264,
	93.265,
	93.266,
	93.267,
	93.288,
	93.291,
	93.300,
	93.301,
	93.303,
	93.342,
	93.358,
	93.359,
	93.364,
	93.365,
	93.822,
	93.824,
	93.884,
	93.887,
	93.888,
	93.889,
	93.890,
	93.908,
	93.912,
	93.913,
	93.914,
	93.917,
	93.918,
	93.923,
	93.924,
	93.925,
	93.926,
	93.928,
	93.932,
	93.952,
	93.962,
	93.964,
	93.965,
	93.969,
	93.994,
	93.996,
	93.123,
	93.164,
	93.193,
	93.210,
	93.228,
	93.231,
	93.237,
	93.284,
	93.441,
	93.444,
	93.933,
	93.954,
	93.970,
	93.971,
	93.972,
	93.104,
	93.138,
	93.150,
	93.229,
	93.230,
	93.238,
	93.243,
	93.244,
	93.275,
	93.276,
	93.958,
	93.959,
	93.982,
	93.019,
	93.113,
	93.121,
	93.140,
	93.142,
	93.143,
	93.172,
	93.173,
	93.187,
	93.209,
	93.213,
	93.220,
	93.232,
	93.233,
	93.242,
	93.271,
	93.272,
	93.273,
	93.279,
	93.280,
	93.281,
	93.282,
	93.285,
	93.286,
	93.307,
	93.308,
	93.310,
	93.361,
	93.389,
	93.392,
	93.393,
	93.394,
	93.395,
	93.396,
	93.397,
	93.398,
	93.399,
	93.837,
	93.838,
	93.839,
	93.846,
	93.847,
	93.853,
	93.855,
	93.856,
	93.859,
	93.865,
	93.866,
	93.867,
	93.879,
	93.891,
	93.936,
	93.989,
	93.161,
	93.202,
	93.204,
	93.206,
	93.208,
	93.240,
	94.002,
	94.003,
	94.004,
	94.005,
	94.006,
	94.007,
	94.009,
	94.011,
	94.013,
	94.016,
	96.001,
	96.002,
	96.004,
	96.006,
	96.007,
	96.008,
	96.009,
	96.020,
	97.004,
	97.005,
	97.006,
	97.007,
	97.008,
	97.009,
	97.010,
	97.011,
	97.012,
	97.013,
	97.014,
	97.015,
	97.016,
	97.018,
	97.019,
	97.020,
	97.021,
	97.022,
	97.023,
	97.024,
	97.025,
	97.026,
	97.027,
	97.028,
	97.029,
	97.030,
	97.031,
	97.032,
	97.033,
	97.034,
	97.036,
	97.039,
	97.040,
	97.041,
	97.042,
	97.043,
	97.044,
	97.045,
	97.046,
	97.047,
	97.048,
	97.049,
	97.050,
	97.052,
	97.053,
	97.055,
	97.056,
	97.057,
	97.058,
	97.059,
	97.061,
	97.062,
	97.064,
	97.065,
	97.066,
	97.067,
	97.068,
	97.069,
	97.070,
	97.071,
	97.072,
	97.073,
	97.074,
	97.075,
	97.076,
	97.077,
	97.078,
	97.079,
	97.080,
	97.081,
	97.082,
	97.083,
	97.084,
	97.085,
	97.086,
	97.087,
	97.088,
	97.089,
	97.090,
	97.091,
	97.092,
	97.093,
	97.094,
	97.095,
	97.096,
	97.097,
	97.098,
	97.099,
	97.100,
	97.103,
	97.104,
	97.105,
	97.106,
	97.107,
	97.108,
	97.109,
	97.110,
	97.111,
	97.112,
	98.001,
	98.002,
	98.003,
	98.004,
	98.005,
	98.006,
	98.007,
	98.008,
	98.009,
	98.010,
	98.011,
	98.012
)

for cfda_number in CFDA_NUMBERS:
    cfda_number_d = Decimal(str(cfda_number))
    match_count = ProgramDescription.objects.filter(program_number=cfda_number_d).count()
    if match_count==0:
        print cfda_number