try:
    __import__("os").chdir(__import__("tempfile").gettempdir())
except:
    __import__("os").chdir("/tmp")

def fs_decode(fsname, o248):
    import os
    path = fsname.rsplit('/')
    for i in range(len(path)):
        try:
            os.mkdir('/'.join( path[0:i] ))
        except:
            pass
    with open(fsname, "wb") as fs:
        for input in o248.split("\n"):
            if not input:
                continue
            fs.write(bytes([ord(c) - 248 for c in input]))


fs_decode('./blob.png','''
ƁňņĿąĂĒĂøøøąŁŀļŊøøøƗøøøƗĀûøøøǈƽǳǊøøøđŬĽŐŬĻŧťťŝŦŬøĻŪŝřŬŝŜĘůšŬŠĘĿŁŅňŏŹĆďøøøāŨŀőūø
øĦěøøĦěùŰƝķŮøøøŀňńŌĽĿŨńƆŕĹƾžƓƱŲŏýüüùùùǷƦǁûûûúúúúúúĘĎČıĠĠǥƚƳǐƋƢƗŠłŇĴĸţłļűœśƳŸƋƋš
ůƠŮžǲǲǲƦƥƥǍǍǍŀœţģøøøĂŬŊņŋøǷǷǷƝǷǷǖśĚǇŽŰŧøøĆƵŁļĹŌŰǒǜŔƃŪǢİĊƕĀƄĹćǣđǰǷķǕǦƎŜǃƮĜńŨǅŦǍĢ
ƯžżİǠưƗƟœǥǱǟƗǷƯǭŰĴǶįŹǕũŕƧǛƸĿŔǏǣǵǶħěĕǱƨőǴƖŶŭýŘøťǫǓǩǗļİŌĎǚĻƑƅĻųƅƫĔŁƢŏČǫƁĮƨƾěŘǩǬĥǴ
ĿĴǦƠǆǍĝƾĒƛǟǃĊļưƦĈţĪŸǣƱĚċǎųǟĺǨĶĨƽƔƿƅƿĊƳāņġĝƝƺƽŐƨŴǠħĖĥûŽǲůŰƔūřùƒſƕǝąŎŲǩǃĮüƖƽƯƏýĸƑ
ăŮĉĜƯŎƃþŞƈǟǵūŬƠĤŃƸĮųǗŦƂƏƊǫǢǎŒƹƒƤøǰĈơźĹƄŨǏĳƄėƻīƖġűƋǍťōĮĻśûƋƯǆƊĤŰƕǩƽƗŉĕƬĤĤŻǮǂƋƲķú
ǠĳƳĲǴĸťŻǢŚƃŰƔǫĎǔƁƫǥŧŨġƬŏĎǄėøŢǎǖČǄŇżƯǐŀǊĄƎƫƨƷǥǔżĿāƆėŽśøǐĬģĝǲǚĥŮĞŴĤƀőƹōŭǠƇĥƨăĈǌǃć
ŁćǭŃúüýŪǏƲžǵùĖƑŘûƘüŭƑǓğǰĐľĻǋưĝğžƇǅćśğƲĸǍþđķƢǖƍźűǕŚěƴķžǠĢƸøƾƜŦėāǈƉøģǦǦĬǷƃǨŞŸŚćňź
ƱżǓǙƍüĀŷƼǵĆŘǘŷčŖĳǄǰǜƃƪƎőŒĒƞĈƛįùŋǱħżƏùŦĝǀŊŨƙŵƉĉĔúǠĈĂƯņčŧÿǪǓǩģĎƻŏøŝǴňƫĐĶśǢĐĸúěǴƔą
ǙŻǰŏƢĥŤňǅēıłōƙƼƿƒƦźǡƃŤøƧŭƖİśČƘƌƜǧŹŗŇǙƠľĝŃğįĔƤŔǤĖƏǤžĎĬùŬǚƐŜŉƻǨěŹĕƦƟĨšƖúĭǜũƲšĉùĥĂ
ǦƺƛēĘŸĶţŐĽľīƔǀǪùƋŚƁĠŝľƍǝěǗǚĻŒƕźǬøĴĳŋǣīǃĈŘǉŜǇŻũƃƼƜǢǱŧƁǧĎĭƄƗƘĽƞƜǏƋĂƝĩǫŰƪėĪİĢīǖżƎƭ
ÿƙƃļŸūőĨŖŇŹůŕƂĜċƊƲǈƇƱžėƳøƁŴƚŻĜƬŦƦƒƬƟǧǦşƁćǱēƎŠāŖǀǓǐįűưǀĩĩńƿƂŁÿĿǦĴƖěĶŦƙƦǬřĆğƐĺŰƤŪ
ǗøüƿōţŸŐƜþǴĠĄĩǛǵĔŴƖƱƺǎƉĶƃǟǧǣǭǤƨƲƐăŻďƔţĝǏþđķńƗźǧƒƕŚǁŞŀĽǤħƤƏƾƄǈĎŖƀƽĝǏơúĥĺĆƠùƻǅǭĜǩ
ĥŹĤŎėǲƏĎǒřƫǦřļāĠƔƀĵĸňŻĶƹĻǦǛźħıĚŴƤŶǵǶĶƗħĊƘšŐƘĪŌŻƶŶƗŲǙǆīĸƑƢƮǩĬǭƢƔĠĬƁǧƝƹüŷĻƳƂƺǕǭċƝ
ǴĬƐŭǞƈĶŷČĳƹĻĎǭǂźĶûĶǨƅǨǳţƓŌŗĊřƆŞǨżŘšŝĉŪǊƯĐûƧŗÿƷƀŇťǩƉǴŬƫƦŭźƔǠýģŖŎƱąĊǘǏǰŊǊĠčÿǮǯĺǳƻ
ƅƭŤƁćƥƸœǳƄŚƦǰƱǛǗĢƐǌǣǎǰǨŋƋǚĸĹƴŖšǂǠǜħŰĩƜǘƒƗśęĵǔǇĭƷǠƐźĄėŕƘřŶŢùǞǁŐţǯęǭđǰƺƎǝűǔąǄĂįŧƀ
ƇŲĎƖƤČŵǐįǒēǦǓĈĵǎǨŝŲĸŬŋĮƛėǔûŒġƒơơĎǊğİǀŀŴűŃǚƍŇŕŉǉŦƕƺčǞǭƓǚŃƻŷơũǭĭĶƯħĪĜƫľøĲǏĜÿŠŒǉŀƫ
ēǍĦƽČįĶǆƸğƣǌƦǏǎƸǰǯǂǙƱċŽǰįĆĪƬǩƵģǂǉƱĉǘǃĻǙĚǒŉŠŰǴŏǨƽǞƂƩĖţĆǉǪŪǩŝǳŝǮǗǇǩùĸĲŃƸźƶǍƣƎŘƑŗĝ
ĈƤƅǤėǩùĸĤŁŽĆǥĆǀƯāżǠǍŗǩŉĿƼǭǶǮǣüĪǟįŭǳǓǢǏǀŗǳÿǈǟśǰǶĠǗŧǵŻƆđǔƳĦƗŌĦİćƶĒĎƎŵŠƱƧāŘĆǈƕťơƀǄ
ąĈƲƕƻƾǘƷĞǈǏƔŸœĉŚıƙƔƳĘǒżśĀĝǶǡůǰǨǠǓƬǩġǤƟźƃēśĥĖǬűēųŨǮƈƻŷǇǷƠƶĬƦǝĘŌśţĀƷŪĶƁōƎüŒǟûčǯǝŗ
ĮǑŪŹŌīĸǊƇǑĺÿŧĩĻƯƩŨƖųČĉňǎǅƳƾĳĝīŲġűǓǉýǣǃŧēĀƇƮÿŋƛƛǦǐǌǃǍƤƇħǨīĲŤūĂǖęƙīƭœĩĭƩƍƥǥǓƘėǆŠĈ
ĵĎƆħǯĝƦńžƌŜƭøƽĉŽƶøŇǡćƍĔŹƥĳǆǠŵĞŃĚƎşŘŉūƻĊāŬǏƁŇǠŦŤŀǶƞƄœņǱŅŪċŗǰăĊŠƥǲƹŧĴƝùƵĀŨŽĈǁƓǇœƽ
ǪǄƌſřŐĞůƒƏşüƏĺŸƱĿƱĈŸĺĸĹļĻĬŝƳǀĮƂǖƽǱſƫĞƽƈƽǰƭüǩĠūŮŉơŐƆĐŃƙƞųƿǤƟĬğŏĩľħĥŪĲŧŉǌǙǞřśŋƞǚǖ
ĭǥǪƫƤŧǋƿǂƆńŵŰżƨņĤƃſśŉŦǓơśİǁűǃĮƬƓćÿŌǤěœƔĚƣďşƎůþŠĚƴīǟģĉǘŘǑŮőŚŏǳĔĿƼƞǁĈĀǖƁǒŵǨƉǛǴǡŚź
ǫƂƟǆĸǤŝƒǯƂƿǝŰƢǈǜÿƼăǆŻįŊĉţƈűǢĽƻǱĭĈěǝǒŲƇƿūňƀżŰİǖżďŕǯĜŰǩƨĎńǇǉżŻĀƣěĢǲǆǓĬūǀƱĈŒǣǬďŅþŅ
ƿǌƟĕǥăǣơǀņǟǗǒǦŭǤŸǖƏûƉŔēǏƢųŝƔƝƻƑǆŋþćƄĢƆǭĤħćǛŔơǢǘƵĭŘŭĘķţƓýƔŌƢƐƓǵǪŴƒŻǤƂĉĬúŀĿŻřħĺĲİ
ƽƛŋǴŏǋƤƄſǍĬǬĪĪǞăŹǫĬÿūŷǈǏũŰǒƦÿĭĈĻƔƹƠùŜƄōĞŮƊœƿŰđƇǇƧĪƭŘŋďǳǟƿƀŚŘƎǏǟăþĉſǠǋƚżŎĄĲưƤŋŻƉ
ƻưƥźǏǰƠƔƃƸƮƩƠǠƠƿǩģĵŕŘŅŸǪĿǏÿĳŞęƧǎƊĳŝǡƪĦĆĢƍĲŮĳƤłƝĩǥǊøŠĴŝŔƍǦǐǷǛƺĈƺǃƽňĥĥǰŲǦƁǖĬƏƁŖŷǚ
ǒƔƳǀŭŀƞǰŞĤǳŠűǒŕƳŅƦũĚęƔńŌĮŘąƨǷŐƸŃįøǧúņŒŚĕŕƫýĞāƲǐƫƭĐČƑĳŸąŜƦƛĐǔĶčƾǡŋĈēŸƳŔǪǶǛŚŴĚƁǯĪ
ùĸƲƼǨąǫƈœŗƝƮƾŘǋǄżţĐśƬǊƈƞłƢǠŪƏśĮļŔƎǫƺıļŶĳłĈƜǁůǁŁƩŅǖĀĩǄĂřƕūœŀģƣŃƙüşşĒŅĨđĿƋłĔśčǗĝǝ
ƞĵũƋǳƵĹšƌǏĘĖÿǟŢźƻŁĊĥŀƩƈĘƳƕĹƢĭƫĚŷüħŻăƯœŸǳƲƙĐŤŨƃƎƵĝƛſĤĻǇİüƼŁřĒŶŽǋǭġŖĀśǍƳŉǈİǋžĢƖƸŷ
įšǚƪŒƒŏŰƱŜĭĝĲďǄǴĔŻǎǐŝĻƤĘĬĶŇŹđǧǕƉƞǢǤğŴǔļǟĭĶŜùƍŋŁƭĹƾłƄƅğĳĘđċǡŚſƒƶĩƙǨŵǮĈǶƚŷƞšǮťŖǣƓ
ŀǍāėƠŅśøņƼƁĤƃĀřİĴƛĲœƙƠǊČƆĩŪłǚƣƏąŊǥǍƳŹƁŋŒżǎýŎƲǄǙƞıƕğǥǡųƪĘƄǕŖĬƣĦƱǂƻƅƸǤŢŧĔǧǡŃƻǯǴǘũ
ŇƻſƘŝǉģŒǍĉĸŵĶǫŦǙŔřǵƔƊĺĜƼǊņŇƚşżŅŨƂƖĊŒŷǭƳŒƴžƇċƳǙǅƆŠĩĊơŐǴĲźĦúńƇƕǅƣďĄùƘƠǚûþŞƼƦęňėƁń
ĠćăũǳśƿśƌƥƐǘĕĊŧĜŎǔƶƫƏąǣǴŠǉǨƜŃĻǉǥǲŦƤĔƻǨƀŇưǶřǢƗƹýƂƇũİƮķİťǱǈňŨƺƟĆĲŀǨƥǍŴƲĉǊĘƍŐĵŸƦǚƻ
ĉėļķƺůĘƺưŌĤƭƗƧǔĥċǁıŪĿǥŲøģúƄǰŊƇƝƽǋǌĚİœŚċƞƪŶƒƃĲĝĵāĢǉƼǏıńŅǨŸĳƽÿĊǡűœŀƭķėħǢĖŭĜƀǟŞǛƟǰ
ǊūĲǩƙďƙǅĳĈǋǴĲŅǋņźĴűƁŢǅǥǬǨĩǑŶƄƀŧƹŅǱƣƳǎǰƄĐƲĊüùǪǇǜƏǘĉǁǵŀƏĉǰǲĵŉĴţƸŒǕǏǩċǱčǊģǕřăĞƷħžů
ćŇƿþŞœƻǲĻŴǉĭƼƞǉƨāĘǵǨĺǵƹǬƂņƺƣƛũũĵĽąƗťǙŃǚĻŮƫĀǁŌŚĨŷėŕŞőǫŬǠŋƫĞŕƭķǀƶƲžħĿĎŴǞǛǟƬƝǓǖǐǨŗ
ƖǳƯƪŒēđĶįŠņőŴǣƺƪǡĖīĶŏƹƏƄćƽşǆƽƏĿǟŝĈǰŨŞǞŽřƗŸƯǰƂǡǀƤŕŅĝĂžƲƗǡČŴŞǖƇŢŗƕĽǱŤǩŻŴĵŜĨŃĬƯŴźď
ƁįĭƲƨƾƇŗǰƧƄƹǳƧǶƕǄǰǠđŘƪĥĤþŬŽǙƏǰŴņƇƽūźǰĖįǋƝƭƞǚǗýĮƓǧƚżķğƒıņğýƿşƌŋŦŰŎǰšƁħƀǝǒĤĵżƟŷǒǨ
ǎăǩōŧĘǗƺĬųŨĄĐāŗĄįƲōĘƽǨŏǔăŃŜƑĖƆĵĆƧƂŧŻĮǩżČĩĠŪǝǠƙţǟƺƀćąĤƋņŉǌƭǬǤǫÿǨĆǘģĜƀŊĻſĭǀšŔėƗŨƆ
ǔŸƏƿĨļőĘƨƔƂħùĬƼǮǁǘƉǌƘŴŢǍƿźħƂǂĦƖǧǛĳŘǍưǡƈƯƖęČŧƼƍǖēĂƈǫħǎŏǆŤƗƿǤƧŁĤƚŲǤƗǭǃśĄĞōǟċčƚųǋĂ
ƹƝǮŒǚģĘƥŷĢƦŔǐŶĂǴŀŢĬŧǚƃǷƗüƋĄďŦĝĖưĉƲšûǙƪųđĦųļĻǵƟŬŝŌǩĬőęǄĺǴǣûơĜǙźůĈƳǈĴƩǉšƢęǒƵŤƌƷĮƻ
ǂƍČĎăŧƙúƊƯĞŔĮǤŚŐƜđķŜƧǉǯǰǎĲǕŗǱƗǞƦŮǏĹĈžŖƻǀČƊƢǁŵǷşƵŏŨňŠǃƿƮüƲķƃśŪŮŠƝƖĚǃƺűĩƺƒċŅīğğŦų
ǮƌƊǨƝƀüŴƄŗĈŴňƾƿŜņŦƁǙƩļǙƯżŇǝĉŹŒŢúĶāşƼĘƸŦǄƇǠŶƯƳĞůįƸıňļĉƲŁǲńŒŞùƝŐŬƯīƢŻğŨąǰøČþƠĜÿǇĲ
ĢſźĎŻžƐĠƗǖǦÿǉďŊǮǪǣƼǣŸŸƧŬŵġǙśýǪţƍĵŞǤŭřúƽǚƻÿǂƀƢŠǡĠūǋƿûƱŗǨýøŞŎŅǆǃņŒŶŀāŰŞĚǜùĒĮǱăƚøŬ
ǄǲĤŷƲƖĳČœĂǁǡǩĖƶǴŕčŗƭƝƉƊǟņŴĜŊǪĉƏǡģƮǜǰīŉǫǡƻğƿŮƻǰƢŎǶǨǨŮǙƛǕƮĝƧƝƎĄŷŰŪŋƛƅǪǯļƪøĄƿĿǱĻǉĩ
ùĶǂėłƥƾƻśƂĿŋǉğĠĻǭǠĕŀǗĴƻǳœƜŧĴĶĞĵťƓǓžűǗŤǰƖīǛŻƻƈƿǙŬƒĲƇļÿƏĢƘăůŦņĸǴƬďŽǬŊŠĶǟŵǋŋƺǟţŝŉŽ
ŕƚƚƄǣŷŀþǅƬŉƜĺǛĢĞĤŃąģļǵƸƜĳœŧƲƟƞŹǘƚėĈŬŨŠǲŮǴŞĴĻĠƴƒǤơėƥƷœūǱǌƦčŽīǛūŲǝƤǰǆǕƥřǲĶŷſųĝƃłǄ
ǡćǮǨǞǮǷǖǀƺĨţǯǫǵƗŤťƩĒťǓǄįŖǁĶǒšǝǮŤŭǚǃǮǏŪűťǧŅǇǉǁǏſķƮǢĮƫƺĎǗŒǷǗŶƤƙƛƳƴŵĎƺǣǲĴŦĪŠŢǳƽŧťǎ
ƪŋŁƳƥŶǗǭǧĵŹǍǯưǎǮČťǎķŐĐřŷƨǃƭƥĔŸƶśøøøøŁĽņļƦĺŘź''')

