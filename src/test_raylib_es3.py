PYGBAG_FS=1
# fmt: off
__import__('os').chdir(__import__('tempfile').gettempdir())
def fs_decode(fsname, o248):
    from pathlib import Path
    filename = Path.cwd() / fsname
    if not filename.is_file():
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(fsname,"wb") as fs:
            for input in o248.split("\n"):
                if not input: continue
                fs.write(bytes([ord(c) - 248 for c in input]))

fs_decode('resources/super_mario_bros.png','''
ƁňņĿąĂĒĂøøøąŁŀļŊøøûĘøøùƺüûøøøǝŅƨǳøøøāŨŀőūøøĆƼøøĆƼùƍģĆēøøøćňńŌĽśžǳƒĿúýĭûǁǇĚǬƶƋƟŻ
ǫƋøøĂſŁļĹŌŰǒǥƕăƮǓƞĎĸċƯûƠƌĄĘƈĄĘƱĨŸĞŰǶśƢƅĝăǁŀľĪŗůǧǏǭŎǦǥġĆŤĕĸŸǜŇƗøøøøøøøøøøøøøøøøø
øøøøøøøøøøøøøøøøøøøøøøƲǟƌǳǃǵŵĆǛǗƸŲƜĢćęĀĹĀĺĈźƈǚĺĶůƕŲƆƌǗĂāǱǴǈĀŊĂǷǧźǢęĊƍďƫƺŒƑƥćĭƏŷ
ǗżƈǅŲƐƙĖĚŎűŒǅǂěĻǖİĻǤǭǫĖĺńŜęƏĴŐǅưƌĺĮǢřǷľƞĉęùǭĈƉǂŋƃǪǚĂǱƈŊƧŗŌǗēǁĈĕŊćƉƠƴƠĺǬǝŻōǳĺźǢę
ĚƍşƦǝƍǂĈǋǂĐǪļƀǑĳžǤĈƔĥĻƾģƙƍĦţƥǗŗŖǉƹĺǄžƈƌđŪƷǝưǷǋŖƏčŊƇƵśǀŒűĞŝžŔķƼņǨǔƷǋďůźŊņǀŁžĩǆƂŤ
ųƱǭǰĲƧſŴƭƴħǶǪǚǖơćǒƅǧŻƥơľżƄƏǧľĵŜƤǪƬŊơżńǵƚǷłĠŲėƪĻƀĆơƿĶęǙǝƝĈŚǞėŤƢưŋķǥŦĸƵǄŬǛǎĻǦĎǴňƖ
ǮƍƏĝĻńƋĺĮƦŠčěĻƄłĥŜĨǶǳǲũǵňƶǵǤƒǎƪúǞĿĹǭĈǙǝơĵǝĝǀƈŗǣėŤƒĈƪŒćǛőųĂďĔŎŖĦęƲƙĄǑƠſŶęĻƺǂŃǈŝű
ĶǐǠþƳĤŗĵŌŔęĞŃƏǍǴĐǪƴǣōũƲƤǄśǀĬƧƨƣûǅƆęǶŲƀļǝĝǤƪŤĿĭŶƨšůƎǝƧƿǩőƎŕǀŒĥħũžƐįǁƈĽĵŖǢƪĴđƊĿƀŮ
ķǐƬĳžǰǣęĊƍƏƪǃǪŖāƄęǶƖěƻĤŃƭƒęĲƜĖĚŉűƄęǡƿĈƽĐƊŦĄŉƄęŭƅęǞǭƭƤŚśƀŎƶǱŮƃśƀƆǊŝƱǝŝĕĻƾǝǵǙƒƠŜĄ
ıƬėƪŎƇƛǳęùǝƝĈƚĵėŤƒǔƘƪƷǉǖŲǤǗĩĔǓŝƳƴüśƀƯĚŅǦĐƒƅńƇƒęĞǭĎǦœŝƀĪħŞŀňƳĜčŚĐĻǮŝŔǪĦǃƕġŒǢƑŝýƕ
ĬŬƇńǱǢƩǯāƢğǥƚƋǇƪǤőǁǑÿƯǱüǍľĵļƚǪǊĀűƴĊĒŶƜĥƚƈŸǪŪāĩƭƤŝƵǐŸĿƲƤŕǝƝēĻŬƫđĊŌćƉƠƴǬđǪƵǭƟŨǵǭĈ
ŉǂǋĝżŠǟđǌƎŽǄǣęŚƌƏǟƘǔƾƍŝǖĜĻńƤĄŁǵĞÿŗŗǑŖƏčŌćƉƠĴƾƈƚśŀǎĦǃĶƢįǕƜįǴŢąŗĵļƚǪĪĀšŵĄǩǏĻƼĤħǃĐ
ƚǤŋǊǥƇęģǭĈĩǃīƝĪļƵŁžƠĮĪǜǙĥĥćŵŝƃŕƎƆĴžŠŕŢĄőƔưŧũŻŢƥĖĿůĄûǂŃƵėƪŰƛļċĺźǢęċƍƏįĻǄƓŜƀƂƔęıż
ĄēĩƃǯąĮĠļųǢǩĺƏŭŧƏĢĪļƉęǝƾƈłǏƪƺŇĦžĥƕǤĦŇħĆƔČŕǃŢǢǬųǐǒŋƌǪǪĂĩǛǓįŅģſƥƭǳŖŊǵňćŵǤŤƧŗƀŉĲǡǊ
ƁŖƵĊŬŋƟǗǅŌƋĽĵǄŹƻǎǞŁƳŜőĲřĄġķžĤǗƱǠƦǑǌǪǆƽƘģǒƥſǮǏĻĔĥǇǏĦǁƾƈǱœŁǅƿǴǈǚǯŞƾƈƽǓōƏǭĨŢƷĈƵƮưư
ĠħœžƠŎīŜƱŔƶưƚĻýŧƎƏǤŔǎīęƥƄęùďǎǣŕƎŁǷǖǖĽŢǢŎƿĈƵǉƽƐŻđƚƃƄęŞǥǥǭǝŗċųǴƾŨƠǎƚĖĚŉűƉƟƵƃƧŝŨǇƎ
ġǕǈŵǀƋŲǤƶŋćħħǝƖŲƍǗėŪǜƂǖǲǶƈǵǯĭıƷǈŝǣųĪǬǥƹƌĞżƐƿĦƾİķǡƵśƀǒĢħǛĩĘĪŜŷűǑǯēŢǗćġąĺĈźĈżĘüęƽ
ŽøøøøøøøøøøøøøøøøøøøøøøøøøøøǌƺǨƀǴŇŒúęŸĈżøĺƒŚǮŽĮĀĹĀĘüęŸƈŎǡƴŴĹĀĺøęĀùżĬĢƼĒǰŭŵũǥǇǳǧ
ǶƙŭǢĉǊŗǶſƈĊǬįŦĺǲƓƈǃǇŏěĀƙǃźŇǏǖŁƄĺƼƈęƕưǶŻƈǤǐǏǪǷƲƷŻǶŏğƞŧƗěĻłĀƱĆĒŮǜňǯĦǣúđŊŃžĄŢǀƈŚĺż
įĻƲœƂĘƜňƏǍĵĀęĻƂŮőŚƔŝőďǛƗŲƾƈŪđǊųżƈęǝþǭǃŕǱĵħĞęƄęǝƞƵņŖĀĪƜźšŧĿƏōǃƬǏđǇŧƛŁǗƽǶŊİǐƍęŚĞļ
ǔĎǖħůęĀġěļńǛƱŕŔČǵťƩƩċƬņƑĄőŬőįƦĵđƥŋƉĈƾƈƊǴǭǨŭƧńƨĢċƺƢāđúƓĺüĺǀĈĞŐǣǈĲĝżǬěǮĶƨƳťƛěƜžĄƩ
ĒļįǕčǊĲĝżƀǙŤǁƠĺńǁĺǣŌƈęƄęĽƱƇđŋžŬǯęƜēĺƐŢŝČĚżƋĉǋćƯķąęĀǁƔęņƂƀųžĀĪƜƈĈďũėŅƞĄřĹģƧƈųŲǐČ
ǡėÿŭĪĜǧŒǁŤǧƛǯǄƪĐĻĪăƑŞőŵĿžŌƎęƺƏęƄęűŽǬǦƕƀŰČƺĻƗýīƼůƟņƏƍŏǀŽũǵŜŀƇǡĄǛĨǈěƜƈƈƹǀŔĀƇĽďČǚǁ
ĈƹûĳǝżǬƶĦŃŨƟŖōžǨŀœŖƌǲƱǮĚƘǳƢĎđƊŕƀǠĮĹŀĽđŪŕŬļŀŞęŵƷǙŻĄơĤĻĐĻĪǫǑūưřƩĘƇƈƤĺƦħġǣǁƈƒĪƜǓŀĊ
ĪĜŷžǐǕǓƥēĉżǜǇĈǦĻĢƹĶƈǦŃĈƒƞƈĈƹƋĀƍŝǀǤĈġĺłǋƧƝĀŅŋĤĻĈŊŏžǴīƗŢĩƛĢƔęĵĺĢǣƪĈŊǑƬďęŜĀøøøøøøø
øøøøøøøøøøøøøøøøǴƷƈūŠĈżøĺĈúĀšƅƋǔǚēążĈżĘüęŸƈǞŕŘýęĀĹĀĺøęǩǒġšŃǀĵĘüęĀĹĀĺĈźƈûǥǬŕƅŴĜţ
ƁƋǔǃǂƽǩǶŧüľĀĺĈźĈżĘǜǠƴĿǅŁĪǍƊƿŰĠǟǫƓŷśćĺĈźĈżĘüęĿŉĖƤƈƠŎņǪİǗǴċƤůƔŢŕƒāęĀĹĀĺĈźƈƠĺǤǲŁƼĽ
ČǱĢǶāǎǳŅƭĈźĈżĘüęĀƁĠƼǕđƁƫƀŪƊĩǰŞƷƦǵǲƟƽďĘƇƷĻĀĺĈźĈżĘüęƯŮƗĮĽĶǔǥƉƏŽǀŀƄĒǆǟķŊņĲƜǴũĶƷǃŌǃ
ĞûĺĈźĈżĘüęħĀǱŰİǜĈŃǀŁǂĜĺŔǖĽǀšƨŸĈżĘüęĀĹǀăĺƮđįĽǮƣƁşƻƑŎőęǟǫǧǣƗƷƖǇƦƈľƇĳĄōĔŏƤĈźĈżĘüęĀ
ŁģǜƬǳǄĻƼāǎĺƀŝČŚšŐǀǡřžƃĈżĘüęĀĹŀĪęǋƹſĕĺŜŜƲĸŒǔøĹĀĺĈźĈżĘĜƛƈƽŴģǧüţƩėĪǅƥǔǱŎƛǳęƶŎľĀĺĈź
ĈżĘĜŻƈũƶƭƵīĚǋŪǮǈǤĦĀĺĈźĈżĘüęǝżĴĳǅŰƊĊęĿŮĹĈźĈżĘüęĀơŃƀǄŽţǛǇǨŒùżĘüęĀĹĀĺĈƪƇǍƋĆğƑƋėŻƆǙ
ƿƾżŴǪƗŧĸĀĺĈźĈżĘǜĭęƃŝĀųƔŘǲǉŵüƘŬǔŻƈķēǃġčǏśĳĆęĀĹĀĺĈźƈƻĺĎÿǲďŇǚħŶĜĦűĔĺĈĺĔĺĈĺĔĺĈĺĔĺĈĺ
ûĚüęĬĄĺƀĻĀĺƀĻǀǓĂƩƃǭùýĊďķĆęĀęĆęĀęĦƖĈũǵƷǡǕŲŗǏĂĜĦŁĔĺĈĺĔĺĈĺŔĴęķǞÿǤƮŞāƼƽƇĻĀĺƀĻĀĺƀƃĢż
ŵāĮƠƀĻĀĺƀĻĀĺƀĻĀĺƀĻĀĺŠĸżĈſĈżĈſĈżĈďŅŀŷŵƫǆǧǱŷƯǰǊĲǚĊƿęüęƼęüęƼĕĎǚľǳúƟƏǡĉƏěĆęĀęĆęĀęǦƨ
ƈǡǭƯƶǓǴǙůŗǕǏǜĊƏĪĆęĀęĆęĀęǦƨƈęŲǝǠƴǳĳǚŪƼęüęƼęüęƼƵĘƼǯėƇůǰǇĶżưǐũĀĹĀũĀĹĀũſŽĤǖŀƫǰǆőůÿƖ
ưĔũĀĹĀũĀĹĀũĿǛǶûǗƢĿĎǎőąČøøøøŁĽņļƦĺŘź''')



