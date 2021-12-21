#version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in mat4 a_transform;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec2 v_texture;

void main() {
    gl_Position = projection * view * model * a_transform * vec4(a_position, 1.0);
    v_texture = a_texture;
}
