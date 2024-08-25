#version 330 core

#define NO_TONE_MAP 1
#define EXPOSURE_TONE_MAP 2
#define UCHIMURA_TONE_MAP 3
#define LOTTES_TONE_MAP 4
#define ACES_TONE_MAP 5
#define UNCHARTED2_TONE_MAP 6
#define REINHARD2_TONE_MAP 7
#define UNREAL_TONE_MAP 8


// ***********************
// Tone mappings

// Reinhard
vec3 reinhard(vec3 x) {
  return x / (1.0 + x);
}

float reinhard(float x) {
  return x / (1.0 + x);
}

vec3 reinhard2(vec3 x) {
  const float L_white = 4.0;

  return (x * (1.0 + x / (L_white * L_white))) / (1.0 + x);
}

float reinhard2(float x) {
  const float L_white = 4.0;

  return (x * (1.0 + x / (L_white * L_white))) / (1.0 + x);
}

// Narkowicz 2015, "ACES Filmic Tone Mapping Curve"
vec3 aces(vec3 x) {
  const float a = 2.51;
  const float b = 0.03;
  const float c = 2.43;
  const float d = 0.59;
  const float e = 0.14;
  return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
}

float aces(float x) {
  const float a = 2.51;
  const float b = 0.03;
  const float c = 2.43;
  const float d = 0.59;
  const float e = 0.14;
  return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
}

// Filmic Tonemapping Operators http://filmicworlds.com/blog/filmic-tonemapping-operators/
vec3 tonemapFilmic(vec3 x) {
  vec3 X = max(vec3(0.0), x - 0.004);
  vec3 result = (X * (6.2 * X + 0.5)) / (X * (6.2 * X + 1.7) + 0.06);
  return pow(result, vec3(2.2));
}

float tonemapFilmic(float x) {
  float X = max(0.0, x - 0.004);
  float result = (X * (6.2 * X + 0.5)) / (X * (6.2 * X + 1.7) + 0.06);
  return pow(result, 2.2);
}

// Lottes 2016, "Advanced Techniques and Optimization of HDR Color Pipelines"
vec3 lottes(vec3 x) {
  const vec3 a = vec3(1.6);
  const vec3 d = vec3(0.977);
  const vec3 hdrMax = vec3(8.0);
  const vec3 midIn = vec3(0.18);
  const vec3 midOut = vec3(0.267);

  const vec3 b =
      (-pow(midIn, a) + pow(hdrMax, a) * midOut) /
      ((pow(hdrMax, a * d) - pow(midIn, a * d)) * midOut);
  const vec3 c =
      (pow(hdrMax, a * d) * pow(midIn, a) - pow(hdrMax, a) * pow(midIn, a * d) * midOut) /
      ((pow(hdrMax, a * d) - pow(midIn, a * d)) * midOut);

  return pow(x, a) / (pow(x, a * d) * b + c);
}

float lottes(float x) {
  const float a = 1.6;
  const float d = 0.977;
  const float hdrMax = 8.0;
  const float midIn = 0.18;
  const float midOut = 0.267;

  const float b =
      (-pow(midIn, a) + pow(hdrMax, a) * midOut) /
      ((pow(hdrMax, a * d) - pow(midIn, a * d)) * midOut);
  const float c =
      (pow(hdrMax, a * d) * pow(midIn, a) - pow(hdrMax, a) * pow(midIn, a * d) * midOut) /
      ((pow(hdrMax, a * d) - pow(midIn, a * d)) * midOut);

  return pow(x, a) / (pow(x, a * d) * b + c);
}

// Uchimura 2017, "HDR theory and practice"
// Math: https://www.desmos.com/calculator/gslcdxvipg
// Source: https://www.slideshare.net/nikuque/hdr-theory-and-practicce-jp
vec3 uchimura(vec3 x, float P, float a, float m, float l, float c, float b) {
  float l0 = ((P - m) * l) / a;
  float L0 = m - m / a;
  float L1 = m + (1.0 - m) / a;
  float S0 = m + l0;
  float S1 = m + a * l0;
  float C2 = (a * P) / (P - S1);
  float CP = -C2 / P;

  vec3 w0 = vec3(1.0 - smoothstep(0.0, m, x));
  vec3 w2 = vec3(step(m + l0, x));
  vec3 w1 = vec3(1.0 - w0 - w2);

  vec3 T = vec3(m * pow(x / m, vec3(c)) + b);
  vec3 S = vec3(P - (P - S1) * exp(CP * (x - S0)));
  vec3 L = vec3(m + a * (x - m));

  return T * w0 + L * w1 + S * w2;
}

