#version 330

in vec2 v_texture;
out vec4 out_texture;

uniform sampler2D s_texture;

void main() {
    out_texture = texture(s_texture, v_texture);
    if (out_texture.a < 0.1)
        discard;
}