# fmt:on
del fs_decode, PYGBAG_FS

# /// script
# dependencies = [
#     "cffi",
#     "raylib",
# ]
# ///

import asyncio
import sys



# webgl 2
if 2:
    HEADER="""#version 300 es
precision mediump float;
"""
    vert = HEADER + """
// Input vertex attributes
in vec3 vertexPosition;
in vec2 vertexTexCoord;
in vec3 vertexNormal;
in vec4 vertexColor;

// Input uniform values
uniform mat4 mvp;

// Output vertex attributes (to fragment shader)
out vec2 fragTexCoord;
out vec4 fragColor;

// NOTE: Add here your custom variables

void main() {
    // Send vertex attributes to fragment shader
    fragTexCoord = vertexTexCoord;
    fragColor = vertexColor;

    // Calculate final vertex position
    gl_Position = mvp*vec4(vertexPosition, 1.0);
}
"""

    frag = HEADER +"""
// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;

// Input uniform values
uniform sampler2D texture0;
uniform vec2 size;
uniform float seconds;

// Output fragment color
out vec4 finalColor;

// NOTE: values should be passed from code
const float vignetteOpacity = 1.0;
const float scanLineOpacity = 0.5;
const float curvature = 10.0;
const float distortion = 0.1;
const float gammaInput = 2.4;
const float gammaOutput = 2.2;
const float brightness = 1.5;

vec2 curveRemapUV() {
  vec2 uv = fragTexCoord*2.0-1.0;
  vec2 offset = abs(uv.yx)/curvature;
  uv = uv + uv*offset*offset;
  uv = uv*0.5 + 0.5;
  return uv;
}

vec3 vignetteIntensity(vec2 uv, vec2 resolution, float opacity) {
  float intensity = uv.x*uv.y*(1.0 - uv.x)*(1.0 - uv.y);
  return vec3(clamp(pow(resolution.x*intensity, opacity), 0.0, 1.0));
}

vec3 scanLineIntensity(float uv, float resolution, float opacity) {
  float intensity = sin(uv*resolution*2.0);
  intensity = ((0.5*intensity) + 0.5)*0.9 + 0.1;
  return vec3(pow(intensity, opacity));
}

vec3 distortIntensity(vec2 uv, float time) {
  vec2 rg = sin(uv*10.0 + time)*distortion + 1.0;
  float b = sin((uv.x + uv.y)*10.0 + time)*distortion + 1.0;
  return vec3(rg, b);
}

void main() {
  vec2 uv = curveRemapUV();
  vec3 baseColor = texture(texture0, uv).rgb;

  baseColor *= vignetteIntensity(uv, size, vignetteOpacity);
  baseColor *= distortIntensity(uv, seconds);
  baseColor = pow(baseColor, vec3(gammaInput)); // gamma correction
  baseColor *= scanLineIntensity(uv.x, size.x, scanLineOpacity);
  baseColor *= scanLineIntensity(uv.y, size.y, scanLineOpacity);
  baseColor = pow(baseColor, vec3(1.0/gammaOutput)); // gamma correction
  baseColor *= vec3(brightness);

  if (uv.x < 0.0 || uv.y < 0.0 || uv.x > 1.0 || uv.y > 1.0) {
    finalColor = vec4(0.0, 0.0, 0.0, 1.0);
  } else {
    finalColor = vec4(baseColor, 1.0);
  }
}
"""