vec3 uchimura(vec3 x) {
  const float P = 1.0;  // max display brightness
  const float a = 1.0;  // contrast
  const float m = 0.22; // linear section start
  const float l = 0.4;  // linear section length
  const float c = 1.03; // black
  const float b = 0.0;  // pedestal

  return uchimura(x, P, a, m, l, c, b);
}

float uchimura(float x, float P, float a, float m, float l, float c, float b) {
  float l0 = ((P - m) * l) / a;
  float L0 = m - m / a;
  float L1 = m + (1.0 - m) / a;
  float S0 = m + l0;
  float S1 = m + a * l0;
  float C2 = (a * P) / (P - S1);
  float CP = -C2 / P;

  float w0 = 1.0 - smoothstep(0.0, m, x);
  float w2 = step(m + l0, x);
  float w1 = 1.0 - w0 - w2;

  float T = m * pow(x / m, c) + b;
  float S = P - (P - S1) * exp(CP * (x - S0));
  float L = m + a * (x - m);

  return T * w0 + L * w1 + S * w2;
}

float uchimura(float x) {
  const float P = 1.0;  // max display brightness
  const float a = 1.0;  // contrast
  const float m = 0.22; // linear section start
  const float l = 0.4;  // linear section length
  const float c = 1.03; // black
  const float b = 0.0;  // pedestal

  return uchimura(x, P, a, m, l, c, b);
}

// Uncharted
vec3 uncharted2Tonemap(vec3 x) {
  float A = 0.15;
  float B = 0.50;
  float C = 0.10;
  float D = 0.20;
  float E = 0.02;
  float F = 0.30;
  float W = 11.2;
  return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F;
}

vec3 uncharted2(vec3 color) {
  const float W = 11.2;
  float exposureBias = 2.0;
  vec3 curr = uncharted2Tonemap(exposureBias * color);
  vec3 whiteScale = 1.0 / uncharted2Tonemap(vec3(W));
  return curr * whiteScale;
}

float uncharted2Tonemap(float x) {
  float A = 0.15;
  float B = 0.50;
  float C = 0.10;
  float D = 0.20;
  float E = 0.02;
  float F = 0.30;
  float W = 11.2;
  return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F;
}

float uncharted2(float color) {
  const float W = 11.2;
  const float exposureBias = 2.0;
  float curr = uncharted2Tonemap(exposureBias * color);
  float whiteScale = 1.0 / uncharted2Tonemap(W);
  return curr * whiteScale;
}

// Unreal 3, Documentation: "Color Grading"
// Adapted to be close to Tonemap_ACES, with similar range
// Gamma 2.2 correction is baked in, don't use with sRGB conversion!
vec3 unreal(vec3 x) {
  return x / (x + 0.155) * 1.019;
}

float unreal(float x) {
  return x / (x + 0.155) * 1.019;
}


// ***********************
// Color space conversions

/**
// Converts a color from linear RGB to XYZ space
const mat3 RGB_2_XYZ = (mat3(
  0.4124564, 0.2126729, 0.0193339,
  0.3575761, 0.7151522, 0.1191920,
  0.1804375, 0.0721750, 0.9503041
));

// Used to convert from XYZ to linear RGB space
const mat3 XYZ_2_RGB = (mat3(
   3.2404542,-0.9692660, 0.0556434,
  -1.5371385, 1.8760108,-0.2040259,
  -0.4985314, 0.0415560, 1.0572252
));

vec3 rgb_to_xyz(vec3 rgb) {
  return RGB_2_XYZ * rgb;
}

vec3 xyz_to_rgb(vec3 xyz) {
  return XYZ_2_RGB * xyz;
}
**/

