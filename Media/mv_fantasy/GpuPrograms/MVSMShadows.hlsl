// Define inputs from application.
struct VertexIn
{
  float4 position : POSITION0;       // Vertex in object-space
  float2 texCoords  : TEXCOORD0;    // Vertex's Texture Coordinates
};

// Define outputs from vertex shader.
struct Vertex
{
  float4 position   : POSITION0;     // Vertex position in screen-space
  float4 color      : COLOR0;        // Vertex color
  float depth       : TEXCOORD0;    // Vertex depth in eye space
};

Vertex ShadowCasterVP(VertexIn In,
            uniform float4 AmbientLight,          // Ambient light in scene
            uniform float4x4 ModelViewProjection  // Model view projection matrix
           )
{
    Vertex Out;
    
    // Transform vertex position into homogenous screen-space.
    Out.position = mul(In.position, ModelViewProjection);
    //Out.testpos = Out.position;
    
    // Store depth
    Out.depth = Out.position.z;
    
    // Store ambient color
    Out.color = AmbientLight;
    
    // Pass texture coordinates to fragment shader
    //Out.texCoords = In.texCoords;

    return Out;
}

struct Fragment
{
    float4 color  : COLOR0;
};

Fragment ShadowCasterFP(Vertex In,
              uniform float DepthOffset  // Depth offset
              )
{
    Fragment Out;

    // Store non-normalized depth
    float Depth = In.depth;

    // Use some bias to avoid precision issue
    Depth += DepthOffset;
    
    // Write the depth value to the depth map
	Out.color.rgba = 0;
    Out.color.r = Depth;

    return Out;
}

// Define outputs from vertex shader.
struct ReceiverVertex
{
  float4 position		: POSITION;     // Vertex position in screen-space
  float4 lightPosition	: TEXCOORD0;    // Fragment's position in light space
  float4 fade			: TEXCOORD1;
  float fog				: FOG;
};

ReceiverVertex ShadowReceiverVP(VertexIn In,
            uniform float4x4 ModelViewProjection,	// Model view projection matrix
            uniform float4x4 Model,                 // Model matrix
            uniform float4x4 TextureViewProjection,  // Texture view projection matrix
            uniform float4 FadeSettings
           )
{
    ReceiverVertex Out;
    
    // Transform vertex position into homogenous screen-space.
    Out.position = mul(In.position, ModelViewProjection);
    
    // Compute vertex position in light space
    // First object to world space
    Out.lightPosition = mul(In.position, Model);
    // Then world to light space
    Out.lightPosition = mul(Out.lightPosition, TextureViewProjection);
    
    // compute fog
	float fade = clamp(( Out.position.z - FadeSettings[0] ) / (FadeSettings[1] - FadeSettings[0]),0.0,1.0);
    Out.fade = fade;
    //Out.fade = 0;
    Out.fog = 1;
    
    return Out;
}

Fragment ShadowReceiverFP(ReceiverVertex In,
			uniform sampler2D ShadowMap,
			uniform float4 ShadowColor,
			uniform float2 TexelOffset
              )
{
    Fragment Out;
    
    float2 sampleOffsets[4] = { 
	{ 0, 0 },
	{ 1, 0 },
	{ 1, 1 },
	{ 0, 1 } };
	
	float LightDistance = In.lightPosition.z / In.lightPosition.w;
    
        // Compute fragment position in shadow map (texture) space
    float2 ShadowMapTexCoords = float2(In.lightPosition.x / In.lightPosition.w,
                                         In.lightPosition.y / In.lightPosition.w);
 
	//Out.color = tex2D(ShadowMap, ShadowMapTexCoords);
	//return Out;
	   
    // Get the stored nearest fragment distance from light in the shadow map (normalized in [0,1] or not)
    //float3 ShadowDistance = tex2D(ShadowMap, ShadowMapTexCoords).rgb;

	float4 ShadowSamples;
	ShadowSamples.r = tex2D(ShadowMap, ShadowMapTexCoords).r;
	ShadowSamples.g = tex2D(ShadowMap, ShadowMapTexCoords + sampleOffsets[1].xy * TexelOffset.xy).r;
	ShadowSamples.b = tex2D(ShadowMap, ShadowMapTexCoords + sampleOffsets[2].xy * TexelOffset.xy).r;
	ShadowSamples.a = tex2D(ShadowMap, ShadowMapTexCoords + sampleOffsets[3].xy * TexelOffset.xy).r;
	
	float4 InLight = LightDistance <= ShadowSamples;
	
	float percentageInLight = dot(InLight, float4(0.25, 0.25, 0.25, 0.25));
	
    // Perform standard shadow map comparison
    //float4 Lit = (LightDistance <= ShadowDistance.r ? 1 : lerp( ShadowColor, 1, In.fade));

	//float4 Lit = (LightDistance <= ShadowSamples.r ? 1 : lerp( ShadowColor, 1, In.fade));
	float4 Lit = lerp( lerp( ShadowColor, 1, percentageInLight), 1, In.fade);
	
	//float4 Lit = lerp( ShadowColor, 1, percentageInLight);
	//float4 Lit = lerp( ShadowColor, 1, In.fade);
	
    // Attenuate the light contribution as necessary to compute the final color
    Out.color.rgb = Lit;
    Out.color.a = 1;
    return Out;
}