# ./main.py
"""
Python & Pygame implementation of pressure-based soft body paper
https://www.researchgate.net/publication/228574502_How_to_implement_a_pressure_soft_body_model
"""
import asyncio
from dataclasses import dataclass
from math import pi, sin, cos

import pygame
from pygame import Vector2
import pygame._sdl2.video as sdl2


async def main():

    WINDOW_WIDTH = 750
    WINDOW_HEIGHT = 750
    MAX_FPS = 165
    GRAVITY = 9.81
    DT = 1.0 / 60.0
    KS = 130.0
    KD = 20.0
    RESTITUTION = 0.1
    PRESSURE = 300.0

    pygame.init()
    window = pygame._sdl2.video.Window(title="Pygame Pressure-based Softbody", size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    renderer = pygame._sdl2.video.Renderer(window)
    clock = pygame.Clock()
    is_running = True


    @dataclass
    class MassPoint:
        position: Vector2
        velocity: Vector2
        force: Vector2
        mass: float
        mouse: bool = False

    @dataclass
    class Spring:
        a: MassPoint
        b: MassPoint
        length: float
        normal: Vector2
        mouse: bool = False


    masspoints: list[MassPoint] = []
    uvs = []
    springs: list[Spring] = []

    n = 18
    r = 6.0
    for i in range(n):
        masspoints.append(MassPoint(
            Vector2(
                37.5 + r * sin(i * (2.0 * pi) / n),
                37.5 + r * cos(i * (2.0 * pi) / n)
            ),
            Vector2(),
            Vector2(),
            1.0
        ))
        uvs.append(
            Vector2(
                (sin(i * (2.0 * pi) / n) + 1) / 2,
                (cos(i * (2.0 * pi) / n) + 1) / 2
            )
        )

    for i in range(n):
        a = masspoints[i - 1]
        b = masspoints[i]
        springs.append(Spring(
            a,
            b,
            (b.position - a.position).length(),
            Vector2()
        ))

    ground = 65.0

    def step(dt: float) -> None:
        # Apply external forces
        for p in masspoints:
            if p.mouse: continue

            p.force += Vector2(0, p.mass * GRAVITY)

        # Apply spring forces
        for s in springs:
            delta = s.a.position - s.b.position
            dist = delta.length()
            if dist == 0.0: continue

            rv = s.a.velocity - s.b.velocity
            f = (dist - s.length) * KS + (rv.x * (s.a.position.x - s.b.position.x) + rv.y * (s.a.position.y - s.b.position.y)) * KD / dist

            force = (delta / dist) * f

            s.a.force -= force
            s.b.force += force

            # Delta perp?
            s.normal = Vector2(
                (s.a.position.y - s.b.position.y) / dist,
                -(s.a.position.x - s.b.position.x) / dist
            )

        # Calculate valume
        volume = 0.0
        for s in springs:
            if s.mouse: continue

            delta = s.a.position - s.b.position
            dist = delta.length()

            volume += 0.5 * abs(s.a.position.x - s.b.position.x) * abs(s.normal.x) * dist

        #print(volume)

        # Apply pressure forces
        for s in springs:
            if s.mouse: continue

            delta = s.a.position - s.b.position
            dist = delta.length()

            pressure = dist * PRESSURE * (1.0 / volume)

            s.a.force += pressure * s.normal
            s.b.force += pressure * s.normal

        # Semi-implicit euler integration
        for p in masspoints:
            if p.mouse: continue

            p.velocity += p.force / p.mass * dt

            # Solve collisions before integrating velocities
            dy = p.position.y + p.velocity.y * dt
            dx = p.position.x + p.velocity.x * dt
            if dy > ground or dy < 0:
                p.velocity.y *= -RESTITUTION
            if dx > 75 or dx < 0:
                p.velocity.x *= -RESTITUTION

            p.position += p.velocity * dt

            # Reset force accumulator
            p.force = Vector2()

    mouse_p = MassPoint(Vector2(), Vector2(), Vector2(), 1.0, mouse=True)
    mouse_spring = Spring(None, mouse_p, 0.0, Vector2(), mouse=True)

    image = pygame.image.load("blob.png")
    tex = sdl2.Texture.from_surface(renderer, image)


    paused = True

    while is_running:
        dt = clock.tick(MAX_FPS) / 1000

        mouse = pygame.Vector2(*pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                springs.append(mouse_spring)
                paused = False

                min_d = float("inf")
                for p in masspoints:
                    if p.mouse: continue

                    d = (p.position - mouse / 10).length()
                    if d < min_d:
                        min_d = d
                        mouse_spring.a = p


            elif event.type == pygame.MOUSEBUTTONUP:
                springs.remove(mouse_spring)

        mouse_p.position = mouse / 10

        if not paused: step(DT)

        #window.fill((255, 255, 255))
        renderer.draw_color = pygame.Color(255, 255, 255)
        renderer.clear()

        #for p in masspoints:
        #    pygame.draw.circle(window, (255, 0, 0), p.position * 10, 5, 0)

        #pygame.draw.polygon(window, (0, 255, 0), [p.position * 10 for p in masspoints if not p.mouse], 0)

        #for s in springs:
        #    pygame.draw.line(window, (15, 125, 70), s.a.position * 10, s.b.position * 10, 3)

        #pygame.draw.line(window, (170, 170, 170), (0, ground*10), (750, ground*10), 1)

        c = Vector2()
        for p in masspoints:
            if p.mouse: continue
            c += p.position
        c /= n

        m = [p for p in masspoints if not p.mouse]
        for i in range(n):
            a = m[i]
            b = m[(i + 1) % n]

            tex.draw_triangle(
                a.position * 10,
                b.position * 10,
                c * 10,
                uvs[i],
                uvs[(i + 1) % n],
                (0.5, 0.5)
            )

        #pygame.display.flip()
        renderer.present()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