/***/
vec3 xyz_to_rgb(vec3 color)
{
  float var_X = color.r / 100.0; //X from 0.0 to  95.047 (Observer = 2.0 degrees, Illuminant = D65);
  float var_Y = color.g / 100.0; //Y from 0.0 to 100.000;
  float var_Z = color.b / 100.0; //Z from 0.0 to 108.883;

  float var_R = var_X * 3.2406 + var_Y * -1.5372 + var_Z * -0.4986;
  float var_G = var_X * -0.9689 + var_Y * 1.8758 + var_Z * 0.0415;
  float var_B = var_X * 0.0557 + var_Y * -0.2040 + var_Z * 1.0570;

  if (var_R > 0.0031308)
  {
    var_R = 1.055 * pow(var_R, (1.0 / 2.4)) - 0.055;
  }
  else
  {
    var_R = 12.92 * var_R;
  }
  if (var_G > 0.0031308)
  {
    var_G = 1.055 * pow(var_G, (1.0 / 2.4)) - 0.055;
  }
  else
  {
    var_G = 12.92 * var_G;
  }
  if (var_B > 0.0031308)
  {
    var_B = 1.055 * pow(var_B, (1.0 / 2.4)) - 0.055;
  } else
  {
    var_B = 12.92 * var_B;
  }

  float R = var_R;
  float G = var_G;
  float B = var_B;

  return vec3(R, G, B);
}

vec3 rgb_to_xyz(vec3 color)
{
  float var_R = (color.r); //R from 0.0 to 255.0
  float var_G = (color.g); //G from 0.0 to 255.0
  float var_B = (color.b); //B from 0.0 to 255.0

  if (var_R > 0.04045)
  {
    var_R = pow(((var_R + 0.055) / 1.055), 2.4);
  }
  else
  {
    var_R = var_R / 12.92;
  }
  if (var_G > 0.04045)
  {
    var_G = pow(((var_G + 0.055) / 1.055), 2.4);
  }
  else
  {
    var_G = var_G / 12.92;
  }

  if (var_B > 0.04045)
  {
    var_B = pow(((var_B + 0.055) / 1.055), 2.4);
  }
  else
  {
    var_B = var_B / 12.92;
  }

  var_R = var_R * 100.0;
  var_G = var_G * 100.0;
  var_B = var_B * 100.0;

  // Observer = 2.0°, Illuminant = D65
  float X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805;
  float Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722;
  float Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505;

  return vec3(X, Y, Z);
}

vec3 lab_to_lch(vec3 color)
{
  const float MPI = 3.14159265359;

  float var_H = atan(color.b, color.g); //in GLSL this is atan2

  if (var_H > 0.0)
  {
    var_H = (var_H / MPI) * 180.0;
  }
  else
  {
    var_H = 360.0 - (abs(var_H) / MPI) * 180.0;
  }

  float C = sqrt(pow(color.g, 2.0) + pow(color.b, 2.0));
  float H = var_H;

  return vec3(color.r, C, H);
}

vec3 lch_to_lab(vec3 color)
{
  float a = cos(radians(color.b)) * color.g;
  float b = sin(radians(color.b)) * color.g;

  return vec3(color.r, a, b);
}

vec3 xyz_to_lab(vec3 color)
{
  float ref_X = 95.047; //Observer= 2.0°, Illuminant= D65
  float ref_Y = 100.000;
  float ref_Z = 108.883;

  float var_X = color.r / ref_X;
  float var_Y = color.g / ref_Y;
  float var_Z = color.b / ref_Z;

  if (var_X > 0.008856)
  {
    var_X = pow(var_X, (1.0 / 3.0));
  }
  else
  {
    var_X = (7.787 * var_X) + (16.0 / 116.0);
  }
  if (var_Y > 0.008856)
  {
    var_Y = pow(var_Y, (1.0 / 3.0));
  }
  else
  {
    var_Y = (7.787 * var_Y) + (16.0 / 116.0);
  }
  if (var_Z > 0.008856)
  {
    var_Z = pow(var_Z, (1.0 / 3.0));
  }
  else
  {
    var_Z = (7.787 * var_Z) + (16.0 / 116.0);
  }

  float L = (116.0 * var_Y) - 16.0;
  float a = 500.0 * (var_X - var_Y);
  float b = 200.0 * (var_Y - var_Z);

  return vec3(L, a, b);
}