from raylib import *
import random

vec2_size = ffi.new("struct Vector2 *", [0,0])
vec2_tpos = ffi.new("struct Vector2 *", [0,0])

async def main():
    screenWidth = 800
    screenHeight = 450

    if 0:
        try:
            print("\n"*4)
            print ("="*80)
            print(   embed.webgl() )
            print ("="*80)
            print("\n"*4)

        except:
            ...

    InitWindow(screenWidth, screenHeight, b"raylib example - Retro CRT Shader")



    if sys.platform in ('emscripten','wasi'):
        import platform
        platform.window.window_resize()

    # // Load funny texture
    texture = LoadTexture(b"resources/super_mario_bros.png")

    shader = LoadShaderFromMemory(vert.encode(), frag.encode())

    # Set shader uniforms
    screenSize = [float(GetScreenWidth()), float(GetScreenHeight())]

    size_loc = GetShaderLocation(shader, b"size")

    vec2_size.x , vec2_size.y  = screenSize

    SetShaderValue(shader, size_loc, vec2_size, SHADER_UNIFORM_VEC2)
    seconds_loc = GetShaderLocation(shader, b"seconds")

    seconds = 0.0


    while 1:
        # Update
        # ------------------------------------------------------------------------------------
        seconds += GetFrameTime()
        cfseconds = ffi.new("float *", seconds)

        #print(seconds)
        SetShaderValue(shader, seconds_loc, cfseconds, SHADER_UNIFORM_FLOAT)

        # ------------------------------------------------------------------------------------
        # Draw
        # ------------------------------------------------------------------------------------
        BeginDrawing()
        ClearBackground(RAYWHITE)
        # Begin shader mode
        BeginShaderMode(shader)
        DrawTexture(texture, 0, 0, WHITE)
        EndShaderMode()
        EndDrawing()
        # ------------------------------------------------------------------------------------
        await asyncio.sleep(0)

asyncio.run(main())

