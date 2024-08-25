#version 300 es

precision mediump float;


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
  vec2 uvTex = texCoords;
  vec3 hdrColor = texture(texBuffer, uvTex).rgb;


  // Pre tone mapping color effects


  // Hue shift
  float hueShift = mix(u_texSrceHueShift, u_texDestHueShift, u_texHueShiftLerpT);
  hdrColor = GetHueShift(hdrColor, hueShift);

  // 'Chromatic Increase' - https://github.com/gurki/vivid
  vec3 lch = rgb_to_lch(hdrColor);
  lch.y = min(lch.y * 2.0F, 140.0);
  vec3 mapped = lch_to_rgb(lch);

  // Tone mapping
  const float exposureMultiplier = 2.0;
  mapped = lottes(exposureMultiplier * hdrColor);

  const float gamma = 2.2;
  const float A = 5.0;

  //const float contrast = 1.0;
  //mapped = max((contrast * (mapped - 0.5)) + 0.5, -0.0);
  mapped = max((u_texContrast * (mapped - 0.5)) + 0.5, u_texContrastMinChan);

  const float brightnessMultiplier = 1.0;
  mapped = brightnessMultiplier * u_texBrightness * mapped;

  mapped = A * pow(mapped, vec3(1.0 / gamma));

  fragColor = vec4(mapped, 1.0);
}