vec3 lab_to_xyz(vec3 color)
{
  float var_Y = (color.r + 16.0) / 116.0;
  float var_X = color.g / 500.0 + var_Y;
  float var_Z = var_Y - color.b / 200.0;

  if (pow(var_Y, 3.0) > 0.008856)
  {
    var_Y = pow(var_Y, 3.0);
  }
  else
  {
    var_Y = (var_Y - 16.0 / 116.0) / 7.787;
  }
  if (pow(var_X, 3.0) > 0.008856)
  {
    var_X = pow(var_X, 3.0);
  }
  else
  {
    var_X = (var_X - 16.0 / 116.0) / 7.787;
  }
  if (pow(var_Z, 3.0) > 0.008856)
  {
    var_Z = pow(var_Z, 3.0);
  }
  else
  {
    var_Z = (var_Z - 16.0 / 116.0) / 7.787;
  }

  float ref_X = 95.047; //Observer= 2.0 degrees, Illuminant= D65
  float ref_Y = 100.000;
  float ref_Z = 108.883;

  float X = ref_X * var_X;
  float Y = ref_Y * var_Y;
  float Z = ref_Z * var_Z;

  return vec3(X, Y, Z);
}

vec3 rgb_to_lab(vec3 color)
{
  vec3 xyz = rgb_to_xyz(color);
  vec3 lab = xyz_to_lab(xyz);
  return lab;
}

vec3 lab_to_rgb(vec3 color)
{
  vec3 xyz = lab_to_xyz(color);
  vec3 rgb = xyz_to_rgb(xyz);
  return rgb;
}

vec3 rgb_to_lch(vec3 color)
{
  vec3 xyz = rgb_to_xyz(color);
  vec3 lab = xyz_to_lab(xyz);
  vec3 lch = lab_to_lch(lab);
  return lch;
}

vec3 lch_to_rgb(vec3 color)
{
  vec3 lab = lch_to_lab(color);
  vec3 xyz = lab_to_xyz(lab);
  vec3 rgb = xyz_to_rgb(xyz);
  return rgb;
}


vec3 GetHueShift(vec3 color, float hue)
{
  const vec3 k = vec3(0.57735, 0.57735, 0.57735);
  float cosAngle = cos(hue);
  float sinAngle = sin(hue);
  return vec3((color * cosAngle) +
              (sinAngle * cross(k, color)) +
              ((1.0 - cosAngle) * dot(k, color) * k));
}


// ***********************
// Input/Output variables

out vec4 fragColor;

uniform sampler2D texBuffer;
uniform float u_texExposure;
uniform float u_texBrightness;
uniform float u_texContrast;
uniform float u_texContrastMinChan;
uniform float u_texHueShiftLerpT;
uniform float u_texSrceHueShift;
uniform float u_texDestHueShift;
uniform int u_time;
in vec2 texCoords;


