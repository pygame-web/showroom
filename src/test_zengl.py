#!python3


import pygame
pygame.init()


WIDTH = 512
HEIGHT =  512

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
display = pygame.Surface((WIDTH, HEIGHT))
display.set_colorkey((0.5, 0.5, 0.5))




import glcontext
import glcontext.egl

eglcontext = glcontext.egl.create_context()


import zengl

ctx = zengl.context(loader=eglcontext)

async def main():
    size = (256, 256)

    image = ctx.image(size, 'rgba8unorm', samples=1)

    triangle = ctx.pipeline(
        vertex_shader='''
            #version 300 es

            out vec3 v_color;

            vec2 positions[3] = vec2[](
                vec2(0.0, 0.8),
                vec2(-0.6, -0.8),
                vec2(0.6, -0.8)
            );

            vec3 colors[3] = vec3[](
                vec3(1.0, 0.0, 0.0),
                vec3(0.0, 1.0, 0.0),
                vec3(0.0, 0.0, 1.0)
            );

            void main() {
                gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);
                v_color = colors[gl_VertexID];
            }
        ''',
        fragment_shader='''
            #version 300 es
            precision mediump float;
            in vec3 v_color;

            layout (location = 0) out vec4 out_color;

            void main() {
                out_color = vec4(v_color, 1.0);
            }
        ''',
        framebuffer=[image],
        topology='triangles',
        vertex_count=3,
    )


    image.clear_value = (1.0, 1.0, 1.0, 1.0)

    image.clear()

    triangle.render()

# https://webglfundamentals.org/webgl/lessons/webgl-2d-drawimage.html


    pic = pygame.image.frombytes( image.read(), size, "RGBA" , flipped=True)
    print(pic)

    pygame.image.save(pic,"out.png")


asyncio.run( main( ) )