void main()
{
  //#define toneMapType EXPOSURE_TONE_MAP
  //#define toneMapType UCHIMURA_TONE_MAP
  #define toneMapType LOTTES_TONE_MAP
  //#define toneMapType ACES_TONE_MAP
  //#define toneMapType UNCHARTED2_TONE_MAP
  //#define toneMapType REINHARD2_TONE_MAP
  //#define toneMapType UNREAL_TONE_MAP

  // Brightness factor after gamma correction
  float A = 1.0;
  float gamma = 2.2;

  vec2 uvTex = texCoords;
  vec3 hdrColor = texture(texBuffer, uvTex).rgb;


/**
  if (hdrColor.r < 125.0/65535.0 && hdrColor.g < 125.0/65535.0 && hdrColor.b < 125.0/65535.0)
    hdrColor.rgb = vec3(0.5, 0.5, 0.5);
  else if (hdrColor.r < 255.0/65535.0 && hdrColor.g < 255.0/65535.0 && hdrColor.b < 255.0/65535.0)
    hdrColor.rgb = vec3(1.0, 0.0, 0.0);
  else if (hdrColor.r < 512.0/65535.0 && hdrColor.g < 512.0/65535.0 && hdrColor.b < 512.0/65535.0)
    hdrColor.rgb = vec3(0.0, 0.0, 1.0);
  else if (hdrColor.r < 1024.0/65535.0 && hdrColor.g < 1024.0/65535.0 && hdrColor.b < 1024.0/65535.0)
    hdrColor.rgb = vec3(0.0, 1.0, 0.0);
  else if (hdrColor.r < 1.0 && hdrColor.g < 1.0 && hdrColor.b < 1.0)
    hdrColor.rgb = vec3(0.0, 1.0, 1.0);
  else
    hdrColor.rgb = vec3(1.0, 1.0, 1.0);
**/
/**
  if (hdrColor.r > 20.0*1024.0/65535.0 &&
      hdrColor.g > 20.0*1024.0/65535.0 && hdrColor.b > 20.0*1024.0/65535.0)
    hdrColor.rgb = vec3(1.0, 0.0, 0.0);
  else
    hdrColor.rgb = vec3(0.5, 0.5, 0.5);
  fragColor = vec4(hdrColor, 1.0);
  return;
**/


  // Pre tone mapping color effects


  // Hue shift
  float hueShift = mix(u_texSrceHueShift, u_texDestHueShift, u_texHueShiftLerpT);
  hdrColor = GetHueShift(hdrColor, hueShift);

  // 'Chromatic Increase' - https://github.com/gurki/vivid
  vec3 lch = rgb_to_lch(hdrColor);
  lch.y = min(lch.y * 2.0F, 140.0);
  vec3 mapped = lch_to_rgb(lch);

  // Tone mapping
  #if (toneMapType == NO_TONE_MAP)
  {
    A = 5.0;
  }
  #elif (toneMapType == UCHIMURA_TONE_MAP)
  {
    gamma = 1.7;
    const float exposureMultiplier = 2.0;
    mapped = uchimura(exposureMultiplier * u_texExposure * mapped);
    A = 7.0;
  }
  #elif (toneMapType == LOTTES_TONE_MAP)
  {
    gamma = 2.2;
    const float exposureMultiplier = 2.0;
    mapped = lottes(exposureMultiplier * u_texExposure * mapped);
    A = 5.0;
  }
  #elif (toneMapType == ACES_TONE_MAP)
  {
    gamma = 2.3;
    const float exposureMultiplier = 2.0;
    mapped = aces(exposureMultiplier * u_texExposure * mapped);
    A = 5.0;
  }
  #elif (toneMapType == UNCHARTED2_TONE_MAP)
  {
    gamma = 2.2;
    const float exposureMultiplier = 2.0;
    mapped = uncharted2Tonemap(exposureMultiplier * u_texExposure * mapped);
    A = 7.0;
  }
  #elif (toneMapType == REINHARD2_TONE_MAP)
  {
    gamma = 1.7;
    const float exposureMultiplier = 2.0;
    mapped = reinhard2(exposureMultiplier * u_texExposure * mapped);
    A = 7.0;
  }
  #elif (toneMapType == UNREAL_TONE_MAP)
  {
    gamma = 1.1;
    const float exposureMultiplier = 2.0;
    mapped = unreal(exposureMultiplier * u_texExposure * mapped);
    A = 6.0;
  }
  #elif (toneMapType == EXPOSURE_TONE_MAP)
  {
    // Exposure tone mapping
    //const float exposure = 30.0;
    //mapped = vec3(1.0) - exp(-hdrColor * exposure);
    const float exposureMultiplier = 2.0;
    mapped = vec3(1.0) - exp(-mapped * exposureMultiplier * u_texExposure);
    A = 5.0;
  }
  #endif

  //const float contrast = 1.0;
  //mapped = max((contrast * (mapped - 0.5)) + 0.5, -0.0);
  mapped = max((u_texContrast * (mapped - 0.5)) + 0.5, u_texContrastMinChan);

  const float brightnessMultiplier = 1.0;
  mapped = brightnessMultiplier * u_texBrightness * mapped;

  mapped = A * pow(mapped, vec3(1.0 / gamma));

  fragColor = vec4(mapped, 1.0);
}
